from pathlib import Path

from utils.textconstants import BEHAVIORAL, TOTAL, VISUAL

# Path from where to load the raw data
RAW_PATH = Path('../08-Data-Trial_Recordings/raw/')


EEG_FILE_DATA_ENDING = '.eeg'
EEG_FILE_HEADER_ENDING = '.vhdr'
EEG_FILE_MARKER_ENDING = '.vmrk'

# Path to csv with all questions and correct answers
CODE_SNIPPET_PATH_NORMAL = Path('../01-Data-Code_Snippets')
CODE_SNIPPET_PATH_AOI = Path('../01a-Data-Annotated_Code_Snippets')
SNIPPETS_PATH = CODE_SNIPPET_PATH_NORMAL/'snippets.csv'


# Path to screenshot files
SCREENSHOTS_PATH = RAW_PATH.parent/'screenshots'
SCREENSHOTS_PATH_AOI = SCREENSHOTS_PATH/'aoi'
SCREENSHOTS_PATH_NORMAL = SCREENSHOTS_PATH/'normal'
SCREENSHOTS_PATH_FIXATION_CROSS = SCREENSHOTS_PATH/'fixation_cross.png'
SCREENSHOTS_PATH_DUMMY = SCREENSHOTS_PATH/'dummy.png'


# Path where to store the processed data
PROCESSED_PATH = RAW_PATH.parent/'processed/'
X_OFFSET_FILE = PROCESSED_PATH/TOTAL/VISUAL/'accuracy_offset_x_axis.json'
# Path to all processed data aspects
# ALL_FIXATIONS_PATH = PROCESSED_PATH / FIXATIONS / f'{FIXATIONS}.csv'
# ALL_BEHAVIORAL_PATH = PROCESSED_PATH / f'{BEHAVIORAL}.csv'
# ALL_GAZES_PATH = PROCESSED_PATH / FIXATIONS / 'GazeData.csv'
# AOI_PATH =  PROCESSED_PATH / 'aoi'
AOI_SUMMARY_PATH = SCREENSHOTS_PATH/'analysis/aoi_positions.json'
AOI_SIZE_PATH = SCREENSHOTS_PATH / 'analysis/aoi_sizes.csv'
CODE_SIZE_PATH = SCREENSHOTS_PATH / 'analysis/code_sizes.csv'
(SCREENSHOTS_PATH/'analysis').mkdir(parents=True, exist_ok=True)

# Path to store the results from the evaluation
EVAL_PATH = Path('../10-Data_Evaluation_Results/')

EVAL_PATH_AGGREGATED_DATA = EVAL_PATH/BEHAVIORAL/'aggregated_data'
EVAL_PATH_AGGREGATED_DATA_PLOT = EVAL_PATH_AGGREGATED_DATA/'plot'
EVAL_PATH_AGGREGATED_DATA_SUMMARY = EVAL_PATH_AGGREGATED_DATA/'summary.xlsx'

EVAL_PATH_STATISTICS_BLOCK_BASED = EVAL_PATH/BEHAVIORAL/'block_based'
EVAL_PATH_STATISTICS_BLOCK_BASED_SUMMARY = EVAL_PATH_STATISTICS_BLOCK_BASED/'summary.xlsx'

EVAL_PATH_HEATMAPS = EVAL_PATH/VISUAL/'heatmaps/'
EVAL_PATH_GAZEPLOT = EVAL_PATH/VISUAL/'scanpath/'

EVAL_PATH_FRP_MARKERS = EVAL_PATH/'FRP_marked'
