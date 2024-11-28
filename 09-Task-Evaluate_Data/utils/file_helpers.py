import json
import re
from pathlib import Path
from typing import Union

import pandas as pd
from utils.file_settings import (CONDITION_FILE_PATTERN,
                                 SEQUENCE_ORDER_COLUMN_BLOCK,
                                 SEQUENCE_ORDER_COLUMN_BLOCK_INDEX,
                                 SEQUENCE_ORDER_COLUMNS)
from utils.path_helpers import get_exclusion_path
from utils.path_settings import PROCESSED_PATH, RAW_PATH
from utils.textconstants import (BEHAVIORAL, EEG, HDF_FILE, PARTICIPANT,
                                 SNIPPET, VISUAL)


def get_participant_folder_per_participant(raw_folder: bool = True) -> dict[str, Path]:
    '''get participant folder per participant identified in the base path
    requirement: the folder must contain three digits in succession, and should not contain any other digits

    returns: the participant numbers, and per each the participant folder
    '''
    folders = {}
    for participant_folder in (RAW_PATH if raw_folder else PROCESSED_PATH).iterdir():
        if not participant_folder.is_dir():
            continue
        # identify participant number
        numbers = re.findall(r'\d\d\d', participant_folder.stem)
        if not numbers:
            print(
                f'in subfolder {participant_folder.as_posix()}, no participant number could be identified.')
            continue
        participant = numbers[0]
        folders[participant] = participant_folder
    return folders


ExclusionLevels = Union[PARTICIPANT, SNIPPET, HDF_FILE]
DataModes = [EEG, BEHAVIORAL, VISUAL]


def create_exclusion_structure_for_participant(trials: pd.Series | list[str], hdf_files: list[Path]) -> dict[ExclusionLevels, list[str] | dict[str, dict[str, list[str]]]]:
    '''creates the exclusion structure for a participant based on the given trials and the hdf files
    Arguments:
    * trials: a sequence of snippets supposed to be viewed by the participant
    * hdf_files: the hdf5 files created during the experiment run

    returns: a dictionary containing the basic structure for the exclusion, including the participant as a whole, the snippet trials and the hdf files
    '''
    exclusions = {PARTICIPANT: {mode: [] for mode in DataModes},
                  SNIPPET: {snippet: {mode: [] for mode in DataModes} for snippet in trials},
                  HDF_FILE: {f.name: {mode: [] for mode in [BEHAVIORAL, VISUAL]} for f in hdf_files}}
    return exclusions


def update_with_manual_exclusions(exclusions: dict[ExclusionLevels, list[str] | dict[str, list[str]]], manual_exclusions_file: Path):
    '''updates the current exclusion dictionary with the one for manually determined exclusions (in-place)

    Arguments:
    * exclusions: the current state of (automatically defined) exclusions
    * manual_exclusions_file: the file containing the manual exclusions
    '''
    if not manual_exclusions_file.exists():
        return
    with open(manual_exclusions_file, 'r') as f:
        manual_exclusions = json.load(f)
    for level in exclusions:
        if not level in manual_exclusions:
            continue
        if level == PARTICIPANT:
            exclusions[level] += manual_exclusions[level]
        else:
            for key in exclusions[level]:
                if not key in manual_exclusions[level]:
                    continue
                for mode in exclusions[level][key]:
                    if not mode in manual_exclusions[level][key]:
                        continue
                    exclusions[level][key][mode] = sorted(
                        set(exclusions[level][key][mode] + manual_exclusions[level][key][mode]))


def update_exclusion_value(exc, level: ExclusionLevels, mode: Union[EEG, BEHAVIORAL, VISUAL], key: str, value: list[str]):
    if level == PARTICIPANT:
        if not mode in exc[level]:
            print(
                f'wanted mode {mode} of level {level} and not identified in exclusion file, possible keys {exc[level][mode].keys()}')
            raise Exception()
        exc[level][mode] = sorted(set(exc[level][mode]+value))
    else:
        if not key in exc[level]:
            print(
                f'wanted key {key} of level {level} not identified in exclusion file, possible keys {exc[level].keys()}')
            raise Exception()
        if not mode in exc[level][key]:
            print(
                f'wanted mode {mode} of level {level} and key {key} not identified in exclusion file, possible keys {exc[level][key].keys()}')
            raise Exception()
        exc[level][key][mode] = sorted(set(exc[level][key][mode]+value))


def update_exclusions(participant: str, level: ExclusionLevels, mode: str, key_values: dict[str, str]):
    if not key_values:
        return
    with open(get_exclusion_path(participant), 'r+') as f:
        exclusions = json.load(f)
        f.seek(0)
        for key, value in key_values.items():
            if not isinstance(value, list):
                value = [value]
            update_exclusion_value(
                exclusions, level, mode, key, value)
        json.dump(exclusions, f, indent=4, sort_keys=True)
        f.truncate()
    # with open(get_exclusion_path(), 'r+') as f:
    #     exclusions = json.load(f)
    #     f.seek(0)
    #     for key in key_values:
    #         update_exclusion_value(
    #             exclusions[participant], level, key, key_values[key])
    #     json.dump(exclusions, f, indent=4, sort_keys=True)
    #     f.truncate()


def get_exclusions(participant: str, levels: list[ExclusionLevels], modes: list[str] = DataModes):
    with open(get_exclusion_path(participant), 'r+') as f:
        exclusions: dict = json.load(f)
        wanted_exclusions = {}
        for level in levels:
            if level == PARTICIPANT:
                wanted_exclusions[PARTICIPANT] = {
                    m: exclusions[PARTICIPANT][m] for m in modes if m in exclusions[PARTICIPANT]}
            else:
                wanted_exclusions[level] = {k: {m: exclusions[level][k][m]
                                                for m in modes if m in exclusions[level][k]} for k in exclusions[level]}
    return wanted_exclusions


def get_condition_files_per_participant() -> dict[str, tuple[str, str, str]]:
    '''get condition files (3 files as a tuple) per participant folders 
    identified in the base path
    requirement: exactly three Excel files per participant

    returns: the participant numbers, and per each three condition files, each per round
    '''
    condition_files = {}
    for participant, participant_folder in get_participant_folder_per_participant().items():
        condition_files[participant] = []
        for file in participant_folder.iterdir():
            # find excel files with identical participant marking
            match = re.match(CONDITION_FILE_PATTERN, file.name)
            if match:
                if match.groupdict()[PARTICIPANT] != participant:
                    print(
                        f'weird file in {participant_folder}, {file.name} with participant ' +
                        f'{match.groupdict()[PARTICIPANT]} does not match participant ' +
                        f'{participant} identified in folder')
                else:
                    condition_files[participant].append(file)
        # check that there are three files
        if len(condition_files[participant]) == 3:
            condition_files[participant] = tuple(
                sorted(condition_files[participant]))
        else:
            print(
                'Not all three condition files found for participant ' +
                f'{participant}, only {condition_files[participant]}')
            raise Exception()
    return condition_files


def get_sequence_order_per_participant() -> dict[str, pd.DataFrame]:
    f'''get sequence order of snippets from condition files per participant folders
    identified in the {RAW_PATH} path

    returns: the participant numbers, and per each a complete sequence order across all rounds
    '''
    condition_files = get_condition_files_per_participant()
    sequence_orders = {}
    for participant, files in condition_files.items():
        block_orders = []
        for i, file in enumerate(files):
            # add snippets sequence to orders
            block_order = pd.read_excel(file)
            block_order[SNIPPET] = block_order['SnippetName'].apply(
                lambda x: str(x).split('.', 1)[0])
            block_order[SNIPPET] = block_order[SNIPPET].str.replace('\'', '')
            block_order[SEQUENCE_ORDER_COLUMN_BLOCK] = i+1
            block_order[SEQUENCE_ORDER_COLUMN_BLOCK_INDEX] = block_order.index+1
            block_order = block_order.drop(
                columns=[c for c in block_order.columns if not (c in SEQUENCE_ORDER_COLUMNS)])
            block_orders.append(block_order)
        if files:
            sequence_order = pd.concat(block_orders).reset_index(drop=True)
            sequence_orders[participant] = sequence_order
    return sequence_orders
