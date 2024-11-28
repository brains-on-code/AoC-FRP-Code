#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2021.2.3),
    on Dezember 01, 2023, at 13:34
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

from __future__ import absolute_import, division

from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, parallel, iohub, hardware
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard



# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '2021.2.3'
expName = 'Experiment'  # from the Builder filename that created this script
expInfo = {'participant': '', 'session': '001', 'skipIntro': False, 'startRound': '1', 'startLoopPos': '1'}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\Test\\Desktop\\AoC FRP final\\Experiment_lastrun.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# Setup the Window
win = visual.Window(
    size=[1920, 1080], fullscr=True, screen=0, 
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# Setup eyetracking
ioDevice = 'eyetracker.hw.tobii.EyeTracker'
ioConfig = {
    ioDevice: {
        'name': 'tracker',
        'model_name': 'Tobii Pro Spectrum',
        'serial_number': '',
        'runtime_settings': {
            'sampling_rate': 1200.0,
        }
    }
}
ioSession = '1'
if 'session' in expInfo:
    ioSession = str(expInfo['session'])
ioServer = io.launchHubServer(window=win, experiment_code='Experiment', session_code=ioSession, datastore_name=filename, **ioConfig)
eyetracker = ioServer.getDevice('tracker')

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

# Initialize components for Routine "IntroText"
IntroTextClock = core.Clock()
Intro_text = visual.TextStim(win=win, name='Intro_text',
    text='Welcome to the study!\nPress "Enter" to continue',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
key_resp_17 = keyboard.Keyboard()
comments = visual.TextStim(win=win, name='comments',
    text='disabled all eeg ports as not used\nincluding: startEvent, EEG End, Snippet, Rating, Long Pause',
    font='Open Sans',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);

# Initialize components for Routine "Presentation"
PresentationClock = core.Clock()
force_skip_movie = keyboard.Keyboard()
image_2 = visual.ImageStim(
    win=win,
    name='image_2', 
    image='sin', mask=None,
    ori=0.0, pos=(0, 0), size=(1.778, 1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-1.0)
key_resp_4 = keyboard.Keyboard()

# Initialize components for Routine "Example_Begin"
Example_BeginClock = core.Clock()
Example_text = visual.TextStim(win=win, name='Example_text',
    text='Now, we will navigate you through a task example. \nThis trial is not part of the actual study.',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
text_5 = visual.TextStim(win=win, name='text_5',
    text='First, look at the fixation cross to calibrate your eye movement and normalize your brain activity.',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
force_skip_5 = keyboard.Keyboard()

# Initialize components for Routine "Example_Snippet"
Example_SnippetClock = core.Clock()
Background_4 = visual.ImageStim(
    win=win,
    name='Background_4', 
    image='dummy.png', mask=None,
    ori=0.0, pos=(0, 0), size=(0.8, 0.55),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)
etRecord_4 = hardware.eyetracker.EyetrackerControl(
    server=ioServer,
    tracker=eyetracker
)
image_5 = visual.ImageStim(
    win=win,
    name='image_5', 
    image='sin', mask=None,
    ori=0.0, pos=(0, 0), size=(0.75, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-2.0)
skip_4 = keyboard.Keyboard()
force_skip_4 = keyboard.Keyboard()
Snippet_text = visual.TextStim(win=win, name='Snippet_text',
    text='Then, read the presented Java code snippet and determine the value of R at the end of the snippet. \nYou have 30 seconds to read the code.\nIf you have finished early, you can click "Enter" to continue before the timeout.',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-5.0);
circle_1 = visual.ShapeStim(
    win=win, name='circle_1',
    size=(0.08, 0.08), vertices='circle',
    ori=0.0, pos=(0, 0),
    lineWidth=1.0,     colorSpace='rgb',  lineColor='black', fillColor='black',
    opacity=None, depth=-6.0, interpolate=True)
fixation_cross_10 = visual.Line(
    win=win, name='fixation_cross_10',
    start=(-(0.08, 0.08)[0]/2.0, 0), end=(+(0.08, 0.08)[0]/2.0, 0),
    ori=90.0, pos=(0, 0),
    lineWidth=10.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
    opacity=None, depth=-7.0, interpolate=True)
fixation_cross_9 = visual.Line(
    win=win, name='fixation_cross_9',
    start=(-(0.08, 0.08)[0]/2.0, 0), end=(+(0.08, 0.08)[0]/2.0, 0),
    ori=0.0, pos=(0, 0),
    lineWidth=10.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
    opacity=None, depth=-8.0, interpolate=True)
small_circle_2 = visual.ShapeStim(
    win=win, name='small_circle_2',units='pix', 
    size=(8, 8), vertices='circle',
    ori=0.0, pos=(0, 0),
    lineWidth=1.0,     colorSpace='rgb',  lineColor='black', fillColor='black',
    opacity=None, depth=-9.0, interpolate=True)

# Initialize components for Routine "Example_Question"
Example_QuestionClock = core.Clock()
question_4 = visual.TextStim(win=win, name='question_4',
    text='Now answer the following question: \nWhat is the final value in R at the end of the code snippet?',
    font='Open Sans',
    pos=(0, 0.2), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
key_resp_12 = keyboard.Keyboard()
two_answers_4 = visual.Slider(win=win, name='two_answers_4',
    startValue=None, size=(0.9, 0.02), pos=(0, 0), units=None,
    labels=['1','2', '3', "I'm not sure"], ticks=(1, 2, 3, 4), granularity=1.0,
    style='radio', styleTweaks=(), opacity=None,
    color='LightGray', fillColor='Red', borderColor='0.3255, 0.3255, 0.3255', colorSpace='rgb',
    font='Open Sans', labelHeight=0.05,
    flip=False, depth=-2, readOnly=False)
key_image = visual.ImageStim(
    win=win,
    name='key_image', 
    image='key_1.png', mask=None,
    ori=0.0, pos=(-0.45, 0.05), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-3.0)
key_image_4 = visual.ImageStim(
    win=win,
    name='key_image_4', 
    image='key_2.png', mask=None,
    ori=0.0, pos=(-0.15, 0.05), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-4.0)
key_image_5 = visual.ImageStim(
    win=win,
    name='key_image_5', 
    image='key_3.png', mask=None,
    ori=0.0, pos=(0.15, 0.05), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-5.0)
key_image_enter_3 = visual.ImageStim(
    win=win,
    name='key_image_enter_3', 
    image='key_enter.png', mask=None,
    ori=0.0, pos=(0.45, 0.05), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-6.0)

# Initialize components for Routine "Example_Difficulty"
Example_DifficultyClock = core.Clock()
difficulty_4 = visual.TextStim(win=win, name='difficulty_4',
    text='Now answer the following question: \nHow difficult was it for you to understand the code snippet and calculate the final value of R?',
    font='Open Sans',
    pos=(0, 0.2), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
key_resp_13 = keyboard.Keyboard()
answers_4 = visual.Slider(win=win, name='answers_4',
    startValue=None, size=(0.9, 0.02), pos=(0, 0), units=None,
    labels=["easy", "hard", "I'm not \nsure"], ticks=(1, 2, 4), granularity=1.0,
    style='radio', styleTweaks=(), opacity=None,
    color='LightGray', fillColor='Red', borderColor='0.3255, 0.3255, 0.3255', colorSpace='rgb',
    font='Open Sans', labelHeight=0.05,
    flip=False, depth=-2, readOnly=False)
key_image_1_3 = visual.ImageStim(
    win=win,
    name='key_image_1_3', 
    image='key_1.png', mask=None,
    ori=0.0, pos=(-0.45, 0.05), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-3.0)
key_image_2_3 = visual.ImageStim(
    win=win,
    name='key_image_2_3', 
    image='key_2.png', mask=None,
    ori=0.0, pos=(-0.15, 0.05), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-4.0)
key_image_enter_4 = visual.ImageStim(
    win=win,
    name='key_image_enter_4', 
    image='key_enter.png', mask=None,
    ori=0.0, pos=(0.45, 0.05), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-5.0)

# Initialize components for Routine "start"
startClock = core.Clock()
start_experiment = visual.TextStim(win=win, name='start_experiment',
    text='This was the example.\nIf you have any questions, please contact the experimental manager. \nOtherwise, press „Enter“ to start the study. \nFirst comes the calibration.\nPlease remember to sit as unmoving as possible.',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
space_start = keyboard.Keyboard()

# Initialize components for Routine "EEG_Start"
EEG_StartClock = core.Clock()
text_7 = visual.TextStim(win=win, name='text_7',
    text="Please start the EEG recording now if it hasn't started already.",
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
key_resp_15 = keyboard.Keyboard()

# Initialize components for Routine "startEvent"
startEventClock = core.Clock()
experiment_start_event = parallel.ParallelPort(address='0x0378')

# Initialize components for Routine "CheckPos"
CheckPosClock = core.Clock()
Round_marker = visual.TextStim(win=win, name='Round_marker',
    text='',
    font='Open Sans',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "Snippet"
SnippetClock = core.Clock()
Background = visual.ImageStim(
    win=win,
    name='Background', 
    image='dummy.png', mask=None,
    ori=0.0, pos=(0, 0), size=(0.8, 0.55),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)
etRecord = hardware.eyetracker.EyetrackerControl(
    server=ioServer,
    tracker=eyetracker
)
image = visual.ImageStim(
    win=win,
    name='image', 
    image='sin', mask=None,
    ori=0.0, pos=(0, 0), size=(0.75, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-2.0)
skip = keyboard.Keyboard()
snippet_start_event = parallel.ParallelPort(address='0x0378')
import pandas as pd
from datetime import datetime
import datetime as dt
from psychopy import core
df_stimuli = pd.DataFrame([], columns=["stimuli", "startTime", "endTime"])
df_answer = pd.DataFrame([], columns=["task", "answer", "correctness"])
df_eval = pd.DataFrame([], columns=["task", "difficulty"])
df_et = pd.DataFrame([], columns=["time", "position", "left_pupil_diameter", "right_pupil_diameter", "stimuli"])

folder_name = f"./data/test"
# Check if the directory exists
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

start_time = datetime.now()
end_of_stimuli = None

force_skip = keyboard.Keyboard()
p_port_2 = parallel.ParallelPort(address='0x0378')
circle = visual.ShapeStim(
    win=win, name='circle',
    size=(0.08, 0.08), vertices='circle',
    ori=0.0, pos=(0, 0),
    lineWidth=1.0,     colorSpace='rgb',  lineColor='black', fillColor='black',
    opacity=None, depth=-8.0, interpolate=True)
fixation_cross_2 = visual.Line(
    win=win, name='fixation_cross_2',
    start=(-(0.08, 0.08)[0]/2.0, 0), end=(+(0.08, 0.08)[0]/2.0, 0),
    ori=90.0, pos=(0, 0),
    lineWidth=10.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
    opacity=None, depth=-9.0, interpolate=True)
fixation_cross = visual.Line(
    win=win, name='fixation_cross',
    start=(-(0.08, 0.08)[0]/2.0, 0), end=(+(0.08, 0.08)[0]/2.0, 0),
    ori=0.0, pos=(0, 0),
    lineWidth=10.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
    opacity=None, depth=-10.0, interpolate=True)
small_circle = visual.ShapeStim(
    win=win, name='small_circle',units='pix', 
    size=(8, 8), vertices='circle',
    ori=0.0, pos=(0, 0),
    lineWidth=1.0,     colorSpace='rgb',  lineColor='black', fillColor='black',
    opacity=None, depth=-11.0, interpolate=True)

# Initialize components for Routine "Question"
QuestionClock = core.Clock()
question = visual.TextStim(win=win, name='question',
    text='What is the final value in R at the end of the code snippet?',
    font='Open Sans',
    pos=(0, 0.2), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
key_resp = keyboard.Keyboard()
three_answers = visual.Slider(win=win, name='three_answers',
    startValue=None, size=(0.9, 0.02), pos=(0, 0), units=None,
    labels=['placeholder_1','placeholder_2','placeholder_3','placeholder_4'], ticks=(1, 2, 3, 4), granularity=1.0,
    style='radio', styleTweaks=(), opacity=None,
    color='LightGray', fillColor='Red', borderColor='0.3255, 0.3255, 0.3255', colorSpace='rgb',
    font='Open Sans', labelHeight=0.05,
    flip=False, depth=-2, readOnly=False)
two_answers = visual.Slider(win=win, name='two_answers',
    startValue=None, size=(0.9, 0.02), pos=(0, 0), units=None,
    labels=['placeholder_1','placeholder_2','placeholder_3'], ticks=(1, 2, 4), granularity=1.0,
    style='radio', styleTweaks=(), opacity=None,
    color='LightGray', fillColor='Red', borderColor='0.3255, 0.3255, 0.3255', colorSpace='rgb',
    font='Open Sans', labelHeight=0.05,
    flip=False, depth=-4, readOnly=False)
p_port = parallel.ParallelPort(address='0x0378')
key_image_1 = visual.ImageStim(
    win=win,
    name='key_image_1', 
    image='key_1.png', mask=None,
    ori=0.0, pos=(-0.45, 0.05), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-6.0)
key_image_2 = visual.ImageStim(
    win=win,
    name='key_image_2', 
    image='key_2.png', mask=None,
    ori=0.0, pos=(-0.15, 0.05), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-7.0)
key_image_3 = visual.ImageStim(
    win=win,
    name='key_image_3', 
    image='key_3.png', mask=None,
    ori=0.0, pos=(0.15, 0.05), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-8.0)
key_image_enter = visual.ImageStim(
    win=win,
    name='key_image_enter', 
    image='key_enter.png', mask=None,
    ori=0.0, pos=(0.45, 0.05), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-9.0)

# Initialize components for Routine "Difficulty"
DifficultyClock = core.Clock()
difficulty = visual.TextStim(win=win, name='difficulty',
    text='How difficult was it for you to understand the code snippet and calculate the final value in R?',
    font='Open Sans',
    pos=(0, 0.2), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
key_resp_2 = keyboard.Keyboard()
answers_2 = visual.Slider(win=win, name='answers_2',
    startValue=None, size=(0.9, 0.02), pos=(0, 0), units=None,
    labels=["easy", "hard", "I'm not \nsure"], ticks=(1, 2, 4), granularity=1.0,
    style='radio', styleTweaks=(), opacity=None,
    color='LightGray', fillColor='Red', borderColor='0.3255, 0.3255, 0.3255', colorSpace='rgb',
    font='Open Sans', labelHeight=0.05,
    flip=False, depth=-2, readOnly=False)
key_image_1_2 = visual.ImageStim(
    win=win,
    name='key_image_1_2', 
    image='key_1.png', mask=None,
    ori=0.0, pos=(-0.45, 0.05), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-4.0)
key_image_2_2 = visual.ImageStim(
    win=win,
    name='key_image_2_2', 
    image='key_2.png', mask=None,
    ori=0.0, pos=(-0.15, 0.05), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-5.0)
key_image_enter_2 = visual.ImageStim(
    win=win,
    name='key_image_enter_2', 
    image='key_enter.png', mask=None,
    ori=0.0, pos=(0.45, 0.05), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-6.0)

# Initialize components for Routine "Pause"
PauseClock = core.Clock()
text = visual.TextStim(win=win, name='text',
    text='',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
key_resp_3 = keyboard.Keyboard()

# Initialize components for Routine "Long_Pause"
Long_PauseClock = core.Clock()
text_4 = visual.TextStim(win=win, name='text_4',
    text='Long break\nNow you can have a longer break.\nYou can move your arms and legs and have a drink or snack.\nPlease ring the bell and let us know.',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
key_resp_10 = keyboard.Keyboard()
key_resp_14 = keyboard.Keyboard()
pause_start = parallel.ParallelPort(address='0x0378')
pause_ende = parallel.ParallelPort(address='0x0378')

# Initialize components for Routine "End_Study"
End_StudyClock = core.Clock()
End_text = visual.TextStim(win=win, name='End_text',
    text='Now the experiment is finished. Please notify the experimental manager that you have finished the study. Thank you for your participation!',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
key_resp_16 = keyboard.Keyboard()
force_skip_6 = keyboard.Keyboard()

# Initialize components for Routine "EEG_End"
EEG_EndClock = core.Clock()
text_8 = visual.TextStim(win=win, name='text_8',
    text="Please end the EEG recording now if it hasn't ended already.",
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
end_eeg = parallel.ParallelPort(address='0x0378')
force_skip_7 = keyboard.Keyboard()

# Initialize components for Routine "photo"
photoClock = core.Clock()
text_2 = visual.TextStim(win=win, name='text_2',
    text='Photo',
    font='Open Sans',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
force_skip_8 = keyboard.Keyboard()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# set up handler to look after randomisation of conditions etc
IntroLoop = data.TrialHandler(nReps=0 if (expInfo['skipIntro']) else 1, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='IntroLoop')
thisExp.addLoop(IntroLoop)  # add the loop to the experiment
thisIntroLoop = IntroLoop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisIntroLoop.rgb)
if thisIntroLoop != None:
    for paramName in thisIntroLoop:
        exec('{} = thisIntroLoop[paramName]'.format(paramName))

for thisIntroLoop in IntroLoop:
    currentLoop = IntroLoop
    # abbreviate parameter names if possible (e.g. rgb = thisIntroLoop.rgb)
    if thisIntroLoop != None:
        for paramName in thisIntroLoop:
            exec('{} = thisIntroLoop[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "IntroText"-------
    continueRoutine = True
    # update component parameters for each repeat
    key_resp_17.keys = []
    key_resp_17.rt = []
    _key_resp_17_allKeys = []
    # keep track of which components have finished
    IntroTextComponents = [Intro_text, key_resp_17, comments]
    for thisComponent in IntroTextComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    IntroTextClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "IntroText"-------
    while continueRoutine:
        # get current time
        t = IntroTextClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=IntroTextClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *Intro_text* updates
        if Intro_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Intro_text.frameNStart = frameN  # exact frame index
            Intro_text.tStart = t  # local t and not account for scr refresh
            Intro_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Intro_text, 'tStartRefresh')  # time at next scr refresh
            Intro_text.setAutoDraw(True)
        
        # *key_resp_17* updates
        waitOnFlip = False
        if key_resp_17.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_17.frameNStart = frameN  # exact frame index
            key_resp_17.tStart = t  # local t and not account for scr refresh
            key_resp_17.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_17, 'tStartRefresh')  # time at next scr refresh
            key_resp_17.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_17.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_17.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_17.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_17.getKeys(keyList=['return'], waitRelease=False)
            _key_resp_17_allKeys.extend(theseKeys)
            if len(_key_resp_17_allKeys):
                key_resp_17.keys = _key_resp_17_allKeys[-1].name  # just the last key pressed
                key_resp_17.rt = _key_resp_17_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # *comments* updates
        if comments.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            comments.frameNStart = frameN  # exact frame index
            comments.tStart = t  # local t and not account for scr refresh
            comments.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(comments, 'tStartRefresh')  # time at next scr refresh
            comments.setAutoDraw(True)
        if comments.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > comments.tStartRefresh + 0.0-frameTolerance:
                # keep track of stop time/frame for later
                comments.tStop = t  # not accounting for scr refresh
                comments.frameNStop = frameN  # exact frame index
                win.timeOnFlip(comments, 'tStopRefresh')  # time at next scr refresh
                comments.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in IntroTextComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "IntroText"-------
    for thisComponent in IntroTextComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    IntroLoop.addData('Intro_text.started', Intro_text.tStartRefresh)
    IntroLoop.addData('Intro_text.stopped', Intro_text.tStopRefresh)
    # check responses
    if key_resp_17.keys in ['', [], None]:  # No response was made
        key_resp_17.keys = None
    IntroLoop.addData('key_resp_17.keys',key_resp_17.keys)
    if key_resp_17.keys != None:  # we had a response
        IntroLoop.addData('key_resp_17.rt', key_resp_17.rt)
    IntroLoop.addData('key_resp_17.started', key_resp_17.tStartRefresh)
    IntroLoop.addData('key_resp_17.stopped', key_resp_17.tStopRefresh)
    IntroLoop.addData('comments.started', comments.tStartRefresh)
    IntroLoop.addData('comments.stopped', comments.tStopRefresh)
    # the Routine "IntroText" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    Presentations = data.TrialHandler(nReps=1.0, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions('StudyIntroduction.xlsx'),
        seed=None, name='Presentations')
    thisExp.addLoop(Presentations)  # add the loop to the experiment
    thisPresentation = Presentations.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisPresentation.rgb)
    if thisPresentation != None:
        for paramName in thisPresentation:
            exec('{} = thisPresentation[paramName]'.format(paramName))
    
    for thisPresentation in Presentations:
        currentLoop = Presentations
        # abbreviate parameter names if possible (e.g. rgb = thisPresentation.rgb)
        if thisPresentation != None:
            for paramName in thisPresentation:
                exec('{} = thisPresentation[paramName]'.format(paramName))
        
        # ------Prepare to start Routine "Presentation"-------
        continueRoutine = True
        # update component parameters for each repeat
        force_skip_movie.keys = []
        force_skip_movie.rt = []
        _force_skip_movie_allKeys = []
        image_2.setImage("Study Intro Snapshots/"+ Image + ".png")
        key_resp_4.keys = []
        key_resp_4.rt = []
        _key_resp_4_allKeys = []
        # keep track of which components have finished
        PresentationComponents = [force_skip_movie, image_2, key_resp_4]
        for thisComponent in PresentationComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        PresentationClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "Presentation"-------
        while continueRoutine:
            # get current time
            t = PresentationClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=PresentationClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *force_skip_movie* updates
            waitOnFlip = False
            if force_skip_movie.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                force_skip_movie.frameNStart = frameN  # exact frame index
                force_skip_movie.tStart = t  # local t and not account for scr refresh
                force_skip_movie.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(force_skip_movie, 'tStartRefresh')  # time at next scr refresh
                force_skip_movie.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(force_skip_movie.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(force_skip_movie.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if force_skip_movie.status == STARTED and not waitOnFlip:
                theseKeys = force_skip_movie.getKeys(keyList=['q'], waitRelease=False)
                _force_skip_movie_allKeys.extend(theseKeys)
                if len(_force_skip_movie_allKeys):
                    force_skip_movie.keys = _force_skip_movie_allKeys[-1].name  # just the last key pressed
                    force_skip_movie.rt = _force_skip_movie_allKeys[-1].rt
                    # a response ends the routine
                    continueRoutine = False
            
            # *image_2* updates
            if image_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                image_2.frameNStart = frameN  # exact frame index
                image_2.tStart = t  # local t and not account for scr refresh
                image_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(image_2, 'tStartRefresh')  # time at next scr refresh
                image_2.setAutoDraw(True)
            
            # *key_resp_4* updates
            waitOnFlip = False
            if key_resp_4.status == NOT_STARTED and tThisFlip >= min_duration-frameTolerance:
                # keep track of start time/frame for later
                key_resp_4.frameNStart = frameN  # exact frame index
                key_resp_4.tStart = t  # local t and not account for scr refresh
                key_resp_4.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp_4, 'tStartRefresh')  # time at next scr refresh
                key_resp_4.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_resp_4.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_resp_4.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if key_resp_4.status == STARTED and not waitOnFlip:
                theseKeys = key_resp_4.getKeys(keyList=['return'], waitRelease=False)
                _key_resp_4_allKeys.extend(theseKeys)
                if len(_key_resp_4_allKeys):
                    key_resp_4.keys = _key_resp_4_allKeys[-1].name  # just the last key pressed
                    key_resp_4.rt = _key_resp_4_allKeys[-1].rt
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in PresentationComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "Presentation"-------
        for thisComponent in PresentationComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # check responses
        if force_skip_movie.keys in ['', [], None]:  # No response was made
            force_skip_movie.keys = None
        Presentations.addData('force_skip_movie.keys',force_skip_movie.keys)
        if force_skip_movie.keys != None:  # we had a response
            Presentations.addData('force_skip_movie.rt', force_skip_movie.rt)
        Presentations.addData('force_skip_movie.started', force_skip_movie.tStartRefresh)
        Presentations.addData('force_skip_movie.stopped', force_skip_movie.tStopRefresh)
        Presentations.addData('image_2.started', image_2.tStartRefresh)
        Presentations.addData('image_2.stopped', image_2.tStopRefresh)
        # check responses
        if key_resp_4.keys in ['', [], None]:  # No response was made
            key_resp_4.keys = None
        Presentations.addData('key_resp_4.keys',key_resp_4.keys)
        if key_resp_4.keys != None:  # we had a response
            Presentations.addData('key_resp_4.rt', key_resp_4.rt)
        Presentations.addData('key_resp_4.started', key_resp_4.tStartRefresh)
        Presentations.addData('key_resp_4.stopped', key_resp_4.tStopRefresh)
        # the Routine "Presentation" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
    # completed 1.0 repeats of 'Presentations'
    
    
    # ------Prepare to start Routine "Example_Begin"-------
    continueRoutine = True
    routineTimer.add(20.000000)
    # update component parameters for each repeat
    force_skip_5.keys = []
    force_skip_5.rt = []
    _force_skip_5_allKeys = []
    # keep track of which components have finished
    Example_BeginComponents = [Example_text, text_5, force_skip_5]
    for thisComponent in Example_BeginComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    Example_BeginClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Example_Begin"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = Example_BeginClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Example_BeginClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *Example_text* updates
        if Example_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Example_text.frameNStart = frameN  # exact frame index
            Example_text.tStart = t  # local t and not account for scr refresh
            Example_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Example_text, 'tStartRefresh')  # time at next scr refresh
            Example_text.setAutoDraw(True)
        if Example_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > Example_text.tStartRefresh + 10-frameTolerance:
                # keep track of stop time/frame for later
                Example_text.tStop = t  # not accounting for scr refresh
                Example_text.frameNStop = frameN  # exact frame index
                win.timeOnFlip(Example_text, 'tStopRefresh')  # time at next scr refresh
                Example_text.setAutoDraw(False)
        
        # *text_5* updates
        if text_5.status == NOT_STARTED and tThisFlip >= 10-frameTolerance:
            # keep track of start time/frame for later
            text_5.frameNStart = frameN  # exact frame index
            text_5.tStart = t  # local t and not account for scr refresh
            text_5.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_5, 'tStartRefresh')  # time at next scr refresh
            text_5.setAutoDraw(True)
        if text_5.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > text_5.tStartRefresh + 10-frameTolerance:
                # keep track of stop time/frame for later
                text_5.tStop = t  # not accounting for scr refresh
                text_5.frameNStop = frameN  # exact frame index
                win.timeOnFlip(text_5, 'tStopRefresh')  # time at next scr refresh
                text_5.setAutoDraw(False)
        
        # *force_skip_5* updates
        waitOnFlip = False
        if force_skip_5.status == NOT_STARTED and tThisFlip >= 0.1-frameTolerance:
            # keep track of start time/frame for later
            force_skip_5.frameNStart = frameN  # exact frame index
            force_skip_5.tStart = t  # local t and not account for scr refresh
            force_skip_5.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(force_skip_5, 'tStartRefresh')  # time at next scr refresh
            force_skip_5.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(force_skip_5.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(force_skip_5.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if force_skip_5.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > force_skip_5.tStartRefresh + 19.9-frameTolerance:
                # keep track of stop time/frame for later
                force_skip_5.tStop = t  # not accounting for scr refresh
                force_skip_5.frameNStop = frameN  # exact frame index
                win.timeOnFlip(force_skip_5, 'tStopRefresh')  # time at next scr refresh
                force_skip_5.status = FINISHED
        if force_skip_5.status == STARTED and not waitOnFlip:
            theseKeys = force_skip_5.getKeys(keyList=['q'], waitRelease=False)
            _force_skip_5_allKeys.extend(theseKeys)
            if len(_force_skip_5_allKeys):
                force_skip_5.keys = _force_skip_5_allKeys[-1].name  # just the last key pressed
                force_skip_5.rt = _force_skip_5_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Example_BeginComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Example_Begin"-------
    for thisComponent in Example_BeginComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    IntroLoop.addData('Example_text.started', Example_text.tStartRefresh)
    IntroLoop.addData('Example_text.stopped', Example_text.tStopRefresh)
    IntroLoop.addData('text_5.started', text_5.tStartRefresh)
    IntroLoop.addData('text_5.stopped', text_5.tStopRefresh)
    # check responses
    if force_skip_5.keys in ['', [], None]:  # No response was made
        force_skip_5.keys = None
    IntroLoop.addData('force_skip_5.keys',force_skip_5.keys)
    if force_skip_5.keys != None:  # we had a response
        IntroLoop.addData('force_skip_5.rt', force_skip_5.rt)
    IntroLoop.addData('force_skip_5.started', force_skip_5.tStartRefresh)
    IntroLoop.addData('force_skip_5.stopped', force_skip_5.tStopRefresh)
    
    # ------Prepare to start Routine "Example_Snippet"-------
    continueRoutine = True
    routineTimer.add(50.000000)
    # update component parameters for each repeat
    image_5.setImage('images/example/25-clean.png')
    skip_4.keys = []
    skip_4.rt = []
    _skip_4_allKeys = []
    force_skip_4.keys = []
    force_skip_4.rt = []
    _force_skip_4_allKeys = []
    # keep track of which components have finished
    Example_SnippetComponents = [Background_4, etRecord_4, image_5, skip_4, force_skip_4, Snippet_text, circle_1, fixation_cross_10, fixation_cross_9, small_circle_2]
    for thisComponent in Example_SnippetComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    Example_SnippetClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Example_Snippet"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = Example_SnippetClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Example_SnippetClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *Background_4* updates
        if Background_4.status == NOT_STARTED and tThisFlip >= 20-frameTolerance:
            # keep track of start time/frame for later
            Background_4.frameNStart = frameN  # exact frame index
            Background_4.tStart = t  # local t and not account for scr refresh
            Background_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Background_4, 'tStartRefresh')  # time at next scr refresh
            Background_4.setAutoDraw(True)
        if Background_4.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > Background_4.tStartRefresh + 30.0-frameTolerance:
                # keep track of stop time/frame for later
                Background_4.tStop = t  # not accounting for scr refresh
                Background_4.frameNStop = frameN  # exact frame index
                win.timeOnFlip(Background_4, 'tStopRefresh')  # time at next scr refresh
                Background_4.setAutoDraw(False)
        # *etRecord_4* updates
        if etRecord_4.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            etRecord_4.frameNStart = frameN  # exact frame index
            etRecord_4.tStart = t  # local t and not account for scr refresh
            etRecord_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(etRecord_4, 'tStartRefresh')  # time at next scr refresh
            etRecord_4.status = STARTED
        if etRecord_4.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > etRecord_4.tStartRefresh + 50-frameTolerance:
                # keep track of stop time/frame for later
                etRecord_4.tStop = t  # not accounting for scr refresh
                etRecord_4.frameNStop = frameN  # exact frame index
                win.timeOnFlip(etRecord_4, 'tStopRefresh')  # time at next scr refresh
                etRecord_4.status = FINISHED
        
        # *image_5* updates
        if image_5.status == NOT_STARTED and tThisFlip >= 20-frameTolerance:
            # keep track of start time/frame for later
            image_5.frameNStart = frameN  # exact frame index
            image_5.tStart = t  # local t and not account for scr refresh
            image_5.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(image_5, 'tStartRefresh')  # time at next scr refresh
            image_5.setAutoDraw(True)
        if image_5.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > image_5.tStartRefresh + 30-frameTolerance:
                # keep track of stop time/frame for later
                image_5.tStop = t  # not accounting for scr refresh
                image_5.frameNStop = frameN  # exact frame index
                win.timeOnFlip(image_5, 'tStopRefresh')  # time at next scr refresh
                image_5.setAutoDraw(False)
        
        # *skip_4* updates
        waitOnFlip = False
        if skip_4.status == NOT_STARTED and tThisFlip >= 23-frameTolerance:
            # keep track of start time/frame for later
            skip_4.frameNStart = frameN  # exact frame index
            skip_4.tStart = t  # local t and not account for scr refresh
            skip_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(skip_4, 'tStartRefresh')  # time at next scr refresh
            skip_4.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(skip_4.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(skip_4.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if skip_4.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > skip_4.tStartRefresh + 27-frameTolerance:
                # keep track of stop time/frame for later
                skip_4.tStop = t  # not accounting for scr refresh
                skip_4.frameNStop = frameN  # exact frame index
                win.timeOnFlip(skip_4, 'tStopRefresh')  # time at next scr refresh
                skip_4.status = FINISHED
        if skip_4.status == STARTED and not waitOnFlip:
            theseKeys = skip_4.getKeys(keyList=['return'], waitRelease=False)
            _skip_4_allKeys.extend(theseKeys)
            if len(_skip_4_allKeys):
                skip_4.keys = _skip_4_allKeys[-1].name  # just the last key pressed
                skip_4.rt = _skip_4_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # *force_skip_4* updates
        waitOnFlip = False
        if force_skip_4.status == NOT_STARTED and tThisFlip >= 0.1-frameTolerance:
            # keep track of start time/frame for later
            force_skip_4.frameNStart = frameN  # exact frame index
            force_skip_4.tStart = t  # local t and not account for scr refresh
            force_skip_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(force_skip_4, 'tStartRefresh')  # time at next scr refresh
            force_skip_4.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(force_skip_4.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(force_skip_4.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if force_skip_4.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > force_skip_4.tStartRefresh + 49.9-frameTolerance:
                # keep track of stop time/frame for later
                force_skip_4.tStop = t  # not accounting for scr refresh
                force_skip_4.frameNStop = frameN  # exact frame index
                win.timeOnFlip(force_skip_4, 'tStopRefresh')  # time at next scr refresh
                force_skip_4.status = FINISHED
        if force_skip_4.status == STARTED and not waitOnFlip:
            theseKeys = force_skip_4.getKeys(keyList=['q'], waitRelease=False)
            _force_skip_4_allKeys.extend(theseKeys)
            if len(_force_skip_4_allKeys):
                force_skip_4.keys = _force_skip_4_allKeys[-1].name  # just the last key pressed
                force_skip_4.rt = _force_skip_4_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # *Snippet_text* updates
        if Snippet_text.status == NOT_STARTED and tThisFlip >= 5-frameTolerance:
            # keep track of start time/frame for later
            Snippet_text.frameNStart = frameN  # exact frame index
            Snippet_text.tStart = t  # local t and not account for scr refresh
            Snippet_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Snippet_text, 'tStartRefresh')  # time at next scr refresh
            Snippet_text.setAutoDraw(True)
        if Snippet_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > Snippet_text.tStartRefresh + 15-frameTolerance:
                # keep track of stop time/frame for later
                Snippet_text.tStop = t  # not accounting for scr refresh
                Snippet_text.frameNStop = frameN  # exact frame index
                win.timeOnFlip(Snippet_text, 'tStopRefresh')  # time at next scr refresh
                Snippet_text.setAutoDraw(False)
        
        # *circle_1* updates
        if circle_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            circle_1.frameNStart = frameN  # exact frame index
            circle_1.tStart = t  # local t and not account for scr refresh
            circle_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(circle_1, 'tStartRefresh')  # time at next scr refresh
            circle_1.setAutoDraw(True)
        if circle_1.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > circle_1.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                circle_1.tStop = t  # not accounting for scr refresh
                circle_1.frameNStop = frameN  # exact frame index
                win.timeOnFlip(circle_1, 'tStopRefresh')  # time at next scr refresh
                circle_1.setAutoDraw(False)
        
        # *fixation_cross_10* updates
        if fixation_cross_10.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            fixation_cross_10.frameNStart = frameN  # exact frame index
            fixation_cross_10.tStart = t  # local t and not account for scr refresh
            fixation_cross_10.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fixation_cross_10, 'tStartRefresh')  # time at next scr refresh
            fixation_cross_10.setAutoDraw(True)
        if fixation_cross_10.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > fixation_cross_10.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                fixation_cross_10.tStop = t  # not accounting for scr refresh
                fixation_cross_10.frameNStop = frameN  # exact frame index
                win.timeOnFlip(fixation_cross_10, 'tStopRefresh')  # time at next scr refresh
                fixation_cross_10.setAutoDraw(False)
        
        # *fixation_cross_9* updates
        if fixation_cross_9.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            fixation_cross_9.frameNStart = frameN  # exact frame index
            fixation_cross_9.tStart = t  # local t and not account for scr refresh
            fixation_cross_9.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fixation_cross_9, 'tStartRefresh')  # time at next scr refresh
            fixation_cross_9.setAutoDraw(True)
        if fixation_cross_9.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > fixation_cross_9.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                fixation_cross_9.tStop = t  # not accounting for scr refresh
                fixation_cross_9.frameNStop = frameN  # exact frame index
                win.timeOnFlip(fixation_cross_9, 'tStopRefresh')  # time at next scr refresh
                fixation_cross_9.setAutoDraw(False)
        
        # *small_circle_2* updates
        if small_circle_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            small_circle_2.frameNStart = frameN  # exact frame index
            small_circle_2.tStart = t  # local t and not account for scr refresh
            small_circle_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(small_circle_2, 'tStartRefresh')  # time at next scr refresh
            small_circle_2.setAutoDraw(True)
        if small_circle_2.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > small_circle_2.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                small_circle_2.tStop = t  # not accounting for scr refresh
                small_circle_2.frameNStop = frameN  # exact frame index
                win.timeOnFlip(small_circle_2, 'tStopRefresh')  # time at next scr refresh
                small_circle_2.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Example_SnippetComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Example_Snippet"-------
    for thisComponent in Example_SnippetComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    IntroLoop.addData('Background_4.started', Background_4.tStartRefresh)
    IntroLoop.addData('Background_4.stopped', Background_4.tStopRefresh)
    # make sure the eyetracker recording stops
    if etRecord_4.status != FINISHED:
        etRecord_4.status = FINISHED
    IntroLoop.addData('image_5.started', image_5.tStartRefresh)
    IntroLoop.addData('image_5.stopped', image_5.tStopRefresh)
    # check responses
    if skip_4.keys in ['', [], None]:  # No response was made
        skip_4.keys = None
    IntroLoop.addData('skip_4.keys',skip_4.keys)
    if skip_4.keys != None:  # we had a response
        IntroLoop.addData('skip_4.rt', skip_4.rt)
    IntroLoop.addData('skip_4.started', skip_4.tStartRefresh)
    IntroLoop.addData('skip_4.stopped', skip_4.tStopRefresh)
    # check responses
    if force_skip_4.keys in ['', [], None]:  # No response was made
        force_skip_4.keys = None
    IntroLoop.addData('force_skip_4.keys',force_skip_4.keys)
    if force_skip_4.keys != None:  # we had a response
        IntroLoop.addData('force_skip_4.rt', force_skip_4.rt)
    IntroLoop.addData('force_skip_4.started', force_skip_4.tStartRefresh)
    IntroLoop.addData('force_skip_4.stopped', force_skip_4.tStopRefresh)
    IntroLoop.addData('Snippet_text.started', Snippet_text.tStartRefresh)
    IntroLoop.addData('Snippet_text.stopped', Snippet_text.tStopRefresh)
    IntroLoop.addData('circle_1.started', circle_1.tStartRefresh)
    IntroLoop.addData('circle_1.stopped', circle_1.tStopRefresh)
    IntroLoop.addData('fixation_cross_10.started', fixation_cross_10.tStartRefresh)
    IntroLoop.addData('fixation_cross_10.stopped', fixation_cross_10.tStopRefresh)
    IntroLoop.addData('fixation_cross_9.started', fixation_cross_9.tStartRefresh)
    IntroLoop.addData('fixation_cross_9.stopped', fixation_cross_9.tStopRefresh)
    IntroLoop.addData('small_circle_2.started', small_circle_2.tStartRefresh)
    IntroLoop.addData('small_circle_2.stopped', small_circle_2.tStopRefresh)
    
    # ------Prepare to start Routine "Example_Question"-------
    continueRoutine = True
    routineTimer.add(60.000000)
    # update component parameters for each repeat
    key_resp_12.keys = []
    key_resp_12.rt = []
    _key_resp_12_allKeys = []
    two_answers_4.reset()
    # keep track of which components have finished
    Example_QuestionComponents = [question_4, key_resp_12, two_answers_4, key_image, key_image_4, key_image_5, key_image_enter_3]
    for thisComponent in Example_QuestionComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    Example_QuestionClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Example_Question"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = Example_QuestionClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Example_QuestionClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *question_4* updates
        if question_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            question_4.frameNStart = frameN  # exact frame index
            question_4.tStart = t  # local t and not account for scr refresh
            question_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(question_4, 'tStartRefresh')  # time at next scr refresh
            question_4.setAutoDraw(True)
        if question_4.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > question_4.tStartRefresh + 60-frameTolerance:
                # keep track of stop time/frame for later
                question_4.tStop = t  # not accounting for scr refresh
                question_4.frameNStop = frameN  # exact frame index
                win.timeOnFlip(question_4, 'tStopRefresh')  # time at next scr refresh
                question_4.setAutoDraw(False)
        
        # *key_resp_12* updates
        waitOnFlip = False
        if key_resp_12.status == NOT_STARTED and tThisFlip >= 0.1-frameTolerance:
            # keep track of start time/frame for later
            key_resp_12.frameNStart = frameN  # exact frame index
            key_resp_12.tStart = t  # local t and not account for scr refresh
            key_resp_12.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_12, 'tStartRefresh')  # time at next scr refresh
            key_resp_12.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_12.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_12.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_12.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > key_resp_12.tStartRefresh + 59.9-frameTolerance:
                # keep track of stop time/frame for later
                key_resp_12.tStop = t  # not accounting for scr refresh
                key_resp_12.frameNStop = frameN  # exact frame index
                win.timeOnFlip(key_resp_12, 'tStopRefresh')  # time at next scr refresh
                key_resp_12.status = FINISHED
        if key_resp_12.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_12.getKeys(keyList=['end', 'down', 'return'], waitRelease=False)
            _key_resp_12_allKeys.extend(theseKeys)
            if len(_key_resp_12_allKeys):
                key_resp_12.keys = _key_resp_12_allKeys[-1].name  # just the last key pressed
                key_resp_12.rt = _key_resp_12_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # *two_answers_4* updates
        if two_answers_4.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            two_answers_4.frameNStart = frameN  # exact frame index
            two_answers_4.tStart = t  # local t and not account for scr refresh
            two_answers_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(two_answers_4, 'tStartRefresh')  # time at next scr refresh
            two_answers_4.setAutoDraw(True)
        if two_answers_4.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > two_answers_4.tStartRefresh + 60-frameTolerance:
                # keep track of stop time/frame for later
                two_answers_4.tStop = t  # not accounting for scr refresh
                two_answers_4.frameNStop = frameN  # exact frame index
                win.timeOnFlip(two_answers_4, 'tStopRefresh')  # time at next scr refresh
                two_answers_4.setAutoDraw(False)
        
        # *key_image* updates
        if key_image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_image.frameNStart = frameN  # exact frame index
            key_image.tStart = t  # local t and not account for scr refresh
            key_image.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_image, 'tStartRefresh')  # time at next scr refresh
            key_image.setAutoDraw(True)
        if key_image.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > key_image.tStartRefresh + 60-frameTolerance:
                # keep track of stop time/frame for later
                key_image.tStop = t  # not accounting for scr refresh
                key_image.frameNStop = frameN  # exact frame index
                win.timeOnFlip(key_image, 'tStopRefresh')  # time at next scr refresh
                key_image.setAutoDraw(False)
        
        # *key_image_4* updates
        if key_image_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_image_4.frameNStart = frameN  # exact frame index
            key_image_4.tStart = t  # local t and not account for scr refresh
            key_image_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_image_4, 'tStartRefresh')  # time at next scr refresh
            key_image_4.setAutoDraw(True)
        if key_image_4.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > key_image_4.tStartRefresh + 60-frameTolerance:
                # keep track of stop time/frame for later
                key_image_4.tStop = t  # not accounting for scr refresh
                key_image_4.frameNStop = frameN  # exact frame index
                win.timeOnFlip(key_image_4, 'tStopRefresh')  # time at next scr refresh
                key_image_4.setAutoDraw(False)
        
        # *key_image_5* updates
        if key_image_5.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_image_5.frameNStart = frameN  # exact frame index
            key_image_5.tStart = t  # local t and not account for scr refresh
            key_image_5.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_image_5, 'tStartRefresh')  # time at next scr refresh
            key_image_5.setAutoDraw(True)
        if key_image_5.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > key_image_5.tStartRefresh + 60-frameTolerance:
                # keep track of stop time/frame for later
                key_image_5.tStop = t  # not accounting for scr refresh
                key_image_5.frameNStop = frameN  # exact frame index
                win.timeOnFlip(key_image_5, 'tStopRefresh')  # time at next scr refresh
                key_image_5.setAutoDraw(False)
        
        # *key_image_enter_3* updates
        if key_image_enter_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_image_enter_3.frameNStart = frameN  # exact frame index
            key_image_enter_3.tStart = t  # local t and not account for scr refresh
            key_image_enter_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_image_enter_3, 'tStartRefresh')  # time at next scr refresh
            key_image_enter_3.setAutoDraw(True)
        if key_image_enter_3.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > key_image_enter_3.tStartRefresh + 60-frameTolerance:
                # keep track of stop time/frame for later
                key_image_enter_3.tStop = t  # not accounting for scr refresh
                key_image_enter_3.frameNStop = frameN  # exact frame index
                win.timeOnFlip(key_image_enter_3, 'tStopRefresh')  # time at next scr refresh
                key_image_enter_3.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Example_QuestionComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Example_Question"-------
    for thisComponent in Example_QuestionComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    IntroLoop.addData('question_4.started', question_4.tStartRefresh)
    IntroLoop.addData('question_4.stopped', question_4.tStopRefresh)
    # check responses
    if key_resp_12.keys in ['', [], None]:  # No response was made
        key_resp_12.keys = None
    IntroLoop.addData('key_resp_12.keys',key_resp_12.keys)
    if key_resp_12.keys != None:  # we had a response
        IntroLoop.addData('key_resp_12.rt', key_resp_12.rt)
    IntroLoop.addData('key_resp_12.started', key_resp_12.tStartRefresh)
    IntroLoop.addData('key_resp_12.stopped', key_resp_12.tStopRefresh)
    IntroLoop.addData('two_answers_4.response', two_answers_4.getRating())
    IntroLoop.addData('two_answers_4.rt', two_answers_4.getRT())
    IntroLoop.addData('two_answers_4.started', two_answers_4.tStartRefresh)
    IntroLoop.addData('two_answers_4.stopped', two_answers_4.tStopRefresh)
    IntroLoop.addData('key_image.started', key_image.tStartRefresh)
    IntroLoop.addData('key_image.stopped', key_image.tStopRefresh)
    IntroLoop.addData('key_image_4.started', key_image_4.tStartRefresh)
    IntroLoop.addData('key_image_4.stopped', key_image_4.tStopRefresh)
    IntroLoop.addData('key_image_5.started', key_image_5.tStartRefresh)
    IntroLoop.addData('key_image_5.stopped', key_image_5.tStopRefresh)
    IntroLoop.addData('key_image_enter_3.started', key_image_enter_3.tStartRefresh)
    IntroLoop.addData('key_image_enter_3.stopped', key_image_enter_3.tStopRefresh)
    
    # ------Prepare to start Routine "Example_Difficulty"-------
    continueRoutine = True
    routineTimer.add(60.000000)
    # update component parameters for each repeat
    key_resp_13.keys = []
    key_resp_13.rt = []
    _key_resp_13_allKeys = []
    answers_4.reset()
    # keep track of which components have finished
    Example_DifficultyComponents = [difficulty_4, key_resp_13, answers_4, key_image_1_3, key_image_2_3, key_image_enter_4]
    for thisComponent in Example_DifficultyComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    Example_DifficultyClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Example_Difficulty"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = Example_DifficultyClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Example_DifficultyClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *difficulty_4* updates
        if difficulty_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            difficulty_4.frameNStart = frameN  # exact frame index
            difficulty_4.tStart = t  # local t and not account for scr refresh
            difficulty_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(difficulty_4, 'tStartRefresh')  # time at next scr refresh
            difficulty_4.setAutoDraw(True)
        if difficulty_4.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > difficulty_4.tStartRefresh + 60-frameTolerance:
                # keep track of stop time/frame for later
                difficulty_4.tStop = t  # not accounting for scr refresh
                difficulty_4.frameNStop = frameN  # exact frame index
                win.timeOnFlip(difficulty_4, 'tStopRefresh')  # time at next scr refresh
                difficulty_4.setAutoDraw(False)
        
        # *key_resp_13* updates
        waitOnFlip = False
        if key_resp_13.status == NOT_STARTED and tThisFlip >= 0.1-frameTolerance:
            # keep track of start time/frame for later
            key_resp_13.frameNStart = frameN  # exact frame index
            key_resp_13.tStart = t  # local t and not account for scr refresh
            key_resp_13.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_13, 'tStartRefresh')  # time at next scr refresh
            key_resp_13.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_13.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_13.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_13.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > key_resp_13.tStartRefresh + 59.9-frameTolerance:
                # keep track of stop time/frame for later
                key_resp_13.tStop = t  # not accounting for scr refresh
                key_resp_13.frameNStop = frameN  # exact frame index
                win.timeOnFlip(key_resp_13, 'tStopRefresh')  # time at next scr refresh
                key_resp_13.status = FINISHED
        if key_resp_13.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_13.getKeys(keyList=['end', 'down', 'return'], waitRelease=False)
            _key_resp_13_allKeys.extend(theseKeys)
            if len(_key_resp_13_allKeys):
                key_resp_13.keys = _key_resp_13_allKeys[-1].name  # just the last key pressed
                key_resp_13.rt = _key_resp_13_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # *answers_4* updates
        if answers_4.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            answers_4.frameNStart = frameN  # exact frame index
            answers_4.tStart = t  # local t and not account for scr refresh
            answers_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(answers_4, 'tStartRefresh')  # time at next scr refresh
            answers_4.setAutoDraw(True)
        if answers_4.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > answers_4.tStartRefresh + 60-frameTolerance:
                # keep track of stop time/frame for later
                answers_4.tStop = t  # not accounting for scr refresh
                answers_4.frameNStop = frameN  # exact frame index
                win.timeOnFlip(answers_4, 'tStopRefresh')  # time at next scr refresh
                answers_4.setAutoDraw(False)
        
        # *key_image_1_3* updates
        if key_image_1_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_image_1_3.frameNStart = frameN  # exact frame index
            key_image_1_3.tStart = t  # local t and not account for scr refresh
            key_image_1_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_image_1_3, 'tStartRefresh')  # time at next scr refresh
            key_image_1_3.setAutoDraw(True)
        if key_image_1_3.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > key_image_1_3.tStartRefresh + 60-frameTolerance:
                # keep track of stop time/frame for later
                key_image_1_3.tStop = t  # not accounting for scr refresh
                key_image_1_3.frameNStop = frameN  # exact frame index
                win.timeOnFlip(key_image_1_3, 'tStopRefresh')  # time at next scr refresh
                key_image_1_3.setAutoDraw(False)
        
        # *key_image_2_3* updates
        if key_image_2_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_image_2_3.frameNStart = frameN  # exact frame index
            key_image_2_3.tStart = t  # local t and not account for scr refresh
            key_image_2_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_image_2_3, 'tStartRefresh')  # time at next scr refresh
            key_image_2_3.setAutoDraw(True)
        if key_image_2_3.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > key_image_2_3.tStartRefresh + 60-frameTolerance:
                # keep track of stop time/frame for later
                key_image_2_3.tStop = t  # not accounting for scr refresh
                key_image_2_3.frameNStop = frameN  # exact frame index
                win.timeOnFlip(key_image_2_3, 'tStopRefresh')  # time at next scr refresh
                key_image_2_3.setAutoDraw(False)
        
        # *key_image_enter_4* updates
        if key_image_enter_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_image_enter_4.frameNStart = frameN  # exact frame index
            key_image_enter_4.tStart = t  # local t and not account for scr refresh
            key_image_enter_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_image_enter_4, 'tStartRefresh')  # time at next scr refresh
            key_image_enter_4.setAutoDraw(True)
        if key_image_enter_4.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > key_image_enter_4.tStartRefresh + 60-frameTolerance:
                # keep track of stop time/frame for later
                key_image_enter_4.tStop = t  # not accounting for scr refresh
                key_image_enter_4.frameNStop = frameN  # exact frame index
                win.timeOnFlip(key_image_enter_4, 'tStopRefresh')  # time at next scr refresh
                key_image_enter_4.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Example_DifficultyComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Example_Difficulty"-------
    for thisComponent in Example_DifficultyComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    IntroLoop.addData('difficulty_4.started', difficulty_4.tStartRefresh)
    IntroLoop.addData('difficulty_4.stopped', difficulty_4.tStopRefresh)
    # check responses
    if key_resp_13.keys in ['', [], None]:  # No response was made
        key_resp_13.keys = None
    IntroLoop.addData('key_resp_13.keys',key_resp_13.keys)
    if key_resp_13.keys != None:  # we had a response
        IntroLoop.addData('key_resp_13.rt', key_resp_13.rt)
    IntroLoop.addData('key_resp_13.started', key_resp_13.tStartRefresh)
    IntroLoop.addData('key_resp_13.stopped', key_resp_13.tStopRefresh)
    IntroLoop.addData('answers_4.response', answers_4.getRating())
    IntroLoop.addData('answers_4.rt', answers_4.getRT())
    IntroLoop.addData('answers_4.started', answers_4.tStartRefresh)
    IntroLoop.addData('answers_4.stopped', answers_4.tStopRefresh)
    IntroLoop.addData('key_image_1_3.started', key_image_1_3.tStartRefresh)
    IntroLoop.addData('key_image_1_3.stopped', key_image_1_3.tStopRefresh)
    IntroLoop.addData('key_image_2_3.started', key_image_2_3.tStartRefresh)
    IntroLoop.addData('key_image_2_3.stopped', key_image_2_3.tStopRefresh)
    IntroLoop.addData('key_image_enter_4.started', key_image_enter_4.tStartRefresh)
    IntroLoop.addData('key_image_enter_4.stopped', key_image_enter_4.tStopRefresh)
    
    # ------Prepare to start Routine "start"-------
    continueRoutine = True
    # update component parameters for each repeat
    space_start.keys = []
    space_start.rt = []
    _space_start_allKeys = []
    # keep track of which components have finished
    startComponents = [start_experiment, space_start]
    for thisComponent in startComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    startClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "start"-------
    while continueRoutine:
        # get current time
        t = startClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=startClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *start_experiment* updates
        if start_experiment.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            start_experiment.frameNStart = frameN  # exact frame index
            start_experiment.tStart = t  # local t and not account for scr refresh
            start_experiment.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(start_experiment, 'tStartRefresh')  # time at next scr refresh
            start_experiment.setAutoDraw(True)
        
        # *space_start* updates
        waitOnFlip = False
        if space_start.status == NOT_STARTED and tThisFlip >= 0.1-frameTolerance:
            # keep track of start time/frame for later
            space_start.frameNStart = frameN  # exact frame index
            space_start.tStart = t  # local t and not account for scr refresh
            space_start.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(space_start, 'tStartRefresh')  # time at next scr refresh
            space_start.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(space_start.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(space_start.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if space_start.status == STARTED and not waitOnFlip:
            theseKeys = space_start.getKeys(keyList=['return'], waitRelease=False)
            _space_start_allKeys.extend(theseKeys)
            if len(_space_start_allKeys):
                space_start.keys = _space_start_allKeys[-1].name  # just the last key pressed
                space_start.rt = _space_start_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in startComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "start"-------
    for thisComponent in startComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    IntroLoop.addData('start_experiment.started', start_experiment.tStartRefresh)
    IntroLoop.addData('start_experiment.stopped', start_experiment.tStopRefresh)
    # check responses
    if space_start.keys in ['', [], None]:  # No response was made
        space_start.keys = None
    IntroLoop.addData('space_start.keys',space_start.keys)
    if space_start.keys != None:  # we had a response
        IntroLoop.addData('space_start.rt', space_start.rt)
    IntroLoop.addData('space_start.started', space_start.tStartRefresh)
    IntroLoop.addData('space_start.stopped', space_start.tStopRefresh)
    # the Routine "start" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
# completed 0 if (expInfo['skipIntro']) else 1 repeats of 'IntroLoop'


# ------Prepare to start Routine "EEG_Start"-------
continueRoutine = True
routineTimer.add(30.000000)
# update component parameters for each repeat
key_resp_15.keys = []
key_resp_15.rt = []
_key_resp_15_allKeys = []
# keep track of which components have finished
EEG_StartComponents = [text_7, key_resp_15]
for thisComponent in EEG_StartComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
EEG_StartClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "EEG_Start"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = EEG_StartClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=EEG_StartClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_7* updates
    if text_7.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text_7.frameNStart = frameN  # exact frame index
        text_7.tStart = t  # local t and not account for scr refresh
        text_7.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_7, 'tStartRefresh')  # time at next scr refresh
        text_7.setAutoDraw(True)
    if text_7.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > text_7.tStartRefresh + 30-frameTolerance:
            # keep track of stop time/frame for later
            text_7.tStop = t  # not accounting for scr refresh
            text_7.frameNStop = frameN  # exact frame index
            win.timeOnFlip(text_7, 'tStopRefresh')  # time at next scr refresh
            text_7.setAutoDraw(False)
    
    # *key_resp_15* updates
    waitOnFlip = False
    if key_resp_15.status == NOT_STARTED and tThisFlip >= 0.1-frameTolerance:
        # keep track of start time/frame for later
        key_resp_15.frameNStart = frameN  # exact frame index
        key_resp_15.tStart = t  # local t and not account for scr refresh
        key_resp_15.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp_15, 'tStartRefresh')  # time at next scr refresh
        key_resp_15.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp_15.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp_15.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp_15.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > key_resp_15.tStartRefresh + 29.9-frameTolerance:
            # keep track of stop time/frame for later
            key_resp_15.tStop = t  # not accounting for scr refresh
            key_resp_15.frameNStop = frameN  # exact frame index
            win.timeOnFlip(key_resp_15, 'tStopRefresh')  # time at next scr refresh
            key_resp_15.status = FINISHED
    if key_resp_15.status == STARTED and not waitOnFlip:
        theseKeys = key_resp_15.getKeys(keyList=['return'], waitRelease=False)
        _key_resp_15_allKeys.extend(theseKeys)
        if len(_key_resp_15_allKeys):
            key_resp_15.keys = _key_resp_15_allKeys[-1].name  # just the last key pressed
            key_resp_15.rt = _key_resp_15_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in EEG_StartComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "EEG_Start"-------
for thisComponent in EEG_StartComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('text_7.started', text_7.tStartRefresh)
thisExp.addData('text_7.stopped', text_7.tStopRefresh)
# check responses
if key_resp_15.keys in ['', [], None]:  # No response was made
    key_resp_15.keys = None
thisExp.addData('key_resp_15.keys',key_resp_15.keys)
if key_resp_15.keys != None:  # we had a response
    thisExp.addData('key_resp_15.rt', key_resp_15.rt)
thisExp.addData('key_resp_15.started', key_resp_15.tStartRefresh)
thisExp.addData('key_resp_15.stopped', key_resp_15.tStopRefresh)
thisExp.nextEntry()

# ------Prepare to start Routine "startEvent"-------
continueRoutine = True
routineTimer.add(0.100000)
# update component parameters for each repeat
# keep track of which components have finished
startEventComponents = [experiment_start_event]
for thisComponent in startEventComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
startEventClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "startEvent"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = startEventClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=startEventClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    # *experiment_start_event* updates
    if experiment_start_event.status == NOT_STARTED and t >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        experiment_start_event.frameNStart = frameN  # exact frame index
        experiment_start_event.tStart = t  # local t and not account for scr refresh
        experiment_start_event.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(experiment_start_event, 'tStartRefresh')  # time at next scr refresh
        experiment_start_event.status = STARTED
        win.callOnFlip(experiment_start_event.setData, int(1))
    if experiment_start_event.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > experiment_start_event.tStartRefresh + 0.1-frameTolerance:
            # keep track of stop time/frame for later
            experiment_start_event.tStop = t  # not accounting for scr refresh
            experiment_start_event.frameNStop = frameN  # exact frame index
            win.timeOnFlip(experiment_start_event, 'tStopRefresh')  # time at next scr refresh
            experiment_start_event.status = FINISHED
            win.callOnFlip(experiment_start_event.setData, int(0))
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in startEventComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "startEvent"-------
for thisComponent in startEventComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
if experiment_start_event.status == STARTED:
    win.callOnFlip(experiment_start_event.setData, int(0))
thisExp.addData('experiment_start_event.started', experiment_start_event.tStart)
thisExp.addData('experiment_start_event.stopped', experiment_start_event.tStop)

# set up handler to look after randomisation of conditions etc
rounds = data.TrialHandler(nReps=1.0, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('loopTemplate1.xlsx'),
    seed=None, name='rounds')
thisExp.addLoop(rounds)  # add the loop to the experiment
thisRound = rounds.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisRound.rgb)
if thisRound != None:
    for paramName in thisRound:
        exec('{} = thisRound[paramName]'.format(paramName))

for thisRound in rounds:
    currentLoop = rounds
    # abbreviate parameter names if possible (e.g. rgb = thisRound.rgb)
    if thisRound != None:
        for paramName in thisRound:
            exec('{} = thisRound[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "CheckPos"-------
    continueRoutine = True
    routineTimer.add(5.000000)
    # update component parameters for each repeat
    skip_iter = False
    snippet = 0
    if Round < int(expInfo['startRound']):
            continueRoutine = False
            skip_iter = True
    Round_marker.setText("Round " + str(Round))
    # keep track of which components have finished
    CheckPosComponents = [Round_marker]
    for thisComponent in CheckPosComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    CheckPosClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "CheckPos"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = CheckPosClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=CheckPosClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *Round_marker* updates
        if Round_marker.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Round_marker.frameNStart = frameN  # exact frame index
            Round_marker.tStart = t  # local t and not account for scr refresh
            Round_marker.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Round_marker, 'tStartRefresh')  # time at next scr refresh
            Round_marker.setAutoDraw(True)
        if Round_marker.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > Round_marker.tStartRefresh + 5.0-frameTolerance:
                # keep track of stop time/frame for later
                Round_marker.tStop = t  # not accounting for scr refresh
                Round_marker.frameNStop = frameN  # exact frame index
                win.timeOnFlip(Round_marker, 'tStopRefresh')  # time at next scr refresh
                Round_marker.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in CheckPosComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "CheckPos"-------
    for thisComponent in CheckPosComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    rounds.addData('Round_marker.started', Round_marker.tStartRefresh)
    rounds.addData('Round_marker.stopped', Round_marker.tStopRefresh)
    
    # set up handler to look after randomisation of conditions etc
    calibrationLoop = data.TrialHandler(nReps=0 if (skip_iter) else 1, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='calibrationLoop')
    thisExp.addLoop(calibrationLoop)  # add the loop to the experiment
    thisCalibrationLoop = calibrationLoop.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisCalibrationLoop.rgb)
    if thisCalibrationLoop != None:
        for paramName in thisCalibrationLoop:
            exec('{} = thisCalibrationLoop[paramName]'.format(paramName))
    
    for thisCalibrationLoop in calibrationLoop:
        currentLoop = calibrationLoop
        # abbreviate parameter names if possible (e.g. rgb = thisCalibrationLoop.rgb)
        if thisCalibrationLoop != None:
            for paramName in thisCalibrationLoop:
                exec('{} = thisCalibrationLoop[paramName]'.format(paramName))
        
        # -------Run Routine 'calibration'-------
        
        # define target for calibration
        calibrationTarget = visual.TargetStim(win, 
            name='calibrationTarget',
            radius=0.01, fillColor='', borderColor='black', lineWidth=2.0,
            innerRadius=0.0035, innerFillColor='green', innerBorderColor='black', innerLineWidth=2.0,
            colorSpace='rgb', units=None
        )
        # define parameters for calibration
        calibration = hardware.eyetracker.EyetrackerCalibration(win, 
            eyetracker, calibrationTarget,
            units=None, colorSpace='rgb',
            progressMode='time', targetDur=1.5, expandScale=1.5,
            targetLayout='NINE_POINTS', randomisePos=True,
            movementAnimation=True, targetDelay=1.0
        )
        # run calibration
        calibration.run()
        # clear any keypresses from during calibration so they don't interfere with the experiment
        defaultKeyboard.clearEvents()
        # the Routine "calibration" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # -------Run Routine 'validation'-------
        
        # define target for validation
        validationTarget = visual.TargetStim(win, 
            name='validationTarget',
            radius=0.01, fillColor='', borderColor='black', lineWidth=2.0,
            innerRadius=0.0035, innerFillColor='green', innerBorderColor='black', innerLineWidth=2.0,
            colorSpace='rgb', units=None
        )
        # define parameters for validation
        validation = iohub.ValidationProcedure(win,
            target=validationTarget,
            gaze_cursor='green', 
            positions='NINE_POINTS', randomize_positions=True,
            expand_scale=1.5, target_duration=1.5,
            enable_position_animation=True, target_delay=1.0,
            progress_on_key=None,
            show_results_screen=True, save_results_screen=False,
            color_space='rgb', unit_type=None
        )
        # run validation
        validation.run()
        # clear any keypresses from during validation so they don't interfere with the experiment
        defaultKeyboard.clearEvents()
        # the Routine "validation" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
    # completed 0 if (skip_iter) else 1 repeats of 'calibrationLoop'
    
    
    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler(nReps=0 if (skip_iter) else 1, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions("conditions/conditions_" + str(Round) + "_"+expInfo['participant'] +  ".xlsx"),
        seed=None, name='trials')
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            exec('{} = thisTrial[paramName]'.format(paramName))
    
    for thisTrial in trials:
        currentLoop = trials
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                exec('{} = thisTrial[paramName]'.format(paramName))
        
        # ------Prepare to start Routine "Snippet"-------
        continueRoutine = True
        # update component parameters for each repeat
        image.setImage("images/" + ImagePath)
        skip.keys = []
        skip.rt = []
        _skip_allKeys = []
        snippet = snippet + 1
        skipSnippet = False
        continueRoutine = True
        if ((snippet < int(expInfo['startLoopPos'])) and (Round == int(expInfo['startRound']))):
            skipSnippet = True
            continueRoutine = False
        current_time = datetime.now()
        start_of_stimuli = dt.timedelta(seconds=0)
        end_of_stimuli = dt.timedelta(seconds=0)
        current_stimuli = "fixation_cross"
        first_frame = True
        ioServer.sendMessageEvent("Fixation " + SnippetName, category = "FIXATION", sec_time = ioServer.getTime())
        force_skip.keys = []
        force_skip.rt = []
        _force_skip_allKeys = []
        # keep track of which components have finished
        SnippetComponents = [Background, etRecord, image, skip, snippet_start_event, force_skip, p_port_2, circle, fixation_cross_2, fixation_cross, small_circle]
        for thisComponent in SnippetComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        SnippetClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "Snippet"-------
        while continueRoutine:
            # get current time
            t = SnippetClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=SnippetClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Background* updates
            if Background.status == NOT_STARTED and tThisFlip >= 5.0-frameTolerance:
                # keep track of start time/frame for later
                Background.frameNStart = frameN  # exact frame index
                Background.tStart = t  # local t and not account for scr refresh
                Background.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Background, 'tStartRefresh')  # time at next scr refresh
                Background.setAutoDraw(True)
            if Background.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > Background.tStartRefresh + 30.0-frameTolerance:
                    # keep track of stop time/frame for later
                    Background.tStop = t  # not accounting for scr refresh
                    Background.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(Background, 'tStopRefresh')  # time at next scr refresh
                    Background.setAutoDraw(False)
            # *etRecord* updates
            if etRecord.status == NOT_STARTED and t >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                etRecord.frameNStart = frameN  # exact frame index
                etRecord.tStart = t  # local t and not account for scr refresh
                etRecord.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(etRecord, 'tStartRefresh')  # time at next scr refresh
                etRecord.status = STARTED
            if etRecord.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > etRecord.tStartRefresh + 35-frameTolerance:
                    # keep track of stop time/frame for later
                    etRecord.tStop = t  # not accounting for scr refresh
                    etRecord.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(etRecord, 'tStopRefresh')  # time at next scr refresh
                    etRecord.status = FINISHED
            
            # *image* updates
            if image.status == NOT_STARTED and tThisFlip >= 5.0-frameTolerance:
                # keep track of start time/frame for later
                image.frameNStart = frameN  # exact frame index
                image.tStart = t  # local t and not account for scr refresh
                image.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(image, 'tStartRefresh')  # time at next scr refresh
                image.setAutoDraw(True)
            if image.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > image.tStartRefresh + 30-frameTolerance:
                    # keep track of stop time/frame for later
                    image.tStop = t  # not accounting for scr refresh
                    image.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(image, 'tStopRefresh')  # time at next scr refresh
                    image.setAutoDraw(False)
            
            # *skip* updates
            waitOnFlip = False
            if skip.status == NOT_STARTED and tThisFlip >= 8.0-frameTolerance:
                # keep track of start time/frame for later
                skip.frameNStart = frameN  # exact frame index
                skip.tStart = t  # local t and not account for scr refresh
                skip.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(skip, 'tStartRefresh')  # time at next scr refresh
                skip.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(skip.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(skip.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if skip.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > skip.tStartRefresh + 27-frameTolerance:
                    # keep track of stop time/frame for later
                    skip.tStop = t  # not accounting for scr refresh
                    skip.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(skip, 'tStopRefresh')  # time at next scr refresh
                    skip.status = FINISHED
            if skip.status == STARTED and not waitOnFlip:
                theseKeys = skip.getKeys(keyList=['return'], waitRelease=False)
                _skip_allKeys.extend(theseKeys)
                if len(_skip_allKeys):
                    skip.keys = _skip_allKeys[-1].name  # just the last key pressed
                    skip.rt = _skip_allKeys[-1].rt
                    # a response ends the routine
                    continueRoutine = False
            # *snippet_start_event* updates
            if snippet_start_event.status == NOT_STARTED and image.status == STARTED:
                # keep track of start time/frame for later
                snippet_start_event.frameNStart = frameN  # exact frame index
                snippet_start_event.tStart = t  # local t and not account for scr refresh
                snippet_start_event.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(snippet_start_event, 'tStartRefresh')  # time at next scr refresh
                snippet_start_event.status = STARTED
                win.callOnFlip(snippet_start_event.setData, int(start_event))
            if snippet_start_event.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > snippet_start_event.tStartRefresh + 0.1-frameTolerance:
                    # keep track of stop time/frame for later
                    snippet_start_event.tStop = t  # not accounting for scr refresh
                    snippet_start_event.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(snippet_start_event, 'tStopRefresh')  # time at next scr refresh
                    snippet_start_event.status = FINISHED
                    win.callOnFlip(snippet_start_event.setData, int(0))
            if (first_frame and image.status == STARTED):
                ioServer.sendMessageEvent("Start Snippet " + SnippetName, category = "SNIPPETVIEW", sec_time = ioServer.getTime())
                first_frame = False
            current_time = datetime.now()
            since_start = current_time - start_time
            if image.status == STARTED and start_of_stimuli == dt.timedelta(seconds=0):
                start_of_stimuli = since_start
                current_stimuli = SnippetName
            
            sample_data = etRecord.tracker.getLastSample()
            
            left_pupil_diameter = 0
            right_pupil_diameter = 0
            
            #if sample_data is not None:
            #    left_pupil_diameter = sample_data[21]
            #    right_pupil_diameter = sample_data[40]
            
            df_et.loc[len(df_et)] = [since_start, etRecord.pos, left_pupil_diameter, right_pupil_diameter, current_stimuli]
            
            # *force_skip* updates
            waitOnFlip = False
            if force_skip.status == NOT_STARTED and tThisFlip >= 0.1-frameTolerance:
                # keep track of start time/frame for later
                force_skip.frameNStart = frameN  # exact frame index
                force_skip.tStart = t  # local t and not account for scr refresh
                force_skip.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(force_skip, 'tStartRefresh')  # time at next scr refresh
                force_skip.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(force_skip.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(force_skip.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if force_skip.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > force_skip.tStartRefresh + 34.9-frameTolerance:
                    # keep track of stop time/frame for later
                    force_skip.tStop = t  # not accounting for scr refresh
                    force_skip.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(force_skip, 'tStopRefresh')  # time at next scr refresh
                    force_skip.status = FINISHED
            if force_skip.status == STARTED and not waitOnFlip:
                theseKeys = force_skip.getKeys(keyList=['q'], waitRelease=False)
                _force_skip_allKeys.extend(theseKeys)
                if len(_force_skip_allKeys):
                    force_skip.keys = _force_skip_allKeys[-1].name  # just the last key pressed
                    force_skip.rt = _force_skip_allKeys[-1].rt
                    # a response ends the routine
                    continueRoutine = False
            # *p_port_2* updates
            if p_port_2.status == NOT_STARTED and t >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                p_port_2.frameNStart = frameN  # exact frame index
                p_port_2.tStart = t  # local t and not account for scr refresh
                p_port_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(p_port_2, 'tStartRefresh')  # time at next scr refresh
                p_port_2.status = STARTED
                win.callOnFlip(p_port_2.setData, int(3))
            if p_port_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > p_port_2.tStartRefresh + 0.1-frameTolerance:
                    # keep track of stop time/frame for later
                    p_port_2.tStop = t  # not accounting for scr refresh
                    p_port_2.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(p_port_2, 'tStopRefresh')  # time at next scr refresh
                    p_port_2.status = FINISHED
                    win.callOnFlip(p_port_2.setData, int(0))
            
            # *circle* updates
            if circle.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                circle.frameNStart = frameN  # exact frame index
                circle.tStart = t  # local t and not account for scr refresh
                circle.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(circle, 'tStartRefresh')  # time at next scr refresh
                circle.setAutoDraw(True)
            if circle.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > circle.tStartRefresh + 5-frameTolerance:
                    # keep track of stop time/frame for later
                    circle.tStop = t  # not accounting for scr refresh
                    circle.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(circle, 'tStopRefresh')  # time at next scr refresh
                    circle.setAutoDraw(False)
            
            # *fixation_cross_2* updates
            if fixation_cross_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fixation_cross_2.frameNStart = frameN  # exact frame index
                fixation_cross_2.tStart = t  # local t and not account for scr refresh
                fixation_cross_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation_cross_2, 'tStartRefresh')  # time at next scr refresh
                fixation_cross_2.setAutoDraw(True)
            if fixation_cross_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fixation_cross_2.tStartRefresh + 5-frameTolerance:
                    # keep track of stop time/frame for later
                    fixation_cross_2.tStop = t  # not accounting for scr refresh
                    fixation_cross_2.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(fixation_cross_2, 'tStopRefresh')  # time at next scr refresh
                    fixation_cross_2.setAutoDraw(False)
            
            # *fixation_cross* updates
            if fixation_cross.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fixation_cross.frameNStart = frameN  # exact frame index
                fixation_cross.tStart = t  # local t and not account for scr refresh
                fixation_cross.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation_cross, 'tStartRefresh')  # time at next scr refresh
                fixation_cross.setAutoDraw(True)
            if fixation_cross.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fixation_cross.tStartRefresh + 5-frameTolerance:
                    # keep track of stop time/frame for later
                    fixation_cross.tStop = t  # not accounting for scr refresh
                    fixation_cross.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(fixation_cross, 'tStopRefresh')  # time at next scr refresh
                    fixation_cross.setAutoDraw(False)
            
            # *small_circle* updates
            if small_circle.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                small_circle.frameNStart = frameN  # exact frame index
                small_circle.tStart = t  # local t and not account for scr refresh
                small_circle.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(small_circle, 'tStartRefresh')  # time at next scr refresh
                small_circle.setAutoDraw(True)
            if small_circle.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > small_circle.tStartRefresh + 5-frameTolerance:
                    # keep track of stop time/frame for later
                    small_circle.tStop = t  # not accounting for scr refresh
                    small_circle.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(small_circle, 'tStopRefresh')  # time at next scr refresh
                    small_circle.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in SnippetComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "Snippet"-------
        for thisComponent in SnippetComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        trials.addData('Background.started', Background.tStartRefresh)
        trials.addData('Background.stopped', Background.tStopRefresh)
        # make sure the eyetracker recording stops
        if etRecord.status != FINISHED:
            etRecord.status = FINISHED
        trials.addData('image.started', image.tStartRefresh)
        trials.addData('image.stopped', image.tStopRefresh)
        # check responses
        if skip.keys in ['', [], None]:  # No response was made
            skip.keys = None
        trials.addData('skip.keys',skip.keys)
        if skip.keys != None:  # we had a response
            trials.addData('skip.rt', skip.rt)
        trials.addData('skip.started', skip.tStartRefresh)
        trials.addData('skip.stopped', skip.tStopRefresh)
        if snippet_start_event.status == STARTED:
            win.callOnFlip(snippet_start_event.setData, int(0))
        trials.addData('snippet_start_event.started', snippet_start_event.tStartRefresh)
        trials.addData('snippet_start_event.stopped', snippet_start_event.tStopRefresh)
        end_of_stimuli = current_time - start_time
        df_stimuli.loc[len(df_stimuli)] = [SnippetName, start_of_stimuli, end_of_stimuli]
        ioServer.sendMessageEvent("End Snippet " + SnippetName, category = "SNIPPETVIEW", sec_time = ioServer.getTime())
        # check responses
        if force_skip.keys in ['', [], None]:  # No response was made
            force_skip.keys = None
        trials.addData('force_skip.keys',force_skip.keys)
        if force_skip.keys != None:  # we had a response
            trials.addData('force_skip.rt', force_skip.rt)
        trials.addData('force_skip.started', force_skip.tStartRefresh)
        trials.addData('force_skip.stopped', force_skip.tStopRefresh)
        if p_port_2.status == STARTED:
            win.callOnFlip(p_port_2.setData, int(0))
        trials.addData('p_port_2.started', p_port_2.tStart)
        trials.addData('p_port_2.stopped', p_port_2.tStop)
        trials.addData('circle.started', circle.tStartRefresh)
        trials.addData('circle.stopped', circle.tStopRefresh)
        trials.addData('fixation_cross_2.started', fixation_cross_2.tStartRefresh)
        trials.addData('fixation_cross_2.stopped', fixation_cross_2.tStopRefresh)
        trials.addData('fixation_cross.started', fixation_cross.tStartRefresh)
        trials.addData('fixation_cross.stopped', fixation_cross.tStopRefresh)
        trials.addData('small_circle.started', small_circle.tStartRefresh)
        trials.addData('small_circle.stopped', small_circle.tStopRefresh)
        # the Routine "Snippet" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # ------Prepare to start Routine "Question"-------
        continueRoutine = True
        # update component parameters for each repeat
        key_resp.keys = []
        key_resp.rt = []
        _key_resp_allKeys = []
        three_answers.reset()
        answer = None
        if skipSnippet: 
            continueRoutine = False
        if answer3 == "EMPTY": 
            labels = [answer1, answer2, "I'm not \nsure"]
            for i, obj in enumerate(two_answers.labelObjs):
                obj.text = two_answers.labels[i] = labels[i]
            key_image_3.opacity = 0
        
        else: 
            labels = [answer1, answer2, answer3, "I'm not \nsure"]
            for i, obj in enumerate(three_answers.labelObjs):
                obj.text = three_answers.labels[i] = labels[i]
            key_image_3.opacity = 1
        
        
        
        two_answers.reset()
        # keep track of which components have finished
        QuestionComponents = [question, key_resp, three_answers, two_answers, p_port, key_image_1, key_image_2, key_image_3, key_image_enter]
        for thisComponent in QuestionComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        QuestionClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "Question"-------
        while continueRoutine:
            # get current time
            t = QuestionClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=QuestionClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *question* updates
            if question.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                question.frameNStart = frameN  # exact frame index
                question.tStart = t  # local t and not account for scr refresh
                question.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(question, 'tStartRefresh')  # time at next scr refresh
                question.setAutoDraw(True)
            if question.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > question.tStartRefresh + 60-frameTolerance:
                    # keep track of stop time/frame for later
                    question.tStop = t  # not accounting for scr refresh
                    question.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(question, 'tStopRefresh')  # time at next scr refresh
                    question.setAutoDraw(False)
            
            # *key_resp* updates
            waitOnFlip = False
            if key_resp.status == NOT_STARTED and tThisFlip >= 0.1-frameTolerance:
                # keep track of start time/frame for later
                key_resp.frameNStart = frameN  # exact frame index
                key_resp.tStart = t  # local t and not account for scr refresh
                key_resp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
                key_resp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if key_resp.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > key_resp.tStartRefresh + 59.9-frameTolerance:
                    # keep track of stop time/frame for later
                    key_resp.tStop = t  # not accounting for scr refresh
                    key_resp.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(key_resp, 'tStopRefresh')  # time at next scr refresh
                    key_resp.status = FINISHED
            if key_resp.status == STARTED and not waitOnFlip:
                theseKeys = key_resp.getKeys(keyList=['end', 'down', 'pagedown', 'return'], waitRelease=False)
                _key_resp_allKeys.extend(theseKeys)
                if len(_key_resp_allKeys):
                    key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                    key_resp.rt = _key_resp_allKeys[-1].rt
                    # a response ends the routine
                    continueRoutine = False
            
            # *three_answers* updates
            if three_answers.status == NOT_STARTED and answer3 != "EMPTY":
                # keep track of start time/frame for later
                three_answers.frameNStart = frameN  # exact frame index
                three_answers.tStart = t  # local t and not account for scr refresh
                three_answers.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(three_answers, 'tStartRefresh')  # time at next scr refresh
                three_answers.setAutoDraw(True)
            if three_answers.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > three_answers.tStartRefresh + 60-frameTolerance:
                    # keep track of stop time/frame for later
                    three_answers.tStop = t  # not accounting for scr refresh
                    three_answers.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(three_answers, 'tStopRefresh')  # time at next scr refresh
                    three_answers.setAutoDraw(False)
            
            
            
            # *two_answers* updates
            if two_answers.status == NOT_STARTED and answer3 == "EMPTY":
                # keep track of start time/frame for later
                two_answers.frameNStart = frameN  # exact frame index
                two_answers.tStart = t  # local t and not account for scr refresh
                two_answers.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(two_answers, 'tStartRefresh')  # time at next scr refresh
                two_answers.setAutoDraw(True)
            if two_answers.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > two_answers.tStartRefresh + 60-frameTolerance:
                    # keep track of stop time/frame for later
                    two_answers.tStop = t  # not accounting for scr refresh
                    two_answers.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(two_answers, 'tStopRefresh')  # time at next scr refresh
                    two_answers.setAutoDraw(False)
            # *p_port* updates
            if p_port.status == NOT_STARTED and question.status == STARTED:
                # keep track of start time/frame for later
                p_port.frameNStart = frameN  # exact frame index
                p_port.tStart = t  # local t and not account for scr refresh
                p_port.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(p_port, 'tStartRefresh')  # time at next scr refresh
                p_port.status = STARTED
                win.callOnFlip(p_port.setData, int(4))
            if p_port.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > p_port.tStartRefresh + 0.1-frameTolerance:
                    # keep track of stop time/frame for later
                    p_port.tStop = t  # not accounting for scr refresh
                    p_port.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(p_port, 'tStopRefresh')  # time at next scr refresh
                    p_port.status = FINISHED
                    win.callOnFlip(p_port.setData, int(0))
            
            # *key_image_1* updates
            if key_image_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                key_image_1.frameNStart = frameN  # exact frame index
                key_image_1.tStart = t  # local t and not account for scr refresh
                key_image_1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_image_1, 'tStartRefresh')  # time at next scr refresh
                key_image_1.setAutoDraw(True)
            if key_image_1.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > key_image_1.tStartRefresh + 60-frameTolerance:
                    # keep track of stop time/frame for later
                    key_image_1.tStop = t  # not accounting for scr refresh
                    key_image_1.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(key_image_1, 'tStopRefresh')  # time at next scr refresh
                    key_image_1.setAutoDraw(False)
            
            # *key_image_2* updates
            if key_image_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                key_image_2.frameNStart = frameN  # exact frame index
                key_image_2.tStart = t  # local t and not account for scr refresh
                key_image_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_image_2, 'tStartRefresh')  # time at next scr refresh
                key_image_2.setAutoDraw(True)
            if key_image_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > key_image_2.tStartRefresh + 60-frameTolerance:
                    # keep track of stop time/frame for later
                    key_image_2.tStop = t  # not accounting for scr refresh
                    key_image_2.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(key_image_2, 'tStopRefresh')  # time at next scr refresh
                    key_image_2.setAutoDraw(False)
            
            # *key_image_3* updates
            if key_image_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                key_image_3.frameNStart = frameN  # exact frame index
                key_image_3.tStart = t  # local t and not account for scr refresh
                key_image_3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_image_3, 'tStartRefresh')  # time at next scr refresh
                key_image_3.setAutoDraw(True)
            if key_image_3.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > key_image_3.tStartRefresh + 60-frameTolerance:
                    # keep track of stop time/frame for later
                    key_image_3.tStop = t  # not accounting for scr refresh
                    key_image_3.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(key_image_3, 'tStopRefresh')  # time at next scr refresh
                    key_image_3.setAutoDraw(False)
            
            # *key_image_enter* updates
            if key_image_enter.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                key_image_enter.frameNStart = frameN  # exact frame index
                key_image_enter.tStart = t  # local t and not account for scr refresh
                key_image_enter.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_image_enter, 'tStartRefresh')  # time at next scr refresh
                key_image_enter.setAutoDraw(True)
            if key_image_enter.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > key_image_enter.tStartRefresh + 60-frameTolerance:
                    # keep track of stop time/frame for later
                    key_image_enter.tStop = t  # not accounting for scr refresh
                    key_image_enter.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(key_image_enter, 'tStopRefresh')  # time at next scr refresh
                    key_image_enter.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in QuestionComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "Question"-------
        for thisComponent in QuestionComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        trials.addData('question.started', question.tStartRefresh)
        trials.addData('question.stopped', question.tStopRefresh)
        # check responses
        if key_resp.keys in ['', [], None]:  # No response was made
            key_resp.keys = None
        trials.addData('key_resp.keys',key_resp.keys)
        if key_resp.keys != None:  # we had a response
            trials.addData('key_resp.rt', key_resp.rt)
        trials.addData('key_resp.started', key_resp.tStartRefresh)
        trials.addData('key_resp.stopped', key_resp.tStopRefresh)
        trials.addData('three_answers.response', three_answers.getRating())
        trials.addData('three_answers.rt', three_answers.getRT())
        trials.addData('three_answers.started', three_answers.tStartRefresh)
        trials.addData('three_answers.stopped', three_answers.tStopRefresh)
        if key_resp.keys is None: 
            answer = "no Answer"
        else:
            if key_resp.keys == 'end':
                answer = str(answer1)
            
            if key_resp.keys == 'down':
                answer = str(answer2)
            
            if key_resp.keys == 'pagedown':
                answer = str(answer3)
            
            if key_resp.keys == 'enter':
                answer = "skip"
            
        correctness = "not_answered"
        if answer is not None:
            correctness = str(answer == str(correct))
            df_answer.loc[len(df_answer)] = [SnippetName, answer, correctness]
            continueRoutine = False
            
        
        ioServer.sendMessageEvent("Answer " + str(SnippetName) + " " + str(answer) + " " + str(correctness), category = "ANSWER", sec_time = ioServer.getTime())
        trials.addData('two_answers.response', two_answers.getRating())
        trials.addData('two_answers.rt', two_answers.getRT())
        trials.addData('two_answers.started', two_answers.tStartRefresh)
        trials.addData('two_answers.stopped', two_answers.tStopRefresh)
        if p_port.status == STARTED:
            win.callOnFlip(p_port.setData, int(0))
        trials.addData('p_port.started', p_port.tStartRefresh)
        trials.addData('p_port.stopped', p_port.tStopRefresh)
        trials.addData('key_image_1.started', key_image_1.tStartRefresh)
        trials.addData('key_image_1.stopped', key_image_1.tStopRefresh)
        trials.addData('key_image_2.started', key_image_2.tStartRefresh)
        trials.addData('key_image_2.stopped', key_image_2.tStopRefresh)
        trials.addData('key_image_3.started', key_image_3.tStartRefresh)
        trials.addData('key_image_3.stopped', key_image_3.tStopRefresh)
        trials.addData('key_image_enter.started', key_image_enter.tStartRefresh)
        trials.addData('key_image_enter.stopped', key_image_enter.tStopRefresh)
        # the Routine "Question" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # ------Prepare to start Routine "Difficulty"-------
        continueRoutine = True
        routineTimer.add(60.000000)
        # update component parameters for each repeat
        key_resp_2.keys = []
        key_resp_2.rt = []
        _key_resp_2_allKeys = []
        answers_2.reset()
        if skipSnippet: 
            continueRoutine = False
        answer = None
        # keep track of which components have finished
        DifficultyComponents = [difficulty, key_resp_2, answers_2, key_image_1_2, key_image_2_2, key_image_enter_2]
        for thisComponent in DifficultyComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        DifficultyClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "Difficulty"-------
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = DifficultyClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=DifficultyClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *difficulty* updates
            if difficulty.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                difficulty.frameNStart = frameN  # exact frame index
                difficulty.tStart = t  # local t and not account for scr refresh
                difficulty.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(difficulty, 'tStartRefresh')  # time at next scr refresh
                difficulty.setAutoDraw(True)
            if difficulty.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > difficulty.tStartRefresh + 60-frameTolerance:
                    # keep track of stop time/frame for later
                    difficulty.tStop = t  # not accounting for scr refresh
                    difficulty.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(difficulty, 'tStopRefresh')  # time at next scr refresh
                    difficulty.setAutoDraw(False)
            
            # *key_resp_2* updates
            waitOnFlip = False
            if key_resp_2.status == NOT_STARTED and tThisFlip >= 0.1-frameTolerance:
                # keep track of start time/frame for later
                key_resp_2.frameNStart = frameN  # exact frame index
                key_resp_2.tStart = t  # local t and not account for scr refresh
                key_resp_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp_2, 'tStartRefresh')  # time at next scr refresh
                key_resp_2.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_resp_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if key_resp_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > key_resp_2.tStartRefresh + 59.9-frameTolerance:
                    # keep track of stop time/frame for later
                    key_resp_2.tStop = t  # not accounting for scr refresh
                    key_resp_2.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(key_resp_2, 'tStopRefresh')  # time at next scr refresh
                    key_resp_2.status = FINISHED
            if key_resp_2.status == STARTED and not waitOnFlip:
                theseKeys = key_resp_2.getKeys(keyList=['end', 'down', 'return'], waitRelease=False)
                _key_resp_2_allKeys.extend(theseKeys)
                if len(_key_resp_2_allKeys):
                    key_resp_2.keys = _key_resp_2_allKeys[-1].name  # just the last key pressed
                    key_resp_2.rt = _key_resp_2_allKeys[-1].rt
                    # a response ends the routine
                    continueRoutine = False
            
            # *answers_2* updates
            if answers_2.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                answers_2.frameNStart = frameN  # exact frame index
                answers_2.tStart = t  # local t and not account for scr refresh
                answers_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(answers_2, 'tStartRefresh')  # time at next scr refresh
                answers_2.setAutoDraw(True)
            if answers_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > answers_2.tStartRefresh + 60-frameTolerance:
                    # keep track of stop time/frame for later
                    answers_2.tStop = t  # not accounting for scr refresh
                    answers_2.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(answers_2, 'tStopRefresh')  # time at next scr refresh
                    answers_2.setAutoDraw(False)
            
                
            #if key_resp_2.keys == 'r':
            #    answers_2.recordRating(4)
            #    answer = "skip"
            
            
            # *key_image_1_2* updates
            if key_image_1_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                key_image_1_2.frameNStart = frameN  # exact frame index
                key_image_1_2.tStart = t  # local t and not account for scr refresh
                key_image_1_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_image_1_2, 'tStartRefresh')  # time at next scr refresh
                key_image_1_2.setAutoDraw(True)
            if key_image_1_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > key_image_1_2.tStartRefresh + 60-frameTolerance:
                    # keep track of stop time/frame for later
                    key_image_1_2.tStop = t  # not accounting for scr refresh
                    key_image_1_2.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(key_image_1_2, 'tStopRefresh')  # time at next scr refresh
                    key_image_1_2.setAutoDraw(False)
            
            # *key_image_2_2* updates
            if key_image_2_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                key_image_2_2.frameNStart = frameN  # exact frame index
                key_image_2_2.tStart = t  # local t and not account for scr refresh
                key_image_2_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_image_2_2, 'tStartRefresh')  # time at next scr refresh
                key_image_2_2.setAutoDraw(True)
            if key_image_2_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > key_image_2_2.tStartRefresh + 60-frameTolerance:
                    # keep track of stop time/frame for later
                    key_image_2_2.tStop = t  # not accounting for scr refresh
                    key_image_2_2.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(key_image_2_2, 'tStopRefresh')  # time at next scr refresh
                    key_image_2_2.setAutoDraw(False)
            
            # *key_image_enter_2* updates
            if key_image_enter_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                key_image_enter_2.frameNStart = frameN  # exact frame index
                key_image_enter_2.tStart = t  # local t and not account for scr refresh
                key_image_enter_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_image_enter_2, 'tStartRefresh')  # time at next scr refresh
                key_image_enter_2.setAutoDraw(True)
            if key_image_enter_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > key_image_enter_2.tStartRefresh + 60-frameTolerance:
                    # keep track of stop time/frame for later
                    key_image_enter_2.tStop = t  # not accounting for scr refresh
                    key_image_enter_2.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(key_image_enter_2, 'tStopRefresh')  # time at next scr refresh
                    key_image_enter_2.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in DifficultyComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "Difficulty"-------
        for thisComponent in DifficultyComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        trials.addData('difficulty.started', difficulty.tStartRefresh)
        trials.addData('difficulty.stopped', difficulty.tStopRefresh)
        # check responses
        if key_resp_2.keys in ['', [], None]:  # No response was made
            key_resp_2.keys = None
        trials.addData('key_resp_2.keys',key_resp_2.keys)
        if key_resp_2.keys != None:  # we had a response
            trials.addData('key_resp_2.rt', key_resp_2.rt)
        trials.addData('key_resp_2.started', key_resp_2.tStartRefresh)
        trials.addData('key_resp_2.stopped', key_resp_2.tStopRefresh)
        trials.addData('answers_2.response', answers_2.getRating())
        trials.addData('answers_2.rt', answers_2.getRT())
        trials.addData('answers_2.started', answers_2.tStartRefresh)
        trials.addData('answers_2.stopped', answers_2.tStopRefresh)
        if key_resp.keys is None: 
            answer = "no Answer"
        else:
            if key_resp_2.keys == 'end':
                answers_2.recordRating(1)
                answer = "easy"
                
            if key_resp_2.keys == 'down':
                answers_2.recordRating(2)
                answer = "hard"
                
            if key_resp_2.keys == 'enter':
                answers_2.recordRating(3)
                answer = "skip"
            
                
        if answer is not None:
            df_eval.loc[len(df_eval)] = [SnippetName, answer]
            continueRoutine = False
            
            
        ioServer.sendMessageEvent("Perception " + str(SnippetName) + " " + str(answer), category = "PERCEPTION", sec_time = ioServer.getTime())
        trials.addData('key_image_1_2.started', key_image_1_2.tStartRefresh)
        trials.addData('key_image_1_2.stopped', key_image_1_2.tStopRefresh)
        trials.addData('key_image_2_2.started', key_image_2_2.tStartRefresh)
        trials.addData('key_image_2_2.stopped', key_image_2_2.tStopRefresh)
        trials.addData('key_image_enter_2.started', key_image_enter_2.tStartRefresh)
        trials.addData('key_image_enter_2.stopped', key_image_enter_2.tStopRefresh)
        
        # ------Prepare to start Routine "Pause"-------
        continueRoutine = True
        # update component parameters for each repeat
        text.setText("Short break\n" + str(break_length) + " seconds")
        key_resp_3.keys = []
        key_resp_3.rt = []
        _key_resp_3_allKeys = []
        if trials.thisN+1 == trials.nTotal or skipSnippet:
            continueRoutine = False
        # keep track of which components have finished
        PauseComponents = [text, key_resp_3]
        for thisComponent in PauseComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        PauseClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "Pause"-------
        while continueRoutine:
            # get current time
            t = PauseClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=PauseClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *text* updates
            if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                text.frameNStart = frameN  # exact frame index
                text.tStart = t  # local t and not account for scr refresh
                text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
                text.setAutoDraw(True)
            if text.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > text.tStartRefresh + break_length-frameTolerance:
                    # keep track of stop time/frame for later
                    text.tStop = t  # not accounting for scr refresh
                    text.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(text, 'tStopRefresh')  # time at next scr refresh
                    text.setAutoDraw(False)
            
            # *key_resp_3* updates
            waitOnFlip = False
            if key_resp_3.status == NOT_STARTED and tThisFlip >= 5-frameTolerance:
                # keep track of start time/frame for later
                key_resp_3.frameNStart = frameN  # exact frame index
                key_resp_3.tStart = t  # local t and not account for scr refresh
                key_resp_3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp_3, 'tStartRefresh')  # time at next scr refresh
                key_resp_3.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_resp_3.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_resp_3.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if key_resp_3.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > key_resp_3.tStartRefresh + break_length-5-frameTolerance:
                    # keep track of stop time/frame for later
                    key_resp_3.tStop = t  # not accounting for scr refresh
                    key_resp_3.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(key_resp_3, 'tStopRefresh')  # time at next scr refresh
                    key_resp_3.status = FINISHED
            if key_resp_3.status == STARTED and not waitOnFlip:
                theseKeys = key_resp_3.getKeys(keyList=['return'], waitRelease=False)
                _key_resp_3_allKeys.extend(theseKeys)
                if len(_key_resp_3_allKeys):
                    key_resp_3.keys = _key_resp_3_allKeys[-1].name  # just the last key pressed
                    key_resp_3.rt = _key_resp_3_allKeys[-1].rt
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in PauseComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "Pause"-------
        for thisComponent in PauseComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        trials.addData('text.started', text.tStartRefresh)
        trials.addData('text.stopped', text.tStopRefresh)
        # check responses
        if key_resp_3.keys in ['', [], None]:  # No response was made
            key_resp_3.keys = None
        trials.addData('key_resp_3.keys',key_resp_3.keys)
        if key_resp_3.keys != None:  # we had a response
            trials.addData('key_resp_3.rt', key_resp_3.rt)
        trials.addData('key_resp_3.started', key_resp_3.tStartRefresh)
        trials.addData('key_resp_3.stopped', key_resp_3.tStopRefresh)
        # the Routine "Pause" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 0 if (skip_iter) else 1 repeats of 'trials'
    
    
    # ------Prepare to start Routine "Long_Pause"-------
    continueRoutine = True
    # update component parameters for each repeat
    key_resp_10.keys = []
    key_resp_10.rt = []
    _key_resp_10_allKeys = []
    since_start = datetime.now()
    if ((Round == 3) or (Round < int(expInfo['startRound']))): 
        continueRoutine = False
    if trials.thisN+1 == trials.nTotal:
        continueRoutine = False
    key_resp_14.keys = []
    key_resp_14.rt = []
    _key_resp_14_allKeys = []
    # keep track of which components have finished
    Long_PauseComponents = [text_4, key_resp_10, key_resp_14, pause_start, pause_ende]
    for thisComponent in Long_PauseComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    Long_PauseClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Long_Pause"-------
    while continueRoutine:
        # get current time
        t = Long_PauseClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Long_PauseClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_4* updates
        if text_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_4.frameNStart = frameN  # exact frame index
            text_4.tStart = t  # local t and not account for scr refresh
            text_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_4, 'tStartRefresh')  # time at next scr refresh
            text_4.setAutoDraw(True)
        if text_4.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > text_4.tStartRefresh + 300.0-frameTolerance:
                # keep track of stop time/frame for later
                text_4.tStop = t  # not accounting for scr refresh
                text_4.frameNStop = frameN  # exact frame index
                win.timeOnFlip(text_4, 'tStopRefresh')  # time at next scr refresh
                text_4.setAutoDraw(False)
        
        # *key_resp_10* updates
        waitOnFlip = False
        if key_resp_10.status == NOT_STARTED and tThisFlip >= 120-frameTolerance:
            # keep track of start time/frame for later
            key_resp_10.frameNStart = frameN  # exact frame index
            key_resp_10.tStart = t  # local t and not account for scr refresh
            key_resp_10.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_10, 'tStartRefresh')  # time at next scr refresh
            key_resp_10.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_10.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_10.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_10.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > key_resp_10.tStartRefresh + 180-frameTolerance:
                # keep track of stop time/frame for later
                key_resp_10.tStop = t  # not accounting for scr refresh
                key_resp_10.frameNStop = frameN  # exact frame index
                win.timeOnFlip(key_resp_10, 'tStopRefresh')  # time at next scr refresh
                key_resp_10.status = FINISHED
        if key_resp_10.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_10.getKeys(keyList=['return'], waitRelease=False)
            _key_resp_10_allKeys.extend(theseKeys)
            if len(_key_resp_10_allKeys):
                key_resp_10.keys = _key_resp_10_allKeys[-1].name  # just the last key pressed
                key_resp_10.rt = _key_resp_10_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        #current_time = datetime.now()
        #time_elapsed = current_time - since_start
        #td = dt.timedelta(seconds=300) - time_elapsed
        
        #td_str = ""
        #if td.days:
        #   td_str += f"{td.days}d"
        #if td.seconds // 3600:
        #    td_str += f"{td.seconds // 3600}h"
        #if td.seconds % 3600 // 60:
        #    td_str += f"{td.seconds % 3600 // 60}m"
        #if td.seconds % 60:
        #    td_str += f"{td.seconds % 60}s"
        #if td_str == "":
        #    td_str = f"0s"
            
        #break_text = ""
        #break_text = "Break" + "\n" + td_str + " left"  + "\n \n" + "Press Return to skip"
        #text_4.setText(break_text)
        
        # *key_resp_14* updates
        waitOnFlip = False
        if key_resp_14.status == NOT_STARTED and tThisFlip >= 0.1-frameTolerance:
            # keep track of start time/frame for later
            key_resp_14.frameNStart = frameN  # exact frame index
            key_resp_14.tStart = t  # local t and not account for scr refresh
            key_resp_14.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_14, 'tStartRefresh')  # time at next scr refresh
            key_resp_14.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_14.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_14.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_14.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > key_resp_14.tStartRefresh + 299.9-frameTolerance:
                # keep track of stop time/frame for later
                key_resp_14.tStop = t  # not accounting for scr refresh
                key_resp_14.frameNStop = frameN  # exact frame index
                win.timeOnFlip(key_resp_14, 'tStopRefresh')  # time at next scr refresh
                key_resp_14.status = FINISHED
        if key_resp_14.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_14.getKeys(keyList=['q'], waitRelease=False)
            _key_resp_14_allKeys.extend(theseKeys)
            if len(_key_resp_14_allKeys):
                key_resp_14.keys = _key_resp_14_allKeys[-1].name  # just the last key pressed
                key_resp_14.rt = _key_resp_14_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        # *pause_start* updates
        if pause_start.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            pause_start.frameNStart = frameN  # exact frame index
            pause_start.tStart = t  # local t and not account for scr refresh
            pause_start.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(pause_start, 'tStartRefresh')  # time at next scr refresh
            pause_start.status = STARTED
            win.callOnFlip(pause_start.setData, int(2))
        if pause_start.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > pause_start.tStartRefresh + 0.1-frameTolerance:
                # keep track of stop time/frame for later
                pause_start.tStop = t  # not accounting for scr refresh
                pause_start.frameNStop = frameN  # exact frame index
                win.timeOnFlip(pause_start, 'tStopRefresh')  # time at next scr refresh
                pause_start.status = FINISHED
                win.callOnFlip(pause_start.setData, int(0))
        # *pause_ende* updates
        if pause_ende.status == NOT_STARTED and end_of_stimuli != None:
            # keep track of start time/frame for later
            pause_ende.frameNStart = frameN  # exact frame index
            pause_ende.tStart = t  # local t and not account for scr refresh
            pause_ende.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(pause_ende, 'tStartRefresh')  # time at next scr refresh
            pause_ende.status = STARTED
            win.callOnFlip(pause_ende.setData, int(1))
        if pause_ende.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > pause_ende.tStartRefresh + 0.1-frameTolerance:
                # keep track of stop time/frame for later
                pause_ende.tStop = t  # not accounting for scr refresh
                pause_ende.frameNStop = frameN  # exact frame index
                win.timeOnFlip(pause_ende, 'tStopRefresh')  # time at next scr refresh
                pause_ende.status = FINISHED
                win.callOnFlip(pause_ende.setData, int(0))
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Long_PauseComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Long_Pause"-------
    for thisComponent in Long_PauseComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    rounds.addData('text_4.started', text_4.tStartRefresh)
    rounds.addData('text_4.stopped', text_4.tStopRefresh)
    # check responses
    if key_resp_10.keys in ['', [], None]:  # No response was made
        key_resp_10.keys = None
    rounds.addData('key_resp_10.keys',key_resp_10.keys)
    if key_resp_10.keys != None:  # we had a response
        rounds.addData('key_resp_10.rt', key_resp_10.rt)
    rounds.addData('key_resp_10.started', key_resp_10.tStartRefresh)
    rounds.addData('key_resp_10.stopped', key_resp_10.tStopRefresh)
    # check responses
    if key_resp_14.keys in ['', [], None]:  # No response was made
        key_resp_14.keys = None
    rounds.addData('key_resp_14.keys',key_resp_14.keys)
    if key_resp_14.keys != None:  # we had a response
        rounds.addData('key_resp_14.rt', key_resp_14.rt)
    rounds.addData('key_resp_14.started', key_resp_14.tStartRefresh)
    rounds.addData('key_resp_14.stopped', key_resp_14.tStopRefresh)
    if pause_start.status == STARTED:
        win.callOnFlip(pause_start.setData, int(0))
    rounds.addData('pause_start.started', pause_start.tStart)
    rounds.addData('pause_start.stopped', pause_start.tStop)
    if pause_ende.status == STARTED:
        win.callOnFlip(pause_ende.setData, int(0))
    rounds.addData('pause_ende.started', pause_ende.tStart)
    rounds.addData('pause_ende.stopped', pause_ende.tStop)
    # the Routine "Long_Pause" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1.0 repeats of 'rounds'


# ------Prepare to start Routine "End_Study"-------
continueRoutine = True
routineTimer.add(20.000000)
# update component parameters for each repeat
key_resp_16.keys = []
key_resp_16.rt = []
_key_resp_16_allKeys = []
force_skip_6.keys = []
force_skip_6.rt = []
_force_skip_6_allKeys = []
# keep track of which components have finished
End_StudyComponents = [End_text, key_resp_16, force_skip_6]
for thisComponent in End_StudyComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
End_StudyClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "End_Study"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = End_StudyClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=End_StudyClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *End_text* updates
    if End_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        End_text.frameNStart = frameN  # exact frame index
        End_text.tStart = t  # local t and not account for scr refresh
        End_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(End_text, 'tStartRefresh')  # time at next scr refresh
        End_text.setAutoDraw(True)
    if End_text.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > End_text.tStartRefresh + 20-frameTolerance:
            # keep track of stop time/frame for later
            End_text.tStop = t  # not accounting for scr refresh
            End_text.frameNStop = frameN  # exact frame index
            win.timeOnFlip(End_text, 'tStopRefresh')  # time at next scr refresh
            End_text.setAutoDraw(False)
    
    # *key_resp_16* updates
    waitOnFlip = False
    if key_resp_16.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        key_resp_16.frameNStart = frameN  # exact frame index
        key_resp_16.tStart = t  # local t and not account for scr refresh
        key_resp_16.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp_16, 'tStartRefresh')  # time at next scr refresh
        key_resp_16.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp_16.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp_16.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp_16.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > key_resp_16.tStartRefresh + 20-frameTolerance:
            # keep track of stop time/frame for later
            key_resp_16.tStop = t  # not accounting for scr refresh
            key_resp_16.frameNStop = frameN  # exact frame index
            win.timeOnFlip(key_resp_16, 'tStopRefresh')  # time at next scr refresh
            key_resp_16.status = FINISHED
    if key_resp_16.status == STARTED and not waitOnFlip:
        theseKeys = key_resp_16.getKeys(keyList=['space'], waitRelease=False)
        _key_resp_16_allKeys.extend(theseKeys)
        if len(_key_resp_16_allKeys):
            key_resp_16.keys = _key_resp_16_allKeys[-1].name  # just the last key pressed
            key_resp_16.rt = _key_resp_16_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # *force_skip_6* updates
    waitOnFlip = False
    if force_skip_6.status == NOT_STARTED and tThisFlip >= 0.1-frameTolerance:
        # keep track of start time/frame for later
        force_skip_6.frameNStart = frameN  # exact frame index
        force_skip_6.tStart = t  # local t and not account for scr refresh
        force_skip_6.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(force_skip_6, 'tStartRefresh')  # time at next scr refresh
        force_skip_6.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(force_skip_6.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(force_skip_6.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if force_skip_6.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > force_skip_6.tStartRefresh + 19.9-frameTolerance:
            # keep track of stop time/frame for later
            force_skip_6.tStop = t  # not accounting for scr refresh
            force_skip_6.frameNStop = frameN  # exact frame index
            win.timeOnFlip(force_skip_6, 'tStopRefresh')  # time at next scr refresh
            force_skip_6.status = FINISHED
    if force_skip_6.status == STARTED and not waitOnFlip:
        theseKeys = force_skip_6.getKeys(keyList=['q'], waitRelease=False)
        _force_skip_6_allKeys.extend(theseKeys)
        if len(_force_skip_6_allKeys):
            force_skip_6.keys = _force_skip_6_allKeys[-1].name  # just the last key pressed
            force_skip_6.rt = _force_skip_6_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in End_StudyComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "End_Study"-------
for thisComponent in End_StudyComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('End_text.started', End_text.tStartRefresh)
thisExp.addData('End_text.stopped', End_text.tStopRefresh)
# check responses
if key_resp_16.keys in ['', [], None]:  # No response was made
    key_resp_16.keys = None
thisExp.addData('key_resp_16.keys',key_resp_16.keys)
if key_resp_16.keys != None:  # we had a response
    thisExp.addData('key_resp_16.rt', key_resp_16.rt)
thisExp.addData('key_resp_16.started', key_resp_16.tStartRefresh)
thisExp.addData('key_resp_16.stopped', key_resp_16.tStopRefresh)
thisExp.nextEntry()
# check responses
if force_skip_6.keys in ['', [], None]:  # No response was made
    force_skip_6.keys = None
thisExp.addData('force_skip_6.keys',force_skip_6.keys)
if force_skip_6.keys != None:  # we had a response
    thisExp.addData('force_skip_6.rt', force_skip_6.rt)
thisExp.addData('force_skip_6.started', force_skip_6.tStartRefresh)
thisExp.addData('force_skip_6.stopped', force_skip_6.tStopRefresh)
thisExp.nextEntry()

# ------Prepare to start Routine "EEG_End"-------
continueRoutine = True
routineTimer.add(10.000000)
# update component parameters for each repeat
force_skip_7.keys = []
force_skip_7.rt = []
_force_skip_7_allKeys = []
# keep track of which components have finished
EEG_EndComponents = [text_8, end_eeg, force_skip_7]
for thisComponent in EEG_EndComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
EEG_EndClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "EEG_End"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = EEG_EndClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=EEG_EndClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_8* updates
    if text_8.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text_8.frameNStart = frameN  # exact frame index
        text_8.tStart = t  # local t and not account for scr refresh
        text_8.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_8, 'tStartRefresh')  # time at next scr refresh
        text_8.setAutoDraw(True)
    if text_8.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > text_8.tStartRefresh + 10-frameTolerance:
            # keep track of stop time/frame for later
            text_8.tStop = t  # not accounting for scr refresh
            text_8.frameNStop = frameN  # exact frame index
            win.timeOnFlip(text_8, 'tStopRefresh')  # time at next scr refresh
            text_8.setAutoDraw(False)
    # *end_eeg* updates
    if end_eeg.status == NOT_STARTED and t >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        end_eeg.frameNStart = frameN  # exact frame index
        end_eeg.tStart = t  # local t and not account for scr refresh
        end_eeg.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(end_eeg, 'tStartRefresh')  # time at next scr refresh
        end_eeg.status = STARTED
        win.callOnFlip(end_eeg.setData, int(2))
    if end_eeg.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > end_eeg.tStartRefresh + 0.1-frameTolerance:
            # keep track of stop time/frame for later
            end_eeg.tStop = t  # not accounting for scr refresh
            end_eeg.frameNStop = frameN  # exact frame index
            win.timeOnFlip(end_eeg, 'tStopRefresh')  # time at next scr refresh
            end_eeg.status = FINISHED
            win.callOnFlip(end_eeg.setData, int(0))
    
    # *force_skip_7* updates
    waitOnFlip = False
    if force_skip_7.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
        # keep track of start time/frame for later
        force_skip_7.frameNStart = frameN  # exact frame index
        force_skip_7.tStart = t  # local t and not account for scr refresh
        force_skip_7.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(force_skip_7, 'tStartRefresh')  # time at next scr refresh
        force_skip_7.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(force_skip_7.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(force_skip_7.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if force_skip_7.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > force_skip_7.tStartRefresh + 9.5-frameTolerance:
            # keep track of stop time/frame for later
            force_skip_7.tStop = t  # not accounting for scr refresh
            force_skip_7.frameNStop = frameN  # exact frame index
            win.timeOnFlip(force_skip_7, 'tStopRefresh')  # time at next scr refresh
            force_skip_7.status = FINISHED
    if force_skip_7.status == STARTED and not waitOnFlip:
        theseKeys = force_skip_7.getKeys(keyList=['q'], waitRelease=False)
        _force_skip_7_allKeys.extend(theseKeys)
        if len(_force_skip_7_allKeys):
            force_skip_7.keys = _force_skip_7_allKeys[-1].name  # just the last key pressed
            force_skip_7.rt = _force_skip_7_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in EEG_EndComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "EEG_End"-------
for thisComponent in EEG_EndComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('text_8.started', text_8.tStartRefresh)
thisExp.addData('text_8.stopped', text_8.tStopRefresh)
if end_eeg.status == STARTED:
    win.callOnFlip(end_eeg.setData, int(0))
thisExp.addData('end_eeg.started', end_eeg.tStart)
thisExp.addData('end_eeg.stopped', end_eeg.tStop)
# check responses
if force_skip_7.keys in ['', [], None]:  # No response was made
    force_skip_7.keys = None
thisExp.addData('force_skip_7.keys',force_skip_7.keys)
if force_skip_7.keys != None:  # we had a response
    thisExp.addData('force_skip_7.rt', force_skip_7.rt)
thisExp.addData('force_skip_7.started', force_skip_7.tStartRefresh)
thisExp.addData('force_skip_7.stopped', force_skip_7.tStopRefresh)
thisExp.nextEntry()

# ------Prepare to start Routine "photo"-------
continueRoutine = True
routineTimer.add(10.000000)
# update component parameters for each repeat
force_skip_8.keys = []
force_skip_8.rt = []
_force_skip_8_allKeys = []
# keep track of which components have finished
photoComponents = [text_2, force_skip_8]
for thisComponent in photoComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
photoClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "photo"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = photoClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=photoClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_2* updates
    if text_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text_2.frameNStart = frameN  # exact frame index
        text_2.tStart = t  # local t and not account for scr refresh
        text_2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_2, 'tStartRefresh')  # time at next scr refresh
        text_2.setAutoDraw(True)
    if text_2.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > text_2.tStartRefresh + 10-frameTolerance:
            # keep track of stop time/frame for later
            text_2.tStop = t  # not accounting for scr refresh
            text_2.frameNStop = frameN  # exact frame index
            win.timeOnFlip(text_2, 'tStopRefresh')  # time at next scr refresh
            text_2.setAutoDraw(False)
    
    # *force_skip_8* updates
    waitOnFlip = False
    if force_skip_8.status == NOT_STARTED and tThisFlip >= 0.1-frameTolerance:
        # keep track of start time/frame for later
        force_skip_8.frameNStart = frameN  # exact frame index
        force_skip_8.tStart = t  # local t and not account for scr refresh
        force_skip_8.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(force_skip_8, 'tStartRefresh')  # time at next scr refresh
        force_skip_8.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(force_skip_8.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(force_skip_8.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if force_skip_8.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > force_skip_8.tStartRefresh + 9.9-frameTolerance:
            # keep track of stop time/frame for later
            force_skip_8.tStop = t  # not accounting for scr refresh
            force_skip_8.frameNStop = frameN  # exact frame index
            win.timeOnFlip(force_skip_8, 'tStopRefresh')  # time at next scr refresh
            force_skip_8.status = FINISHED
    if force_skip_8.status == STARTED and not waitOnFlip:
        theseKeys = force_skip_8.getKeys(keyList=['q'], waitRelease=False)
        _force_skip_8_allKeys.extend(theseKeys)
        if len(_force_skip_8_allKeys):
            force_skip_8.keys = _force_skip_8_allKeys[-1].name  # just the last key pressed
            force_skip_8.rt = _force_skip_8_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in photoComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "photo"-------
for thisComponent in photoComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('text_2.started', text_2.tStartRefresh)
thisExp.addData('text_2.stopped', text_2.tStopRefresh)
# check responses
if force_skip_8.keys in ['', [], None]:  # No response was made
    force_skip_8.keys = None
thisExp.addData('force_skip_8.keys',force_skip_8.keys)
if force_skip_8.keys != None:  # we had a response
    thisExp.addData('force_skip_8.rt', force_skip_8.rt)
thisExp.addData('force_skip_8.started', force_skip_8.tStartRefresh)
thisExp.addData('force_skip_8.stopped', force_skip_8.tStopRefresh)
thisExp.nextEntry()
df_stimuli.to_csv(f"{folder_name}/Stimuli_Times.csv")
df_answer.to_csv(f"{folder_name}/Task_Answers.csv")
df_eval.to_csv(f"{folder_name}/Task_Eval.csv")
df_et.to_csv(f"{folder_name}/et.csv")


# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
