import matplotlib as mpl
import pandas as pd
from utils.aoi_helpers import *
from utils.aoi_settings import *
from utils.behavioral_helpers import *
from utils.behavioral_settings import *
from utils.eeg_helpers import *
from utils.eeg_settings import *
from utils.file_helpers import *
from utils.file_settings import *
from utils.I2MC_helpers import *
from utils.I2MC_settings import *
from utils.json_helpers import *
from utils.LMEM_settings import *
from utils.path_helpers import *
from utils.path_settings import *
from utils.snippet_helpers import *
from utils.snippet_settings import *
from utils.statistics_helpers import *
from utils.statistics_settings import *
from utils.textconstants import *
from utils.validation_helpers import *
from utils.validation_settings import *
from utils.visual_helpers import *
from utils.visual_settings import *

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['mathtext.default'] = 'regular'

LOGGING = True  # Print outputs to stdout, if True


def get_difference_subsets(data1: pd.DataFrame, data2: pd.DataFrame):
    columns = list(data1.columns.values)
    assert (columns == list(data2.columns.values)
            ), f'columns 1: {columns}, columns 2: {list(data2.columns.values)}'
    # get those of the first DataFrame not present in the second
    data1_extra = data1.merge(data2, 'left', on=columns, indicator=True)
    data1_extra = data1_extra[data1_extra['_merge'] == 'left_only']
    # get those of the second DataFrame not present in the first
    data2_extra = data2.merge(data1, 'left', on=columns, indicator=True)
    data2_extra = data2_extra[data2_extra['_merge'] == 'left_only']
    return data1_extra, data2_extra


# def check_modality_consistency(behavioral_trials: pd.DataFrame, fixation_trials: pd.DataFrame,
#                                eeg_file_references: dict[str, dict[str, dict[str, Path]]], participants_eeg_missing: dict[str, list[str]] = None) -> bool:
#     # prepare data for consistency
#     behavioral_trials = behavioral_trials[[PARTICIPANT, SNIPPET]].drop_duplicates()\
#         .sort_values([PARTICIPANT, SNIPPET]).reset_index(drop=True)
#     fixation_trials = fixation_trials[[PARTICIPANT, SNIPPET]].drop_duplicates()\
#         .sort_values([PARTICIPANT, SNIPPET]).reset_index(drop=True)
#     eeg_data = [(participant, snippet)
#                 for participant in eeg_file_references for snippet in eeg_file_references[participant]]
#     if not (participants_eeg_missing is None):
#         eeg_data = eeg_data+[(participant, snippet)
#                              for participant in participants_eeg_missing for snippet in participants_eeg_missing[participant]]
#     eeg_trials = pd.DataFrame(eeg_data, columns=[PARTICIPANT, SNIPPET]).sort_values(
#         [PARTICIPANT, SNIPPET]).reset_index(drop=True)

#     result_value = True
#     # pairwise comparison on shape and content
#     if behavioral_trials.shape != fixation_trials.shape or \
#             not behavioral_trials.compare(fixation_trials).all(axis=None):
#         print('Behavioral and fixation trials differ')
#         behavioral_trials_extra, fixation_trials_extra = get_difference_subsets(
#             behavioral_trials, fixation_trials)
#         if not behavioral_trials_extra.empty:
#             print('Present in behavior, but not in fixations:\n',
#                   behavioral_trials_extra)
#         if not fixation_trials_extra.empty:
#             print('Present in fixations, but not in behavior:\n',
#                   fixation_trials_extra)
#         result_value = False

#     if eeg_trials.shape != fixation_trials.shape or \
#             not eeg_trials.compare(fixation_trials).all(axis=None):
#         print('EEG and fixation trials differ')
#         eeg_trials_extra, fixation_trials_extra = get_difference_subsets(
#             eeg_trials, fixation_trials)
#         if not eeg_trials_extra.empty:
#             print('Present in EEG, but not in fixations:', eeg_trials_extra)
#         if not fixation_trials_extra.empty:
#             print('Present in fixations, but not in EEG:', fixation_trials_extra)
#         result_value = False

#     if eeg_trials.shape != behavioral_trials.shape or \
#             not eeg_trials.compare(behavioral_trials).all(axis=None):
#         print('EEG and behavioral trials differ')
#         eeg_trials_extra, behavioral_trials_extra = get_difference_subsets(
#             eeg_trials, behavioral_trials)
#         if not eeg_trials_extra.empty:
#             print('Present in EEG, but not in behavioral:', eeg_trials_extra)
#         if not behavioral_trials_extra.empty:
#             print('Present in behavioral, but not in EEG:',
#                   behavioral_trials_extra)
#         result_value = False
#     return result_value
