import numpy as np

# radius of ellipsis marked as central vision in heatmap, in the x axis
ELLIPSIS_X_RADIUS = 0
# radius of ellipsis marked as central vision, in the y axis
ELLIPSIS_Y_RADIUS = 0
GAUSSIAN_RADIUS = 5  # radius of gaussian kernel
# variance for gaussian kernel (how much outside the central vision can be considered)
GAUSSIAN_SIGMA = 5

WIDTH, HEIGHT = 1920, 1080

# in psychopy, (x,y)=(0,0) is in the center, x increases to the right, y increases to the top
# however, the ends of the axes are not 1 / -1, but depend on the height / width ratio
PSYCHOPY_WIDTH = WIDTH / (2*min(WIDTH, HEIGHT))
PSYCHOPY_HEIGHT = HEIGHT / (2*min(WIDTH, HEIGHT))
# can be verified via validation - there is the window boundary mentioned
PSYCHOPY_X_AREA = -PSYCHOPY_WIDTH, PSYCHOPY_WIDTH
PSYCHOPY_Y_AREA = -PSYCHOPY_HEIGHT, PSYCHOPY_HEIGHT

FIXATION_RADIUS = 50
DURATION_SIZE_FACTOR = 20

MIN_FIXATION_COUNT_TRIAL = 2
MAX_GAZE_NA_TOTAL_TOLERANCE = 0.25
MAX_GAZE_NA_INTERVAL_TOLERANCE = 1
MIN_NOTICEABLE_NA_INTERVAL = 0.1

MIN_DURATION_S_FIXATION_EEG = 0.2


def get_eyetracking_frequency(participant):
    '''get frequency of the eye tracker for the participant

    Argument: participant: the number of the participant as a string

    returns: the frequency of the eye tracker
    '''
    return 1200.0


MANUAL_ACCURACY_EVALUATION_CHOICE = 'Choice'
MANUAL_ACCURACY_EVALUATION_FIRST_FIXATION_OUTLIER = 'First Fixation for Fixation Cross (original)'
MANUAL_ACCURACY_EVALUATION_OUTLIER = 'Clear Outliers visible (original)'
MANUAL_ACCURACY_EVALUATION_X_OFFSET = 'Offset on x-axis visible (original)'
MANUAL_ACCURACY_EVALUATION_REASON = 'Reason'
MANUAL_ACCURACY_EVALUATION_ITERATION = 'Correction Iteration'


FIXATION_CORRECTION_ALGORITHM_ORIGINAL = 'original'
FIXATION_CORRECTION_ALGORITHM_CLUSTER_ALLLINES = 'cluster_alllines'
# FIXATION_CORRECTION_ALGORITHM_CLUSTER_ALLLINES_AGGREGATED='cluster_alllines_aggregated'
FIXATION_CORRECTION_ALGORITHM_STRETCH_ALLLINES = 'stretch_alllines'
FIXATION_CORRECTION_ALGORITHM_CLUSTER_ESSENTIALLINES = 'cluster_essentiallines'
# FIXATION_CORRECTION_ALGORITHM_CLUSTER_ESSENTIALLINES_AGGREGATED='cluster_essentiallines_aggregated'
FIXATION_CORRECTION_ALGORITHM_STRETCH_ESSENTIALLINES = 'stretch_essentiallines'
FIXATION_CORRECTION_ALGORITHM_SNIPPET_EXCLUDED = 'excluded'

FIXATION_CORRECTION_ALGORITHMS = [
    FIXATION_CORRECTION_ALGORITHM_ORIGINAL,
    FIXATION_CORRECTION_ALGORITHM_CLUSTER_ALLLINES,
    # FIXATION_CORRECTION_ALGORITHM_CLUSTER_ALLLINES_AGGREGATED,
    FIXATION_CORRECTION_ALGORITHM_STRETCH_ALLLINES,
    FIXATION_CORRECTION_ALGORITHM_CLUSTER_ESSENTIALLINES,
    # FIXATION_CORRECTION_ALGORITHM_CLUSTER_ESSENTIALLINES_AGGREGATED,
    FIXATION_CORRECTION_ALGORITHM_STRETCH_ESSENTIALLINES
]

FIXATION_CORRECTION_ITERATION = [-1]
def current_fixation_correction_iteration():
    global FIXATION_CORRECTION_ITERATION
    return FIXATION_CORRECTION_ITERATION[0]
def previous_fixation_correction_iteration():
    global FIXATION_CORRECTION_ITERATION
    return FIXATION_CORRECTION_ITERATION[0]-1

# 1D array representing the Y coordinates of the lines of code
LINES_OF_CODE_Y = np.array(
    [290, 343, 396, 449, 502, 555, 608, 661, 714, 767, 820], dtype=int)

REFIXATION_PENALTY_FACTOR_Y = 1.5

FIXATION_SELECTION_ALGORITHM = 'fixation selection algorithm'
FIXATION_SELECTION_ALGORITHM_FIRST_AOI_PADDING_SMALL = 'first_fixation_aoi_small'
FIXATION_SELECTION_ALGORITHMS = [
    FIXATION_SELECTION_ALGORITHM_FIRST_AOI_PADDING_SMALL,
]

FIXATION_SELECTION_SHORT_VERSION = {
    FIXATION_SELECTION_ALGORITHM_FIRST_AOI_PADDING_SMALL: 'faois'
}
