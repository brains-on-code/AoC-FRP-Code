import gc
import json
import math
import re
import traceback
from datetime import datetime
from pathlib import Path
from typing import Callable
import typing

import h5py
import matplotlib as mpl
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.patches import Circle
from PIL import Image
from scipy.optimize import minimize
from sklearn.cluster import KMeans
from tqdm.notebook import tqdm
from utils.aoi_helpers import check_point_in_area, get_distance_to_area
from utils.aoi_settings import (AOI_PADDING_LARGE, AOI_PADDING_MEDIUM,
                                AOI_PADDING_MEDIUM_LARGE, AOI_PADDING_NO,
                                AOI_PADDING_SMALL, POS_BOTTOM, POS_LEFT,
                                POS_RIGHT, POS_TOP)
from utils.file_helpers import (get_participant_folder_per_participant,
                                update_exclusions)
from utils.file_settings import (BEHAVIORAL_COLUMN_DURATION,
                                 BEHAVIORAL_COLUMN_END,
                                 BEHAVIORAL_COLUMN_FIXATION_START,
                                 BEHAVIORAL_COLUMN_START, COLUMN_TIME,
                                 EYE_COLUMN_GAZE_X, EYE_COLUMN_GAZE_Y,
                                 EYE_COLUMN_LEFT_GAZE_X,
                                 EYE_COLUMN_LEFT_GAZE_Y, EYE_COLUMN_RADIUS_X,
                                 EYE_COLUMN_RADIUS_Y, EYE_COLUMN_RIGHT_GAZE_X,
                                 EYE_COLUMN_RIGHT_GAZE_Y, EYE_COLUMNS,
                                 FIXATION_COLUMN_DURATION, FIXATION_COLUMN_END,
                                 FIXATION_COLUMN_RADIUS_X,
                                 FIXATION_COLUMN_RADIUS_Y,
                                 FIXATION_COLUMN_REFIXATION,
                                 FIXATION_COLUMN_START, FIXATION_COLUMN_X,
                                 FIXATION_COLUMN_Y, FIXATION_COLUMNS,
                                 HDF_INDEX, ROUNDING_COORDINATES,
                                 ROUNDING_TIME, SEPARATOR)
from utils.I2MC_helpers import I2MC
from utils.path_helpers import (get_calibration_image_path, get_fixations_path,
                                get_refixation_plot_path, get_screenshot_path,
                                get_selected_fixations_path,
                                get_snippet_gaze_path,
                                get_special_fixations_path)
from utils.path_settings import SCREENSHOTS_PATH_FIXATION_CROSS, X_OFFSET_FILE
from utils.snippet_helpers import (get_snippet_number, get_snippet_variant,
                                   get_snippet_version)
from utils.snippet_settings import CONDITION, CONDITION_VARIANT_MATCH
from utils.textconstants import OPTIMAL, PARTICIPANT, RESULT, SNIPPET, VISUAL
from utils.visual_settings import *

# (
#     DURATION_SIZE_FACTOR, FIXATION_CORRECTION_ALGORITHM_CLUSTER_ALLLINES,
#     FIXATION_CORRECTION_ALGORITHM_CLUSTER_ESSENTIALLINES,
#     FIXATION_CORRECTION_ALGORITHM_ORIGINAL,
#     FIXATION_CORRECTION_ALGORITHM_STRETCH_ALLLINES,
#     FIXATION_CORRECTION_ALGORITHM_STRETCH_ESSENTIALLINES, FIXATION_RADIUS,
#     HEIGHT, LINES_OF_CODE_Y, MIN_DURATION_S_FIXATION_EEG, PSYCHOPY_HEIGHT,
#     PSYCHOPY_WIDTH, PSYCHOPY_X_AREA, PSYCHOPY_Y_AREA, WIDTH, I2MC_options)


def get_hdf_files_per_participant() -> dict[str, list[Path]]:
    '''get hdf files per participant folders identified in the RAW_PATH path

    returns: the participant numbers, and per each the identified hdf files
    '''
    hdf_files = {}

    for participant, participant_folder in get_participant_folder_per_participant().items():
        hdf_files[participant] = []
        for file in participant_folder.iterdir():
            if file.suffix == '.hdf5':
                hdf_files[participant].append(file)
    for participant, files in hdf_files.items():
        files.sort()
    return hdf_files


def anonymize_psychopy_data(hdf_files: list[Path], participant: str):
    '''anonymizes psychopy files in-place by removing all traces of timestamps in the filenames, as well as csv files

    Arguments:
    * hdf_file: a list of paths for the hdf files
    * participant: the participant number as string
    '''
    hdf_files.sort()
    for i, hdf_file in enumerate(hdf_files):
        files = hdf_file.parent.glob(f'{hdf_file.stem}.*')
        for file in files:
            if file.suffix == '.csv':
                # remove columns 'date','participant','session' or delete file as a whole (currently unused)
                file_content = pd.read_csv(file)
                file_content = file_content.drop(
                    columns=['date', 'participant', 'session'], errors='ignore')
                file_content.to_csv(file)
                # file.unlink()
            elif file.suffix == '.log':
                # TODO: for change in participant numbers, replace "conditions_\d_\old_no.xlsx" with "conditions_\d_\new_no.xlsx" or delete file as a whole (currently unused)
                # file.unlink()
                pass
            elif file.suffix == '.psydat':
                # TODO: for change in participant numbers, delete file as a whole (currently unused)
                # file.unlink()
                pass
            elif file.suffix == '.hdf5':
                # replace timestamp in first log entry
                with h5py.File(file, 'r+') as f:
                    # read log events from hdf5 info in data_collection->events->experiment->LogEvent
                    log_events = f['data_collection/events/experiment/LogEvent']
                    log_events['text', 0] = 'Server Time Offset: Anonymized'

            file.rename(
                file.parent/f'Experiment_{participant}_part{str(i+1).zfill(2)}{file.suffix}')


def retrieve_eye_events(hdf5_event_data_file: Path) -> pd.DataFrame:
    '''retrieve message and eye events as dataframes from the hdf file

    Arguments:
    * hdf5_event_data_file: the path to the hdf file

    returns: the eye events
    '''
    with h5py.File(hdf5_event_data_file, 'r') as f:
        # read eye events from hdf5 info in data_collection->events->eyetracker->BinocularEyeSampleEvent
        eye_events = f['data_collection']['events']['eyetracker']['BinocularEyeSampleEvent']
        # h5py syntax to retrieve all data
        eye_events = pd.DataFrame(eye_events[()])
        # keep only useful columns
        eye_events = eye_events.drop(
            columns=[col for col in eye_events.columns if col not in EYE_COLUMNS])

        return eye_events

#############################
# transform for fixation data
#############################


def clean_prepare_eye_events(eye_events: pd.DataFrame, drop_nans: bool = False) -> pd.DataFrame:
    '''prepares eye events for further use.
    Drops nan's, those gazes outside the screen field.
    Recalculates gaze positions for the eyes to pixels instead of center-based coordinates.
    Calculate average gaze position from both eyes, and radius 

    Arguments: 
    * eye_events: a dataframe containing the relevant eye_events
    * drop_nans: whether to drop nan's 

    returns: prepared eye events
    '''
    #  set eye events with values outside screen to nan values
    eye_events.loc[~(eye_events[EYE_COLUMN_LEFT_GAZE_X].between(*PSYCHOPY_X_AREA, 'both') &
                     eye_events[EYE_COLUMN_LEFT_GAZE_Y].between(*PSYCHOPY_Y_AREA, 'both') &
                     eye_events[EYE_COLUMN_RIGHT_GAZE_X].between(*PSYCHOPY_X_AREA, 'both') &
                     eye_events[EYE_COLUMN_RIGHT_GAZE_Y].between(*PSYCHOPY_Y_AREA, 'both')),
                   [EYE_COLUMN_LEFT_GAZE_X, EYE_COLUMN_LEFT_GAZE_Y, EYE_COLUMN_RIGHT_GAZE_X, EYE_COLUMN_RIGHT_GAZE_Y]] = np.nan

    # drop nans if wanted
    if drop_nans:
        eye_events = eye_events.dropna(axis=0, how='any',
                                       subset=[EYE_COLUMN_LEFT_GAZE_X, EYE_COLUMN_LEFT_GAZE_Y, EYE_COLUMN_RIGHT_GAZE_X, EYE_COLUMN_RIGHT_GAZE_Y])

    # recalculate to pixels / usual python image coordinates
    # usually in python, (x,y)=(0,0) is in the upper left corner, and x increases to the right, y to the bottom until WIDTH, HEIGHT is reached
    # in psychopy, (x,y)=(0,0) is in the center, x increases to the right, y increases to the top
    # however, the ends of the axes are not +-1 or pixel based, but depend on the height / width ratio
    # drop data outside screen depending on axis ends (identified by ratio)
    # rescale axis to 1 / -1 at each end (origin at center, top left (-1,1), bottom left (-1,-1), bottom right (1,-1), top right (1,1))
    eye_events[[EYE_COLUMN_LEFT_GAZE_Y, EYE_COLUMN_RIGHT_GAZE_Y]] = eye_events[[
        EYE_COLUMN_LEFT_GAZE_Y, EYE_COLUMN_RIGHT_GAZE_Y]] / PSYCHOPY_HEIGHT
    eye_events[[EYE_COLUMN_LEFT_GAZE_X, EYE_COLUMN_RIGHT_GAZE_X]] = eye_events[[
        EYE_COLUMN_LEFT_GAZE_X, EYE_COLUMN_RIGHT_GAZE_X]] / PSYCHOPY_WIDTH
    # relocate origin (0,0) from center to bottom left corner via (x,y)->1+(x,y)/2 --> top left (0,1), top right (1,1), bottom left (0,0), bottom right (1,0)
    eye_events[[EYE_COLUMN_LEFT_GAZE_X, EYE_COLUMN_RIGHT_GAZE_X]] = (
        1+eye_events[[EYE_COLUMN_LEFT_GAZE_X, EYE_COLUMN_RIGHT_GAZE_X]])/2
    eye_events[[EYE_COLUMN_LEFT_GAZE_Y, EYE_COLUMN_RIGHT_GAZE_Y]] = (
        1+eye_events[[EYE_COLUMN_LEFT_GAZE_Y, EYE_COLUMN_RIGHT_GAZE_Y]])/2
    # change in direction of y axis via y->1-y --> top left (0,0), top right (1,0), bottom left (0,1), top right (1,1)
    eye_events[[EYE_COLUMN_LEFT_GAZE_Y, EYE_COLUMN_RIGHT_GAZE_Y]] = 1 - \
        eye_events[[EYE_COLUMN_LEFT_GAZE_Y, EYE_COLUMN_RIGHT_GAZE_Y]]
    # multiply to pixel level by (x,y)->(x*WIDTH, y*HEIGHT)
    eye_events[[EYE_COLUMN_LEFT_GAZE_X, EYE_COLUMN_RIGHT_GAZE_X]] = (WIDTH *
                                                                     eye_events[[EYE_COLUMN_LEFT_GAZE_X, EYE_COLUMN_RIGHT_GAZE_X]]).round(ROUNDING_COORDINATES)
    eye_events[[EYE_COLUMN_LEFT_GAZE_Y, EYE_COLUMN_RIGHT_GAZE_Y]] = (HEIGHT *
                                                                     eye_events[[EYE_COLUMN_LEFT_GAZE_Y, EYE_COLUMN_RIGHT_GAZE_Y]]).round(ROUNDING_COORDINATES)
    # calculate average position for both eyes, and radius
    eye_events[EYE_COLUMN_GAZE_Y] = ((
        eye_events[EYE_COLUMN_LEFT_GAZE_Y] + eye_events[EYE_COLUMN_RIGHT_GAZE_Y])/2).round(ROUNDING_COORDINATES)
    eye_events[EYE_COLUMN_GAZE_X] = ((
        eye_events[EYE_COLUMN_LEFT_GAZE_X] + eye_events[EYE_COLUMN_RIGHT_GAZE_X])/2).round(ROUNDING_COORDINATES)
    eye_events[EYE_COLUMN_RADIUS_Y] = (abs(
        eye_events[EYE_COLUMN_LEFT_GAZE_Y]-eye_events[EYE_COLUMN_RIGHT_GAZE_Y])/2).round(ROUNDING_COORDINATES)
    eye_events[EYE_COLUMN_RADIUS_X] = (abs(
        eye_events[EYE_COLUMN_LEFT_GAZE_X]-eye_events[EYE_COLUMN_RIGHT_GAZE_X])/2).round(ROUNDING_COORDINATES)
    eye_events[COLUMN_TIME] = eye_events[COLUMN_TIME].round(ROUNDING_TIME)
    eye_events = eye_events.drop(columns=[])
    return eye_events


def extract_relevant_eye_events(behavioral_data: pd.DataFrame, eye_events: pd.DataFrame, get_fixation_cross=False) -> dict[str, pd.DataFrame]:
    '''extracts relevant eye events for all snippet view data for each snippet.
    Only those during snippet views (and before) are kept

    Arguments:
    * behavioral_data: a dataframe containing the snippet views (start and end)
    * eye_events: a dataframe containing the relevant eye_events
    * get_fixation_cross: whether to get fixation data for the snippet or the real snippet view data

    returns: eye events per snippet
    '''
    snippet_gazes = {}
    for _, row in behavioral_data.iterrows():
        snippet = row[SNIPPET]
        # use snippet start and end, if given
        start = row[BEHAVIORAL_COLUMN_START] if not get_fixation_cross else row[BEHAVIORAL_COLUMN_FIXATION_START]
        end = row[BEHAVIORAL_COLUMN_END] if not get_fixation_cross else row[BEHAVIORAL_COLUMN_START]
        if np.isnan(start) or np.isnan(end):
            snippet_gazes[snippet] = pd.DataFrame()
            continue
        # slice gaze data
        gaze_data = eye_events[eye_events[COLUMN_TIME].between(
            start, end, 'both')].copy()
        if gaze_data.empty:
            snippet_gazes[snippet] = pd.DataFrame()
            continue
        # add snippet information
        gaze_data[SNIPPET] = snippet
        gaze_data[HDF_INDEX] = row[HDF_INDEX]
        snippet_gazes[snippet] = gaze_data
    return snippet_gazes


def check_gaze_data(snippet_gazes: dict[str, pd.DataFrame], fixation_cross_gazes: dict[str, pd.DataFrame], participant: str, error_marker: str):
    '''checks whether the gaze data for each snippet is usable or must be excluded

    Arguments:
    * snippet_gazes: dataframes per snippet containing the relevant eye_events during snippet view
    * fixation_cross_gazes: dataframes per snippet containing the relevant eye_events during fixation cross view
    * participant: the participant marker
    * error_marker: the error message marker to be included into all error messages
    '''
    excluded_snippet_gazes: dict[str, list[str]] = {}
    for snippet, gazes in snippet_gazes.items():
        # Find NA
        gazes['NA'] = gazes.isna().any(axis=1)
        # Calculate NA percentage
        _, _, na_percentage = calculate_na_percentage(gazes)
        # Exclude if NA percentage too high
        if na_percentage > MAX_GAZE_NA_TOTAL_TOLERANCE:
            excluded_snippet_gazes[snippet] = [
                f'{error_marker}: Too many NA gazes']
            continue
        _, na_intervals = calculate_na_intervals(gazes, participant)
        if na_intervals[BEHAVIORAL_COLUMN_DURATION].max() > MAX_GAZE_NA_INTERVAL_TOLERANCE:
            excluded_snippet_gazes[snippet] = [
                f'{error_marker}: Too long NA interval']
            continue
        gazes.drop(columns=['NA', 'NA_interval_index'],
                   inplace=True, errors='ignore')
    if excluded_snippet_gazes:
        update_exclusions(participant, SNIPPET, VISUAL, excluded_snippet_gazes)
    return excluded_snippet_gazes


def calculate_na_percentage(gazes: pd.DataFrame):
    na_count = (gazes['NA']*1).sum()
    # Calculate NA percentage
    gaze_count = gazes.shape[0]
    na_percentage = na_count/gaze_count
    return gaze_count, na_count, na_percentage


def calculate_na_intervals(gazes: pd.DataFrame, participant: str):
    # Calculate NA time intervals
    # increase index if not NA, so that consecutive NA have identical index
    gazes['NA_interval_index'] = (1-(gazes['NA']*1)).cumsum()
    na_gazes = gazes[gazes['NA']].copy()
    na_intervals: list = list(na_gazes['NA_interval_index'].unique())
    na_interval_count = len(na_intervals)
    # Reset index of NA intervals to start from 0
    na_gazes['NA_interval_index'] = na_gazes['NA_interval_index'].apply(
        lambda v: na_intervals.index(v))
    # Calculate start and end of NA interval
    na_intervals: pd.DataFrame = na_gazes.groupby(
        ['NA_interval_index']).agg({COLUMN_TIME: ['min', 'max']})
    na_intervals.columns = [BEHAVIORAL_COLUMN_START, BEHAVIORAL_COLUMN_END]
    na_intervals = na_intervals.reset_index(names=['Interval'])
    # Calculate duration, including end point
    na_intervals[BEHAVIORAL_COLUMN_DURATION] = na_intervals[BEHAVIORAL_COLUMN_END] - \
        na_intervals[BEHAVIORAL_COLUMN_START] + \
        (1/get_eyetracking_frequency(participant))
    return na_interval_count, na_intervals


def calculate_fixations(snippet_gazes: dict[str, pd.DataFrame], participant: str, i2mc_options) -> dict[str, pd.DataFrame]:
    '''calculates the fixations from the gaze data of the snippets via I2MC

    Arguments: 
    * snippet_gazes: the gaze data from eye events per snippet
    * participant: the participant the data is from

    returns: a dataframe describing the fixations per snippet
    '''
    snippet_fixations = {}
    for snippet in tqdm(snippet_gazes, leave=False):
        gaze_data = snippet_gazes[snippet]
        successful = True
        fixations = {}
        if gaze_data.empty:
            snippet_fixations[snippet] = pd.DataFrame(
                [], columns=FIXATION_COLUMNS)
            continue
        # run I2MC
        try:
            fixations, data, par = I2MC({'L_X': gaze_data[EYE_COLUMN_LEFT_GAZE_X].to_numpy(),
                                        'L_Y': gaze_data[EYE_COLUMN_LEFT_GAZE_Y].to_numpy(),
                                        'R_X': gaze_data[EYE_COLUMN_RIGHT_GAZE_X].to_numpy(),
                                        'R_Y': gaze_data[EYE_COLUMN_RIGHT_GAZE_Y].to_numpy(),
                                        'time': gaze_data[COLUMN_TIME].to_numpy()},
                                        i2mc_options, logging=False)
        except:
            print(f'\t\tError in file for snippet {snippet}:')
            traceback.print_exc()
            successful = False
        # Check if I2MC returned a fixation
        if not fixations:
            print(
                f'{participant}-{snippet}: Fixation calculation had some problem, thus return gaze data as mini-fixations')
            successful = False
        elif len(fixations['startT']) == 0:
            successful = False

        if successful:
            # extract fixation data
            fixation_data = pd.concat([pd.Series(fixations['startT']).round(ROUNDING_TIME),
                                       pd.Series(fixations['endT']).round(
                                           ROUNDING_TIME),
                                       pd.Series(fixations['xpos']).round(
                                           ROUNDING_COORDINATES),
                                       pd.Series(fixations['ypos']).round(
                                           ROUNDING_COORDINATES),
                                       pd.Series(fixations['fixRangeX']).round(
                                           ROUNDING_COORDINATES),
                                       pd.Series(fixations['fixRangeY']).round(ROUNDING_COORDINATES)],
                                      axis=1, keys=[FIXATION_COLUMN_START, FIXATION_COLUMN_END,
                                                    FIXATION_COLUMN_X, FIXATION_COLUMN_Y,
                                                    FIXATION_COLUMN_RADIUS_X, FIXATION_COLUMN_RADIUS_Y])
            fixation_data[FIXATION_COLUMN_DURATION] = (fixation_data[FIXATION_COLUMN_END] -
                                                       fixation_data[FIXATION_COLUMN_START]).round(ROUNDING_TIME)
            # add snippet and participant as columns (for unambiguous assignment later on)
            fixation_data[SNIPPET] = snippet
            fixation_data[PARTICIPANT] = participant
            fixation_data[CONDITION] = CONDITION_VARIANT_MATCH[get_snippet_variant(
                snippet)]
            snippet_fixations[snippet] = fixation_data
        else:
            snippet_fixations[snippet] = pd.DataFrame(
                [], columns=FIXATION_COLUMNS)
    return snippet_fixations


def check_fixation_cross_fixation_outliers(snippet_fixations: dict[str, pd.DataFrame], fixation_cross_fixations: dict[str, pd.DataFrame], participant: str):
    '''check the fixations to identify potential outliers

    Arguments:
    * snippet_fixations: dataframes per snippet containing the relevant eye_events during snippet view
    * fixation_cross_fixations: dataframes per snippet containing the relevant eye_events during fixation cross view
    '''
    # details = pd.DataFrame([], columns=[PARTICIPANT, SNIPPET, 'fc_'+FIXATION_COLUMN_X, 'fc_'+FIXATION_COLUMN_Y, 's_'+FIXATION_COLUMN_X, 's_'+FIXATION_COLUMN_Y, 'dist_x', 'dist_y', 'dropped'])
    for snippet in set(snippet_fixations.keys()).intersection(fixation_cross_fixations.keys()):
        s_f = snippet_fixations[snippet]
        fc_f: pd.DataFrame = fixation_cross_fixations[snippet]
        if fc_f.shape[0] == 0:
            continue
        last_fixation_cross_x = fc_f.iloc[-1][FIXATION_COLUMN_X]
        last_fixation_cross_y = fc_f.iloc[-1][FIXATION_COLUMN_Y]
        on_fixation_cross = True
        while (on_fixation_cross):  # remove all beginning fixations on the position of the fixation cross
            pos_x = s_f[FIXATION_COLUMN_X].iloc[0]
            pos_y = s_f[FIXATION_COLUMN_Y].iloc[0]
            dist_x = round(abs(pos_x - last_fixation_cross_x),
                           ROUNDING_COORDINATES)
            dist_y = round(abs(pos_y - last_fixation_cross_y),
                           ROUNDING_COORDINATES)
            # details.loc[details.shape[0]] = [participant, snippet, last_fixation_cross_x, last_fixation_cross_y, pos_x, pos_y, dist_x, dist_y, False]
            if (dist_x <= FIXATION_RADIUS and dist_y <= FIXATION_RADIUS):
                s_f.drop(s_f.index[0], inplace=True)
                # details.at[details.shape[0]-1, 'dropped'] = 'True'
            else:
                on_fixation_cross = False
    # details.to_csv(f'./test check fix cross fix {participant} {str(datetime.now()).replace(":","-")}.csv', sep=SEPARATOR, decimal=',')


def create_fixation_cross_accuracy_image(participant: str, snippet: str, fixation_data: pd.DataFrame):
    try:
        # create image based on fixations
        # take first eye gazes by snippet and visualize them on the screenshot
        cm_a = mpl.cm.ScalarMappable(
            cmap='hsv', norm=plt.Normalize(vmin=0, vmax=fixation_data.shape[0]+2))
        # +2 to to not receive identical color on start and end

        fig, ax = plt.subplots(1, 1, figsize=(WIDTH/300, HEIGHT/300))
        # show how the calibration works for the fixation cross
        with Image.open(SCREENSHOTS_PATH_FIXATION_CROSS) as image:
            ax.imshow(image)
        # generate circle patch for gaze
        for index, (_, row) in enumerate(fixation_data.iterrows()):
            alpha = 0.2
            c = cm_a.to_rgba(index)
            p = Circle((row[FIXATION_COLUMN_X], row[FIXATION_COLUMN_Y]),
                       radius=10, color=c, alpha=alpha, linewidth=1)
            ax.add_patch(p)
        ax.axis('off')
        fig.tight_layout()
        # add legend
        handles, labels = [ax.patches[0]], ['1st Fixation']
        if fixation_data.shape[0] > 2:
            handles.append(ax.patches[fixation_data.shape[0]//2])
            labels.append('Median Fixation')
        if fixation_data.shape[0] > 1:
            handles.append(ax.patches[fixation_data.shape[0]-1])
            labels.append('Last Fixation')
        fig.legend(handles=handles, labels=labels)
        # save figure
        fig.savefig(get_calibration_image_path(participant, snippet, True),
                    bbox_inches='tight', pad_inches=0)
        plt.close()
    except Exception:
        traceback.print_exc()
        return False
    return True


def fixation_correction_algorithm_cluster(fixation_data: pd.DataFrame, line_relevance: list[int], aggregate: bool = False):
    '''performs fixation correction based on K-means clustering

    Arguments:
    * fixation_data: the dataframe containing the fixation coordinates
    * line_coordinates_y: the y-coordinates for the code lines (not given as numbers because some lines might be skipped in pre-selection!)
    returns: the dataframe with modified coordinates
    '''
    # if only 1 line, assign all fixations to that line
    if len(line_relevance) == 1:
        fixation_data[FIXATION_COLUMN_Y] = LINES_OF_CODE_Y[0]
        return fixation_data
    # return empty if more lines than fixations
    if fixation_data.shape[0] < sum(line_relevance):
        return pd.DataFrame([], columns=fixation_data.columns)
    fixation_Y = fixation_data[FIXATION_COLUMN_Y].to_numpy().reshape(-1, 1)
    clusters = KMeans(sum(line_relevance), n_init=100,
                      max_iter=300).fit_predict(fixation_Y)

    def calculate_cluster_centers(clusters):
        c_centers: dict[int, float] = {i: fixation_data[FIXATION_COLUMN_Y][clusters == i].mean(
        ) for i in range(sum(line_relevance))}
        return c_centers

    def rename_clusters_ordered(centers, clusters):
        cluster_order = [i for i, center in sorted(
            centers.items(), key=lambda x: x[1])]
        ordered_clusters = [cluster_order.index(i) for i in clusters]
        ordered_centers = {cluster_order.index(
            i): centers[i] for i in range(sum(line_relevance))}
        return ordered_clusters, ordered_centers
    centers = calculate_cluster_centers(clusters)
    clusters, centers = rename_clusters_ordered(centers, clusters)
    if aggregate:
        line_assignment = {}
        for i in range(sum(line_relevance)-1):
            if i == 0:
                line_assignment[i] = 0
            j = i+1
            # distance to center of first cluster assigned to the line
            clusters_previous_line_assignment = [
                k for k in line_assignment if line_assignment[k] == line_assignment[i]]
            center_distance = centers[j] - \
                centers[min(clusters_previous_line_assignment)]
            assert (center_distance >= 0)
            if center_distance % 53 < 20:
                line_assignment[j] = int(
                    line_assignment[i]+center_distance // 53)
            elif center_distance % 53 > 33:
                line_assignment[j] = int(
                    line_assignment[i]+1+center_distance // 53)
            else:
                # check each element in cluster whether it belongs to i or i+2 (if available)
                line_assignment[j] = int(
                    line_assignment[i]+1+center_distance // 53)
                if line_assignment[j] >= len(line_relevance):
                    # go back to previous if more (future) clusters than lines
                    line_assignment[j] -= 1
                elif line_assignment[j]+(sum(line_relevance)-j-1) >= len(line_relevance):
                    # go back to previous if more (future) clusters than lines
                    line_assignment[j] -= 1
        for i in line_assignment:
            if line_assignment[i] >= len(LINES_OF_CODE_Y):
                line_assignment[i] = len(LINES_OF_CODE_Y)-1
            elif line_assignment[i] < 0:
                line_assignment[i] = 0
    else:
        pass
        cumsum = [sum(line_relevance[:i+1]) -
                  1 for i in range(len(line_relevance))]
        line_assignment = {i: cumsum.index(i)
                           for i in range(sum(line_relevance))}
    fixation_data[FIXATION_COLUMN_Y] = [
        LINES_OF_CODE_Y[line_assignment[i]] for i in clusters]
    return fixation_data


def fixation_correction_algorithm_stretch(fixation_data: pd.DataFrame, line_coordinates_y: list[int]):
    '''performs fixation correction based on K-means clustering

    Arguments:
    * fixation_data: the dataframe containing the fixation coordinates
    * line_coordinates_y: the y-coordinates for the code lines (not given as numbers because some lines might be skipped in pre-selection!)
    returns: the dataframe with modified coordinates
    '''
    scale_bounds = (0.9, 1.1)
    offset_bounds = (-50, 50)

    n = fixation_data.shape[0]

    def fit_lines(params, return_correction=False):
        candidate_Y = fixation_data[FIXATION_COLUMN_Y] * params[0] + params[1]
        corrected_Y = np.zeros(n)
        for fixation_i in range(n):
            line_i = np.argmin(
                abs(line_coordinates_y - candidate_Y[fixation_i]))
            corrected_Y[fixation_i] = line_coordinates_y[line_i]
        if return_correction:
            return corrected_Y
        return sum(abs(candidate_Y - corrected_Y))

    best_fit = minimize(fit_lines, [1, 0], bounds=[
                        scale_bounds, offset_bounds])
    fixation_data[FIXATION_COLUMN_Y] = fit_lines(
        best_fit.x, return_correction=True)
    return fixation_data


def calculate_corrected_fixations(snippet_fixations: pd.DataFrame, code_sizes: pd.DataFrame):
    corrected_snippet_fixations = {}
    for snippet in snippet_fixations:
        corrected_fixation_datasets = {}
        # algorithm 1: cluster by line
        line_relevance = [1 for i in range(code_sizes.at[snippet, 'LoC'])]
        corrected_fixations = fixation_correction_algorithm_cluster(
            snippet_fixations[snippet].copy(), line_relevance)
        if corrected_fixations.empty:
            print(
                f'\tNo corrected fixation data possible for {snippet} for cluster_alllines')
        else:
            corrected_fixation_datasets[FIXATION_CORRECTION_ALGORITHM_CLUSTER_ALLLINES] = corrected_fixations
        # algorithm 2: stretch by line
        line_y = LINES_OF_CODE_Y[:code_sizes.at[snippet, 'LoC']]
        corrected_fixations = fixation_correction_algorithm_stretch(
            snippet_fixations[snippet].copy(), line_y)
        if corrected_fixations.empty:
            print(
                f'\tNo corrected fixation data possible for {snippet} for stretch_alllines')
        else:
            corrected_fixation_datasets[FIXATION_CORRECTION_ALGORITHM_STRETCH_ALLLINES] = corrected_fixations
        line_relevance = eval(code_sizes.at[snippet, 'EssentialCodeLines'])
        if not len(line_relevance) == sum(line_relevance):
            # algorithm 3: cluster by essential lines
            corrected_fixations = fixation_correction_algorithm_cluster(
                snippet_fixations[snippet].copy(), line_relevance)
            if corrected_fixations.empty:
                print(
                    f'\tNo corrected fixation data possible for {snippet} for cluster_essentiallines')
            else:
                corrected_fixation_datasets[FIXATION_CORRECTION_ALGORITHM_CLUSTER_ESSENTIALLINES] = corrected_fixations
            # algorithm 4: stretch by essential lines
            line_y = [LINES_OF_CODE_Y[i]
                      for i, v in enumerate(line_relevance) if v == 1]
            corrected_fixations = fixation_correction_algorithm_stretch(
                snippet_fixations[snippet].copy(), line_y)
            if corrected_fixations.empty:
                print(
                    f'\tNo corrected fixation data possible for {snippet} for stretch_essentiallines')
            else:
                corrected_fixation_datasets[FIXATION_CORRECTION_ALGORITHM_STRETCH_ESSENTIALLINES] = corrected_fixations
        # remove duplicate results
        duplicate_algo = []
        for i1, algo1 in enumerate(corrected_fixation_datasets):
            for i2, algo2 in enumerate(corrected_fixation_datasets):
                if i1 >= i2 or (algo1 in duplicate_algo) or (algo2 in duplicate_algo):
                    continue
                delta = (corrected_fixation_datasets[algo1][FIXATION_COLUMN_Y] -
                         corrected_fixation_datasets[algo2][FIXATION_COLUMN_Y]).abs()
                if (delta < 0.0001).all():
                    duplicate_algo.append(algo2)
        for algo in duplicate_algo:
            data = corrected_fixation_datasets.pop(algo)
            del data
        if not corrected_fixation_datasets:
            print(f'\tNo corrected fixation data possible for {snippet}')
        corrected_fixation_datasets[FIXATION_CORRECTION_ALGORITHM_ORIGINAL] = snippet_fixations
        corrected_snippet_fixations[snippet] = corrected_fixation_datasets
    return corrected_snippet_fixations


def get_x_offsets(iteration: typing.Callable[[], int] = current_fixation_correction_iteration):
    if not X_OFFSET_FILE.exists():
        with open(X_OFFSET_FILE, 'w', encoding='utf-8') as f:
            f.write('{}')
        print(f'File {X_OFFSET_FILE} did not exist, was created')
        return {}
    with open(X_OFFSET_FILE, 'r', encoding='utf-8') as f:
        x_offsets = json.load(f)
    if f'{iteration()}' in x_offsets:
        return x_offsets[f'{iteration()}']
    else:
        return {}


def get_snippet_x_offset(participant_x_offsets: dict[str, int], snippet: str):
    x_offset = 0
    version = get_snippet_version(snippet)
    if version in participant_x_offsets:
        x_offset = participant_x_offsets[version]
    if snippet in participant_x_offsets:
        x_offset = participant_x_offsets[snippet]
    return x_offset


def create_accuracy_image(participant: str, snippet: str, fixation_datasets: dict[str, pd.DataFrame], offset_correction: int = 0):
    try:
        datasets = {algo: data for algo,
                    data in fixation_datasets.items() if data.shape[0] > 0}
        # take first eye gazes by snippet and visualize them on the screenshot
        cm_a = mpl.cm.ScalarMappable(
            cmap='hsv', norm=plt.Normalize(vmin=0, vmax=max(data.shape[0] for data in datasets.values())+2))
        # +2 to to not receive identical color on start and end
        fig, axes = plt.subplots(len(datasets), 1, figsize=(
            WIDTH/300, len(datasets)*HEIGHT/300))
        if len(datasets) == 1:
            axes = [axes]
        patches = []
        with Image.open(get_screenshot_path(snippet)) as image:
            for i, (algo, data) in enumerate(datasets.items()):
                axes[i].imshow(image)
        del image
        gc.collect()
        for i, (algo, data) in enumerate(datasets.items()):
            # generate circle patch for gaze
            for index, (_, row) in enumerate(data.iterrows()):
                alpha = 0.2
                c = cm_a.to_rgba(index)
                p = Circle((row[FIXATION_COLUMN_X], row[FIXATION_COLUMN_Y]),
                           radius=10, color=c, alpha=alpha, linewidth=1)
                axes[i].add_patch(p)
                patches.append(p)
            axes[i].axis('off')
            axes[i].set_title(algo)
            # add legend
            handles, labels = [axes[i].patches[0]], ['Fixation 1']
            RAINBOW_INTERVALS = 6
            if data.shape[0] > RAINBOW_INTERVALS:
                for j in np.linspace(0, data.shape[0]-1, RAINBOW_INTERVALS+1).tolist()[1:-1]:
                    j = int(round(j, 0))
                    handles.append(axes[i].patches[j])
                    labels.append(f'Fixation {j+1}')
            elif data.shape[0] > 2:
                handles.append(axes[i].patches[data.shape[0]//2])
                labels.append('Fixation Median')
            if data.shape[0] > 1:
                handles.append(axes[i].patches[data.shape[0]-1])
                labels.append(f'Fixation {data.shape[0]}')
            axes[i].legend(handles=handles, labels=labels)

        # save figure
        fig.tight_layout()
        if offset_correction:
            fig.suptitle(
                f'For this dataset an offset correction on the axis of {offset_correction} pixels to the right was performed.')
        fig.show()
        fig.savefig(get_calibration_image_path(
            participant, snippet, False, current_fixation_correction_iteration),
            bbox_inches='tight', pad_inches=0)
        plt.close()
        plt.close('all')
        del patches
        del cm_a
        del datasets
        del handles
        del axes
        del fig
        gc.collect()
    except Exception:
        print(traceback.format_exc())
        return False
    return True


def plot_refixation_clusters(snippet: str, fixation_data: pd.DataFrame, participant: str):
    refixation_clusters = list(
        set(fixation_data[FIXATION_COLUMN_REFIXATION].unique()))
    refixation_clusters.sort()
    if -1 in refixation_clusters:
        refixation_clusters.remove(-1)
    cm_a = mpl.cm.ScalarMappable(
        cmap='hsv', norm=plt.Normalize(vmin=0, vmax=len(refixation_clusters)))
    fig, axis = plt.subplots(1, 1, figsize=(WIDTH/500, HEIGHT/500))
    with Image.open(get_screenshot_path(snippet)) as image:
        axis.imshow(image)
        for index, row in fixation_data.iterrows():
            alpha = 0.2
            # color based on index in refixation
            if row[FIXATION_COLUMN_REFIXATION] > -1:
                alpha = 0.2
                c = cm_a.to_rgba(refixation_clusters.index(
                    row[FIXATION_COLUMN_REFIXATION]))
            elif index in refixation_clusters:
                alpha = 0.5
                c = cm_a.to_rgba(refixation_clusters.index(index))
            else:
                c = 'gray'
            p = Circle((row[FIXATION_COLUMN_X], row[FIXATION_COLUMN_Y]),
                       radius=10, color=c, alpha=alpha, linewidth=1)
            axis.add_patch(p)
            axis.axis('off')
    plt.savefig(get_refixation_plot_path(participant, snippet))
    plt.close()


def create_manual_accuracy_evaluation(snippet_algorithms: dict[str, list[str]]) -> pd.DataFrame:
    """
    creates a dataframe for filling out the accuracy, for each snippet either the algorithm options or excluded
    """
    manual_evaluation = pd.DataFrame({SNIPPET: snippet_algorithms.keys()})
    manual_evaluation.sort_values([SNIPPET], inplace=True, key=lambda snippet_column: [int(
        get_snippet_number(snippet)) + int(get_snippet_version(snippet)[-1])/10 for snippet in snippet_column])
    manual_evaluation[MANUAL_ACCURACY_EVALUATION_FIRST_FIXATION_OUTLIER] = False
    manual_evaluation[MANUAL_ACCURACY_EVALUATION_OUTLIER] = 0
    manual_evaluation[MANUAL_ACCURACY_EVALUATION_X_OFFSET] = 0
    manual_evaluation[MANUAL_ACCURACY_EVALUATION_REASON] = ''
    manual_evaluation[MANUAL_ACCURACY_EVALUATION_CHOICE] = manual_evaluation[SNIPPET].apply(lambda snippet: str(
        [algo for algo in snippet_algorithms[snippet]]).replace('\'', '').replace('[', '').replace(']', '')).apply(lambda algos: algos if algos else FIXATION_CORRECTION_ALGORITHM_SNIPPET_EXCLUDED)
    manual_evaluation[MANUAL_ACCURACY_EVALUATION_ITERATION] = current_fixation_correction_iteration()
    if current_fixation_correction_iteration()==1:
        manual_evaluation[MANUAL_ACCURACY_EVALUATION_ITERATION] = manual_evaluation[MANUAL_ACCURACY_EVALUATION_CHOICE].apply(
            lambda algos: previous_fixation_correction_iteration() if algos==FIXATION_CORRECTION_ALGORITHM_SNIPPET_EXCLUDED else current_fixation_correction_iteration())
        manual_evaluation[MANUAL_ACCURACY_EVALUATION_REASON] = manual_evaluation[MANUAL_ACCURACY_EVALUATION_CHOICE].apply(
            lambda algos: 'Excluded due to missing or problematic data' if algos==FIXATION_CORRECTION_ALGORITHM_SNIPPET_EXCLUDED else '')
        manual_evaluation.sort_values([MANUAL_ACCURACY_EVALUATION_ITERATION, SNIPPET], inplace=True)
    manual_evaluation[SNIPPET] = manual_evaluation[SNIPPET].apply(
        lambda snippet: f'0{snippet}' if get_snippet_number(snippet) == 0 else snippet)
    return manual_evaluation


def check_basic_manual_accuracy_evaluation(manual_evaluation: pd.DataFrame, participant: str, snippets: list[str]) -> None:
    # transform snippet
    manual_evaluation[SNIPPET] = manual_evaluation[SNIPPET].apply(
        lambda snippet: snippet[1:] if get_snippet_number(snippet) == 0 and snippet[0] == '0' else snippet)
    # check snippet set exactly as supposed to be
    assert (set(manual_evaluation[SNIPPET].values) == set(snippets)), f'''Only snippets seen by the participant, but all of them, should be included in the file. {
        set(manual_evaluation[SNIPPET].values).symmetric_difference(snippets)}'''
    # check that all fields have accepted value type
    assert manual_evaluation[MANUAL_ACCURACY_EVALUATION_FIRST_FIXATION_OUTLIER].apply(
        lambda v: v in [True, False]).all(), f'All first fixation markers must be either "True" or "False".'
    # assert manual_evaluation[MANUAL_ACCURACY_EVALUATION_OUTLIER].str.isdigit().all(), f'All outlier counts must be integer.'
    # assert manual_evaluation[MANUAL_ACCURACY_EVALUATION_X_OFFSET].str.isdigit().all(), f'All outlier counts must be integer.'
    assert (manual_evaluation[MANUAL_ACCURACY_EVALUATION_REASON].str.len()>0).all(), f'''Some of the snippets have no reason assigned to the choice made. Please correct that {
        manual_evaluation[~(manual_evaluation[MANUAL_ACCURACY_EVALUATION_REASON].str.len()>0)]}'''
    # check certain cross-column conditions
    assert (~manual_evaluation[MANUAL_ACCURACY_EVALUATION_FIRST_FIXATION_OUTLIER] | (manual_evaluation[MANUAL_ACCURACY_EVALUATION_OUTLIER] > 0)).all(
    ), 'If there is an outlier for fixation cross, then at least one outlier must be noted'
    assert ((manual_evaluation[MANUAL_ACCURACY_EVALUATION_ITERATION] <= current_fixation_correction_iteration()).all(
    )), f'All trial iterations must be lower or equal to the current one ({current_fixation_correction_iteration()}).'

    # 1. check that each snippet has a choice made
    assert ((manual_evaluation[MANUAL_ACCURACY_EVALUATION_CHOICE].str.len() > 0) | (manual_evaluation[MANUAL_ACCURACY_EVALUATION_OUTLIER] > 0) | (manual_evaluation[MANUAL_ACCURACY_EVALUATION_X_OFFSET] > 0)).all(), f'''Some of the snippets have no choice assigned. Please correct that {
        manual_evaluation[~(manual_evaluation[MANUAL_ACCURACY_EVALUATION_CHOICE].str.len() > 0) | (manual_evaluation[MANUAL_ACCURACY_EVALUATION_OUTLIER] > 0) | (manual_evaluation[MANUAL_ACCURACY_EVALUATION_X_OFFSET] > 0)]}'''
    # 2. check that there is no more than one choice per snippet, and that choice is among accepted
    manual_evaluation['AllowedChoice'] = (manual_evaluation[MANUAL_ACCURACY_EVALUATION_CHOICE].isin(
        FIXATION_CORRECTION_ALGORITHMS+[FIXATION_CORRECTION_ALGORITHM_SNIPPET_EXCLUDED]) | (manual_evaluation[MANUAL_ACCURACY_EVALUATION_OUTLIER] > 0) | (manual_evaluation[MANUAL_ACCURACY_EVALUATION_X_OFFSET] > 0))
    assert manual_evaluation['AllowedChoice'].all(), f'''Some of the snippets have choices assigned that are not allowed. Please correct that {
        manual_evaluation[~manual_evaluation['AllowedChoice']]}'''
    # 4. check whether paths exist towards choice --> choice is possible for this snippet
    manual_evaluation['RequiredPathsExist'] = manual_evaluation.apply(
        lambda row: (row[MANUAL_ACCURACY_EVALUATION_CHOICE] == FIXATION_CORRECTION_ALGORITHM_SNIPPET_EXCLUDED) or (row[MANUAL_ACCURACY_EVALUATION_OUTLIER] > 0) or (row[MANUAL_ACCURACY_EVALUATION_X_OFFSET] > 0) or (get_fixations_path(participant, row[SNIPPET], False, row[MANUAL_ACCURACY_EVALUATION_CHOICE], row[MANUAL_ACCURACY_EVALUATION_CHOICE] == FIXATION_CORRECTION_ALGORITHM_ORIGINAL, lambda:row[MANUAL_ACCURACY_EVALUATION_ITERATION])).exists(), axis=1)
    assert manual_evaluation['RequiredPathsExist'].all(), f'''Some of the snippets have a choice assigned for which there exists no data file. Please correct that {
        manual_evaluation[~manual_evaluation['RequiredPathsExist']]}'''


def get_to_rework_manual_accuracy_evaluation(manual_evaluation: pd.DataFrame, participant: str, snippets: list[str]) -> pd.DataFrame:
    check_basic_manual_accuracy_evaluation(
        manual_evaluation, participant, snippets)
    if current_fixation_correction_iteration() <= 2:
        return manual_evaluation[manual_evaluation[MANUAL_ACCURACY_EVALUATION_CHOICE] != FIXATION_CORRECTION_ALGORITHM_SNIPPET_EXCLUDED]
    possible_rework = manual_evaluation[manual_evaluation[MANUAL_ACCURACY_EVALUATION_ITERATION]
                                        == previous_fixation_correction_iteration()]
    to_rework = possible_rework[possible_rework[MANUAL_ACCURACY_EVALUATION_FIRST_FIXATION_OUTLIER] |
                                (possible_rework[MANUAL_ACCURACY_EVALUATION_OUTLIER] > 0) |
                                (possible_rework[MANUAL_ACCURACY_EVALUATION_X_OFFSET] > 0)]
    return to_rework


def check_outlier_offset_actions(to_rework, participant: str):
    current_x_offsets = get_x_offsets()
    previous_x_offsets = get_x_offsets(previous_fixation_correction_iteration)
    for i, row in to_rework.iterrows():
        if row[MANUAL_ACCURACY_EVALUATION_OUTLIER] > 0 and row[MANUAL_ACCURACY_EVALUATION_ITERATION] == previous_fixation_correction_iteration():
            # check that outliers removed version exists and contains less fixations
            original_fixations_path = get_fixations_path(
                participant, row[SNIPPET], False, no_outliers_if_exists=False, iteration=previous_fixation_correction_iteration)
            no_outliers_fixations_path = get_fixations_path(
                participant, row[SNIPPET], False, no_outliers_if_exists=True, iteration=previous_fixation_correction_iteration)
            if original_fixations_path == no_outliers_fixations_path:
                raise Exception(f'''Snippet {row[SNIPPET]}\nIf outliers were detected in a previous iteration, there must be a file with fixations removed. Original fixations path {
                                original_fixations_path}''')
            original_fixation_data = pd.read_csv(
                original_fixations_path, index_col=False, sep=SEPARATOR, dtype={PARTICIPANT: str})
            no_outliers_fixation_data = pd.read_csv(
                no_outliers_fixations_path, index_col=False, sep=SEPARATOR, dtype={PARTICIPANT: str})
            outlier_count = max(0, row[MANUAL_ACCURACY_EVALUATION_OUTLIER])
            if original_fixation_data.shape[0]-outlier_count != no_outliers_fixation_data.shape[0]:
                raise Exception(f'Snippet {row[SNIPPET]}\nThe outliers removed file must contain at least {outlier_count} less fixations than the original.\n' +
                                f'Original fixations {original_fixation_data.shape[0]}, outlier removed fixations {no_outliers_fixation_data.shape[0]}')
            # check that indexes with the removed version are those listed in the reason text
            outliers = original_fixation_data.merge(
                no_outliers_fixation_data, how='left', indicator=True)
            outliers = outliers[outliers['_merge'] == 'left_only']
            # starts with 1, thus +1
            outlier_indices = {str(i+1) for i in outliers.index}
            listed_outliers = re.findall(
                r'\d+', row[MANUAL_ACCURACY_EVALUATION_REASON])
            if outlier_indices != set(listed_outliers):
                raise Exception(f'''Snippet {row[SNIPPET]}\nThe outliers removed in the file (starting with 1, {outlier_indices}) must be identical to the outliers named in the evaluation file (starting with 1, {listed_outliers}).\n
                                Outliers: {outliers}''')
        if row[MANUAL_ACCURACY_EVALUATION_X_OFFSET]:
            # check that offset is there and differs from previous one
            previous_x_offset = get_snippet_x_offset(
                previous_x_offsets[participant], row[SNIPPET])
            current_x_offset = get_snippet_x_offset(
                current_x_offsets[participant], row[SNIPPET])
            if previous_x_offset == current_x_offset:
                raise Exception(f'''Snippet {row[SNIPPET]}\nPrevious and current offset have to differ for the next iteration\nprevious {
                                previous_x_offset} current {current_x_offset}''')


def check_manual_accuracy_evaluation(manual_evaluation: pd.DataFrame, participant: str, snippets: list[str]) -> bool:
    check_basic_manual_accuracy_evaluation(
        manual_evaluation, participant, snippets)

    usable = True
    included_snippets = manual_evaluation[manual_evaluation[MANUAL_ACCURACY_EVALUATION_CHOICE]
                                          != FIXATION_CORRECTION_ALGORITHM_SNIPPET_EXCLUDED]
    # Outliers or offset problems
    # 1. check that there is no snippet with the first fixation being the fixation cross
    if included_snippets[MANUAL_ACCURACY_EVALUATION_FIRST_FIXATION_OUTLIER].any():
        print('Some of the snippets contain a first fixation that stems from the fixation cross and has to be removed')
        assert (~included_snippets[MANUAL_ACCURACY_EVALUATION_FIRST_FIXATION_OUTLIER] | included_snippets[MANUAL_ACCURACY_EVALUATION_OUTLIER] > 0).all(
        ), 'If there is an outlier for fixation cross, then at least one outlier must be noted'
        print(
            included_snippets[included_snippets[MANUAL_ACCURACY_EVALUATION_FIRST_FIXATION_OUTLIER]])
        usable = False
    # 2. check that there is no snippet with clear outliers
    if included_snippets[MANUAL_ACCURACY_EVALUATION_OUTLIER].any():
        print('Some of the snippets contain outliers that should be removed.')
        print(
            included_snippets[included_snippets[MANUAL_ACCURACY_EVALUATION_OUTLIER] > 0])
        usable = False
    # 3. check that there is no snippet with clear offset
    if included_snippets[MANUAL_ACCURACY_EVALUATION_X_OFFSET].any():
        print('Some of the snippets contain a clearly visible x-offset that should be corrected.')
        print(
            included_snippets[included_snippets[MANUAL_ACCURACY_EVALUATION_X_OFFSET]])
        usable = False
    return usable


def calculate_fixation_statistics(participant: str, snippets: dict):
    statistics_fixations = pd.DataFrame([], columns=[PARTICIPANT, SNIPPET, 'Fixation Count', 'Fixation Duration Min',
                                                     'Fixation Duration Mean', 'Fixation Duration Median', 'Fixation Duration Max', 'Fixation Duration Total',
                                                     'Saccade Count', 'Saccade Duration Min', 'Saccade Duration Mean', 'Saccade Duration Median', 'Saccade Duration Max', 'Saccade Duration Total'])
    for snippet in snippets:
        # Load fixations
        fixations_path = get_selected_fixations_path(participant, snippet)
        if not fixations_path.exists():
            raise Exception(
                f'Snippet {snippet} was not excluded for participant {participant}, but fixation file {fixations_path.as_posix()} does not exist.')
        fixations = pd.read_csv(
            fixations_path, index_col=False, sep=SEPARATOR, dtype={PARTICIPANT: str})
        # Calculate metrics & assess
        fixation_count = fixations.shape[0]
        fixation_duration = fixations[FIXATION_COLUMN_DURATION].agg(
            ['min', 'mean', 'median', 'max', 'sum'])
        if fixations.shape[0] == 0:
            saccade_count = 0
            saccade_duration = saccade_data.agg([0, 0, 0, 0])
        else:
            saccade_count = fixation_count-1
            saccade_data = fixations[FIXATION_COLUMN_START].shift(
                periods=-1, fill_value=0)-fixations[FIXATION_COLUMN_END]
            saccade_data.pop(saccade_data.index[-1])
            saccade_duration = saccade_data.agg(
                ['min', 'mean', 'median', 'max', 'sum'])
        statistics_fixations.loc[statistics_fixations.shape[0]] = [
            participant, snippet, fixation_count, *fixation_duration,
            saccade_count, *saccade_duration]
    return statistics_fixations


def calculate_gaze_statistics(participant: str, snippets: dict):
    statistics_gazes = pd.DataFrame([], columns=[PARTICIPANT, SNIPPET, 'Gaze Count',
                                                 'NA Gaze Count', 'NA Percentage', 'NA Interval Count',
                                                 'NA Interval Duration Min', 'NA Interval Duration Mean', 'NA Interval Duration Median',
                                                 'NA Interval Duration Max', 'NA Interval Duration Total', 'Start of noticeable NA Intervals (>=100ms)'])
    for snippet in snippets:
        # Load gazes
        gazes_path = get_snippet_gaze_path(participant, snippet)
        if not gazes_path.exists():
            raise Exception(
                f'Snippet {snippet} was not excluded for participant {participant}, but fixation file {gazes_path.as_posix()} does not exist.')
        gazes: pd.DataFrame = pd.read_csv(
            gazes_path, index_col=False, sep=SEPARATOR, dtype={PARTICIPANT: str})
        # Calculate metrics
        # Find NA
        gazes['NA'] = gazes.isna().any(axis=1)
        # Calculate NA percentage
        gaze_count, na_count, na_percentage = calculate_na_percentage(gazes)
        # Calculate NA intervals
        na_interval_count, na_intervals = calculate_na_intervals(
            gazes, participant)
        na_interval_data = na_intervals[BEHAVIORAL_COLUMN_DURATION].agg(
            ['min', 'mean', 'median', 'max', 'sum'])
        na_intervals['longer'] = na_intervals[BEHAVIORAL_COLUMN_DURATION] >= MIN_NOTICEABLE_NA_INTERVAL
        noticeable_na_intervals = na_intervals[na_intervals['longer']]
        if noticeable_na_intervals.empty:
            noticeable_na_interval_starts = ''
        else:
            noticeable_na_interval_starts = str(
                noticeable_na_intervals[BEHAVIORAL_COLUMN_START].to_list())
        # Assess suitability
        statistics_gazes.loc[statistics_gazes.shape[0]] = [
            participant, snippet, gaze_count, na_count, na_percentage,
            na_interval_count, *na_interval_data, noticeable_na_interval_starts]
    return statistics_gazes


def identify_special_fixations(participant, snippets, aoi_data):
    special_fixation_statistics = pd.DataFrame(
        [], columns=[PARTICIPANT, SNIPPET, FIXATION_SELECTION_ALGORITHM, RESULT])
    special_fixation_data = pd.DataFrame(
        [], columns=FIXATION_COLUMNS+[FIXATION_SELECTION_ALGORITHM])
    for snippet in snippets:
        snippet_fixations_path = get_selected_fixations_path(
            participant, snippet)
        fixation_data = pd.read_csv(
            snippet_fixations_path, index_col=False, sep=SEPARATOR, dtype={PARTICIPANT: str})
        fixation_data = add_refixations(fixation_data)
        plot_refixation_clusters(snippet, fixation_data, participant)
        if snippet in aoi_data[SNIPPET].values:
            aois = aoi_data[aoi_data[SNIPPET] == snippet]
            optimal_aoi = aois[aois[OPTIMAL]]
        else:
            raise Exception(f'No aoi found for {snippet}')
        # use multiple fixation detection algorithms and add markers
        for i, f_a in enumerate(FIXATION_SELECTION_ALGORITHMS):
            algorithm = FIXATION_SELECTION_ALGORITHM_FUNCTIONS[f_a]
            fixation: pd.Series = algorithm(fixation_data, aois)
            if fixation is None:
                print(
                    f'\tFor snippet {snippet}, the algorithm {f_a} could not identify a suitable fixation.')
                special_fixation_statistics.loc[special_fixation_statistics.shape[0]] = {
                    PARTICIPANT: participant, SNIPPET: snippet, FIXATION_SELECTION_ALGORITHM: f_a, RESULT: 'None'}
                continue
            special_fixation_data.loc[special_fixation_data.shape[0]] = (
                fixation.to_dict() | {FIXATION_SELECTION_ALGORITHM: f_a})
            special_fixation_statistics.loc[special_fixation_statistics.shape[0]] = {
                PARTICIPANT: participant, SNIPPET: snippet, FIXATION_SELECTION_ALGORITHM: f_a, RESULT: 'Existing'}
    return special_fixation_data, special_fixation_statistics


def get_ellipsis_as_array(width: int, height: int, x_center: float, y_center: float, x_radius: float, y_radius: float, factor: float) -> np.ndarray:
    '''creates an ellipsis inside an array to add to a heatmap

    Arguments:
    * width, height: dimensions of the array the ellipsis shall be in
    * x_center, y_center: center of the ellipsis in the array
    * x_radius, y_radius: radius of the ellipsis in both dimensions
    * factor: the factor to multiply to the ellipsis (1 for normal )

    returns: an array of dimensions width, height describing an ellipsis
    '''
    # code for creating a calculated shape in numpy: https://stackoverflow.com/questions/10031580/how-to-write-simple-geometric-shapes-into-numpy-arrays
    xx, yy = np.mgrid[:width, :height]
    # circles contains the squared distance to the (100, 100) point
    # ellipse equation: https://saylordotorg.github.io/text_intermediate-algebra/s11-03-ellipses.html
    if (x_center == 0) or (y_radius == 0):
        ellipsis_equation = xx-(xx-5)+yy-(yy-5)
    else:
        ellipsis_equation = ((xx - x_center) / x_radius) ** 2 + \
            ((yy - y_center) / y_radius) ** 2
    # result contains 1's and 0's organized in an ellipse shape
    # <= leads to a full eclipse, == to the surrounding eclipse shape only
    # you apply 2 thresholds on circle to define the shape
    full_ellipsis = (ellipsis_equation <= 1) * factor
    return full_ellipsis


# # Fixations
def add_refixations(fixation_data: pd.DataFrame, ) -> pd.DataFrame:
    '''transforms fixations by adding the refixations column

    A refixation is identified as the first fixation in the sequence (until the fixation to consider) that has less distance than the fixation radius to  the fixation to consider.
    The index of this first fixation is then stored in the new column for the fixation to consider

    Arguments: fixation_data: the fixations located in one participant's view of the snippet

    returns: the modified dataframe
    '''
    fixation_data[FIXATION_COLUMN_REFIXATION] = -1
    for i, row1 in fixation_data.iterrows():
        # look at all previous fixations
        sub_data = fixation_data.loc[:i-1]
        possible_refixations = {}
        for j, row2 in sub_data.iterrows():
            distance_x = abs(row2[FIXATION_COLUMN_X]-row1[FIXATION_COLUMN_X])
            distance_y = abs(row2[FIXATION_COLUMN_Y]-row1[FIXATION_COLUMN_Y])
            distance = math.sqrt(
                distance_x**2 + (REFIXATION_PENALTY_FACTOR_Y*distance_y)**2)
            # if the distance is less than the fixation radius, add the previous fixation to the current one's new column
            if distance <= FIXATION_RADIUS:
                possible_refixations[j] = distance
                if row2[FIXATION_COLUMN_REFIXATION] > -1:
                    # refixation transient: refixation on refixated fixation should also be accepted? If so, look for minimum!
                    if row2[FIXATION_COLUMN_REFIXATION] in possible_refixations:
                        possible_refixations[row2[FIXATION_COLUMN_REFIXATION]] = min(
                            possible_refixations[row2[FIXATION_COLUMN_REFIXATION]], distance)
                    else:
                        possible_refixations[row2[FIXATION_COLUMN_REFIXATION]] = distance
        # set refixation to fixation with shortest distance
        if possible_refixations:
            min_arg, min_value = -1, FIXATION_RADIUS
            for index in sorted(possible_refixations.keys()):
                if possible_refixations[index] < min_value-0.0001:
                    min_arg, min_value = index, possible_refixations[index]
            fixation_data.loc[i, FIXATION_COLUMN_REFIXATION] = min_arg
    return fixation_data


def get_longest_fixation(fixation_data: pd.DataFrame, aoi_data: pd.DataFrame = None,
                         min_duration_s: float = MIN_DURATION_S_FIXATION_EEG) -> pd.Series:
    '''Identifies the longest fixation that extends the minimal duration

    Arguments:
    * fixation_data: the fixations located in one participant's view of the snippet
    * aoi_data: the AoIs identified in the snippet (here unused)
    * min_duration_s: the minimal duration of a fixation to be considered

    returns: the longest fixation longer than min_duration_s if found, else None
    '''
    if fixation_data.empty:
        return None
    longest_fixation_index = fixation_data[FIXATION_COLUMN_DURATION].idxmax()
    longest_fixation = fixation_data.loc[longest_fixation_index]
    if longest_fixation[FIXATION_COLUMN_DURATION] >= min_duration_s:
        return longest_fixation
    return None


def get_longest_refixation(fixation_data: pd.DataFrame, aoi_data: pd.DataFrame = None,
                           min_duration_s: float = MIN_DURATION_S_FIXATION_EEG) -> pd.Series:
    '''Identifies the longest refixation that extends the minimal duration.
    Refixation means that a later fixation has been located at near the location of this fixation.

    Arguments:
    * fixation_data: the fixations located in one participant's view of the snippet
    * aoi_data: the AoIs identified in the snippet (here unused)
    * min_duration_s: the minimal duration of a fixation to be considered

    returns: the longest refixation longer than min_duration_s if found, else None
    '''
    if fixation_data.empty:
        return None
    refixations = fixation_data[fixation_data[FIXATION_COLUMN_REFIXATION] > -1]
    if refixations.empty:
        return None
    longest_refixation_index = refixations[FIXATION_COLUMN_DURATION].idxmax()
    longest_refixation = fixation_data.loc[longest_refixation_index]
    if longest_refixation[FIXATION_COLUMN_DURATION] >= min_duration_s:
        return longest_refixation
    return None


def get_first_fixation_of_most_fixated(fixation_data: pd.DataFrame, aoi_data: pd.DataFrame = None,
                                       min_duration_s: float = MIN_DURATION_S_FIXATION_EEG) -> pd.Series:
    '''Identifies the set of fixations where there is the most refixation, and longest fixation that extends the minimal duration

    Arguments:
    * fixation_data: the fixations located in one participant's view of the snippet
    * aoi_data: the AoIs identified in the snippet (here unused)
    * min_duration_s: the minimal duration of a fixation to be considered as result

    returns: the first fixation with the most other refixations longer than min_duration_s if found, else None
    '''
    fixation_data = fixation_data.reset_index(drop=True)
    fixation_counter = {}
    for i, row in fixation_data.iterrows():
        original_fixation_index = row[FIXATION_COLUMN_REFIXATION]
        # store all refixations in a dictionary by inserting them to their original fixation
        if original_fixation_index > -1:
            if not original_fixation_index in fixation_counter:
                fixation_counter[original_fixation_index] = {
                    'all_count': 0, 'long_count': 0, 'short_count': 0,
                    'list': [original_fixation_index]}
            fixation_counter[original_fixation_index]['all_count'] += 1
            fixation_counter[original_fixation_index]['list'].append(i)
            if row[FIXATION_COLUMN_DURATION] > min_duration_s:
                fixation_counter[original_fixation_index]['long_count'] += 1
            else:
                fixation_counter[original_fixation_index]['short_count'] += 1
    if len(fixation_counter) == 0:
        return None
    # sort the refixation clusters by frequency using comparator
    sorted_fixation_counter = sorted(
        fixation_counter.items(), key=lambda x: (x[1]['all_count'], x[1]['long_count']), reverse=True)
    # for most frequent refixation, take the first that exceeds the minimal duration
    for fixation_index in sorted_fixation_counter[0][1]['list']:
        fixation = fixation_data.loc[fixation_index]
        if fixation[FIXATION_COLUMN_DURATION] >= min_duration_s:
            return fixation
    print('For most refixations no fixation with given duration found.')
    return None


def get_longest_fixation_optimal_aoi(fixation_data: pd.DataFrame, aoi_data: pd.DataFrame, aoi_padding: dict[str, float],
                                     min_duration_s: float = MIN_DURATION_S_FIXATION_EEG) -> pd.Series:
    '''Identifies the longest fixation that extends the minimal duration

    Arguments:
    * fixation_data: the fixations located in one participant's view of the snippet
    * aoi_data: the AoIs identified in the snippet (here unused)
    * min_duration_s: the minimal duration of a fixation to be considered

    returns: the longest fixation longer than min_duration_s if found, else None
    '''
    return get_longest_fixation(get_fixations_in_aoi(fixation_data, aoi_data, aoi_padding), aoi_data, min_duration_s)


def get_longest_refixation_optimal_aoi(fixation_data: pd.DataFrame, aoi_data: pd.DataFrame, aoi_padding: dict[str, float],
                                       min_duration_s: float = MIN_DURATION_S_FIXATION_EEG) -> pd.Series:
    '''Identifies the longest fixation that extends the minimal duration

    Arguments:
    * fixation_data: the fixations located in one participant's view of the snippet
    * aoi_data: the AoIs identified in the snippet (here unused)
    * min_duration_s: the minimal duration of a fixation to be considered

    returns: the longest fixation longer than min_duration_s if found, else None
    '''
    return get_longest_refixation(get_fixations_in_aoi(fixation_data, aoi_data, aoi_padding), aoi_data, min_duration_s)


def get_first_fixation_optimal_aoi(fixation_data: pd.DataFrame, aoi_data: pd.DataFrame, aoi_padding: dict[str, float],
                                   min_duration_s: float = MIN_DURATION_S_FIXATION_EEG) -> pd.Series:
    '''Identifies the set of fixations where there is the most refixation, and longest fixation that extends the minimal duration

    Arguments:
    * fixation_data: the fixations located in one participant's view of the snippet
    * aoi_data: the AoIs identified in the snippet (here unused)
    * min_duration_s: the minimal duration of a fixation to be considered as result

    returns: the first fixation with the most other refixations longer than min_duration_s if found, else None
    '''
    fixation_data = get_fixations_in_aoi(fixation_data, aoi_data, aoi_padding)
    for i, fixation in fixation_data.iterrows():
        if fixation[FIXATION_COLUMN_DURATION] >= min_duration_s:
            return fixation
    return None


def get_first_fixation(fixation_data: pd.DataFrame, aoi_data: pd.DataFrame, min_duration_s: float = MIN_DURATION_S_FIXATION_EEG) -> pd.Series:
    '''Identifies the first fixation

    Arguments:
    * fixation_data: the fixations located in one participant's view of the snippet
    * aoi_data: the AoIs identified in the snippet (here unused)
    * min_duration_s: the minimal duration of a fixation to be considered as result

    returns: the first fixation with the most other refixations longer than min_duration_s if found, else None
    '''
    return fixation_data.iloc[0]


def get_fixations_in_aoi(fixation_data: pd.DataFrame, aoi_data: pd.DataFrame, aoi_padding: dict[str, int]):
    optimal_aoi = aoi_data[aoi_data[OPTIMAL]].squeeze()
    aoi_area = {POS_BOTTOM: optimal_aoi[POS_BOTTOM]+aoi_padding[POS_BOTTOM],
                POS_TOP: optimal_aoi[POS_TOP]-aoi_padding[POS_TOP],
                POS_LEFT: optimal_aoi[POS_LEFT]-aoi_padding[POS_LEFT],
                POS_RIGHT: optimal_aoi[POS_RIGHT]+aoi_padding[POS_RIGHT]}
    fixation_data = fixation_data[fixation_data.apply(lambda row: check_point_in_area(
        row[FIXATION_COLUMN_X], row[FIXATION_COLUMN_Y], row[FIXATION_COLUMN_RADIUS_X], row[FIXATION_COLUMN_RADIUS_Y], aoi_area), axis=1)]
    return fixation_data


def identify_closest_long_fixation(fixation_data: pd.DataFrame, aoi_data: pd.DataFrame,
                                   aoi_padding: dict[str, int], min_duration_s: float = MIN_DURATION_S_FIXATION_EEG,
                                   try_for_better_order: int = 2, try_for_better_distance_worsening: int = 10, try_for_better_distance_optimizing: int = 5):
    '''identifies the suitable fixation for FRP via duration, distance to AOI and order

    using a sophisticated algorithm:
      - from all fixations longer than a certain duration 
      - get the first fixation within a given boundary of the AOI (use direct AOI boundary retrieved from image)
      - with a certain tradeoff between proximity to AOI and order of fixations

    Arguments:
    * fixation_data: contains the data of the fixations for one participant's trial
    * AOIs: the markers of the AOI borders (in pixels), each given by AOI name and inside given via the 4 position markers '{POS_TOP}', '{POS_LEFT}', '{POS_BOTTOM}', '{POS_RIGHT}'
    * min_duration_s: the minimum required duration of a fixation to be considered for FRP
    * aoi_padding: the accepted padding around an AOI in which a suitable fixation can be considered for FRP (in pixels)
    * try_for_better_order: the amount of fixations with a given duration that shall be tested for better fit after identifying the first suitable fixation
    * try_for_better_distance_worsening: the maximum worsening in distance allowed for finding a better fixation after the first suitable one has been found, considers also unsuitable fixations. (in pixels)
    * try_for_better_distance_optimizing: the distance a better fixation has to reduce after the first suitable one has been found (only for suitable fixations). (in pixels)

    returns: the starting point of a fixation that should be used for FRP, if such could be identified. Otherwise -1
'''
    if aoi_data is None or (aoi_data.empty):
        print('No AOIs given')
        return None
    optimal_aoi = aoi_data[aoi_data[OPTIMAL]].squeeze()
    aoi_area = {POS_BOTTOM: optimal_aoi[POS_BOTTOM]+aoi_padding[POS_BOTTOM],
                POS_TOP: optimal_aoi[POS_TOP]-aoi_padding[POS_TOP],
                POS_LEFT: optimal_aoi[POS_LEFT]-aoi_padding[POS_LEFT],
                POS_RIGHT: optimal_aoi[POS_RIGHT]+aoi_padding[POS_RIGHT]}
    found_better = -1
    for i, row in fixation_data.iterrows():
        # for i, duration_suitable, start_time, x, y, range_x, range_y in fixations:
        x, y = row[FIXATION_COLUMN_X], row[FIXATION_COLUMN_Y]
        radius_x, radius_y = row[FIXATION_COLUMN_RADIUS_X], row[FIXATION_COLUMN_RADIUS_Y]
        if found_better > -1:
            if i < found_better:
                continue
            elif i == found_better:
                found_better = -1
            else:
                print(
                    f'How did this happen: i {i} found_better {found_better}')
                break
        # check that fixation duration is acceptable
        if row[FIXATION_COLUMN_DURATION] > min_duration_s:
            # check that fixation is in acceptable distance to AOI
            if not check_point_in_area(x, y, radius_x, radius_y, aoi_area):
                continue
            # print(
            #     f'found suitable fixation at index {i} and position ({x},{y}). Now check that there is not a better one later on')
            # TODO: factor in direction?
            distance_to_AOI, direction_from_AOI = get_distance_to_area(
                x, y, radius_x, radius_y, optimal_aoi)
            # found suitable fixation at index i. Now check that there is not a better one later on
            for i_try, row_try in fixation_data.loc[i+1:i+try_for_better_order+1].iterrows():
                x_try, y_try = row_try[FIXATION_COLUMN_X], row_try[FIXATION_COLUMN_Y]
                radius_x_try, radius_y_try = row_try[FIXATION_COLUMN_RADIUS_X], row_try[FIXATION_COLUMN_RADIUS_Y]
                # check tradeoff between this and later fixations
                # check that distance hasn't worsened too much
                distance_to_AOI_try, direction_from_AOI_try = get_distance_to_area(
                    x_try, y_try, radius_x_try, radius_y_try, optimal_aoi)
                if distance_to_AOI_try > try_for_better_distance_worsening+distance_to_AOI:
                    break
                # check that fixation duration is acceptable
                if row_try[FIXATION_COLUMN_DURATION] <= min_duration_s:
                    continue
                # check that fixation is in acceptable distance to AOI
                if not check_point_in_area(x_try, y_try, radius_x_try, radius_y_try, aoi_area):
                    continue
                # check that fixation has a better distance
                if distance_to_AOI_try < distance_to_AOI-try_for_better_distance_optimizing:
                    found_better = i_try
            if found_better == -1:
                return row
    return None


# Mapping of fixation algorithm to function (functions have all identical fixation_data: pd.Series and AOIs, the rest is optional)
FIXATION_SELECTION_ALGORITHM_FUNCTIONS: \
    dict[str, Callable[[pd.DataFrame, pd.DataFrame, float], pd.Series]] = {
        FIXATION_SELECTION_ALGORITHM_FIRST_AOI_PADDING_SMALL: lambda fixation_data, aoi_data: get_first_fixation_optimal_aoi(fixation_data, aoi_data, AOI_PADDING_SMALL)
    }

FIXATION_SELECTION_ALGORITHM_COLORS: dict[str, str] = {
    FIXATION_SELECTION_ALGORITHM_FIRST_AOI_PADDING_SMALL: '',
}


def create_scanpath_image(participant: str, snippet: str, fixation_data: pd.DataFrame, special_fixation_data: pd.DataFrame):
    try:
        # take first eye gazes by snippet and visualize them on the screenshot
        cm_a = mpl.cm.ScalarMappable(
            cmap='hsv', norm=plt.Normalize(vmin=0, vmax=fixation_data.shape[0] + 2))
        # +2 to to not receive identical color on start and end
        fig, axis = plt.subplots(1, 1, figsize=(WIDTH/100, HEIGHT/100))
        with Image.open(get_screenshot_path(snippet, aoi_version=True)) as image:
            axis.imshow(image)
            patches = []
            labels = []
            # generate circle patch for gaze
            for index, (_, row) in enumerate(fixation_data.iterrows()):
                x, y = int(row[FIXATION_COLUMN_X]), int(row[FIXATION_COLUMN_Y])
                duration = row[FIXATION_COLUMN_DURATION]
                alpha = 0.2
                c = cm_a.to_rgba(index)
                p = Circle((x, y), radius=duration*DURATION_SIZE_FACTOR,
                           color=c, alpha=alpha, linewidth=1)
                axis.add_patch(p)
                if duration >= MIN_DURATION_S_FIXATION_EEG:
                    patch = Circle((x, y), radius=duration*DURATION_SIZE_FACTOR+1,
                                   color='black', alpha=0.5, linewidth=1, fill=False)
                    axis.add_patch(patch)
                    if len(patches) == 1:
                        patches.append(patch)
                        labels.append(
                            f'Fixation duration >= {MIN_DURATION_S_FIXATION_EEG} s')
                patches.append(p)
                # Plot paths between fixations as arrows
                if index == fixation_data.index[-1]:
                    continue  # no arrows from last entry
                delta_x = int(
                    fixation_data.loc[index + 1, FIXATION_COLUMN_X])-x
                delta_y = int(
                    fixation_data.loc[index + 1, FIXATION_COLUMN_Y])-y
                axis.arrow(x, y, delta_x, delta_y,
                           color=c, alpha=0.8,
                           head_width=20, length_includes_head=True, width=5, linewidth=0)
            # special fixations
            special_fixation_data = special_fixation_data[special_fixation_data[PARTICIPANT]
                                                          == participant & special_fixation_data[SNIPPET] == snippet]
            for i, fixation in special_fixation_data.iterrows():
                fixation_selection_algorithm = fixation[FIXATION_SELECTION_ALGORITHM]
                patch = Circle((int(fixation[FIXATION_COLUMN_X]), int(fixation[FIXATION_COLUMN_Y])), radius=fixation[FIXATION_COLUMN_DURATION]
                               * DURATION_SIZE_FACTOR, alpha=0.5, color=FIXATION_SELECTION_ALGORITHM_COLORS[fixation_selection_algorithm], linewidth=1, fill=False)
                patches.append(patch)
                labels.append(
                    f'{fixation_selection_algorithm.replace("_", " ")} (offset {round(fixation[FIXATION_COLUMN_START] / 1000, 3)}s)')

            axis.axis('off')

            axis.set_title(f'{snippet} - {participant}')
            # add legend
            handles, labels = [axis.patches[0]], ['Fixation 1']
            RAINBOW_INTERVALS = 6
            if fixation_data.shape[0] > RAINBOW_INTERVALS:
                for j in np.linspace(0, fixation_data.shape[0]-1, RAINBOW_INTERVALS+1).tolist()[1:-1]:
                    j = int(round(j, 0))
                    handles.append(axis.patches[j])
                    labels.append(f'Fixation {j+1}')
            elif fixation_data.shape[0] > 2:
                handles.append(axis.patches[fixation_data.shape[0]//2])
                labels.append('Fixation Median')
            if fixation_data.shape[0] > 1:
                handles.append(axis.patches[fixation_data.shape[0]-1])
                labels.append(f'Fixation {fixation_data.shape[0]}')
            axis.legend(handles=handles, labels=labels)
        # save figure
        fig.tight_layout()
        # fig.savefig(get_scanpath_image_path(  # type: ignore
        #     participant, snippet, False),
        #     bbox_inches='tight', pad_inches=0)
        plt.close()
        for p in patches:
            del p
    except Exception:
        print(traceback.format_exc())
        return False
    return True


def get_special_fixation_add_patch(fixation_algorithm_type: str, fixation_data: pd.DataFrame, aois: dict[str, dict[str, int]], patches: list, labels: list):
    fixation: pd.Series = FIXATION_SELECTION_ALGORITHM_FUNCTIONS[fixation_algorithm_type](
        fixation_data, aois)
    patch = None
    if fixation is not None:
        patch = Circle((int(fixation[FIXATION_COLUMN_X]), int(fixation[FIXATION_COLUMN_Y])), radius=fixation[FIXATION_COLUMN_DURATION]
                       * DURATION_SIZE_FACTOR, alpha=0.5, color=FIXATION_SELECTION_ALGORITHM_COLORS[fixation_algorithm_type], linewidth=1, fill=False)
        patches.append(patch)
        labels.append(
            f'{fixation_algorithm_type.replace("_", " ")} (offset {round(fixation[FIXATION_COLUMN_START] / 1000, 3)}s)')
    return fixation, patch
