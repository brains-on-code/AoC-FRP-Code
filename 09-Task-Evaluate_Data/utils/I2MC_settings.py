import numpy as np
from utils.visual_settings import FIXATION_RADIUS, HEIGHT, WIDTH

# Options for I2MC algorithm - General variables for eye-tracking data
I2MC_options = {
    'xres': WIDTH,  # maximum value of horizontal resolution in pixels
    'yres': HEIGHT,  # maximum value of vertical resolution in pixels
    'freq': 60,  # sampling frequency of data
    # adapt to real frequency in data

    # Variables for the calculation of visual angle
    # These values are used to calculate noise measures (RMS and BCEA) of
    # fixations. The may be left as is, but don't use the noise measures then.
    # If either or both are empty, the noise measures are provided in pixels
    # instead of degrees.
    'scrSz': [55.0, 32.5],  # screen size in cm
    'disttoscreen': 65.0,  # distance to screen in cm.

    # STEFFEN INTERPOLATION
    # max duration (s) of missing values for interpolation to occur
    'windowtimeInterp': 0.1,
    # amount of data (number of samples) at edges needed for interpolation
    'edgeSampInterp': 2,

    # # K-MEANS CLUSTERING
    # time window (s) over which to calculate 2-means clustering (choose value so that max. 1 saccade can occur)
    'windowtime': 0.2,
    # time window shift (s) for each iteration. Use zero for sample by sample processing
    'steptime': 0.02,
    'maxerrors': 100,  # maximum number of errors allowed in k-means clustering procedure before proceeding to next file
    'downsamples': [2, 5, 10],
    # use chebychev filter when down sampling? 1: yes, 0: no. requires signal processing toolbox. is what matlab's
    # down sampling internal_helpers do, but could cause trouble (ringing) with the hard edges in eye-movement data
    'downsampFilter': False,

    # # FIXATION DETERMINATION
    # number of standard deviations above mean k-means weights will be used as fixation cutoff
    'cutoffstd': 2.0,
    # number of MAD away from median fixation duration. Will be used to walk forward at fixation starts and backward at
    'onoffsetThresh': 3.0,
    # fixation ends to refine their placement and stop algorithm from eating into saccades
    # maximum Euclidean distance in pixels between fixations for merging
    'maxMergeDist': FIXATION_RADIUS,
    'maxMergeTime': 60.0,  # maximum time in ms between fixations for merging
    'minFixDur': 0.2,  # minimum fixation duration after merging, fixations with shorter duration are removed from output
    # TODO adapted from original
    # eliminate randomness in i2mc by fixating the initial cluster based on those two values
    'first_cluster_fixed_value': 0.25,
    'second_cluster_fixed_value': 0.75,

}
# maximum displacement during missing for interpolation to be possible
I2MC_options['maxdisp'] = I2MC_options['xres'] * 0.2 * np.sqrt(2)
# internal_helpers as signal for data loss
# missing value for horizontal position in eye-tracking data (example data uses -xres). used throughout
I2MC_options['missingx'] = -I2MC_options['xres']
# missing value for vertical position in eye-tracking data (example data uses -yres). used throughout
I2MC_options['missingy'] = -I2MC_options['yres']
