import re

import pandas as pd
from utils.file_settings import (BEHAVIORAL_COLUMN_END,
                                 BEHAVIORAL_COLUMN_START, COLUMN_TIME,
                                 MESSAGE_CATEGORY_VALIDATION,
                                 MESSAGE_COLUMN_CATEGORY, MESSAGE_COLUMN_TEXT)
from utils.textconstants import RESULT, SNIPPET
from utils.validation_settings import (ARRAY_LIST_PATTERN, COLUMN_INDEX,
                                       COLUMN_KEY, COLUMN_VALUE,
                                       END_TARGET_POSITION, HEAD_INDEX,
                                       START_TARGET_POSITION)
from utils.visual_settings import (HEIGHT, PSYCHOPY_X_AREA, PSYCHOPY_Y_AREA,
                                   WIDTH)


def split_validation_results(message_events: pd.DataFrame) -> pd.DataFrame:
    validation_results = {}
    # Filter validation results (remove other events with category VALIDATION)
    validation_result_data = message_events[message_events[MESSAGE_COLUMN_CATEGORY]
                                            == MESSAGE_CATEGORY_VALIDATION].copy()
    # get iteration index
    validation_result_data['time_diff_previous'] = validation_result_data[COLUMN_TIME].diff(
    ).fillna(0)
    # 1 indicates new start of iteration, 0 within
    validation_result_data['separators'] = 1 * \
        (validation_result_data['time_diff_previous'] > 1)
    validation_result_data['iteration_index'] = validation_result_data['separators'].cumsum(
    )
    # store result texts per index
    for i_index in validation_result_data['iteration_index'].unique():
        relevant_validation_result_data = validation_result_data[
            validation_result_data['iteration_index'] == i_index]
        validation_results[i_index] = (relevant_validation_result_data[COLUMN_TIME].iloc[0],
                                       relevant_validation_result_data[MESSAGE_COLUMN_TEXT].to_list())
    validation_data = pd.DataFrame.from_dict(
        validation_results, orient='index', columns=[BEHAVIORAL_COLUMN_END, RESULT])
    return validation_data


def split_validation_events(message_events: pd.DataFrame, validation_data: pd.DataFrame) -> pd.DataFrame:
    useless_text_starts = (
        'CONTRACT_SIZE', 'EXPAND_SIZE', 'POS_UPDATE', 'ended')
    # Filter actual validation events (remove other events without a category)
    if message_events.empty:
        return pd.DataFrame()
    if message_events.iat[-1, -1] == 'VALIDATION TERMINATED BY USER':
        return pd.DataFrame()
    validation_data['events'] = None
    validation_data[BEHAVIORAL_COLUMN_START] = None
    validation_data = validation_data.astype({'events': 'object'})
    validation_event_data = message_events[(
        message_events[MESSAGE_COLUMN_CATEGORY] == '')]
    validation_event_data = validation_event_data[~validation_event_data[MESSAGE_COLUMN_TEXT].str.startswith(
        useless_text_starts)].copy()
    # get iteration index
    validation_event_data['iteration_index'] = validation_event_data['logged_'+COLUMN_TIME].apply(
        lambda t: (1*(validation_data[BEHAVIORAL_COLUMN_END] < t)).sum())
    # assert (set(validation_data.index.to_numpy()) == set(
    #     validation_event_data['iteration_index'].to_numpy())), f"{set(validation_data.index.to_numpy())}, {set(validation_event_data['iteration_index'].to_numpy())}"
    # add results per index
    for i_index in validation_data.index:
        relevant_validation_event_data = validation_event_data[
            validation_event_data['iteration_index'] == i_index]
        validation_data.at[i_index,
                           'events'] = relevant_validation_event_data[MESSAGE_COLUMN_TEXT].to_list()
        validation_data.at[i_index,
                           BEHAVIORAL_COLUMN_START] = relevant_validation_event_data[COLUMN_TIME].min()
        validation_data.at[i_index,
                           BEHAVIORAL_COLUMN_END] = relevant_validation_event_data[COLUMN_TIME].max()
    validation_data.index.name = SNIPPET
    validation_data = validation_data.reset_index()
    return validation_data


def serialize_validation_results(results: list[str]):
    results.pop(0)
    results.pop()
    results = [r.split(': ') for r in results]
    res = []
    target_position_index = HEAD_INDEX
    for r in results:
        if len(r) != 2:
            print('Wrong data', r)
            continue
        key, value = r[0], r[1]
        if value[0] == '[':
            value = re.sub(ARRAY_LIST_PATTERN, r'\1, ', value)
        try:
            value = eval(value)
        except Exception:
            if 'array' in value:
                try:
                    value = eval(value.replace('array', ''))
                except Exception:
                    print(key, value)
        if key == START_TARGET_POSITION:
            target_position_index = value
        res.append({COLUMN_KEY: key, COLUMN_VALUE: value,
                   COLUMN_INDEX: target_position_index})
        if key == END_TARGET_POSITION:
            target_position_index = HEAD_INDEX
    result_data = pd.DataFrame.from_records(res)
    return result_data


def parse_validation_results(results: list[str]):
    result_data = serialize_validation_results(results)
    head_data = result_data[result_data[COLUMN_INDEX] == HEAD_INDEX]

    dbounds = head_data[head_data[COLUMN_KEY] == 'display_bounds'].squeeze()[
        COLUMN_VALUE].copy()
    dbounds.sort()
    required_dbounds = [*PSYCHOPY_X_AREA, *PSYCHOPY_Y_AREA]
    required_dbounds.sort()
    assert (dbounds == required_dbounds)

    pixels = head_data[head_data[COLUMN_KEY] == 'display_pix'].squeeze()[
        COLUMN_VALUE].copy()
    pixels.sort()
    assert (pixels == sorted([WIDTH, HEIGHT]))

    errors = {row[COLUMN_KEY]: row[COLUMN_VALUE]
              for i, row in head_data[head_data[COLUMN_KEY].str.endswith('error')].iterrows()}

    position_counts = head_data[head_data[COLUMN_KEY] == 'position_count'].squeeze()[
        COLUMN_VALUE]
    positions = head_data[head_data[COLUMN_KEY] == 'target_positions'].squeeze()[
        COLUMN_VALUE]
    positions_unavailable = False
    if isinstance(positions, str):
        positions_unavailable = True
    else:
        assert (position_counts == len(positions))
    position_indices = list(result_data[COLUMN_INDEX].unique())
    position_indices.remove(HEAD_INDEX)
    assert (position_counts == len(position_indices))
    passed = head_data[head_data[COLUMN_KEY] == 'passed'].squeeze()[
        COLUMN_VALUE]

    position_results = {}
    for index in position_indices:
        position_data = result_data[result_data[COLUMN_INDEX] == index]
        assert (index == position_data[position_data[COLUMN_KEY]
                == START_TARGET_POSITION].squeeze()[COLUMN_VALUE])
        assert (index == position_data[position_data[COLUMN_KEY] == COLUMN_INDEX].squeeze()[
                COLUMN_VALUE])
        target_position = position_data[position_data[COLUMN_KEY] == 'target_position'].squeeze()[
            COLUMN_VALUE]
        if not positions_unavailable:
            assert target_position in positions, f'''target_position {
                target_position} not in positions {positions}'''
        position_result = {row[COLUMN_KEY]: row[COLUMN_VALUE]
                           for i, row in position_data[~position_data[COLUMN_KEY].isin([START_TARGET_POSITION, END_TARGET_POSITION, COLUMN_INDEX])].iterrows()}
        position_results[index] = position_result

    return [passed, errors, position_results]
