from pathlib import Path
from typing import Any

import h5py
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from utils.behavioral_settings import (MIN_ACCEPTED_CORRECTNESS,
                                       TUKEY_ACCEPTANCE_INTERVAL)
from utils.eeg_settings import (EEG_STIMULUS_FIXATION_CROSS,
                                EEG_STIMULUS_SNIPPET_END,
                                EEG_STIMULUS_SNIPPET_START)
from utils.file_helpers import update_exclusions
from utils.file_settings import (BEHAVIORAL_COLUMN_ANSWER,
                                 BEHAVIORAL_COLUMN_CORRECTNESS,
                                 BEHAVIORAL_COLUMN_DURATION,
                                 BEHAVIORAL_COLUMN_END,
                                 BEHAVIORAL_COLUMN_FIXATION_START,
                                 BEHAVIORAL_COLUMN_RATING,
                                 BEHAVIORAL_COLUMN_START, BEHAVIORAL_COLUMNS,
                                 COLUMN_TIME, EEG_COLUMN_STIMULUS,
                                 MESSAGE_CATEGORIES, MESSAGE_CATEGORY_ANSWER,
                                 MESSAGE_CATEGORY_FIXATION,
                                 MESSAGE_CATEGORY_PERCEPTION,
                                 MESSAGE_CATEGORY_SNIPPETVIEW,
                                 MESSAGE_CATEGORY_VALIDATION,
                                 MESSAGE_COLUMN_CATEGORY, MESSAGE_COLUMN_TEXT,
                                 ROUNDING_TIME, SEPARATOR,
                                 SNIPPET_COLUMN_AOC_CATEGORY,
                                 SNIPPET_COLUMN_RIGHT_ANSWER,
                                 SNIPPET_COLUMN_SNIPPET,
                                 SNIPPET_COLUMN_VARIANT)
from utils.path_helpers import get_eval_aggregation_snippet_categories_path
from utils.path_settings import *
from utils.snippet_helpers import get_snippet_base, get_snippet_variant
from utils.snippet_settings import (ANSWER_CORRECTNESS, CONDITION, CONDITION_CLEAN,
                                    CONDITION_COLORS, CONDITION_CONFUSING,
                                    CONDITION_VARIANT_MATCH, RATINGS)
from utils.textconstants import ACCEPTED, PARTICIPANT, SNIPPET, TIME

# how many snippets were shown and how often


def retrieve_message_events(hdf5_event_data_file: Path, retrieve_validation: bool = False) -> pd.DataFrame:
    '''retrieve message and eye events as dataframes from the hdf file

    Arguments:
    * hdf5_event_data_file: the path to the hdf file
    * retrieve_validation: whether to ask for validation message events or trial data

    returns: the message events (validation or trial data)
    '''
    with h5py.File(hdf5_event_data_file, 'r') as f:
        # read message events from hdf5 info in data_collection->events->experiment->MessageEvent
        message_events = f['data_collection']['events']['experiment']['MessageEvent']
        # h5py syntax to retrieve all data
        message_events = pd.DataFrame(message_events[()])
        # convert text into utf from binary
        message_events[MESSAGE_COLUMN_CATEGORY] = message_events[MESSAGE_COLUMN_CATEGORY].str.decode(
            'utf-8')
        message_events[MESSAGE_COLUMN_TEXT] = message_events[MESSAGE_COLUMN_TEXT].str.decode(
            'utf-8').str.replace('\'', '')
        # take only useful messages depending on category and requirements
        if retrieve_validation:
            useful_message_events = message_events[message_events[MESSAGE_COLUMN_CATEGORY].isin([
                                                                                                '', MESSAGE_CATEGORY_VALIDATION])].copy()
        else:
            useful_message_events = message_events[message_events[MESSAGE_COLUMN_CATEGORY].isin(
                MESSAGE_CATEGORIES)].copy()
        useful_message_events[COLUMN_TIME] = useful_message_events[COLUMN_TIME].round(
            ROUNDING_TIME)
        return useful_message_events


###############################
# transform for behavioral data
###############################


def get_fixation_cross_data(message_events: pd.DataFrame) -> pd.DataFrame:
    '''get fixation cross data from message events.
    Uses the fixation cross events with start time

    Arguments: message events: a dataframe containing the relevant message events

    returns: fixation cross data (start per snippet (not as index))
    '''

    # FIXATION: Fixation 17-obf-v0.png
    snippet_fixation_events = message_events[message_events[MESSAGE_COLUMN_CATEGORY] == MESSAGE_CATEGORY_FIXATION].copy(
    )
    if snippet_fixation_events.empty:
        return pd.DataFrame(columns=[SNIPPET, BEHAVIORAL_COLUMN_FIXATION_START])
    snippet_fixation_events[['event', SNIPPET]
                            ] = snippet_fixation_events[MESSAGE_COLUMN_TEXT].str.split(' ', n=1).to_list()
    snippet_fixation_events[BEHAVIORAL_COLUMN_FIXATION_START] = snippet_fixation_events[COLUMN_TIME]
    snippet_fixation_events = snippet_fixation_events[[
        SNIPPET, BEHAVIORAL_COLUMN_FIXATION_START]]
    return snippet_fixation_events.reset_index()


def get_snippet_view_data(message_events: pd.DataFrame, snippet_fixation_events: pd.DataFrame) -> pd.DataFrame:
    '''get snippet view data from message events.
    Uses the snippetview events, from which start, end and duration are calculated

    Arguments: message events: a dataframe containing the relevant message events

    returns: snippet view data (start, end and duration per snippet (not as index))
    '''
    # SNIPPETVIEW: Start Snippet 10-obf-v0.png, End Snippet 10-obf-v0.png
    snippet_duration_events = message_events[message_events[MESSAGE_COLUMN_CATEGORY] == MESSAGE_CATEGORY_SNIPPETVIEW].copy(
    )
    if snippet_duration_events.empty:
        return pd.DataFrame(columns=[SNIPPET, BEHAVIORAL_COLUMN_START, BEHAVIORAL_COLUMN_END, BEHAVIORAL_COLUMN_DURATION])
    snippet_duration_events[['event', '', SNIPPET]
                            ] = snippet_duration_events[MESSAGE_COLUMN_TEXT].str.split(' ', n=2).to_list()
    snippet_duration_events = snippet_duration_events.pivot(
        index=SNIPPET, columns='event', values=COLUMN_TIME)
    assert (snippet_duration_events[snippet_duration_events[BEHAVIORAL_COLUMN_START]
            > snippet_duration_events[BEHAVIORAL_COLUMN_END]].empty)
    # if 'start' is missing, use fixation time +5s. no replacement for 'end' possible
    if snippet_duration_events[BEHAVIORAL_COLUMN_START].isnull().any():

        print('"Na" values in start time identified, trying to fill it with fixation information')
        # calculate possible starting point based on fixation cross
        snippet_fixation_events[BEHAVIORAL_COLUMN_START] = snippet_fixation_events[BEHAVIORAL_COLUMN_FIXATION_START]+5
        snippet_fixation_events.index = snippet_fixation_events[SNIPPET]
        # fill na in duration with this possible value
        snippet_duration_events[BEHAVIORAL_COLUMN_START] = snippet_duration_events[BEHAVIORAL_COLUMN_START].fillna(
            snippet_fixation_events[BEHAVIORAL_COLUMN_START])
        snippet_fixation_events.reset_index(drop=True, inplace=True)
        snippet_fixation_events.drop(
            columns=[BEHAVIORAL_COLUMN_START], inplace=True)
        # sanity check: missing value likely caused by wanted skip of the snippet
        # if this is so, then the start should now have a higher value than the end
        # in that case, delete the entry completely
        rows_to_delete = snippet_duration_events[snippet_duration_events[BEHAVIORAL_COLUMN_START]
                                                 > snippet_duration_events[BEHAVIORAL_COLUMN_END]]
        if not rows_to_delete.empty:
            print('Filling attempt failed occasionally (start after end), deleting rows')
            snippet_duration_events = snippet_duration_events.drop(
                index=[i for i in rows_to_delete.index])

    snippet_duration_events[BEHAVIORAL_COLUMN_DURATION] = (snippet_duration_events[BEHAVIORAL_COLUMN_END] -
                                                           snippet_duration_events[BEHAVIORAL_COLUMN_START]).round(ROUNDING_TIME)
    return snippet_duration_events.reset_index()


def get_snippet_answer_data(message_events: pd.DataFrame) -> pd.DataFrame:
    '''get answer data from message events.
    Uses the answer events, from which answer and correctness are calculated

    Arguments: message events: a dataframe containing the relevant message events

    returns: snippet answers (answer and correctness per snippet (not as index))
    '''
    # ANSWER Answer 10-obf-v0.png 1 False
    snippet_answer_events = message_events[message_events[MESSAGE_COLUMN_CATEGORY] == MESSAGE_CATEGORY_ANSWER].copy(
    )
    if snippet_answer_events.empty:
        return pd.DataFrame(columns=[SNIPPET, BEHAVIORAL_COLUMN_ANSWER, BEHAVIORAL_COLUMN_CORRECTNESS])
    snippet_answer_events[['x', SNIPPET, BEHAVIORAL_COLUMN_ANSWER, BEHAVIORAL_COLUMN_CORRECTNESS]
                          ] = snippet_answer_events[MESSAGE_COLUMN_TEXT].str.split(' ', n=3).to_list()
    # replace None in Answer with Na and not(_/ )answered in Correctness with False
    snippet_answer_events[BEHAVIORAL_COLUMN_ANSWER] = snippet_answer_events[BEHAVIORAL_COLUMN_ANSWER].replace(
        {'None': np.nan}).fillna(value=np.nan)
    snippet_answer_events[BEHAVIORAL_COLUMN_CORRECTNESS] = snippet_answer_events[BEHAVIORAL_COLUMN_CORRECTNESS].replace(
        {'True': True, 'False': False, 'not_answered': False, 'not answered': False})
    snippet_answer_events = snippet_answer_events[[
        SNIPPET, BEHAVIORAL_COLUMN_ANSWER, BEHAVIORAL_COLUMN_CORRECTNESS]]
    return snippet_answer_events.reset_index(drop=True)


def get_snippet_perception_data(message_events: pd.DataFrame) -> pd.DataFrame:
    '''get perception data from message events.
    Uses the perception events, from which rating is calculated

    Arguments: message events: a dataframe containing the relevant message events

    returns: snippet perception (rating per snippet (not as index))
    '''
    # PERCEPTION Perception 10-obf-v0.png easy
    snippet_perception_events = message_events[message_events[
        MESSAGE_COLUMN_CATEGORY] == MESSAGE_CATEGORY_PERCEPTION].copy()
    if snippet_perception_events.empty:
        return pd.DataFrame(columns=[SNIPPET, BEHAVIORAL_COLUMN_RATING])
    snippet_perception_events[['x', SNIPPET, BEHAVIORAL_COLUMN_RATING]
                              ] = snippet_perception_events[MESSAGE_COLUMN_TEXT].str.split(' ', n=2).to_list()
    # replace None in Rating with Na
    snippet_perception_events[BEHAVIORAL_COLUMN_RATING] = snippet_perception_events[BEHAVIORAL_COLUMN_RATING].replace(
        {'None': np.nan}).fillna(value=np.nan)
    snippet_perception_events = snippet_perception_events[[
        SNIPPET, BEHAVIORAL_COLUMN_RATING]]
    return snippet_perception_events.reset_index(drop=True)


def transform_snippet_data(snippet_fixation_events: pd.DataFrame, snippet_duration_events: pd.DataFrame, snippet_answer_events: pd.DataFrame,
                           snippet_perception_events: pd.DataFrame, snippets_data: pd.DataFrame) -> pd.DataFrame:
    snippet_data = pd.merge(pd.merge(snippet_fixation_events, snippet_duration_events, on=SNIPPET), pd.merge(
        snippet_answer_events, snippet_perception_events, on=SNIPPET), on=SNIPPET)
    snippet_data[SNIPPET] = snippet_data[SNIPPET].str.replace('\'', '')
    # delete snippet in row if only fixation cross was shown, nothing more (if expected, then only in the last row)
    only_fixation_cross = snippet_data.apply(lambda row: all([row.isna(
    )[c] for c in snippet_data.columns if c not in [BEHAVIORAL_COLUMN_FIXATION_START, SNIPPET]]), axis=1)
    if only_fixation_cross.any():
        snippets_before = snippet_data[SNIPPET].value_counts().to_dict()
        snippet_data = snippet_data.drop(
            index=only_fixation_cross[only_fixation_cross].index)
        snippets_after = snippet_data[SNIPPET].value_counts().to_dict()
        removed_snippets = {
            s: snippets_before[s] for s in snippets_before if s not in snippets_after}\
            | {s: (snippets_before[s]-snippets_after[s])
               for s in snippets_after if snippets_after[s] != snippets_before[s]}
        print('\tThe following snippets were removed due to only fixation cross',
              removed_snippets)
    # add input from snippets file (all possible additional input, verify correctness)
    behavioral_data = pd.merge(snippet_data, snippets_data,
                               left_on=SNIPPET, right_on=SNIPPET_COLUMN_SNIPPET)
    # overwriting correctness due to type errors in psychopy comparison for correctness
    behavioral_data[BEHAVIORAL_COLUMN_CORRECTNESS] = behavioral_data[
        BEHAVIORAL_COLUMN_ANSWER] == behavioral_data[SNIPPET_COLUMN_RIGHT_ANSWER]
    behavioral_data[SNIPPET] = behavioral_data[SNIPPET].apply(
        lambda filename: filename.split('.')[0])
    behavioral_data[CONDITION] = behavioral_data[SNIPPET_COLUMN_VARIANT].apply(
        lambda v: CONDITION_VARIANT_MATCH[v])
    return behavioral_data


def prepare_for_EEG_synchronization(snippet_fixation_events: pd.DataFrame, snippet_duration_events: pd.DataFrame) -> pd.DataFrame:
    snippet_fixation_events = pd.DataFrame(snippet_fixation_events[[
        SNIPPET, BEHAVIORAL_COLUMN_FIXATION_START]])
    snippet_fixation_events.columns = [SNIPPET, TIME]
    snippet_fixation_events[EEG_COLUMN_STIMULUS] = EEG_STIMULUS_FIXATION_CROSS
    if snippet_duration_events is None:
        snippet_start_events = pd.DataFrame([], columns=[SNIPPET, TIME])
        snippet_end_events = pd.DataFrame([], columns=[SNIPPET, TIME])
    else:
        snippet_start_events = pd.DataFrame(snippet_duration_events[[
            SNIPPET, BEHAVIORAL_COLUMN_START]])
        snippet_start_events.columns = [SNIPPET, TIME]
        snippet_start_events[EEG_COLUMN_STIMULUS] = snippet_start_events[SNIPPET].\
            apply(
                lambda x: EEG_STIMULUS_SNIPPET_START[CONDITION_VARIANT_MATCH[get_snippet_variant(x)]])
        snippet_end_events = pd.DataFrame(snippet_duration_events[[
            SNIPPET, BEHAVIORAL_COLUMN_END]])
        snippet_end_events.columns = [SNIPPET, TIME]
        snippet_end_events[EEG_COLUMN_STIMULUS] = EEG_STIMULUS_SNIPPET_END
    behavioral_events = pd.concat(
        [snippet_fixation_events, snippet_start_events, snippet_end_events]).sort_values([TIME]).reset_index(drop=True)
    behavioral_events[SNIPPET] = behavioral_events[SNIPPET].str.replace(
        '.png', '')
    return behavioral_events


def compare_behavioral_to_sequence_order(participant: str, behavioral_data: pd.DataFrame, sequence_order: pd.DataFrame, error_message: str):
    # check whether all snippets are there (otherwise mark as excluded), and that all are correctly shown
    assert sequence_order[SNIPPET].shape[0] == 72, "The participant should have been given 72 snippets to view in the condition files."

    behavioral_data = manage_duplicates(behavioral_data)
    note_missing_snippets(behavioral_data, sequence_order, participant, error_message)

    check_sequence_order(behavioral_data, sequence_order)
    
    behavioral_data = behavioral_data.merge(sequence_order, how='outer', on=[
                                            SNIPPET], suffixes=['', '_so'])
    behavioral_data = behavioral_data.drop(
        columns=[c for c in behavioral_data.columns if not (c in BEHAVIORAL_COLUMNS)])
    if behavioral_data[[BEHAVIORAL_COLUMN_START, BEHAVIORAL_COLUMN_END, SNIPPET]].isna().any(axis=None):
        print(
            f'Some rows with empty entries are removed {behavioral_data[behavioral_data[[BEHAVIORAL_COLUMN_START, BEHAVIORAL_COLUMN_END, SNIPPET]].isna().any(axis=1)]}')
        behavioral_data = behavioral_data.dropna(
            subset=[BEHAVIORAL_COLUMN_START, BEHAVIORAL_COLUMN_END, SNIPPET], axis='index')
    behavioral_data[EEG_COLUMN_STIMULUS] = behavioral_data[CONDITION].apply(
        lambda condition: EEG_STIMULUS_SNIPPET_START[condition])
    return behavioral_data


def manage_duplicates(behavioral_data: pd.DataFrame):
    # check whether all snippets are there (otherwise mark as excluded), and that all are correctly shown

    # identify duplicates
    duplicate_snippets = behavioral_data[behavioral_data.duplicated([
                                                                    SNIPPET], False)]
    for snippet in duplicate_snippets[SNIPPET].unique():
        duplicate_rows = behavioral_data[behavioral_data[SNIPPET] == snippet]
        first_duplicate_row = duplicate_rows.iloc[0]
        while duplicate_rows.shape[0] > 1:
            if pd.isna(first_duplicate_row[BEHAVIORAL_COLUMN_START]) and pd.isna(first_duplicate_row[BEHAVIORAL_COLUMN_END]):
                # if first iteration, snippet was not visible at all, drop this iteration and look at other data
                duplicate_rows = duplicate_rows.drop(duplicate_rows.index[0])
                first_duplicate_row = duplicate_rows.iloc[0]
            elif not pd.isna(first_duplicate_row[BEHAVIORAL_COLUMN_START]) and pd.isna(first_duplicate_row[BEHAVIORAL_COLUMN_END]):
                # if first iteration, snippet was seen but not finished, keep all viewings as duplicate
                break
            elif not pd.isna(first_duplicate_row[BEHAVIORAL_COLUMN_START]) and not pd.isna(first_duplicate_row[BEHAVIORAL_COLUMN_END]):
                if pd.isna(first_duplicate_row[BEHAVIORAL_COLUMN_RATING]) and pd.isna(first_duplicate_row[BEHAVIORAL_COLUMN_ANSWER]):
                    # if first iteration, snippet was totally visible but not rated or answered, delete
                    break
                # if first iteration, snippet was totally visible and answered or rated, keep this iteration and delete the others
                duplicate_rows = duplicate_rows.drop(duplicate_rows.index[0])
                first_duplicate_row = duplicate_rows.iloc[0]
                break
            else:
                raise Exception("There should not be an end but not a start")
        if duplicate_rows.shape[0] == 1:
            # if only 1 row left, keep it
            duplicate_snippets = duplicate_snippets.drop(
                index=first_duplicate_row.name)
    # remove unnecessary duplicate lines
    if not duplicate_snippets.empty:
        print('Dropped duplicate lines', duplicate_snippets)
        behavioral_data = behavioral_data[~behavioral_data.index.isin(
            duplicate_snippets.index)]
    return behavioral_data


def note_missing_snippets(behavioral_data: pd.DataFrame, sequence_order: pd.DataFrame, participant: str, error_message: str):
    # check whether all snippets are there (number-wise)
    if sequence_order[SNIPPET].shape[0] != behavioral_data[SNIPPET].shape[0]:
        print(f'The number of trials in the condition files and the behavioral data from the hdf files differs. The snippets not given in the behavioral data will be excluded from further analysis.')
        # identify missing
        missing_snippets = {
            s for s in sequence_order[SNIPPET] if s not in set(behavioral_data[SNIPPET].values)}
        # mark in exclusion file
        update_exclusions(participant, SNIPPET, BEHAVIORAL, {
                          m: (error_message+': No behavioral data for snippet found.') for m in missing_snippets})
        # identify irregular ones
        if len(set(sequence_order[SNIPPET])) != len(set(behavioral_data[SNIPPET])) + len(missing_snippets):
            raise Exception(
                f'The participant has seen snippets they were not supposed to see: {[s for s in behavioral_data[SNIPPET] if s not in sequence_order[SNIPPET]]}')

def check_sequence_order(behavioral_data: pd.DataFrame, sequence_order: pd.DataFrame):
    # check whether sequence order is maintained
    behavioral_data_so = behavioral_data.merge(
        sequence_order, how='outer', left_index=True, right_index=True, suffixes=['', '_so'])
    compare_sequence_order = behavioral_data_so[
        SNIPPET] == behavioral_data_so[f'{SNIPPET}_so']
    if not compare_sequence_order.all():
        print('The order of trials in the condition files and those from the hdf files differs. Differences are in:')
        print(behavioral_data_so[~compare_sequence_order])
        # raise Exception()


def get_all_behavioral_data(behavioral_files: dict[str, Path]) -> pd.DataFrame:
    p_data = []
    for participant in behavioral_files:
        behavioral_data = pd.read_csv(
            behavioral_files[participant], sep=SEPARATOR, dtype={PARTICIPANT: str})
        behavioral_data = behavioral_data.drop(
            index=behavioral_data[behavioral_data[PARTICIPANT].isna()].index)
        p_data.append(behavioral_data)
    behavioral_data = pd.concat(p_data)
    return behavioral_data


def check_correctness(behavioral_data: pd.DataFrame) -> pd.DataFrame:
    behavioral_data[BEHAVIORAL_COLUMN_CORRECTNESS] = behavioral_data[BEHAVIORAL_COLUMN_CORRECTNESS]*1
    correctness_data: pd.DataFrame = behavioral_data.groupby(
        # mean represents relative correctness in percent, sum absolute correctness in trials
        [PARTICIPANT]).agg({BEHAVIORAL_COLUMN_CORRECTNESS: ['mean', 'sum']})
    # drop the first level that just contains BEHAVIORAL_COLUMN_CORRECTNESS
    correctness_data.columns = correctness_data.columns.droplevel()
    correctness_data[ACCEPTED] = correctness_data['mean'] >= MIN_ACCEPTED_CORRECTNESS
    return correctness_data


def calculate_duration_acceptance(behavioral_data: pd.DataFrame) -> pd.DataFrame:
    mean_duration, std_duration = behavioral_data[BEHAVIORAL_COLUMN_DURATION].mean(
    ), behavioral_data[BEHAVIORAL_COLUMN_DURATION].std()
    min_accepted_duration = mean_duration-TUKEY_ACCEPTANCE_INTERVAL*std_duration
    max_accepted_duration = mean_duration+TUKEY_ACCEPTANCE_INTERVAL*std_duration
    print('Mean duration:', mean_duration,
          'std duration', std_duration)
    print('Acceptance interval:', min_accepted_duration,
          'to', max_accepted_duration)

    axes = behavioral_data.boxplot(
        column=BEHAVIORAL_COLUMN_DURATION, whis=TUKEY_ACCEPTANCE_INTERVAL)
    plt.show()
    sns.violinplot(behavioral_data, y=BEHAVIORAL_COLUMN_DURATION)
    plt.show()

    behavioral_data[ACCEPTED] = behavioral_data[BEHAVIORAL_COLUMN_DURATION].between(
        min_accepted_duration, max_accepted_duration, 'both')
    print('Acceptance rate:',
          behavioral_data[behavioral_data[ACCEPTED]].shape[0]/behavioral_data.shape[0])
    return behavioral_data


def count_occurrences(df: pd.DataFrame, key: str):
    df = df[[SNIPPET, key]]
    values = df[SNIPPET].value_counts().reset_index()
    values['occurrences'] = values['count']
    overview = values[[SNIPPET, 'occurrences']
                      ].groupby(['occurrences']).count()
    overview.columns = [f'{SNIPPET}_{key}']
    return overview, values


def count_instances(values: pd.Series, value: Any):
    '''count the occurrence of value in the values'''
    value_counts = dict(values.value_counts())
    if value in value_counts:
        return value_counts[value]
    return 0


def count_instances_rel(values: pd.Series, value: Any):
    '''count the relative occurrence of value in the values'''
    value_counts = values.value_counts()
    if value in value_counts:
        return value_counts[value]/values.shape[0]
    return 0


def contrast_by_condition(df: pd.DataFrame, condition_column: str, metric_columns: list[str], label_column: str, result_description: str, display_df: True):
    '''pivot condition_column to contrast clarified and obfuscated values for metric_column. 
    Use first column and label_column as constant indices (of which clean and confusing are removed)
    store result in csv file and display it in the notebook'''
    if not set(metric_columns).issubset(df.columns):
        raise KeyError(
            f'Columns expected in Dataframe: {metric_columns} in {df.columns}.')
    df2 = df.copy(True)
    df2 = df2.astype({label_column: str, list(df.columns)[0]: str})
    if list(df.columns)[0] == SNIPPET:
        df2[list(df.columns)[0]] = df2[list(df.columns)[0]].apply(
            lambda snippet: get_snippet_base(snippet))
    df_pivot = df2.pivot(columns=condition_column, index=list(
        {list(df.columns)[0], label_column}), values=metric_columns)
    full_size = df_pivot.shape[0]
    df_pivot = df_pivot.dropna()
    if full_size-df_pivot.shape[0] > 0:
        print(
            f'removed {full_size-df_pivot.shape[0]} cases of {full_size} due to NAs.')
    for metric_column in metric_columns:
        df_pivot.loc[:, (metric_column, 'confusing_more')] = df_pivot.loc[:,
                                                                          (metric_column, CONDITION_CLEAN)] <= df_pivot.loc[:, (metric_column, CONDITION_CONFUSING)]
        df_pivot.loc[:, (metric_column, 'confusing_less')] = df_pivot.loc[:,
                                                                          (metric_column, CONDITION_CLEAN)] >= df_pivot.loc[:, (metric_column, CONDITION_CONFUSING)]
    if result_description:
        df_pivot.to_csv(get_eval_aggregation_snippet_categories_path(
            f'{result_description}_contrast'), sep=';')
        with pd.ExcelWriter(EVAL_PATH_AGGREGATED_DATA_SUMMARY, mode=('a'if EVAL_PATH_AGGREGATED_DATA_SUMMARY.exists() else 'w'), engine='openpyxl') as writer:
            df_pivot.to_excel(
                writer, sheet_name=f'{result_description}_contrast')
    return df_pivot


def scatter_contrast_by_condition(df_pivot: pd.DataFrame, metric_column: str, label_column: str, result_description: str):
    '''Contrast clean / confusing values in df_pivot for metric_column to identify which clean is better than confusing
    x-axis: metric_column for clean, y-axis: metric_column for confusing
    label_column to color scatters by group
    store result of plots
    '''
    labels = df_pivot[label_column].unique()
    colors = plt.get_cmap('viridis')(np.linspace(0, 1, len(labels)))

    fig, ax = plt.subplots()
    for i, label in enumerate(labels):
        df_pivot[df_pivot[label_column] == label].plot.scatter(
            x=CONDITION_CLEAN, y=CONDITION_CONFUSING, color=colors[i], label=label, legend=True, ax=ax)
    plt.legend()
    # legend1 = plt.legend(*scatter.collections[0].legend_elements(),
    #                     loc='lower left', title='Categories')
    # scatter.add_artist(legend1)

    ax.axline((0, 0), slope=1, color='grey')
    plt.xlabel(f'{metric_column} {CONDITION_CLEAN}')
    plt.ylabel(f'{metric_column} {CONDITION_CONFUSING}')
    plt.tight_layout()
    plot_path = get_eval_aggregation_snippet_categories_path(
        f'{result_description}_{metric_column.lower()}_contrast', plot=True)
    plt.savefig(plot_path,
                bbox_inches='tight', pad_inches=0)
    plt.savefig(plot_path.with_suffix('.png'),
                bbox_inches='tight', pad_inches=0)
    plt.show()


def distribution_contrast_by_condition(df_pivot: pd.DataFrame, metric_column: str, label_column: str, result_description: str):
    fig, ax = plt.subplots(1, 4, figsize=(20, 5))
    plt.title(metric_column)
    sns.set_palette([
        CONDITION_COLORS[CONDITION_CLEAN],
        CONDITION_COLORS[CONDITION_CONFUSING]])
    sns.swarmplot(
        data=df_pivot[[CONDITION_CLEAN, CONDITION_CONFUSING]], ax=ax[0])
    sns.boxplot(
        data=df_pivot[[CONDITION_CLEAN, CONDITION_CONFUSING]], ax=ax[1])
    sns.violinplot(
        data=df_pivot[[CONDITION_CLEAN, CONDITION_CONFUSING]], ax=ax[2])
    sns.stripplot(
        data=df_pivot[[CONDITION_CLEAN, CONDITION_CONFUSING]], ax=ax[3])
    # ax.invert_yaxis()
    plot_path = get_eval_aggregation_snippet_categories_path(
        f'{result_description}_{metric_column.lower()}_swarm', plot=True)
    plt.savefig(plot_path,
                bbox_inches='tight', pad_inches=0)
    plt.savefig(plot_path.with_suffix('.png'),
                bbox_inches='tight', pad_inches=0)
    plt.show()


def group_aggregate_behavioral(df: pd.DataFrame, group_factors: list[str], result_description: str, display_df=True, plot_contrast_df=True):
    '''Aggregates behavioral measures (answer times and answer correctness, difficulty assessment )'''
    # column level for answer type and assessment
    # group by group_factors
    behavioral_data_grouped = df.groupby(by=group_factors).agg({
        'Duration': [min, max, 'mean', 'std'],
        # 'Difficulty_Time':[min, max, 'mean'],
        'Correctness': [lambda x:count_instances(x, ANSWER_CORRECTNESS[0]),
                        lambda x:count_instances(x, ANSWER_CORRECTNESS[1]),
                        lambda x:count_instances(x, ANSWER_CORRECTNESS[2]),
                        lambda x:count_instances_rel(x, ANSWER_CORRECTNESS[0]),
                        lambda x:count_instances_rel(x, ANSWER_CORRECTNESS[1]),
                        lambda x:count_instances_rel(x, ANSWER_CORRECTNESS[2]),
                        ],
        'Rating': [lambda x:count_instances(x, RATINGS[0]),
                   lambda x:count_instances(x, RATINGS[1]),
                   lambda x:count_instances(x, RATINGS[2]),
                   lambda x:count_instances_rel(x, RATINGS[0]),
                   lambda x:count_instances_rel(x, RATINGS[1]),
                   lambda x:count_instances_rel(x, RATINGS[2]),
                   ],
    })

    # rename columns
    behavioral_data_grouped.columns = ([f'{c[0]}_{c[1].title()}' for c in behavioral_data_grouped.columns[:4]] +
                                       [f'Correctness_{s}' for s in ANSWER_CORRECTNESS] +
                                       [f'Correctness_Rel_{s}' for s in ANSWER_CORRECTNESS] +
                                       [f'Rating_{s}' for s in RATINGS] +
                                       [f'Rating_Rel_{s}' for s in RATINGS])
    # set group_factors back as columns instead of as index
    behavioral_data_grouped = behavioral_data_grouped.reset_index()
    if result_description:
        behavioral_data_grouped.to_csv(get_eval_aggregation_snippet_categories_path(
            result_description), sep=';', index=False)
        with pd.ExcelWriter(EVAL_PATH_AGGREGATED_DATA_SUMMARY, mode=('a'if EVAL_PATH_AGGREGATED_DATA_SUMMARY.exists() else 'w'), engine='openpyxl') as writer:
            behavioral_data_grouped.to_excel(
                writer, sheet_name=result_description, index=False)
    if display_df:
        display(behavioral_data_grouped)
    if {CONDITION, SNIPPET_COLUMN_AOC_CATEGORY}.issubset(group_factors):
        df_pivot = contrast_by_condition(behavioral_data_grouped, CONDITION, [
            'Duration_Mean', 'Correctness_Rel_True'], 'AoC_category', display_df=display_df, result_description=result_description)
        if plot_contrast_df:
            answers = df_pivot['Duration_Mean'].reset_index()
            scatter_contrast_by_condition(
                answers, 'Duration_Mean', SNIPPET_COLUMN_AOC_CATEGORY,  result_description=result_description)
            distribution_contrast_by_condition(
                answers, 'Duration_Mean', SNIPPET_COLUMN_AOC_CATEGORY,  result_description=result_description)
            correctness = df_pivot['Correctness_Rel_True'].reset_index()
            scatter_contrast_by_condition(
                correctness, 'Correctness_Rel_True', SNIPPET_COLUMN_AOC_CATEGORY,  result_description=result_description)
            distribution_contrast_by_condition(
                correctness, 'Correctness_Rel_True', SNIPPET_COLUMN_AOC_CATEGORY,  result_description=result_description)
    else:
        df_pivot = None
    return behavioral_data_grouped, df_pivot
