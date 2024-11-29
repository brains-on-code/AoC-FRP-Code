from pathlib import Path
from typing import Union
import typing

from utils.path_settings import (CODE_SNIPPET_PATH_AOI,
                                 CODE_SNIPPET_PATH_NORMAL,
                                 EEG_FILE_HEADER_ENDING, EVAL_PATH,
                                 EVAL_PATH_AGGREGATED_DATA,
                                 EVAL_PATH_AGGREGATED_DATA_PLOT,
                                 PROCESSED_PATH, SCREENSHOTS_PATH_AOI,
                                 SCREENSHOTS_PATH_DUMMY,
                                 SCREENSHOTS_PATH_NORMAL)
from utils.snippet_settings import SNIPPET_GROUP_ALL
from utils.textconstants import (ACCURACY, BEHAVIORAL, DIFF, EEG, EEG_ERP,
                                 EEG_FRP, FIXATIONS, GAZE_DATA, SNIPPET, TOTAL,
                                 VISUAL)
from utils.visual_settings import (FIXATION_CORRECTION_ALGORITHM_ORIGINAL,
                                   FIXATION_CORRECTION_ALGORITHMS,
                                   FIXATION_SELECTION_ALGORITHMS,
                                   FIXATION_SELECTION_SHORT_VERSION,
                                   current_fixation_correction_iteration,
                                   previous_fixation_correction_iteration)


def get_code_snippet_path(snippet: str, aoi_version: bool = False) -> Path:
    '''creates code snippet path from snippet name and purpose

    Arguments:
    * snippet: the snippet name
    * aoi_version: whether to use the aoi version instead the normal screenshot

    returns: the path of the original code snippet (java file), using the aoi_version if specified
    '''
    code_snippet_base_path = CODE_SNIPPET_PATH_AOI if aoi_version else CODE_SNIPPET_PATH_NORMAL
    snippet = snippet.split('.')[0]
    snippet_version = snippet.split('-')[-1]
    code_snippet_path = code_snippet_base_path / \
        snippet_version / f'{snippet}.java'
    if code_snippet_path.exists():
        return code_snippet_path
    else:
        print(
            f'No file for this snippet {snippet} in version \'{"aoi" if aoi_version else "normal"}\' found.')
        raise Exception()


def get_screenshot_path(snippet: str, aoi_version: bool = False) -> Path:
    '''creates screenshot path from snippet name and purpose

    Arguments:
    * snippet: the snippet name
    * aoi_version: whether to use the aoi version instead the normal screenshot

    returns: the path of the screenshot, using the aoi_version if specified, and using a dummy link if no file found
    '''
    screenshot_base_path = SCREENSHOTS_PATH_AOI if aoi_version else SCREENSHOTS_PATH_NORMAL
    snippet = snippet.split('.')[0]
    screenshot_path = screenshot_base_path / f'{snippet}.png'
    if screenshot_path.exists():
        return screenshot_path
    else:
        print(
            f'No file for this snippet {snippet} in version \'{"aoi" if aoi_version else "normal"}\' found.')
        return SCREENSHOTS_PATH_DUMMY


def get_exclusion_path(participant: str = TOTAL) -> Path:
    '''creates exclusion file path from participant marker
    Arguments: participant: participant marker
    returns: the path of the exclusion file, using the participant path if specified, otherwise for all participants
    '''
    path = PROCESSED_PATH/participant/'exclusions.json'
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_impedance_path(participant: str = TOTAL) -> Path:
    '''creates impedance path from participant marker
    Arguments: participant: participant marker
    returns: the path of the impedance file, using the participant path if specified, otherwise for all participants
    '''
    path = PROCESSED_PATH/participant/EEG/'impedances.csv'
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_validation_paths(participant: str = TOTAL) -> tuple[Path, Path]:
    '''creates validation paths from participant marker
    Arguments: participant: participant marker
    returns: the paths of the validation files, using the participant path if specified, otherwise for all participants
    '''

    gazes_path = PROCESSED_PATH/participant/VISUAL/'validation_gazes.csv'
    intervals_path = PROCESSED_PATH/participant/VISUAL/'validation_intervals.csv'
    gazes_path.parent.mkdir(exist_ok=True, parents=True)
    return gazes_path, intervals_path


def get_behavioral_events_path(participant: str = TOTAL) -> Path:
    '''creates behavioral events path from participant marker
    Arguments: participant: participant marker
    returns: the paths of the behavioral event file, using the participant path if specified, otherwise for all participants
    '''
    path = PROCESSED_PATH/participant / BEHAVIORAL/f'{BEHAVIORAL}_events.csv'
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_behavioral_data_path(participant: str = TOTAL, final_data_exclusion: bool = True, analysis_prep:bool=False) -> Path:
    '''creates behavioral data path from participant marker
    Arguments: participant: participant marker
    returns: the paths of the behavioral event file, using the participant path if specified, otherwise for all participants
    '''
    assert final_data_exclusion if analysis_prep else True, 'If LMER_prep is True, final_data_exclusion must be True.'
    path = PROCESSED_PATH/participant / BEHAVIORAL/(f'{BEHAVIORAL}' +
                                                    (('_analysis' if analysis_prep else '_included') if final_data_exclusion else '')+'.csv')
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_snippet_gaze_path(participant: str = TOTAL, snippet: str = '', fixation_cross: bool = False) -> Path:
    '''creates snippet gaze path from participant marker
    Arguments: 
    * participant: participant marker
    * snippet: the name of the snippet file
    * fixation_cross: whether to get the data for the fixation cross or the snippet view
    returns: the paths of the snippet gaze file, using the participant path if specified, otherwise for all participants
    '''
    path = PROCESSED_PATH/participant / VISUAL / GAZE_DATA / \
        (f'{GAZE_DATA}_{snippet}' +
         ('_fixation_cross' if fixation_cross else '')+'.csv')
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_fixations_path(participant: str = TOTAL, snippet: str = '', fixation_cross: bool = False, modified_version: str = FIXATION_CORRECTION_ALGORITHM_ORIGINAL, 
                       no_outliers_if_exists: bool = False, iteration: typing.Callable[[], int] = current_fixation_correction_iteration) -> Path:
    '''creates fixations path from participant marker
    Arguments: 
    * participant: participant marker
    * snippet: the name of the snippet file
    * fixation_cross: returns the path for the fixation cross fixations if accepted, otherwise the fixations for the snippet-view fixations
    * no_outliers_if_exists: returns the path for the outliers removed in the original snippet-view fixations, if it exists, otherwise the standard file path

    returns: the paths of the fixations file, using the participant path if specified, otherwise for all participants
    '''
    if modified_version != FIXATION_CORRECTION_ALGORITHM_ORIGINAL:
        assert not fixation_cross, f'''If a correction algorithm {
            modified_version} was chosen, the fixation_cross cannot be active.'''
        assert not no_outliers_if_exists, f'''If a correction algorithm {
            modified_version} was chosen, the no_outliers_if_exists cannot be active.'''
    assert (not fixation_cross) or (
        not no_outliers_if_exists), 'fixation_cross and no_outliers_if_exists cannot be active simultaneously.'
    path = PROCESSED_PATH/participant / VISUAL / FIXATIONS
    if fixation_cross:
        path = path / 'fixation_cross' / \
            f'{FIXATIONS}_{snippet}_fixation_cross.csv'
    elif modified_version != FIXATION_CORRECTION_ALGORITHM_ORIGINAL:
        path = path / f'iteration_{iteration()}' / \
            f'{FIXATIONS}_{snippet}_{modified_version}.csv'
    else:
        path = path / f'iteration_{iteration()}' / f'{FIXATIONS}_{snippet}.csv'
    if no_outliers_if_exists:
        path2 = path.with_stem(path.stem+'_outliers_removed')
        if path2.exists():
            # if we prefer the outliers-removed function, select it if it exists already
            path = path2
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_all_fixation_correction_paths(participant: str, snippet: str = '*', iteration: typing.Callable[[], int] = current_fixation_correction_iteration) -> list[Path]:
    '''determines all fixation correction paths for a participant and a snippet
    Arguments: 
    * participant: participant marker
    * snippet: the name of the snippet file

    returns: all fixation correction paths for a participant
    '''
    paths = [p for modified_version in FIXATION_CORRECTION_ALGORITHMS for p in (PROCESSED_PATH / participant / VISUAL / FIXATIONS / f'iteration_{iteration()}').glob(
        f'{FIXATIONS}_{snippet}_{modified_version}.csv') if modified_version != FIXATION_CORRECTION_ALGORITHM_ORIGINAL]
    return paths


def get_selected_fixations_path(participant: str = TOTAL, snippet: str = '') -> Path:
    '''creates fixations path from participant marker
    Arguments: 
    * participant: participant marker
    * snippet: the name of the snippet file
    returns: the paths of the fixations file, using the participant path if specified, otherwise for all participants
    '''
    path = PROCESSED_PATH/participant / VISUAL / \
        FIXATIONS / 'selected'/f'{FIXATIONS}_{snippet}.csv'
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_calibration_image_path(participant: str = TOTAL, snippet: str = '', fixation_cross: bool = False, iteration: typing.Callable[[], int] = lambda:0) -> Path:
    '''creates calibration image gaze path from participant marker
    Arguments: 
    * participant: participant marker
    * snippet: the name of the snippet file
    * fixation_cross: whether to get the data for the fixation cross or the snippet view
    returns: the paths of the calibration image file, using the participant path if specified, otherwise for all participants
    '''
    assert fixation_cross ^ iteration()
    path = PROCESSED_PATH/participant / VISUAL / ACCURACY
    if fixation_cross:
        path = path/'fixation_cross' / \
            f'{ACCURACY}_{FIXATIONS}_{snippet}_fixation_cross.png'
    else:
        path = path / f'iteration_{iteration()}' / \
            f'{ACCURACY}_{FIXATIONS}_{snippet}.png'
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_manual_accuracy_evaluation_path(participant: str = TOTAL, performed: bool = False, iteration: typing.Callable[[], int] = current_fixation_correction_iteration) -> Path:
    '''creates manual accuracy evaluation path from participant marker
    Arguments: participant: participant marker
    returns: the paths of the manual accuracy evaluation file, using the participant path if specified, otherwise for all participants
    '''

    path = PROCESSED_PATH.parent/'manual_accuracy_evaluation'/f'iteration_{iteration()}' / ('combined' if performed else 'template') /\
        (f'{participant}_{ACCURACY}_manual_evaluation' +
         ('_combined' if performed else '')+'.csv')
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def exist_previous_manual_accuracy_evaluation_paths(previous_iteration: typing.Callable[[], int] = previous_fixation_correction_iteration) -> list[Path]:
    '''checks whether there exist any manual accuracy evaluation files from previous iteration

    returns: all evaluation paths per participant
    '''
    if previous_iteration() == 0:
        return []
    paths = [p for p in (PROCESSED_PATH.parent/'manual_accuracy_evaluation' /
                         f'iteration_{previous_iteration()}' / 'combined').glob(
        (f'*_{ACCURACY}_manual_evaluation_combined.csv'))]
    paths = {path.stem.split('_')[0]: path for path in paths}
    return paths


def get_snippet_rework_paths(participant: str = TOTAL, previous_iteration: typing.Callable[[], int] = previous_fixation_correction_iteration) -> Path:
    '''creates manual accuracy rework path from participant marker
    Arguments: 
    * participant: participant marker

    returns: manual accuracy rework path
    '''
    if previous_iteration() == 0:
        return None
    path = PROCESSED_PATH.parent/'manual_accuracy_evaluation' / f'iteration_{previous_iteration()}' /\
        'to_rework'/f'{participant}_{ACCURACY}_to_rework.csv'
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_refixation_plot_path(participant: str, snippet: str) -> Path:
    '''creates special fixations path from participant marker
    Arguments: 
    * participant: participant marker
    returns: the paths of the LMEM model file
    '''
    path = PROCESSED_PATH/participant / VISUAL / \
        FIXATIONS / f'refixation/refixation_plot{snippet}.png'
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_special_fixations_path(participant: str = TOTAL) -> Path:
    '''creates special fixations path from participant marker
    Arguments: 
    * participant: participant marker
    returns: the paths of the LMEM model file
    '''
    path = PROCESSED_PATH/participant / VISUAL / \
        FIXATIONS / ('special_fixations.csv')
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_special_fixation_statistics_path() -> Path:
    '''creates file path for noting all trials where special fixations of a certain algorithm could not be determined
    returns: the file path
    '''
    path = PROCESSED_PATH/TOTAL / VISUAL / \
        ('special_fixations_statistics.csv')
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_manual_ICA_reasoning_path(participant: str = TOTAL, performed: bool = False) -> Path:
    '''creates manual ICA reasoning path from participant marker
    Arguments: participant: participant marker
    returns: the paths of the manual ICA reasoning file, using the participant path if specified, otherwise for all participants
    '''
    if not performed:
        path = PROCESSED_PATH/participant / EEG / \
            (f'manual_ICA_reasoning_{participant}.csv')
    else:
        path = PROCESSED_PATH/'../prepared_EEG_files/reasoning files artifact manual evaluation' /\
            f'manual_ICA_reasoning_{participant}_performed.csv'
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_prepared_eeg_path(participant: str) -> Path:
    '''creates prepared eeg path (after BrainVision Analyzer preparation) from participant marker
    Arguments: participant: participant marker
    returns: the paths of the cropped eeg file, using the participant path if specified
    '''
    path = PROCESSED_PATH/'../prepared_EEG_files' / EEG /\
        f'AoCfrp_{participant}_New Reference{EEG_FILE_HEADER_ENDING}'
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_trial_annotations_path(participant: str, performed: bool = False) -> Path:
    '''deartifacted eeg path from participant marker
    Arguments: participant: participant marker
    returns: the paths of the deartifacted eeg file, using the participant path if specified
    '''
    path = PROCESSED_PATH.parent/'prepared_EEG_files' / 'trial_annotations' / \
        (f'{participant}_trial_annotation' +
         ('_performed' if performed else '')+'.csv')
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_cropped_eeg_path(participant: str) -> Path:
    '''creates cropped eeg path from participant marker
    Arguments: participant: participant marker
    returns: the paths of the cropped eeg file, using the participant path if specified
    '''
    path = PROCESSED_PATH/participant / EEG / \
        f'{EEG}_cropped{EEG_FILE_HEADER_ENDING}'
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_eeg_violations_path(participant: str) -> Path:
    '''creates eeg violations path from participant marker
    Arguments: 
    * participant: participant marker
    returns: the paths of the eeg violations file, using the participant path if specified
    '''
    path = PROCESSED_PATH/participant / EEG / \
        f'{EEG_ERP}_violations.csv'
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_eeg_trial_path(erp_frp: bool, participant: str, snippet: str) -> Path:
    '''creates eeg trial path from participant marker
    Arguments: 
    * erp_frp: whether it is erp or a certain type of frp
    * participant: participant marker
    * snippet: the name of the snippet file
    returns: the paths of the eeg trial file, using the participant path if specified
    '''
    assert (erp_frp in [True, False]), erp_frp
    path = PROCESSED_PATH/participant / EEG / (f'{EEG_ERP if erp_frp is True else EEG_FRP}') /\
        f'''{EEG_ERP if erp_frp is True else EEG_FRP}_trial_{
            snippet}{EEG_FILE_HEADER_ENDING}'''
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_statistic_fixations_path(participant: str = TOTAL) -> Path:
    '''creates statistic fixations path
    returns: the paths of the statistic fixations file
    '''
    path = PROCESSED_PATH/participant / VISUAL / 'statistic_fixations.csv'
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_statistic_gazes_path(participant: str = TOTAL) -> Path:
    '''creates statistic gazes path
    returns: the paths of the statistic gazes file
    '''
    path = PROCESSED_PATH/participant / VISUAL / 'statistic_gazes.csv'
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_statistic_summary_path(description: str) -> Path:
    '''creates statistic summary path
    Arguments: 
    * behavioral_only: whether to return the path for behavioral only exclusions
    returns: the paths of the statistic summary file
    '''
    path = PROCESSED_PATH/TOTAL / \
        (f'statistic_summary_exclusion_{description}.csv')
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_eval_aggregation_snippet_categories_path(result_description: str, plot: bool = False) -> Path:
    '''creates eval aggregated data per snippet categories path from result description
    Arguments: 
    * result_description: the description
    returns: the paths of the eval aggregated data per snippet categories file
    '''
    path = (EVAL_PATH_AGGREGATED_DATA_PLOT if plot else EVAL_PATH_AGGREGATED_DATA) /\
        (f'snippet_categories_{result_description}' +
         ('.pdf' if plot else '.csv'))
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_eval_subjectwise_averages_behavioral_path(result_description: str) -> Path:
    '''creates eval subjectwise_averages statistics from result description
    Arguments: 
    * result_description: the description
    returns: the paths of the eval statistics file
    '''
    path = EVAL_PATH/BEHAVIORAL / \
        f'subjectwise_averages/statistics_{result_description}.csv'
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_LMEM_model_path(description: str, model:bool=True, image:bool=False) -> Path:
    '''creates LMEM model path from result description
    Arguments: 
    * description: the description
    * model: whether it is for the model storage
    returns: the paths of the LMEM model file
    '''
    path = EVAL_PATH/BEHAVIORAL/'LMEM'
    if model:
        path = path / 'model'
    path = path/(f'{description}.'+('pdf' if image else 'json'))
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_scanpath_path(participant: str, snippet: str) -> Path:
    '''creates scanpath file path from participant marker
    Arguments: 
    * participant: participant marker
    returns: the paths of the LMEM model file
    '''
    path = EVAL_PATH/VISUAL/'scanpath'/f'{snippet}_scanpath_{participant}.png'
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_erp_epoch_path(erp_frp: bool | str, snippet_group: str, description: str, participant: str, snippet: str) -> Path:
    '''creates erp/frp epoch path from participant marker and condition
    Arguments: 
    * erp_frp: whether it is erp or a certain type of frp
    * description: description of erp/frp (interval, data group etc.)
    * participant: participant marker if given else TOTAL for grand average
    * condition: the condition of the data to write / get, otherwise TOTAL for across conditions
    * plot_type: whether there is a plot of a specific type or the data just needs to be saved
    returns: the paths of the erp/frp average file, using the participant path if specified
    '''
    assert (erp_frp is True or erp_frp in FIXATION_SELECTION_ALGORITHMS), erp_frp
    folder = EVAL_PATH / EEG / \
        (EEG_ERP if erp_frp is True else (f'{EEG_FRP}_{FIXATION_SELECTION_SHORT_VERSION[erp_frp]}'+(f'_{snippet_group}' if snippet_group != SNIPPET_GROUP_ALL else ''))) / \
        'epochs'/participant
    path = folder / f'{description}_epoch_{participant}_{snippet}_epo.fif'
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_all_erp_epoch_paths(erp_frp: bool, snippet_group: str, description: str, participant: str) -> list[Path]:
    '''creates erp/frp average path from participant marker and condition
    Arguments: 
    * erp_frp: whether it is erp or a certain type of frp
    * participant: participant marker if given else TOTAL for grand average
    * condition: the condition of the data to write / get, otherwise TOTAL for across conditions
    * plot_type: whether there is a plot of a specific type or the data just needs to be saved
    returns: the paths of the erp average file, using the participant path if specified
    '''
    assert (erp_frp is True or erp_frp in FIXATION_SELECTION_ALGORITHMS), erp_frp
    folder = EVAL_PATH / EEG / \
        (EEG_ERP if erp_frp is True else (f'{EEG_FRP}_{FIXATION_SELECTION_SHORT_VERSION[erp_frp]}'+(f'_{snippet_group}' if snippet_group != SNIPPET_GROUP_ALL else ''))) / \
        'epochs'/participant
    paths = folder.glob(f'{description}_epoch_{participant}_*_epo.fif')
    snippet_epoch_paths = {}
    for path in paths:
        snippet = path.stem.split('_')[-2]
        assert not snippet in snippet_epoch_paths
        snippet_epoch_paths[snippet] = path
    return snippet_epoch_paths


def get_erp_status_path(erp_frp: bool | str, snippet_group: str, description: str, participant: str) -> Path:
    '''creates erp/frp exclusion status path from participant marker
    Arguments: 
    * erp_frp: whether it is erp or a certain type of frp
    * snippet_group: the name of a snippet subgroup
    * description: description of erp/frp (interval, data group etc.)
    * participant: participant marker if given else TOTAL for grand average
    returns: the paths of the erp/frp average file, using the participant path if specified
    '''
    assert (erp_frp is True or erp_frp in FIXATION_SELECTION_ALGORITHMS), erp_frp
    folder = EVAL_PATH / EEG / \
        (EEG_ERP if erp_frp is True else (f'{EEG_FRP}_{FIXATION_SELECTION_SHORT_VERSION[erp_frp]}'+(f'_{snippet_group}' if snippet_group != SNIPPET_GROUP_ALL else ''))) / \
        'epochs'/participant
    path = folder/f'{description}_{participant}_exclusions.json'
    path.parent.mkdir(exist_ok=True, parents=True)
    return path

def get_erp_average_path(erp_frp: bool | str, snippet_group: str, description: str, participant: str = TOTAL, condition: str = TOTAL, plot_type: str = None) -> Path:
    '''creates erp/frp average path from participant marker and condition
    Arguments: 
    * erp_frp: whether it is erp or a certain type of frp
    * description: description of erp/frp (interval, data group etc.)
    * participant: participant marker if given else TOTAL for grand average
    * condition: the condition of the data to write / get, otherwise TOTAL for across conditions
    * plot_type: whether there is a plot of a specific type or the data just needs to be saved
    returns: the paths of the erp/frp average file, using the participant path if specified
    '''
    assert (erp_frp is True or erp_frp in FIXATION_SELECTION_ALGORITHMS), erp_frp
    folder = EVAL_PATH / EEG / \
        (EEG_ERP if erp_frp is True else (f'{EEG_FRP}_{FIXATION_SELECTION_SHORT_VERSION[erp_frp]}'+(f'_{snippet_group}' if snippet_group != SNIPPET_GROUP_ALL else ''))) / \
        'epochs'/participant
    path = folder/('.' if plot_type is None else 'plot') / (f'{description}_{"grand" if participant == TOTAL else participant}_average_{condition}' +
                                                            ('_ave.fif' if plot_type is None else f'_{plot_type}.png'))
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_erp_fixation_analysis_path(erp_frp: bool | str, snippet_group: str, description: str, analysis_topic: str) -> Path:
    '''creates erp/frp average path from participant marker and condition
    Arguments: 
    * erp_frp: whether it is erp or a certain type of frp
    returns: the paths of the erp average file, using the participant path if specified
    '''
    assert (erp_frp is True or erp_frp in FIXATION_SELECTION_ALGORITHMS), erp_frp
    path = EVAL_PATH / EEG / \
        (EEG_ERP if erp_frp is True else (f'{EEG_FRP}_{FIXATION_SELECTION_SHORT_VERSION[erp_frp]}')+(f'_{snippet_group}' if snippet_group != SNIPPET_GROUP_ALL else '')) / 'fixation_analysis' /\
        f'{description}_trial_{analysis_topic}.csv'
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_erp_nave_path(erp_frp: bool | str, snippet_group: str, description: str) -> Path:
    '''creates erp/frp average path from participant marker and condition
    Arguments: 
    * erp_frp: whether it is erp or a certain type of frp
    * participant: participant marker if given else TOTAL for grand average
    * condition: the condition of the data to write / get, otherwise TOTAL for across conditions
    * plot_type: whether there is a plot of a specific type or the data just needs to be saved
    returns: the paths of the erp average file, using the participant path if specified
    '''
    assert (erp_frp is True or erp_frp in FIXATION_SELECTION_ALGORITHMS), erp_frp
    path = EVAL_PATH / EEG /  \
        (EEG_ERP if erp_frp is True else (f'{EEG_FRP}_{FIXATION_SELECTION_SHORT_VERSION[erp_frp]}')+(f'_{snippet_group}' if snippet_group != SNIPPET_GROUP_ALL else '')) / 'epochs' /\
        f'{description}_nave.csv'
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_erp_parameters_path(erp_frp: bool) -> Path:  # type: ignore
    '''creates erp/frp parameters path where all parameter combinations for the erp/frp calculation are stored
    Arguments: 
    * erp_frp: whether it is erp or a certain type of frp
    returns: the paths of the erp/frp parameters file, using the participant path if specified
    '''
    assert (erp_frp in [True, False]), erp_frp
    path = EVAL_PATH / EEG / (EEG_ERP if erp_frp is True else (EEG_FRP)) / \
        'parameter_combinations.json'
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_erp_statistics_path(erp_frp: bool | str, snippet_group: str, description: str, statistic_type: str, file_ending: str, positive_only: bool = False) -> Path:
    '''creates erp/frp statistics path
    Arguments: 
    * erp_frp: whether it is erp or a certain type of frp
    * description: description of erp/frp (interval, data group etc.)
    * statistic_type: which statistic was performed
    * positive_only: whether only positive results will be stored at the path
    returns: the paths of the erp/frp statistics file
    '''
    assert (erp_frp is True or erp_frp in FIXATION_SELECTION_ALGORITHMS), erp_frp
    path = EVAL_PATH / EEG / (EEG_ERP if erp_frp is True else (f'{EEG_FRP}_{FIXATION_SELECTION_SHORT_VERSION[erp_frp]}')+(f'_{snippet_group}' if snippet_group != SNIPPET_GROUP_ALL else '')) / 'statistics' / statistic_type
    path = path/('plot' if file_ending == 'png' else ('data' if file_ending in ['csv','xlsx'] else'.')) / \
        f'''{description} {
            "positive" if positive_only else "all"}.{file_ending}'''
    path.parent.mkdir(exist_ok=True, parents=True)
    return path


def get_all_frp_statistics_paths(statistic_type: str) -> list[Path]:
    '''gets all frp statistic paths of a certain type
    Arguments: 
    * statistic_type: which statistic was performed
    * positive_only: whether only positive results will be stored at the path
    returns: the paths of the erp/frp statistics file
    '''
    paths = (EVAL_PATH / EEG).glob(f'{EEG_FRP}_*/statistics/{statistic_type.split(" ")[0]}/{statistic_type}/' +
                                   f'''* positive.json''')
    return sorted(paths)


def get_all_erp_nave_paths(erp_frp: bool) -> list[Path]:
    '''creates erp/frp average path from participant marker and condition
    Arguments: 
    * erp_frp: whether it is erp or a certain type of frp
    * participant: participant marker if given else TOTAL for grand average
    * condition: the condition of the data to write / get, otherwise TOTAL for across conditions
    * plot_type: whether there is a plot of a specific type or the data just needs to be saved
    returns: the paths of the erp average file, using the participant path if specified
    '''
    paths = (
        EVAL_PATH / EEG).glob(f'{EEG_ERP if erp_frp else f"{EEG_FRP}_*"}/epochs/*_nave.csv')
    return sorted(paths)


def get_all_erp_fixation_analysis_paths(erp_frp: bool, analysis_topic: str) -> list[Path]:
    '''creates erp/frp average path from participant marker and condition
    Arguments: 
    * erp_frp: whether it is erp or a certain type of frp
    * participant: participant marker if given else TOTAL for grand average
    * condition: the condition of the data to write / get, otherwise TOTAL for across conditions
    * plot_type: whether there is a plot of a specific type or the data just needs to be saved
    returns: the paths of the erp average file, using the participant path if specified
    '''
    paths = (
        EVAL_PATH / EEG).glob(f'{EEG_ERP if erp_frp else f"{EEG_FRP}_*"}/fixation_analysis/*all_trial_{analysis_topic}.csv')
    paths = sorted(paths)
    paths = [path for path in paths]
    return paths
