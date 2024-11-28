import gc
import json
import re
from math import log10
from pathlib import Path
from typing import Union

import mne
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib as mpl
from mne.io import Raw
from tqdm.notebook import tqdm
from utils.eeg_settings import (ACCEPTED_SYNCHRONIZATION_OFFSET, EEG_CHANNELS,
                                EEG_FREQUENCY, EEG_LONG_BUFFER,
                                EEG_MEAN_BUFFER, EEG_SHORT_BUFFER,
                                EEG_STIMULUS, EEG_STIMULUS_FIXATION_CROSS,
                                EEG_STIMULUS_SNIPPET_END,
                                EEG_STIMULUS_SNIPPET_START,
                                EEG_VOLTAGE_OVERALL, EEG_VOLTAGE_STEP,
                                EEG_VOLTAGE_WINDOW, EOG_CHANNELS, ERP_PARAMETER_CORRECT_TRIALS_ONLY, ERP_PARAMETER_EPOCH_INTERVAL,
                                FRP_EEG_STIMULUS_SNIPPET_START,
                                IMPEDANCE_UPPER_BOUND, IMPEDANCE_VALUE, MNE_KEY_FREQUENCY,
                                STIMULUS_EVENT_NAMES)
from utils.file_helpers import (get_exclusions,
                                get_participant_folder_per_participant)
from utils.file_settings import (ANNOTATION_COLUMN_DESCRIPTION,
                                 ANNOTATION_COLUMN_ONSET,
                                 ANNOTATION_COLUMN_ONSET_FLOAT,
                                 BEHAVIORAL_COLUMN_CORRECTNESS,
                                 BEHAVIORAL_COLUMN_END,
                                 BEHAVIORAL_COLUMN_FIXATION_START,
                                 BEHAVIORAL_COLUMN_START, COLUMN_TIME,
                                 EEG_COLUMN_STIMULUS, FIXATION_COLUMN_START,
                                 HDF_INDEX, SEPARATOR)
from utils.path_helpers import (get_all_erp_epoch_paths, get_behavioral_data_path, get_erp_average_path,
                                get_eeg_trial_path, get_erp_epoch_path,
                                get_erp_fixation_analysis_path,
                                get_erp_nave_path, get_erp_status_path)
from utils.path_settings import (EEG_FILE_DATA_ENDING, EEG_FILE_HEADER_ENDING,
                                 EEG_FILE_MARKER_ENDING, PROCESSED_PATH)
from utils.snippet_helpers import get_snippet_number, get_snippet_variant
from utils.snippet_settings import (CONDITION, CONDITION_CLEAN,
                                    CONDITION_COLORS, CONDITION_CONFUSING,
                                    CONDITION_DIFF, CONDITION_VARIANT_MATCH,
                                    PANDAS_DESCRIPTION_AGG_FUNCTIONS,
                                    PANDAS_DESCRIPTION_AGG_NAMES, SNIPPET_GROUP_ALL, SNIPPET_NUMBERS)
from utils.textconstants import (BEHAVIORAL, EEG, EEG_ERP, FIXATIONS,
                                 PARTICIPANT, SNIPPET, TIME, TOTAL, VISUAL)
from utils.visual_settings import (FIXATION_SELECTION_ALGORITHM,
                                   FIXATION_SELECTION_ALGORITHMS,
                                   FIXATION_SELECTION_SHORT_VERSION)


def check_file_existence(files: dict[str, Path], file: Path, file_ending: str, participant: str):
    '''check whether file has the given extension and there already exists one.

    Arguments: 
    * files: where to add suitable files per ending
    * file: the path to check
    * file_endings: the file ending to check for
    * participant: the participant to name when problems arise

    raises: Exception if file with given ending has already been identified
    '''
    if file.suffix == file_ending:
        if file_ending in files:
            print(
                f'Multiple \'{file_ending}\' files found for participant {participant}: {files[file_ending].name}, new: {file.name}')
            raise Exception()
        files[file_ending] = file


def get_eeg_files_per_participant() -> dict[str, dict[str, Path]]:
    f'''get eeg files (3 files as dictionary) per participant folders identified in the base path
    requirement: exactly one eeg file of each file ending per participant (or none at all, then participant is ignored)

    returns: the participant numbers, and per each the three eeg files
            {{'{EEG_FILE_HEADER_ENDING}': path to the eeg header file,
            '{EEG_FILE_MARKER_ENDING}': path to the eeg marker file,
            '{EEG_FILE_DATA_ENDING}': path to the eeg data file}}
    '''
    eeg_files = {}

    for participant, participant_folder in get_participant_folder_per_participant().items():
        files = {}
        for file in participant_folder.iterdir():
            check_file_existence(
                files, file, EEG_FILE_DATA_ENDING, participant)
            check_file_existence(
                files, file, EEG_FILE_HEADER_ENDING, participant)
            check_file_existence(
                files, file, EEG_FILE_MARKER_ENDING, participant)
        # check that either all three files exits, or none at all
        if ((EEG_FILE_DATA_ENDING in files) ^ (EEG_FILE_HEADER_ENDING in files)) or ((EEG_FILE_DATA_ENDING in files) ^ (EEG_FILE_MARKER_ENDING in files)):
            print(f'Not all files found for {participant}: {files}')
            return None
        # only add if all files exist
        if files:
            eeg_files[participant] = files
    return eeg_files


EEG_HEADER_DATE = re.compile('Impedance \[kOhm\] at (\d\d:\d\d:\d\d) :')
EEG_MARKER_DATE = re.compile(r'New Segment,,(\d+),1,0,(\d+)')


def anonymize_eeg_data(eeg_file: dict[str, Path]):
    '''anonymizes eeg files in-place by removing all traces of timestamps in the marker and header files

    Argument: eeg_file: a dictionary mapping the eeg file keys to the respective paths of the files
    '''
    with open(eeg_file[EEG_FILE_HEADER_ENDING], 'r+') as f:
        eeg_header_content = f.read()
        f.seek(0)
        eeg_header_content = EEG_HEADER_DATE.sub(
            'Impedance [kOhm] at the beginning of the experiment :', eeg_header_content)
        f.write(eeg_header_content)
        f.truncate()
    with open(eeg_file[EEG_FILE_MARKER_ENDING], 'r+') as f:
        eeg_marker_content = f.read()
        f.seek(0)
        eeg_marker_content = EEG_MARKER_DATE.sub(
            r'New Segment,,\1,1,0,0', eeg_marker_content, count=0)
        f.write(eeg_marker_content)
        f.truncate()


def load_eeg_data(filepath: Path, preload: bool = True) -> tuple[Raw, float]:
    raw_eeg = mne.io.read_raw_brainvision(filepath, eog=tuple(EOG_CHANNELS),
                                          preload=preload)
    frequency = raw_eeg.info[MNE_KEY_FREQUENCY]
    return raw_eeg, frequency


def check_impedances(impedance_data: pd.DataFrame, log: bool = True) -> bool:
    impedance_data[f'{IMPEDANCE_UPPER_BOUND}_check'] = impedance_data.apply(lambda row: max(
        0, row[IMPEDANCE_VALUE]-row[IMPEDANCE_UPPER_BOUND]), 1)
    # display(impedance_data)
    impedance_errors = ((
        impedance_data[f'{IMPEDANCE_UPPER_BOUND}_check'] > 0)*1).sum(), \
        impedance_data[f'{IMPEDANCE_UPPER_BOUND}_check'].max(), \
        impedance_data[f'{IMPEDANCE_UPPER_BOUND}_check'].sum()

    impedance_okay = not (impedance_errors[0] > 2 or
                          impedance_errors[1] > 5 or
                          impedance_errors[2] >= 7)
    if log:
        print(
            f'{impedance_errors[0]} errors with impedances, maximum breach of {impedance_errors[1]}, sum of breaches in total {impedance_errors[2]}.\n\tImpedances accepted: {impedance_okay}')
    return impedance_okay


def prepare_annotation_information(eeg_data: Raw) -> tuple[pd.DataFrame, float]:
    '''extracts and prepares annotation information from the given EEG data

    Arguments: eeg_data: the eeg data

    returns: a tuple of
    * the annotations as DataFrame with columns onset, duration and description extracted from the eeg data, as well as an additional column describing the onset as a float value to be used for cropping, reinsert, ...
    * the duration of the eeg data in seconds
    '''
    # get recording information required+
    # offset in seconds between start of the file counter and start of samples
    recording_offset = eeg_data.first_time
    recording_duration = (eeg_data.n_times-1) / \
        eeg_data.info[MNE_KEY_FREQUENCY]  # duration of recording

    annotation_data = eeg_data.annotations.to_data_frame()
    # transform onset of an annotation into a float based on recording start, erasing offset, to use for cropping
    annotation_data[ANNOTATION_COLUMN_ONSET_FLOAT] = annotation_data[ANNOTATION_COLUMN_ONSET].apply(
        lambda onset: (onset-pd.Timestamp(year=1970, month=1, day=1)).total_seconds()-recording_offset)

    return annotation_data, recording_duration


def crop_to_complete_annotation_range(eeg_data: Raw) -> None:
    '''crop given Raw object by the annotations present in the object.

    The new sequence starts shortly before first fixation cross, 
    and end shortly after last snippet end, or longer after the last fixation cross

    Arguments:
    * eeg_data: the eeg data 
    * time_before_first_snippet: the time buffer to add before the first fixation cross
    * time_after_last_snippet: the time buffer to add after the last snippet end if found
    * time_constant_without_ending: the time buffer to add after the last fixation cross if no end found
    '''
    # get required information from annotations
    annotation_data, recording_duration = prepare_annotation_information(
        eeg_data)

    # get first fixation cross or start
    start_buffer = {EEG_STIMULUS_FIXATION_CROSS: EEG_SHORT_BUFFER} | {
        stimuli: EEG_MEAN_BUFFER for stimuli in EEG_STIMULUS_SNIPPET_START.values()}
    snippets_start_row = annotation_data[annotation_data[ANNOTATION_COLUMN_DESCRIPTION].isin(
        start_buffer.keys())].iloc[0]

    snippets_start_time = snippets_start_row[ANNOTATION_COLUMN_ONSET_FLOAT] - \
        start_buffer[snippets_start_row[ANNOTATION_COLUMN_DESCRIPTION]]
    snippets_start_time = max(0.0, snippets_start_time)

    # get snippet ends and use them to calculate the end of the cropped recording
    end_buffer = {EEG_STIMULUS_SNIPPET_END: EEG_SHORT_BUFFER} | {
        stimuli: EEG_LONG_BUFFER for stimuli in EEG_STIMULUS_SNIPPET_START.values()}
    snippets_end_row = annotation_data[annotation_data[ANNOTATION_COLUMN_DESCRIPTION].isin([
        EEG_STIMULUS_FIXATION_CROSS, *EEG_STIMULUS_SNIPPET_START.values(), EEG_STIMULUS_SNIPPET_END])]

    if not snippets_end_row.empty:
        snippets_end_time = snippets_end_row.iloc[-1][ANNOTATION_COLUMN_ONSET_FLOAT] + \
            EEG_MEAN_BUFFER
    # otherwise, add a longer buffer to the last fixation
    else:
        snippets_end_time = min(
            recording_duration, snippets_end_row[ANNOTATION_COLUMN_ONSET_FLOAT] +
            end_buffer[snippets_end_row[ANNOTATION_COLUMN_DESCRIPTION]])
    # crop
    assert (recording_duration >= snippets_end_time-snippets_start_time)
    eeg_data.crop(tmin=snippets_start_time,
                  tmax=snippets_end_time, include_tmax=True)


def export_eeg_brainvision(eeg_data: Raw, eeg_path: Path):
    assert (eeg_path.suffix == EEG_FILE_HEADER_ENDING)
    eeg_data.export(eeg_path, overwrite=True, verbose=False)
    eeg_marker_path = eeg_path.with_suffix(EEG_FILE_MARKER_ENDING)
    with open(eeg_marker_path, 'r+') as f:
        eeg_marker_content = f.read()
        f.seek(0)
        eeg_marker_content = eeg_marker_content.replace(
            'Comment,Bad Interval/', 'Bad Interval,')
        eeg_marker_content = eeg_marker_content.replace(
            'Comment,Bad', 'Bad Interval,Bad')
        f.write(eeg_marker_content)
        f.truncate()


def check_manual_ICA_reasoning(artifact_reasoning: pd.DataFrame):
    # print(artifact_reasoning)
    # check that all components are still there
    expected_components = set(f'F{str(i).zfill(2)}' for i in range(32))
    given_components = set(artifact_reasoning['Component'].values)
    assert given_components == expected_components, f'''The components are not correct, \n\twanted {
        expected_components},\n\tgiven {given_components}'''
    # check that description & topology are filled
    assert (artifact_reasoning['Description'].apply(lambda v: not pd.isna(
        v)).all()), 'Description must be filled for each component.'
    assert (artifact_reasoning['Topology'].apply(lambda v: not pd.isna(
        v)).all()), 'Topology must be filled for each component.'
    # check that reason is given if artifact... is not false
    assert artifact_reasoning.apply(lambda row: not pd.isna(row['Reason']) if row['Artifact or Channel related'] != False else True, axis=1).all(
    ), 'Each component identified as possibly being artifact or channel related must have a reason towards the choice of inclusion or not.'
    # check that included is not false if artifact... is false
    assert artifact_reasoning.apply(lambda row: row['Included'] != False if row['Artifact or Channel related'] == False else True, axis=1).all(
    ), 'Each component not identified as possibly being artifact or channel related must be included.'


def assign_trials_to_annotations(eeg_data: Raw, behavioral_events: pd.DataFrame) -> tuple[bool, pd.DataFrame]:
    '''Split given Raw object to receive eeq splits per snippet.

    Each split starts shortly before first fixation cross, 
    and end shortly after next snippet end, or until the next fixation cross.
    If there is no other way of determination, a long buffer is added to the current fixation crops of the split.

    Arguments:
    * eeg_data: the eeg data
    * sequence_order: the snippet sequence order to assign eeg splits to each snippet
    * time_before_first_snippet: the time buffer to add before the first fixation cross
    * time_after_last_snippet: the time buffer to add after the last snippet end if found
    * time_constant_without_ending: the time buffer to add after the last fixation cross if no end found

    returns: eeg split per snippet
    '''
    annotation_data, _ = prepare_annotation_information(
        eeg_data)
    annotation_data = annotation_data[annotation_data[ANNOTATION_COLUMN_DESCRIPTION].isin([EEG_STIMULUS_FIXATION_CROSS,
                                                                                           EEG_STIMULUS_SNIPPET_END,
                                                                                           *EEG_STIMULUS_SNIPPET_START.values()])]

    def annotation_synchronization_check(data: pd.DataFrame, time_check: bool = False) -> bool:
        data['stimuli_check'] = data[ANNOTATION_COLUMN_DESCRIPTION] == data[EEG_COLUMN_STIMULUS]
        if time_check:
            data['time_check'] = data.apply(lambda row: (row['onset_e'] < 0) or
                                            ((row['onset_a'] - row['onset_e']) < ACCEPTED_SYNCHRONIZATION_OFFSET), axis=1)
        if not data['stimuli_check'].all():
            return False
        if time_check and not data['time_check'].all():
            return False
        data = data.drop(columns=[c for c in data if (c == 'onset_a') or (
            (c != SNIPPET) and (not c in annotation_data.columns))])
        return True

    print('annotations:', annotation_data.shape[0],
          'behavioral_events:', behavioral_events.shape[0])

    annotation_data.reset_index(drop=True, inplace=True)
    behavioral_events.reset_index(drop=True, inplace=True)
    # possibility 1: match via index if both are the same length
    if annotation_data.shape[0] == behavioral_events.shape[0]:
        annotation_data['onset_a'] = 0
        behavioral_events['onset_e'] = 0
        for hdf_index in behavioral_events[HDF_INDEX].unique():
            hdf_data = behavioral_events[behavioral_events[HDF_INDEX] == hdf_index]
            anno_data = annotation_data[behavioral_events[HDF_INDEX] == hdf_index]
            behavioral_events.loc[hdf_data.index,
                                  'onset_e'] = hdf_data['Time'] - hdf_data['Time'].iloc[0]
            annotation_data.loc[anno_data.index, 'onset_a'] = anno_data[ANNOTATION_COLUMN_ONSET_FLOAT] - \
                anno_data[ANNOTATION_COLUMN_ONSET_FLOAT].iloc[0]

        com_data = pd.concat([behavioral_events, annotation_data], axis=1)
        if annotation_synchronization_check(com_data):
            return True, com_data
    test_data = pd.concat([behavioral_events, annotation_data], axis=1)
    # possibility 2: match via time based on first event / annotation
    # com_data = pd.DataFrame([], columns = [c for c in test_data.columns])
    # annotations_index, behavioral_index=0, 0
    # annotation_data['onset_a'] = 0
    # behavioral_events['onset_e'] = 0
    # for hdf_index in behavioral_events[HDF_INDEX].unique():
    #     hdf_data = behavioral_events[behavioral_events[HDF_INDEX]==hdf_index]
    #     anno_data = annotation_data[behavioral_events[HDF_INDEX]==hdf_index]
    #     behavioral_events.loc[hdf_data.index, 'onset_e'] = hdf_data['Time'] - hdf_data['Time'].iloc[0]
    #     annotation_data.loc[anno_data.index, 'onset_a'] = anno_data[ANNOTATION_COLUMN_ONSET_FLOAT] - anno_data[ANNOTATION_COLUMN_ONSET_FLOAT].iloc[0]
    # while (annotations_index<annotation_data.shape[0] and behavioral_index<behavioral_events.shape[0]):
    #     pass
    # if (not com_data.empty) and annotation_synchronization_check(com_data):
    #     return True, com_data
    # possibility 3: match via time based on last event / annotation
    # com_data = pd.DataFrame([], columns = [c for c in test_data.columns])
    # annotations_index, behavioral_index=annotation_data.shape[0]-1, behavioral_events.shape[0]-1
    # while (annotations_index>=0 and behavioral_index<behavioral_events>=0):
    # if (not com_data.empty) and annotation_synchronization_check(com_data):
    #     return True, com_data
    # possibility 4: match via time diff based on events / annotation
    # com_data = pd.DataFrame([], columns = [c for c in test_data.columns])
    # if (not com_data.empty) and annotation_synchronization_check(com_data):
    #     return True, com_data
    return False, test_data


def check_trial_annotations(trial_annotation_data: pd.DataFrame, eeg_data: Raw):
    # print(trial_annotation_data)
    annotation_data, _ = prepare_annotation_information(eeg_data)
    annotation_data = annotation_data[annotation_data[ANNOTATION_COLUMN_DESCRIPTION].isin([EEG_STIMULUS_FIXATION_CROSS,
                                                                                           EEG_STIMULUS_SNIPPET_END,
                                                                                           *EEG_STIMULUS_SNIPPET_START.values()])]
    data1 = (trial_annotation_data[[ANNOTATION_COLUMN_DESCRIPTION, ANNOTATION_COLUMN_ONSET_FLOAT]].dropna(axis='index')
             .sort_values([ANNOTATION_COLUMN_ONSET_FLOAT]).reset_index(drop=True))
    data2 = (annotation_data[[ANNOTATION_COLUMN_DESCRIPTION, ANNOTATION_COLUMN_ONSET_FLOAT]]
             .sort_values([ANNOTATION_COLUMN_ONSET_FLOAT]).reset_index(drop=True))
    # check that all annotations covered by a line
    assert data1[ANNOTATION_COLUMN_DESCRIPTION].equals(
        data2[ANNOTATION_COLUMN_DESCRIPTION]), 'All annotations must be present.'
    data1[ANNOTATION_COLUMN_ONSET_FLOAT] = data1[ANNOTATION_COLUMN_ONSET_FLOAT].round(
        3)
    data2[ANNOTATION_COLUMN_ONSET_FLOAT] = data2[ANNOTATION_COLUMN_ONSET_FLOAT].round(
        3)
    time_delta = (data2[ANNOTATION_COLUMN_ONSET_FLOAT] -
                  data1[ANNOTATION_COLUMN_ONSET_FLOAT]).abs().ge(1.5/EEG_FREQUENCY)
    assert not time_delta.any(), f'All annotations must be present with their given frame'
    # check that all annotations, that are not fixation crosses, have an assigned snippet
    assert (trial_annotation_data.apply(lambda row: (pd.isna(row[ANNOTATION_COLUMN_DESCRIPTION]) or row[ANNOTATION_COLUMN_DESCRIPTION] == EEG_STIMULUS_FIXATION_CROSS) or pd.notna(
        row[SNIPPET]), axis=1).all()), "All annotations that are not fixation crosses require an assigned event."
    # check that stimuli identical
    assert (trial_annotation_data.dropna(axis='index').apply(lambda row: row[EEG_COLUMN_STIMULUS] == row[ANNOTATION_COLUMN_DESCRIPTION], axis=1).all(
    )), 'The stimuli of event and annotation must be identical'
    # check time synchronization between events and annotations work within a hdf file index
    for hdf_index in trial_annotation_data[HDF_INDEX].unique():
        if pd.isna(hdf_index):
            continue
        hdf_trials = trial_annotation_data[trial_annotation_data[HDF_INDEX] == hdf_index].dropna(
            axis='index')
        if hdf_trials.empty:
            continue
        hdf_trials['Time delta beh eeg'] = hdf_trials[ANNOTATION_COLUMN_ONSET_FLOAT] - hdf_trials[TIME]
        assert (hdf_trials['Time delta beh eeg'].max() - hdf_trials['Time delta beh eeg'].min() < 0.3), \
            f'''The difference between eeg annotation timestamp and behavioral event timestamp should remain within a second of time.\n {
                hdf_trials["Time delta beh eeg"]}'''


def get_synchronized_annotations(trial_annotation_data: pd.DataFrame, behavioral_data: pd.DataFrame) -> pd.DataFrame:
    annotations_to_delete = []
    # check isna and print na lines to delete
    na_rows = trial_annotation_data[trial_annotation_data.isna().any(axis=1)]
    if not na_rows.empty:
        print(f'\tThese rows will be deleted (ignored) due to nas in the rows')
        print(na_rows)
    relevant_trial_annotation_data = trial_annotation_data.dropna(axis='index')
    for i, row in relevant_trial_annotation_data.iterrows():
        behavioral_row = behavioral_data[behavioral_data[SNIPPET] == row[SNIPPET]].squeeze(
        )
        if behavioral_row.empty:
            annotations_to_delete.append(i)
            continue
        if row[ANNOTATION_COLUMN_DESCRIPTION] == EEG_STIMULUS_FIXATION_CROSS:
            behavioral_time = behavioral_row[BEHAVIORAL_COLUMN_FIXATION_START]
        elif row[ANNOTATION_COLUMN_DESCRIPTION] in EEG_STIMULUS_SNIPPET_START.values():
            behavioral_time = behavioral_row[BEHAVIORAL_COLUMN_START]
        elif row[ANNOTATION_COLUMN_DESCRIPTION] == EEG_STIMULUS_SNIPPET_END:
            behavioral_time = behavioral_row[BEHAVIORAL_COLUMN_END]
        if abs(row[TIME] - behavioral_time) > 0.0001:
            annotations_to_delete.append(i)
            print(
                f'\tAnnotation {row} ignored even though assigned behavioral event, as the behavioral time is expected to be {behavioral_time} from {behavioral_row[[SNIPPET, PARTICIPANT, BEHAVIORAL_COLUMN_FIXATION_START, BEHAVIORAL_COLUMN_START, BEHAVIORAL_COLUMN_END]]}.')
    relevant_trial_annotation_data = relevant_trial_annotation_data[~relevant_trial_annotation_data.index.isin(
        annotations_to_delete)]
    return relevant_trial_annotation_data


def transform_synchronized_annotations(trial_annotation_data: pd.DataFrame) -> pd.DataFrame:
    eeg_snippet_data = trial_annotation_data.pivot(
        columns=EEG_COLUMN_STIMULUS, index=SNIPPET, values=ANNOTATION_COLUMN_ONSET_FLOAT)
    eeg_snippet_data[BEHAVIORAL_COLUMN_FIXATION_START] = eeg_snippet_data[EEG_STIMULUS_FIXATION_CROSS]
    eeg_snippet_data[BEHAVIORAL_COLUMN_START] = eeg_snippet_data.apply(
        lambda row: [row[stimulus] for stimulus in EEG_STIMULUS_SNIPPET_START.values() if not pd.isna(row[stimulus])][0], axis=1)
    eeg_snippet_data[BEHAVIORAL_COLUMN_END] = eeg_snippet_data[EEG_STIMULUS_SNIPPET_END]
    eeg_snippet_data = eeg_snippet_data[[
        BEHAVIORAL_COLUMN_FIXATION_START, BEHAVIORAL_COLUMN_START, BEHAVIORAL_COLUMN_END]]
    return eeg_snippet_data


def split_eeg_segments(eeg_data: Raw, trial_annotations: pd.DataFrame) -> dict[str, Raw]:
    '''Split given Raw object to receive eeg segments per snippet.

    Each split starts shortly before first fixation cross, 
    and end shortly after next snippet end, or until the next fixation cross.
    If there is no other way of determination, a long buffer is added to the current fixation crops of the split.

    Arguments:
    * eeg_data: the eeg data
    * sequence_order: the snippet sequence order to assign eeg segments to each snippet
    * time_before_first_snippet: the time buffer to add before the first fixation cross
    * time_after_last_snippet: the time buffer to add after the last snippet end if found
    * time_constant_without_ending: the time buffer to add after the last fixation cross if no end found

    returns: eeg split per snippet
    '''
    eeg_segments = {}
    for snippet, row in trial_annotations.iterrows():
        start = 0
        if not pd.isna(row[BEHAVIORAL_COLUMN_FIXATION_START]):
            start = row[BEHAVIORAL_COLUMN_FIXATION_START]
        elif not pd.isna(row[BEHAVIORAL_COLUMN_START]):
            start = row[BEHAVIORAL_COLUMN_START]-5.0
        else:
            print(
                f'ignored snippet {snippet} of row {row} due to missing start')
            continue
        start = max(0, start)
        end = 0
        if not pd.isna(row[BEHAVIORAL_COLUMN_END]):
            end = row[BEHAVIORAL_COLUMN_END]
        else:
            end = start+EEG_LONG_BUFFER
        end = min(end, eeg_data.times[-1])
        if start >= end:
            print(start, end)
        eeg_segment_data: Raw = eeg_data.copy().crop(
            tmin=start, tmax=end, include_tmax=True)
        # remove unneeded annotations
        segment_annotations = eeg_segment_data.annotations.to_data_frame()
        segment_annotations['unnecessary'] = ~segment_annotations[ANNOTATION_COLUMN_DESCRIPTION].isin(
            list(EEG_STIMULUS_SNIPPET_START.values())+[EEG_STIMULUS_FIXATION_CROSS, EEG_STIMULUS_SNIPPET_END])
        eeg_segment_data.annotations.delete(
            segment_annotations[segment_annotations['unnecessary']].index)
        # add begin annotation to add snippet name to file
        eeg_segment_data.annotations.append(
            start, 1/EEG_FREQUENCY, f'SNIPPET {snippet}')
        eeg_segments[snippet] = eeg_segment_data
    return eeg_segments


def check_voltage_per_segment(eeg_segments: dict[str, Raw]) -> pd.DataFrame:
    snippet_violation_data = pd.DataFrame(index=[snippet for snippet in eeg_segments],
                                          columns=['Voltage Step Count', 'Voltage Step Channels',
                                                   'Voltage Step Frames', 'Voltage Difference Count',
                                                   'Voltage Difference Channels', 'Voltage Difference Frames'], dtype=object)

    for snippet in eeg_segments:
        eeg_segment = eeg_segments[snippet]
        snippet_violations = check_voltage_in_segment(eeg_segment)
        for key in snippet_violations:
            snippet_violation_data.at[snippet, key] = snippet_violations[key]
    return snippet_violation_data


def check_voltage_in_segment(eeg_segment: Raw, is_epoch: bool = False) -> pd.DataFrame:
    snippet_violations = {}
    assert eeg_segment.info[MNE_KEY_FREQUENCY] == EEG_FREQUENCY
    # check voltage steps
    eeg_content_data: np.ndarray = eeg_segment.get_data(
        picks=EEG_CHANNELS,units='uV')
    if is_epoch:
        eeg_content_data = eeg_content_data[0]
    # * voltage steps >= 30µV/1ms --> (or 60µV/2ms ?)
    voltage_step = np.diff(eeg_content_data, 1)
    abs_voltage_step = np.abs(voltage_step)
    high_voltage_step = abs_voltage_step >= EEG_VOLTAGE_STEP
    has_high_voltage_step = np.any(high_voltage_step)
    if has_high_voltage_step:
        count_high_voltage_step = np.sum(high_voltage_step*1)
        snippet_violations['Voltage Step Count'] = count_high_voltage_step
        channel_high_voltage_step = np.sum(high_voltage_step*1, -1)
        snippet_violations['Voltage Step Channels'] = [
            {channel: channel_high_voltage_step[i] for i, channel in enumerate(EEG_CHANNELS) if channel_high_voltage_step[i] > 0}]
        time_high_voltage_step = np.sum(high_voltage_step*1, 0)
        frame_high_voltage_step = np.nonzero(time_high_voltage_step)[0]
        snippet_violations['Voltage Step Frames'] = [
            {frame: time_high_voltage_step[frame] for frame in frame_high_voltage_step}]
        starts = [eeg_segment.first_time + f /
                  EEG_FREQUENCY for f in frame_high_voltage_step]
        eeg_segment.annotations.append(
            starts, 1/EEG_FREQUENCY, 'BAD Voltage step')
        # plot_eeg(eeg_segment, True, True)
        del count_high_voltage_step
        del time_high_voltage_step
        if is_epoch:
            return snippet_violations
    del voltage_step
    del abs_voltage_step
    del high_voltage_step
    # * voltage difference > 100 µV within 0.2 s
    voltage_windows = np.lib.stride_tricks.sliding_window_view(
        eeg_content_data, 101, -1)
    min_voltage_windows = np.min(voltage_windows, 2)
    max_voltage_windows = np.max(voltage_windows, 2)
    high_difference_voltage = (
        max_voltage_windows-min_voltage_windows) > EEG_VOLTAGE_WINDOW
    has_high_difference_voltage = np.any(high_difference_voltage)
    if has_high_difference_voltage:
        count_high_difference_voltage = np.sum(high_difference_voltage*1)
        snippet_violations['Voltage Difference Count'] = count_high_difference_voltage
        channel_high_difference_voltage = np.sum(
            high_difference_voltage*1, -1)
        snippet_violations['Voltage Difference Channels'] = [
            {channel: channel_high_difference_voltage[i] for i, channel in enumerate(EEG_CHANNELS) if channel_high_difference_voltage[i] > 0}]
        time_high_difference_voltage = np.sum(high_difference_voltage*1, 0)
        frame_high_difference_voltage = np.nonzero(
            time_high_difference_voltage)[0]
        # snippet_violation_data.loc[snippet,'Voltage Difference Frames'] =[{frame:time_high_difference_voltage[frame] for frame in frame_high_difference_voltage.flat}]
        first_time = eeg_segment.tmin if is_epoch else eeg_segment.first_time
        starts = [first_time + f /
                  EEG_FREQUENCY for f in frame_high_difference_voltage]
        last_time = eeg_segment.tmax if is_epoch else eeg_segment._last_time
        durations = [
            min(s+100/EEG_FREQUENCY, last_time)-s for s in starts]
        eeg_segment.annotations.append(
            starts, durations, 'BAD Voltage difference')
        # print(eeg_segment.annotations.to_data_frame())
        # plot_eeg(eeg_segment, True, True)
        del count_high_difference_voltage
        del time_high_difference_voltage
    del voltage_windows
    del min_voltage_windows
    del max_voltage_windows
    del high_difference_voltage
    return snippet_violations


def check_voltage_amplitude(epochs) -> bool:
    # * greater absolute amplitude difference than 140 µV --> or if baseline corrected, then within +/-70 µV
    eeg_content_data = epochs[0].get_data(picks=EEG_CHANNELS,units='uV')[0]
    min_overall_voltage = np.min(eeg_content_data, (0, 1))
    max_overall_voltage = np.max(eeg_content_data, (0, 1))
    if (min_overall_voltage < EEG_VOLTAGE_OVERALL[0]) or (max_overall_voltage > EEG_VOLTAGE_OVERALL[1]):
        return True
    return False


def perform_eeg_erp_averaging(participants: list[str], erp_frp: bool | str = True, correct_data_only: bool = False, epoch_interval: tuple[int, int] = (-0.2, 1),
                              conditional_stimuli: dict[str, str] = EEG_STIMULUS_SNIPPET_START, topomap_times: list[float] = [0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1],
                              plot: bool = False, snippet_group: str = SNIPPET_GROUP_ALL, snippet_numbers: list[int] = SNIPPET_NUMBERS) -> tuple[dict[str, dict[str, mne.Evoked], dict[str, mne.Evoked]]]:
    assert (erp_frp is True or erp_frp in FIXATION_SELECTION_ALGORITHMS), erp_frp
    assert epoch_interval[0] < epoch_interval[1]
    assert all([t >= epoch_interval[0] and t <= epoch_interval[1]
               for t in topomap_times])
    description = get_erp_description(
        erp_frp, correct_data_only, epoch_interval)
    subjectwise_nave = {}
    subjectwise_averages = {}
    subjectwise_frp_offsets = {}
    for participant in tqdm(participants):
        print('----------------------------------------------')
        print(PARTICIPANT, participant)
        # skip participant if excluded
        exclusions = get_exclusions(participant, [PARTICIPANT], [
                                    BEHAVIORAL, EEG, VISUAL])[PARTICIPANT]
        if any(exclusions.values()):
            print('excluded')
            continue
        # Load behavioral data
        if correct_data_only:
            behavioral_data = pd.read_csv(get_behavioral_data_path(
                participant, final_data_exclusion=True), index_col=False, sep=SEPARATOR, dtype={PARTICIPANT: str})
            correct_snippets = behavioral_data[behavioral_data[BEHAVIORAL_COLUMN_CORRECTNESS]][SNIPPET].to_list()
        else:
            correct_snippets = None
        # Load raw data for all snippets
        snippet_segments = get_all_eeg_trial_segments(
            erp_frp == True, participant, correct_trials=correct_snippets, accepted_snippet_numbers=snippet_numbers)

        # Transform annotations to event to epoch and apply baseline correction
        snippet_epochs, frp_fixation_offsets = extract_epochs_from_snippet_segments(erp_frp, description, participant, snippet_group,
                                                                                    snippet_segments, conditional_stimuli.values(), epoch_interval, (epoch_interval[0], 0), True, True)
        frp_fixation_offsets[PARTICIPANT] = participant
        subjectwise_frp_offsets[participant] = frp_fixation_offsets
        # Concatenate epochs
        snippet_groups = [list(snippet_epochs.keys())]
        group_epochs = mne.concatenate_epochs([snippet_epochs[snippet] for snippet in snippet_groups[0]], add_offset=True).pick(
            picks=EEG_CHANNELS).set_montage("easycap-M1")
        # Calculate and plot subjectwise average per condition
        averaged_evoked: mne.Evoked = group_epochs.average(by_event_type=True)
        averaged_evoked = {ev.comment: ev for ev in averaged_evoked}
        averaged_evoked = {
            condition: averaged_evoked[conditional_stimuli[condition]] for condition in conditional_stimuli}
        assert (averaged_evoked[CONDITION_CLEAN].comment == conditional_stimuli[CONDITION_CLEAN]) and (averaged_evoked[CONDITION_CONFUSING].comment == conditional_stimuli[CONDITION_CONFUSING]), \
            f'''{averaged_evoked[CONDITION_CLEAN].comment} should be {conditional_stimuli[CONDITION_CLEAN]} and {
                averaged_evoked[CONDITION_CONFUSING].comment} should be {conditional_stimuli[CONDITION_CONFUSING]}'''
        subjectwise_averages[participant] = averaged_evoked
        subjectwise_nave[participant] = {
            condition: averaged_evoked[condition].nave for condition in averaged_evoked}
        if plot:
            plot_all_evoked_low_frequency(erp_frp, description, averaged_evoked,
                                          participant, topomap_times, False)
        # comparison to BrainVision results
        # ae_c,_ = load_eeg_data(f'E:/PHD/Studies/aoc-frp-main-studies/Main_Study_Part/08-Data-Trial_Recordings/prepared_EEG_files/ERP subjectwise averages/AoCfrp_{participant}__averaged_confusing.vhdr', preload=True)
        # ae_c_events, ae_c_event_dict = mne.events_from_annotations(ae_c, {'Time 0/':11})
        # ae_c_epochs = mne.Epochs(ae_c, ae_c_events, tmin=ERP_INTERVAL[0]+1/EEG_FREQUENCY, tmax=ERP_INTERVAL[1]-1/EEG_FREQUENCY, event_id=ae_c_event_dict, preload=True, baseline=(ERP_INTERVAL[0]+1/EEG_FREQUENCY,0))
        # ae_c_averaged_epochs =ae_c_epochs.average()
        # plot_evoked(ae_c_averaged_epochs)
        # ae_nc,_ = load_eeg_data(f'E:/PHD/Studies/aoc-frp-main-studies/Main_Study_Part/08-Data-Trial_Recordings/prepared_EEG_files/ERP subjectwise averages/AoCfrp_{participant}__averaged_non_confusing.vhdr', preload=True)
        # ae_nc_events, ae_nc_event_dict = mne.events_from_annotations(ae_nc, {'Time 0/':12})
        # ae_nc_epochs = mne.Epochs(ae_nc, ae_nc_events, tmin=ERP_INTERVAL[0]+1/EEG_FREQUENCY, tmax=ERP_INTERVAL[1]-1/EEG_FREQUENCY, event_id=ae_nc_event_dict, preload=True, baseline=(ERP_INTERVAL[0]+1/EEG_FREQUENCY,0))
        # ae_nc_averaged_epochs =ae_nc_epochs.average()
        # plot_evoked(ae_nc_averaged_epochs)
        # Calculate and plot subjectwise difference wave
        diff_wave = mne.combine_evoked(
            [averaged_evoked[CONDITION_CONFUSING], averaged_evoked[CONDITION_CLEAN]], weights=[1, -1])
        subjectwise_averages[participant][CONDITION_DIFF] = diff_wave
        if plot:
            plot_all_evoked_low_frequency(erp_frp, description, {
                CONDITION_DIFF: diff_wave}, participant, topomap_times, False)
        # Save subjectwise averages
        for condition in averaged_evoked:
            averaged_evoked[condition].save(get_erp_average_path(
                erp_frp, snippet_group, description, participant, condition), overwrite=True)
    # save included snippets, offsets
    frp_offset_data = pd.concat(subjectwise_frp_offsets.values())
    frp_offset_data[ERP_PARAMETER_EPOCH_INTERVAL] = [
        epoch_interval for _ in range(frp_offset_data.shape[0])]
    frp_offset_data[ERP_PARAMETER_CORRECT_TRIALS_ONLY] = correct_data_only
    if erp_frp != True:
        frp_offset_data[FIXATION_SELECTION_ALGORITHM] = erp_frp
    frp_offset_data.to_csv(get_erp_fixation_analysis_path(
        erp_frp, snippet_group, description, 'erp frp offset'), sep=SEPARATOR, index=False)
    # statistics and plot distribution (best in other method)
    if erp_frp != True:
        statistics_distribution(erp_frp, snippet_group, description,
                                frp_offset_data, 'erp frp offset', 'Delay to stimulus onset')
    # Save subjectwise naves
    nave_data = pd.DataFrame.from_dict(subjectwise_nave, 'index')
    nave_data.to_csv(get_erp_nave_path(
        erp_frp, snippet_group, description), sep=SEPARATOR)
    # Calculate and plot grand averages per condition
    grand_averages = {}
    for condition in [CONDITION_CONFUSING, CONDITION_CLEAN]:
        grand_average = mne.grand_average(
            [subjectwise_averages[participant][condition] for participant in subjectwise_averages])
        grand_averages[condition] = grand_average
    if plot:
        plot_all_evoked_low_frequency(erp_frp, description, grand_averages,
                                      TOTAL, topomap_times, False)
    # Calculate and plot grand averages difference wave
    diff_wave = mne.combine_evoked(
        [grand_averages[CONDITION_CONFUSING], grand_averages[CONDITION_CLEAN]], weights=[1, -1])
    grand_averages[CONDITION_DIFF] = diff_wave
    if plot:
        plot_all_evoked_low_frequency(erp_frp, description, {
            CONDITION_DIFF: diff_wave}, TOTAL, topomap_times, False)
    # Save grand averages
    for condition in grand_averages:
        grand_averages[condition].save(get_erp_average_path(
            erp_frp, snippet_group, description, TOTAL, condition=condition), overwrite=True)
    return subjectwise_averages, grand_averages, subjectwise_nave


def get_erp_description(erp_frp: str, correct_data_only: bool, epoch_interval: tuple[int, int]) -> str:
    description = f'{"erp" if erp_frp is True else FIXATION_SELECTION_SHORT_VERSION[erp_frp]}_{int(epoch_interval[0]*1000)}_{int(epoch_interval[1]*1000)}_{"correct" if correct_data_only else "all"}'
    return description


def get_stimulus_number(stimuli: list[str] = EEG_STIMULUS) -> dict[str, int]:
    '''get stimulus number (event number) per recognized stimulus (used in description of annotations)

    returns: stimulus text and number per recognized stimulus'''
    return {stimulus: int(stimulus[-3:]) for stimulus in stimuli}


def get_event_name_numbers(given_stimuli: list[str]) -> dict[str, int]:
    '''get event name per event number for each recognized stimulus (used in description of annotations)

    Arguments: given_stimuli: the stimuli to return

    returns: event name and event number per recognized stimulus'''
    given_stimuli = [
        stimulus for stimulus in given_stimuli if stimulus in EEG_STIMULUS]
    stimulus_numbers = get_stimulus_number()
    return {STIMULUS_EVENT_NAMES[stimulus]: stimulus_numbers[stimulus] for stimulus in given_stimuli}


def get_all_eeg_trial_segments(erp_frp: bool | str, participant: str, correct_trials: list[str] = None, accepted_snippet_numbers: list[int] = None) -> dict[str, Raw]:
    '''load eeg trial segments for participant

    Arguments:
    * erp_frp: whether it is erp or a certain type of frp
    * participant: the participant to get segments for
    * visual_exclude: whether to exclude based on visual as well (required for FRP)

    returns: the non-excluded trial segments for this participant
    '''
    assert (erp_frp in [True, False]), erp_frp
    modes = [BEHAVIORAL, EEG]
    if not erp_frp:
        modes.append(VISUAL)
    exclusions = get_exclusions(participant, [SNIPPET], modes)[SNIPPET]
    snippet_segments: dict[str, Raw] = {}
    for snippet in exclusions:
        if any(exclusions[snippet].values()):
            # print(f'\t{snippet} was excluded due to {exclusions[snippet]}')
            continue
        # if correct only (correct trials given) and snippet not correctly answered
        if not (correct_trials is None) and not (snippet in correct_trials):
            # print(f'\t{snippet} was excluded due to being answered incorrectly')
            continue
        # if correct only (correct trials given) and snippet not correctly answered
        if not (accepted_snippet_numbers is None) and not (get_snippet_number(snippet) in accepted_snippet_numbers):
            # print(f'\t{snippet} was excluded due to not being in the group')
            continue
        eeg_data, _ = load_eeg_data(get_eeg_trial_path(
            erp_frp is True, participant, snippet))
        snippet_segments[snippet] = eeg_data
    return snippet_segments


def plot_epoch(eeg_data: mne.Epochs):
    return eeg_data.plot(EEG_CHANNELS, n_epochs=1, events=eeg_data.events)


def round_time_EEG(time: float, frequency=EEG_FREQUENCY):
    return round(time, int(round(log10(frequency), 0))+1)


def extract_epochs_from_snippet_segments(erp_frp: bool | str, description: str, participant: str, snippet_group: str, snippet_segments: dict[str, Raw], condition_stimuli: list[str],
                                         epoch_interval: tuple[int, int], baseline_interval: tuple[int, int] = None, perform_voltage_checks: bool = True, save_epoch_data: bool = True):
    regarded_stimuli = get_stimulus_number(condition_stimuli)
    snippet_epochs = {}
    frp_fixation_offsets = pd.DataFrame([], columns=[
                                        PARTICIPANT, CONDITION, SNIPPET, 'Stimulus Onset', 'Fixation Onset', 'Delay to stimulus onset'])
    snippet_status = {}
    # calculate epoch
    for snippet in snippet_segments:
        try:
            events, event_dict = mne.events_from_annotations(
                snippet_segments[snippet], regarded_stimuli)
        except ValueError:
            if erp_frp != True:
                print(
                    f'''{snippet}: No stimulus of {list(condition_stimuli)} found in annotations in {snippet_segments[snippet].annotations.to_data_frame()[ANNOTATION_COLUMN_DESCRIPTION].values}''')
                snippet_status[snippet] = 'No stimulus found, fixation data of this trials likely did not contain any fixation fulfilling the requirements for this FRP calculation.'
                continue
            else:
                raise ValueError(
                    f'''In ERP, all stimuli must be found. No stimulus of {list(condition_stimuli)} found in annotations for {snippet} {snippet_segments[snippet].annotations.to_data_frame()[ANNOTATION_COLUMN_DESCRIPTION].values}''')
        # create epoch and perform baseline correction if specified
        if baseline_interval is None:
            epochs = mne.Epochs(snippet_segments[snippet], events, tmin=epoch_interval[0],
                                tmax=epoch_interval[1], event_id=event_dict, preload=True)
        else:
            epochs = mne.Epochs(snippet_segments[snippet], events, tmin=epoch_interval[0], tmax=epoch_interval[1],
                                event_id=event_dict, preload=True, baseline=(baseline_interval[0], baseline_interval[1]))
        # check whether epoch really exists (not too short)
        if erp_frp != True and len(epochs) < 1 and 'TOO_SHORT' in epochs.drop_log[0]:
            anno = snippet_segments[snippet].annotations.to_data_frame()
            relevant_stimuli =  anno[anno[ANNOTATION_COLUMN_DESCRIPTION].isin([EEG_STIMULUS_SNIPPET_END, *EEG_STIMULUS_SNIPPET_START.values(), *condition_stimuli])]
            snippet_status[snippet] = f'Data for existing stimuli too short, {relevant_stimuli}'
            print(
                f'''{snippet}: Data for existing stimuli {list(event_dict.keys())[0]} too short {epochs.drop_log[0]} {relevant_stimuli}''')
            continue
        assert len(epochs) == 1
        # exclude based on all previously marked violations
        if perform_voltage_checks:
            if check_voltage_amplitude(epochs):
                print(f'\t{snippet} excluded due to overall voltage violation')
                # plot_epoch(epochs)
                snippet_segments[snippet].close()
                snippet_status[snippet] = 'Voltage violation absolute of segment'
                continue
            if check_voltage_in_segment(epochs, True):
                print(
                    f'\t{snippet} excluded due to voltage violation inside epoch')
                # plot_epoch(epochs)+-
                snippet_segments[snippet].close()
                snippet_status[snippet] = 'Voltage violation in interval of segment'
                continue
        snippet_status[snippet] = 'Included'
        snippet_epochs[snippet] = epochs
        # calculate frp offset to erp
        annotation_data, _ = prepare_annotation_information(
            snippet_segments[snippet])
        erp_onset = annotation_data[annotation_data[ANNOTATION_COLUMN_DESCRIPTION].isin(
            EEG_STIMULUS_SNIPPET_START.values())][ANNOTATION_COLUMN_ONSET_FLOAT].values[0]
        if erp_frp != True:
            frp_onset = annotation_data[annotation_data[ANNOTATION_COLUMN_DESCRIPTION].isin(
                condition_stimuli)][ANNOTATION_COLUMN_ONSET_FLOAT].values[0]
            frp_fixation_offsets.loc[frp_fixation_offsets.shape[0]] = [None, CONDITION_VARIANT_MATCH[get_snippet_variant(
                snippet)], snippet, round_time_EEG(erp_onset), round_time_EEG(frp_onset), round_time_EEG(frp_onset-erp_onset)]
        else:
            frp_fixation_offsets.loc[frp_fixation_offsets.shape[0]] = [None, CONDITION_VARIANT_MATCH[get_snippet_variant(
                snippet)], snippet, round_time_EEG(erp_onset), round_time_EEG(erp_onset), .0]
    with open(get_erp_status_path(erp_frp, snippet_group, description, participant), 'w') as f:
        json.dump(snippet_status, f, indent=4, sort_keys=True)
    if save_epoch_data:
        # save all epochs
        for snippet, epoch in snippet_epochs.items():
            epoch.save(get_erp_epoch_path(erp_frp, snippet_group, description,
                       participant, snippet), fmt='double', overwrite=True)
    return snippet_epochs, frp_fixation_offsets


def plot_all_evoked(erp_frp: bool | str, snippet_group, description: str, conditional_evoked: dict[str, mne.Evoked], participant: str = TOTAL, topomap_times: list[float] = [0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1], show: bool = True):
    assert (erp_frp is True or erp_frp in FIXATION_SELECTION_ALGORITHMS), erp_frp
    for condition, evoked in conditional_evoked.items():
        fig = evoked.plot(picks='eeg', show=show,
                          window_title=condition, time_unit='ms')
        fig.savefig(get_erp_average_path(erp_frp, snippet_group, description,
                    participant, condition, 'butterfly'))
        plt.close()
    for condition, evoked in conditional_evoked.items():
        fig1 = evoked.plot_topomap(times=[min(
            time, evoked.tmax) for time in topomap_times], time_unit='ms', show=False)
        # TODO: hier Daten für Topoplots abgreifen
        fig1.suptitle(f'Topomap {description}')
        fig1.savefig(get_erp_average_path(erp_frp, snippet_group, description,
                    participant, condition, 'topomap'))
        fig1.show()
        if erp_frp!=True:
            fig2 = evoked.plot_topomap(times=[min(
                round_time_EEG(time+0.0255, 10000), evoked.tmax) for time in topomap_times],average=0.05199, time_unit='ms', show=False)
            fig2_path = get_erp_average_path(erp_frp, snippet_group, description,
                        participant, condition, 'topomap_averaged_50ms')
            for i, ax in enumerate(fig2.get_axes()[:-1]):
                title:str = ax.get_title()[:-3]
                start, end = [int(i)/1000 for i in title.split(' – ')]
                new_title = fig1.axes[i].get_title()
                data = evoked.copy().crop(tmin=start, tmax=end).to_data_frame(index='time', time_format='ms')
                data.index.name='Time (ms)'
                data.to_csv(fig2_path.with_name(f'Data Figure2b amplitudes {new_title} interval.csv'), sep=SEPARATOR)
                ax.set_title(new_title)
            fig2.suptitle(f'Topomap {description}')
            fig2.savefig(fig2_path)
            fig2.show()
        else:
            fig2 = evoked.plot_topomap(times=[min(
                round_time_EEG(time+0.1015, 10000), evoked.tmax) for time in topomap_times],average=0.201, time_unit='ms', show=False)
            fig2_path = get_erp_average_path(erp_frp, snippet_group, description,
                        participant, condition, 'topomap_averaged_200ms')
            for i, ax in enumerate(fig2.get_axes()[:-1]):
                title:str = ax.get_title()[:-3]
                start, end = [int(i)/1000 for i in title.split(' – ')]
                new_title = fig1.axes[i].get_title()
                data = evoked.copy().crop(tmin=start, tmax=end).to_data_frame(index='time', time_format='ms')
                data.index.name='Time (ms)'
                data.to_csv(fig2_path.with_name(f'Data Figure3b amplitudes {new_title} interval.csv'), sep=SEPARATOR)
                ax.set_title(new_title)
            fig2.suptitle(f'Topomap {description}')
            fig2.savefig(fig2_path)
            fig2.show()
        plt.close('all')
    if all([condition in CONDITION_COLORS for condition in conditional_evoked]):
        colors = {condition: CONDITION_COLORS[condition]
                  for condition in conditional_evoked}
    else:
        colors = None
    fig = mne.viz.plot_compare_evokeds(
        conditional_evoked, show_sensors=True, title=f'Topographic comparison {description}', axes='topo', show=show, colors=colors, time_unit='ms')
    fig[0].savefig(get_erp_average_path(erp_frp, snippet_group, description, participant, (condition if len(
        conditional_evoked) == 1 else TOTAL), f'topo_channels'))
    plt.close()
    minimum, maximum = [], []
    for condition, evoked in conditional_evoked.items():
        eeg_data = evoked.get_data(EEG_CHANNELS,units='uV')
        minimum.append(np.min(eeg_data))
        maximum.append(np.max(eeg_data))
    minimum, maximum = min(minimum), max(maximum)  # from volt to microvolt scale
    for channel in EEG_CHANNELS:
        fig = mne.viz.plot_compare_evokeds(conditional_evoked, picks=channel, title=f'Electrode {channel}', show=show, colors=colors,
                                           show_sensors=False,
                                           # for identical scaling
                                           ylim={'eeg': (minimum, maximum)}, time_unit='ms', )
        fig[0].get_axes()[0].get_legend().remove()
        fig_path = get_erp_average_path(erp_frp, snippet_group, description, participant, (condition if len(
            conditional_evoked) == 1 else TOTAL), f'channel_{channel}')
        fig[0].savefig(fig_path)
        plt.close()
    if CONDITION_DIFF in conditional_evoked:
        return
    fig_data_path = get_erp_average_path(erp_frp, snippet_group, description, participant, (condition if len(
            conditional_evoked) == 1 else TOTAL), f'data').with_suffix('.csv')
    for channel in EEG_CHANNELS:
        if channel[0] in 'FCP' and channel[1] in '34z':
            data = []
            for condition in conditional_evoked:
                cond_data = conditional_evoked[condition].to_data_frame(channel, index='time', time_format='ms')
                cond_data.columns = [condition]
                data.append(cond_data)
            data = pd.concat(data, axis=1)
            data.index.name = 'Time (ms)'
            data.to_csv(fig_data_path.with_stem(f'Data Figure{3 if erp_frp==True else 2}a {channel} conditional amplitude'), sep=SEPARATOR)

def plot_all_evoked_low_frequency(erp_frp: bool | str, snippet_group: str, description: str, conditional_evoked: dict[str, mne.Evoked], participant: str = TOTAL, topomap_times: list[float] = [0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1], show: bool = False):
    # plot_all_evoked(erp_frp, description, conditional_evoked, participant, topomap_times, show)
    conditional_evoked = {condition: evoked.copy().resample(
        20) for condition, evoked in conditional_evoked.items()}
    plot_all_evoked(erp_frp, snippet_group,
                    f'{description}_20Hz', conditional_evoked, participant, topomap_times, show)


def statistics_distribution(erp_frp: bool | str, snippet_group: str, description: str, fixation_analysis_data: pd.DataFrame, analysis_topic: str, analysis_column: str):
    fixation_analysis_data[f'{analysis_column} (ms)'] = fixation_analysis_data[analysis_column]*1000
    analysis_column = f'{analysis_column} (ms)'
    conditional_offset = fixation_analysis_data[[CONDITION, analysis_column]].groupby(
        [CONDITION]).agg({analysis_column: PANDAS_DESCRIPTION_AGG_FUNCTIONS})
    conditional_offset.columns = PANDAS_DESCRIPTION_AGG_NAMES
    conditional_offset.to_csv(get_erp_fixation_analysis_path(
        erp_frp, snippet_group, f'{description}_statistics', analysis_topic), sep=SEPARATOR, decimal=',')
    fig, axis = plt.subplots(1, 1, figsize=(8, 3))
    plt.rcParams.update({'font.size': 12})
    # , palette=[CONDITION_COLORS[CONDITION_CLEAN], CONDITION_COLORS[CONDITION_CONFUSING]])
    sns.violinplot(fixation_analysis_data, x=analysis_column, y=CONDITION, legend=False, inner="box", cut=0, ax=axis)
    plt.tight_layout()
    plt.savefig(get_erp_fixation_analysis_path(erp_frp, snippet_group,
                f'{description}_statistics', analysis_topic).with_suffix('.pdf'), bbox_inches='tight', pad_inches=0)
    plt.savefig(get_erp_fixation_analysis_path(erp_frp, snippet_group,
                f'{description}_statistics', analysis_topic).with_suffix('.png'), bbox_inches='tight', pad_inches=0)
    plt.close()
    participant_conditional_offset = fixation_analysis_data[[PARTICIPANT, CONDITION, analysis_column]].groupby(
        [PARTICIPANT, CONDITION]).agg({analysis_column: PANDAS_DESCRIPTION_AGG_FUNCTIONS})
    participant_conditional_offset.columns = PANDAS_DESCRIPTION_AGG_NAMES
    participant_conditional_offset.to_csv(get_erp_fixation_analysis_path(
        erp_frp, snippet_group, f'{description}_participant_statistics', analysis_topic), sep=SEPARATOR, decimal=',')
    fig, axis = plt.subplots(1, 1, figsize=(8, 24))
    plt.rcParams.update({'font.size': 12})
    sns.violinplot(fixation_analysis_data, x=analysis_column,
                   y=PARTICIPANT, hue=CONDITION, inner="stick", cut=0, ax=axis)
    plt.tight_layout()
    plt.savefig(get_erp_fixation_analysis_path(erp_frp, snippet_group,
                f'{description}_participant_statistics', analysis_topic).with_suffix('.pdf'), bbox_inches='tight', pad_inches=0)
    plt.savefig(get_erp_fixation_analysis_path(erp_frp, snippet_group,
                f'{description}_participant_statistics', analysis_topic).with_suffix('.png'), bbox_inches='tight', pad_inches=0)
    plt.close()
    return conditional_offset, participant_conditional_offset


def load_all_erp_averages(erp_frp: bool | str, snippet_group: str, correct_data_only: bool, epoch_interval: tuple[int, int], subjectwise: bool,
                          participants: list[str], grand: bool, conditional: bool, diff: bool) -> Union[tuple[dict[str, dict[str, mne.Evoked], dict[str, mne.Evoked]]], dict[str, dict[str, mne.Evoked]], dict[str, mne.Evoked]]:
    assert (erp_frp is True or erp_frp in FIXATION_SELECTION_ALGORITHMS), erp_frp
    assert ((not subjectwise) or (len(participants) > 0)
            ), "if subjectwise participants are required, send with the participants to use"
    assert (subjectwise or grand), "Subjectwise or grand or both must be chosen"
    description = get_erp_description(
        erp_frp, correct_data_only, epoch_interval)
    conditions = []
    if conditional:
        conditions.extend([CONDITION_CONFUSING, CONDITION_CLEAN])
    if diff:
        conditions.append(CONDITION_DIFF)
    if grand:
        grand_averages = {}
        for condition in conditions:
            path = get_erp_average_path(
                erp_frp, snippet_group, description, condition=condition)
            grand_averages[condition] = mne.read_evokeds(path)[0]
        if not subjectwise:
            return grand_averages
    if subjectwise:
        subjectwise_averages = {}
        for participant in participants:
            averages = {}
            for condition in conditions:
                path = get_erp_average_path(
                    erp_frp, snippet_group, description, participant, condition=condition)
                averages[condition] = mne.read_evokeds(path)[0]
            subjectwise_averages[participant] = averages
        if not grand:
            return subjectwise_averages
    return subjectwise_averages, grand_averages


def load_all_erp_epochs(erp_frp: bool | str, snippet_group: str, description: str, participants: list[str]) -> dict[str, dict[str, mne.Epochs]]:
    assert (erp_frp is True or erp_frp in FIXATION_SELECTION_ALGORITHMS), erp_frp
    subjectwise_epochs = {}
    for participant in participants:
        snippet_epochs = {}
        snippet_epoch_paths = get_all_erp_epoch_paths(
            erp_frp, snippet_group, description, participant)
        for snippet, epoch_path in snippet_epoch_paths.items():
            snippet_epochs[snippet] = mne.read_epochs(
                epoch_path, proj=True, preload=True, verbose=None)
        subjectwise_epochs[participant] = snippet_epochs
    return subjectwise_epochs


def plot_eeg(eeg_data: Raw, plot_annotations: bool, plot_data: bool) -> None:
    '''plot eeg data or its events.

    Each split starts shortly before first fixation cross, 
    and end shortly after next snippet end, or until the next fixation cross.
    If there is no other way of determination, a long buffer is added to the current fixation crops of the split.

    Arguments:
    * eeg_data: the eeg data
    * plot_annotations: whether to plot the annotations as events
    * plot_data: plot the eeg data
    '''
    events, event_id = mne.events_from_annotations(
        eeg_data, get_stimulus_number())
    event_dict = get_event_name_numbers(event_id.keys())
    event_color = {3: 'r', 4: 'b', 11: 'g', 12: 'y', }
    print('Events ID:', event_id, event_dict)
    if plot_data:
        eeg_data.plot(events=events, start=0, duration=30, color='gray', event_color={k: event_color[k] for k in event_color if k in event_id.values()},
                      )
# prepare data
# for erp_parameters in tqdm(all_erp_parameter_combinations):


def plot_waveforms(erp_frp: bool | str, snippet_group: str, correct_data_only: bool, epoch_interval: tuple[float, float], subjectwise: bool, grand: bool, participants: list[str], topomap_times: list[float]):
    assert (erp_frp is True or erp_frp in FIXATION_SELECTION_ALGORITHMS), erp_frp
    description = get_erp_description(
        erp_frp, correct_data_only, epoch_interval)
    print(description)
    data = load_all_erp_averages(erp_frp, snippet_group, correct_data_only, epoch_interval,
                                 subjectwise=subjectwise, participants=participants, grand=grand, diff=True, conditional=True)
    if subjectwise and grand:
        subjectwise_data, total_data = data
    elif subjectwise:
        subjectwise_data = data
    elif grand:
        total_data = data
    if subjectwise:
        for participant in tqdm(participants):
            plot_all_evoked(erp_frp, snippet_group, description, {condition: subjectwise_data[participant][condition] for condition in [CONDITION_CLEAN, CONDITION_CONFUSING]},
                            participant, topomap_times, False)
            plot_all_evoked(erp_frp, snippet_group, description, {CONDITION_DIFF: subjectwise_data[participant][CONDITION_DIFF]},
                            participant, topomap_times, False)
        del subjectwise_data
    if grand:
        plot_all_evoked(erp_frp, snippet_group, description, {condition: total_data[condition] for condition in [CONDITION_CLEAN, CONDITION_CONFUSING]},
                        TOTAL, topomap_times, False)
        plot_all_evoked(erp_frp, snippet_group, description, {CONDITION_DIFF: total_data[CONDITION_DIFF]},
                        TOTAL, topomap_times, False)
        for channel in EEG_CHANNELS:
            fig, axis = plt.subplots(1, 1, figsize=(8, 3))
            plt.rcParams.update({'font.size': 12})
            mne.viz.plot_compare_evokeds(total_data, picks=channel, # show_sensors=True,
                                         title=f'Electrode {channel}', show=False, colors=CONDITION_COLORS, time_unit='ms', axes=axis, truncate_yaxis=False)
            fig.savefig(get_erp_average_path(erp_frp, snippet_group, description, TOTAL, 'all',
                        f'channel_{channel}').with_suffix('.pdf'), bbox_inches='tight', pad_inches=0)
            plt.clf()
            plt.close()
        total_data[CONDITION_DIFF].plot_topomap(times=[0.400, 0.450, 0.500, 0.550, 0.600, 0.650, 0.700], show=False, time_unit='ms')
        fig.savefig(get_erp_average_path(erp_frp, snippet_group, description,
                    TOTAL, CONDITION_DIFF, 'topomap').with_suffix('.pdf'), bbox_inches='tight', pad_inches=0)
        plt.close()
        total_data.pop(CONDITION_DIFF)
        # plt.figure(figsize=(16, 16))
        fig = mne.viz.plot_compare_evokeds(
            {condition:data.copy().crop(tmax=min(data.tmax, 1.0), include_tmax=True) for condition, data in total_data.items()}, picks=['F3','Fz', 'F4','C3','Cz', 'C4','P3','Pz', 'P4', 'F7','F8'], 
            show_sensors=True, title=f'Topographic comparison with 9 crucial electrodes {description}', axes='topo', 
            colors={condition:CONDITION_COLORS[condition] for condition in total_data}, time_unit='ms', )
        # fig[0].tight_layout()
        fig[0].savefig(get_erp_average_path(erp_frp, snippet_group, description, TOTAL, 'all', 'topo_9_channels_1sec').with_suffix('.pdf'))#, bbox_inches='tight', pad_inches=0)
        fig = mne.viz.plot_compare_evokeds(
            total_data, picks=['F3','Fz', 'F4','C3','Cz', 'C4','P3','Pz', 'P4', 'F7','F8'], 
            show_sensors=True, title=f'Topographic comparison with 9 crucial electrodes {description}', axes='topo', show=False,
            colors={condition:CONDITION_COLORS[condition] for condition in total_data}, time_unit='ms', )
        # fig[0].tight_layout()
        fig[0].savefig(get_erp_average_path(erp_frp, snippet_group, description, TOTAL, 'all', 'topo_9_channels').with_suffix('.pdf'))#, bbox_inches='tight', pad_inches=0)
        plt.close()
        del total_data
    gc.collect()


def add_frp_marker_by_special_fixations(participant: str, snippets: list[str], behavioral_data: pd.DataFrame, special_fixation_data: pd.DataFrame, eeg_trials: dict[str, mne.io.Raw]) -> float:
    for snippet in snippets:
        snippet_behavioral_start = behavioral_data[behavioral_data[SNIPPET] == snippet].squeeze(
        )[BEHAVIORAL_COLUMN_START]
        eeg_segment_data: mne.io.Raw = eeg_trials[snippet]
        snippet_condition = CONDITION_VARIANT_MATCH[get_snippet_variant(
            snippet)]
        eeg_annotations, _ = prepare_annotation_information(eeg_segment_data)
        eeg_start = eeg_annotations[eeg_annotations[ANNOTATION_COLUMN_DESCRIPTION]
                                    == EEG_STIMULUS_SNIPPET_START[snippet_condition]].squeeze()[ANNOTATION_COLUMN_ONSET_FLOAT]
        snippet_special_fixation_data: pd.DataFrame = special_fixation_data[
            special_fixation_data[SNIPPET] == snippet]
        for f_a in snippet_special_fixation_data[FIXATION_SELECTION_ALGORITHM].unique():
            fixation_start = snippet_special_fixation_data[snippet_special_fixation_data[FIXATION_SELECTION_ALGORITHM] == f_a].squeeze(
            )[FIXATION_COLUMN_START]
            eeg_fixation_start = transform_eye_to_eeg(fixation_start,
                                                      snippet_behavioral_start, eeg_start)
            eeg_segment_data.annotations.append(eeg_fixation_start, 1/EEG_FREQUENCY,
                                                FRP_EEG_STIMULUS_SNIPPET_START[f_a][snippet_condition])
        export_eeg_brainvision(
            eeg_segment_data, get_eeg_trial_path(False, participant, snippet))


# transform eye-tracking timestamp to eeg frame
def transform_eye_to_eeg(eye_timestamp: float, eye_start_time: float, eeg_start_time: float) -> float:
    '''transforms the eye-tracking timestamp into an eeg frame

    Arguments:
    * eye_timestamp: timestamp of eye-tracking to transform (in seconds with milliseconds floating precision)
    * eye_start_time: timestamp of eye-tracking marking the starting point (in seconds with milliseconds floating precision)
    * eeg_start_time: frame that corresponds to the eye_start timestamp
    * eeg_sampling_rate: the frequency of frames logged in the data (frames per second)

    returns: the frame corresponding to the eye_timestamp
    '''
    eye_offset = eye_timestamp-eye_start_time
    eeg_timestamp = eeg_start_time+eye_offset
    return eeg_timestamp
