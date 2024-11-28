# Unexpected but informative: What fixation-related potentials tell us about the processing of ambiguous program code

## Concept

Inspired by existing studies on atoms of confusions such as Langhout et Aniche: Atoms of Confusion in Java (ICPC 2021), which analyzed confusing code patterns in program code, but is extended to a EEG and eye-tracking setup to detect neurocognitive processes on a deeper and more detailed level using fixation-related potentials.

## Requirements

The software has been developed and used on Windows 10 and 11 OS. There are no specific hardware requirements

The major share of the code is presented as jupyter notebooks, for which Python3 is required (implementation in Python 3.11).
It is recommended to create a virtual environment to use for the execution of those snippets.
The required packages can be installed via the [requirements](requirements.txt) file. This should require only a few minutes.

```pip install -r requirements.txt```

For some aspects like the study presentation, we used other programming languages. For the presentation, we used scripts generated in PsychoPy, so the script presented in [06-Task-Presentation_Recording](06-Task-Presentation_Recording/) is created and executed with PsychoPy (Version 2021.3.2).
Additionally, for GLMERs we use R (4.3.2), which has to be installed and usable in jupyter notebook.

## Study

### Purpose

This folder contains all parts used for the study, where we showed the participants code snippets and captured their gaze and brain activity (eye tracker and eeg waves) while understanding the presented code.

### Pipeline and Folders

In the folder, there exist the following folders for an iteration:

* [01-Data-Code_Snippets](01-Data-Code_Snippets/) contains the [adapted versions (v0)](01-Data-Code_Snippets/v0/) we created for our study and the versions we made to each in [v1](01-Data-Code_Snippets/v1/) and [v2](01-Data-Code_Snippets/v2/) to increase our snippet database. They are based on Langhout et Aniche's snippets but shortened to suit an FRP setup.
  The correct solutions of those snippets, provided wrong solutions and additional information such as aoc categories are stored in a csv file [snippets.csv](01-Data-Code_Snippets/snippets.csv).
* [03-Data-Code_Snippet_Images](03-Data-Code_Snippet_Images/) contain:
  * the [Pictures](06-Task-Study_Presentation_Software/images/) generated for this study for each of our snippets, whose content is located in the presentation image folder.
  * AOI/Pictures/: [Pictures](03-Data-Code_Snippet_Images/AOI/Pictures/) contains an annotated version of the snippets, where the atoms of confusion and the expected area of interest for the reader are marked. Those were used later for FRP analysis.
  There, we have categorized the heterogeneous AoIs into multiple categories depending on the amount / type of expression used. For blocks (multiple lines of code) the color blue was used, for marking whole statements the color green was used, for marking larger expressions / areas the color yellow was used, for marking small expressions / parts of an expression the color orange was used and for marking crucial operators or keywords the color red was used. All snippet pairs have identical AoI categories, the AoIs will only differ in their size and position. For the FRP analysis, only the AoI with the lowest category (and smallest size) for each snippet pair were used.
  
* [04-Task-Generate_Block_Sequences](04-Task-Generate_Block_Sequences/) contains a task [GenerateBlockSequences](04-Task-Generate_Block_Sequences/GenerateBlockSequences.ipynb) that uses the information on the snippets to create presentation sequences for all participants of the study by randomly ordering the snippets based on some constraints, and creating the condition files for the presentation.
* [05-Data-Trial_Runs](05-Data-Trial_Runs/) stores the three condition file sequences for each participant. They can be found with the raw data in the data repository.
* [06-Task-Study_Presentation_Software](06-Task-Study_Presentation_Software/) contains the final presentation script created with PsychoPy, including all images as generated into [Pictures](03-Data-Code_Snippet_Images/Pictures/). In the sub-folder [conditions](06-Task-Study_Presentation_Software/conditions), you need to store the condition files as found with the raw data in the data repository.
* [07-Task-Study management and execution](<07-Task-Study management and execution>) contains the template for the documents used for the study, such as the questionnaires and consent forms, as well as a document that describes the study procedure.
* [08-Data-Trial_Recordings](08-Data-Trial_Recordings/) needs to store the results received from the participants' trials, and is structured into 
  - [raw](08-Data-Trial_Recordings/raw/) folder, whose data is taken directly from the presentation and eeg recording scripts, 
  - and the [processed](08-Data-Trial_Recordings/processed/) folder, which contains the transformed data to be used for analysis,
  - [manual_accuracy_evaluation](08-Data-Trial_Recordings/manual_accuracy_evaluation/) contains the iterative approach of evaluation the fixations, the evaluation sheets of each of the 2 reviewers as 1 excel file and the combination (the fixation data itself is in a sub-folder of [processed](08-Data-Trial_Recordings/processed/).
  - [screenshots](08-Data-Trial_Recordings/screenshots/) should contain the screenshots [without aoi](08-Data-Trial_Recordings/screenshots/aoi/) and [with aoi boxes](08-Data-Trial_Recordings/screenshots/normal/)).

  All required files for this folder can be found with the raw data in the data repository.
* [09-Task-Evaluate_Data](09-Task-Evaluate_Data/) contains the framework scripts to preprocess (PRE) and evaluate (EVAL) the recorded data, consisting of behavioral, visual and eeg input. They are structured as numbered jupyter notebooks for the analysis pipeline and need to be executed in this order (except for 01d4 and 01d5, which should be executed by iteration and then number, e.g., [01d4_PRE_VIS_Fixation_Correction-it1](09-Task-Evaluate_Data/01d4_PRE_VIS_Fixation_Correction-it1.ipynb), [01d5_PRE_VIS_Snippet_Correction_Accuracy_Image-it1](09-Task-Evaluate_Data/01d5_PRE_VIS_Snippet_Correction_Accuracy_Image-it1.ipynb), [01d4_PRE_VIS_Fixation_Correction-it2](09-Task-Evaluate_Data/01d4_PRE_VIS_Fixation_Correction-it2.ipynb), [01d5_PRE_VIS_Snippet_Correction_Accuracy_Image-it2](09-Task-Evaluate_Data/01d5_PRE_VIS_Snippet_Correction_Accuracy_Image-it2.ipynb), [01d4_PRE_VIS_Fixation_Correction-it3](09-Task-Evaluate_Data/01d4_PRE_VIS_Fixation_Correction-it3.ipynb), [01d5_PRE_VIS_Snippet_Correction_Accuracy_Image-it3](09-Task-Evaluate_Data/01d5_PRE_VIS_Snippet_Correction_Accuracy_Image-it3.ipynb), [01d4_PRE_VIS_Fixation_Correction-it4](09-Task-Evaluate_Data/01d4_PRE_VIS_Fixation_Correction-it4.ipynb), [01d5_PRE_VIS_Snippet_Correction_Accuracy_Image-it4](09-Task-Evaluate_Data/01d5_PRE_VIS_Snippet_Correction_Accuracy_Image-it4.ipynb)), 
  - The core functionality is extracted in a separate [utils](09-Task-Evaluate_Data/utils/) package, detailed in [the package's README](09-Task-Evaluate_Data/utils/README.md).
  - [image](09-Task-Evaluate_Data/image/) contains images for instruction readmes in this folder.

  The jupyter notebooks have the following content:
  - [00_1_PRE_VIS_Screenshot_AOI_identification](09-Task-Evaluate_Data/00_1_PRE_VIS_Screenshot_AOI_identification.ipynb) extracts the AoI positions from the screenshots
  - [01a1_PRE_Date_Anonymization](09-Task-Evaluate_Data/01a1_PRE_Date_Anonymization.ipynb) anonymizes all raw data extracted from each experiment run
  - [01a2_PRE_Exclusion_Files](09-Task-Evaluate_Data/01a2_PRE_Exclusion_Files.ipynb) creates the exclusion files for each participant
  - [01b_PRE_EEG_Metadata_Check](09-Task-Evaluate_Data/01b_PRE_EEG_Metadata_Check.ipynb) checks the impedances of the EEG recording for each participant's experiment run
  - [01c1_PRE_BEH_Event_Data](09-Task-Evaluate_Data/01c1_PRE_BEH_Event_Data.ipynb) extracts and cleans the behavioral data
  - [01c2_PRE_BEH_Trial_Exclusion](09-Task-Evaluate_Data/01c2_PRE_BEH_Trial_Exclusion.ipynb) excludes trials based on behavioral data on participant-level if the overall correctness is under the expected result due to chance, or on trial-level if there are outliers in the comprehension time (no exclusion for this study)  
  - [01d1_PRE_VIS_Event_Gaze_Data](09-Task-Evaluate_Data/01d1_PRE_VIS_Event_Gaze_Data.ipynb) extracts eye gaze data as stream of x-y coordinates
  - [01d2_PRE_VIS_Fixation_Calculation](09-Task-Evaluate_Data/01d2_PRE_VIS_Fixation_Calculation.ipynb) calculates the fixations based on the gaze data. Attention! This uses the [I2MC algorithm](https://github.com/dcnieho/I2MC_Python) which is unstable. We set made random parameters constant, but you might still receive different results. 
  - [01d3_PRE_VIS_Fixation_Cross_Accuracy_Image](09-Task-Evaluate_Data/01d3_PRE_VIS_Fixation_Cross_Accuracy_Image.ipynb) creates the accuracy images for the fixation-cross view displaying the fixations over the screenshot for each trial
  - [01d4_PRE_VIS_Fixation_Correction-it1](09-Task-Evaluate_Data/01d4_PRE_VIS_Fixation_Correction-it1.ipynb) performs the first iteration of fixation correction (which is nothing, as the data is already there and the first iteration is exclusively used for outlier removal)
  - [01d5_PRE_VIS_Snippet_Correction_Accuracy_Image-it1](09-Task-Evaluate_Data/01d5_PRE_VIS_Snippet_Correction_Accuracy_Image-it1.ipynb) performs the first iteration of creating accuracy images for the snippet-view to detect outliers and of creating the template to be filled by the evaluators
  - [01d6_PRE_VIS_Manual_Accuracy_Evaluation](09-Task-Evaluate_Data/01d6_PRE_VIS_Manual_Accuracy_Evaluation.md) evaluators perform accuracy evaluation separately and combine their results (after 01d5 of each iteration)
  - [01d4_PRE_VIS_Fixation_Correction-it2](09-Task-Evaluate_Data/01d4_PRE_VIS_Fixation_Correction-it2.ipynb) performs the second iteration of fixation correction (by applying up to 4 correction algorithms to the existing data for all trials), does not apply x-offset correction in correction algorithm
  - [01d5_PRE_VIS_Snippet_Correction_Accuracy_Image-it2](09-Task-Evaluate_Data/01d5_PRE_VIS_Snippet_Correction_Accuracy_Image-it2.ipynb) performs the second iteration of creating accuracy images for different algorithm results in comparison to the original version in the snippet-view to detect outliers and of creating the template to be filled by the evaluators, considers x-offset when plotting the results
  - [01d6_PRE_VIS_Manual_Accuracy_Evaluation](09-Task-Evaluate_Data/01d6_PRE_VIS_Manual_Accuracy_Evaluation.md) evaluators perform accuracy evaluation separately and combine their results (after 01d5 of each iteration)
  - [01d4_PRE_VIS_Fixation_Correction-it3](09-Task-Evaluate_Data/01d4_PRE_VIS_Fixation_Correction-it3.ipynb) performs the third iteration of fixation correction (by applying up to 4 correction algorithms to the existing data for all trials __that need to be reworked__), does not apply x-offset correction in correction algorithm
  - [01d5_PRE_VIS_Snippet_Correction_Accuracy_Image-it3](09-Task-Evaluate_Data/01d5_PRE_VIS_Snippet_Correction_Accuracy_Image-it3.ipynb) performs the third iteration of creating accuracy images for different algorithm results in comparison to the original version in the snippet-view to detect outliers and of creating the template to be filled by the evaluators (for all trials __that need to be reworked__), considers x-offset when plotting the results
  - [01d6_PRE_VIS_Manual_Accuracy_Evaluation](09-Task-Evaluate_Data/01d6_PRE_VIS_Manual_Accuracy_Evaluation.md) evaluators perform accuracy evaluation separately and combine their results (after 01d5 of each iteration)
  - [01d4_PRE_VIS_Fixation_Correction-it4](09-Task-Evaluate_Data/01d4_PRE_VIS_Fixation_Correction-it4.ipynb) performs the fourth iteration of fixation correction (by applying up to 4 correction algorithms to the existing data for all trials __that need to be reworked__), does not apply x-offset correction in correction algorithm 
  - [01d5_PRE_VIS_Snippet_Correction_Accuracy_Image-it4](09-Task-Evaluate_Data/01d5_PRE_VIS_Snippet_Correction_Accuracy_Image-it4.ipynb) performs the fourth iteration of creating accuracy images for different algorithm results in comparison to the original version in the snippet-view to detect outliers and of creating the template to be filled by the evaluators (for all trials __that need to be reworked__), considers x-offset when plotting the results 
  - [01d6_PRE_VIS_Manual_Accuracy_Evaluation](09-Task-Evaluate_Data/01d6_PRE_VIS_Manual_Accuracy_Evaluation.md) evaluators perform accuracy evaluation separately and combine their results (after 01d5 of each iteration)
  - [01d7_PRE_VIS_Gaze_Selection_Fixation](09-Task-Evaluate_Data/01d7_PRE_VIS_Gaze_Selection_Fixation.ipynb) check that the manual evaluation was executed correctly, and applying the outlier removal, exclusions and corrections to the final dataset
  - [01d8_PRE_VIS_Statistics](09-Task-Evaluate_Data/01d8_PRE_VIS_Statistics.ipynb) correct gaze and fixation statistics about the final dataset
  - [01d9_PRE_VIS_Special_Fixations](09-Task-Evaluate_Data/01d9_PRE_VIS_Special_Fixations.ipynb) determine the fixation in each trial to be used for ERP analysis
  - [01d11_PRE_VIS_Outlier_Trials](09-Task-Evaluate_Data/01d11_PRE_VIS_Outlier_Trials.ipynb) aggregates outlier statistics for each phase of the eye-tracking preprocessing (01d1-01d7)
  - [01e1_PRE_EEG_ICA_Reasoning_File](09-Task-Evaluate_Data/01e1_PRE_EEG_ICA_Reasoning_File.ipynb) creates the template for performing ICA using BrainVision Analyzer
  - [01e2_PRE_EEG_BVA_preparation](09-Task-Evaluate_Data/01e2_PRE_EEG_BVA_preparation.md) the preprocessing steps performed in BrainVision Analyzer
  - [01e3_PRE_EEG_Filter_Trial_Assignments](09-Task-Evaluate_Data/01e3_PRE_EEG_Filter_Trial_Assignments.ipynb) loads and crops EEG data to relevant part, then tries to automatically assign trial information (snippet) to each event in the EEG recording using information generated by [01c1_PRE_BEH_Event_Data](09-Task-Evaluate_Data/01c1_PRE_BEH_Event_Data.ipynb). Otherwise, the trial information assignment has to be performed manually based on a provided information template
  - [01e4_PRE_EEG_Trial_Assignments_Split](09-Task-Evaluate_Data/01e4_PRE_EEG_Trial_Assignments_Split.ipynb) creates EEG segments for each trial as previously assigned 
  - [01f1_PRE_ALL_Summary_Participant_Exclusion](09-Task-Evaluate_Data/01f1_PRE_ALL_Summary_Participant_Exclusion.ipynb) summarizes all exclusions in either data mode including the reason
  - [01g1_PRE_EEG_VIS_Set_FRP_markers](09-Task-Evaluate_Data/01g1_PRE_EEG_VIS_Set_FRP_markers.ipynb) copies the EEG segments and synchronizes with eye-tracking data by adding a marker at the time of the special fixation for FRP analysis
  - [03a1_EVAL_BEH_Confusion_Distribution](09-Task-Evaluate_Data/03a1_EVAL_BEH_Confusion_Distribution.ipynb) analyzes the behavioral data by generating overviews of the dependent variables for each condition and for different levels of abstraction
  - [03a2_EVAL_BEH_Confusion_LMEM Correctness](<09-Task-Evaluate_Data/03a2_EVAL_BEH_Confusion_LMEM Correctness.ipynb>) displays the steps of the backtracking algorithm to determine to optimal model for answer correctness
  - [03a2_EVAL_BEH_Confusion_LMEM Duration](<09-Task-Evaluate_Data/03a2_EVAL_BEH_Confusion_LMEM Duration.ipynb>) displays the steps of the backtracking algorithm to determine to optimal model for comprehension time
  - [03a2_EVAL_BEH_Confusion_LMEM Rating](<09-Task-Evaluate_Data/03a2_EVAL_BEH_Confusion_LMEM Rating.ipynb>) displays the steps of the backtracking algorithm to determine to optimal model for subjective difficulty rating
  - [03c1_EVAL_ERP](09-Task-Evaluate_Data/03c1_EVAL_ERP.ipynb) aggregate EEG segments to subject average and grand average based on stimulus onset
  - [03c2_EVAL_ERP_Mass_Univariate_sdiff 03-15 100Hz](<09-Task-Evaluate_Data/03c2_EVAL_ERP_Mass_Univariate_sdiff 03-15 100Hz.ipynb>) performs the cluster-based permutation test
  - [03c2_EVAL_ERP_plot](09-Task-Evaluate_Data/03c2_EVAL_ERP_plot.ipynb) creates different visualizations of the grand averages
  - [03d1_EVAL_FRP](09-Task-Evaluate_Data/03d1_EVAL_FRP.ipynb) aggregate EEG segments to subject average and grand average based on fixation onset
  - [03d2_EVAL_FRP_fixation_analysis](09-Task-Evaluate_Data/03d2_EVAL_FRP_fixation_analysis.ipynb) analyzes fixation-based metrics for all trials included in FRP analysis, such as onset delay
  - [03d2_EVAL_FRP_Permutation_sdiff_01-10_100Hz](09-Task-Evaluate_Data/03d2_EVAL_FRP_Permutation_sdiff_01-10_100Hz.ipynb) performs the cluster-based permutation test
  - [03d2_EVAL_FRP_plot](09-Task-Evaluate_Data/03d2_EVAL_FRP_plot.ipynb) creates different visualizations of the grand averages
  - [03e1_EVAL_VIS_Reading_Metrics](09-Task-Evaluate_Data/03e1_EVAL_VIS_Reading_Metrics.ipynb) analyzes reading-based metrics, such as first-pass in aoi 
* [10-Data_Evaluation_Results](10-Data_Evaluation_Results/) will be created to store the evaluation results such as behavioral statistics, GLMER models for the behavioral metrics, and ERP and FRP analyses with their epoch data and statistical analysis.

The data of this project is stored on [Zenodo](https://doi.org/10.5281/zenodo.14229849) upon publication.

### Terminology
Some terms used in the paper have another correspondence in the code analysis due to project evolution.

- Duration -> Comprehension Time
- Correctness -> Answer Correctness
- Rating -> Subjective Difficulty Rating
- Clean -> Ambiguous
- Obf -> Unambiguous
- Block_No -> BlockNo
- In_Block_No -> ItemOrder

Clarification of further terms:
- Conditions = Ambiguous, Unambiguous
- Snippets: one program code stimulus, also referred to as (code) snippet
- Snippet pair: two corresponding snippets differing only in the condition 
- Snippet number: the snippet number as assigned by Langhout et Aniche, stands for 3 snippet pairs with differ only in their version number (v0,v1,v2)
- Trials: A unique combination of snippet and Participant
- Behavioral data = Comprehension Time, Answer Correctness, Subjective Difficulty Rating


## License

The work is licensed as Creative Commons Attribution 4.0 International.

The Creative Commons Attribution license allows re-distribution and re-use of a licensed work on the condition that the creator is appropriately credited.
