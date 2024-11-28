
from pathlib import Path
import cv2
import matplotlib
from math import ceil, sqrt
from typing import Any
from matplotlib.colors import LinearSegmentedColormap
import mne
import numpy as np
import pandas as pd
import scipy
from cliffs_delta import cliffs_delta
from matplotlib import cm as cm
from matplotlib import pyplot as plt
from scipy.stats import norm, shapiro
from tqdm.notebook import tqdm
from utils.eeg_helpers import (get_erp_description, load_all_erp_averages,
                               round_time_EEG, statistics_distribution)
from utils.eeg_settings import *
from utils.file_settings import SEPARATOR, SNIPPET_COLUMN_VARIANT
from utils.json_helpers import JSONFileBuffers, JSONTypesEncoder
from utils.path_helpers import (get_erp_fixation_analysis_path,
                                get_erp_statistics_path)
from utils.snippet_settings import (CONDITION, CONDITION_CLEAN,
                                    CONDITION_COLORS, CONDITION_CONFUSING,
                                    CONDITION_DIFF, SNIPPET_CLEAN, SNIPPET_OBF)
from utils.statistics_settings import (ALPHA, ALTERNATIVE_HYPOTHESIS,
                                       ALTERNATIVE_HYPOTHESIS_GREATER,
                                       ALTERNATIVE_HYPOTHESIS_LESS, EFFECT_STRENGTH_LARGE, EFFECT_STRENGTH_MEDIUM, EFFECT_STRENGTH_NEGLIGIBLE, EFFECT_STRENGTH_SMALL, MEAN,
                                       MEASURE,
                                       PERMUTATION_CONFIDENCE_INTERVAL,
                                       PERMUTATION_COUNT,
                                       PERMUTATION_COUNT_MAX,
                                       PERMUTATION_COUNT_START,
                                       PERMUTATION_MAX_STEP_FREQUENCY_FACTOR, PERMUTATION_PLOT_PIXEL_X, PERMUTATION_PLOT_PIXEL_Y,
                                       PERMUTATION_TEST_COLORS,
                                       PERMUTATION_TEST_PARAMETERS, PVALUE,
                                       STATISTIC_INFER_H1_ACCEPTED,
                                       STATISTIC_INFER_H1_NON_ACCEPTED, STD,
                                       TEST, TEST_FUNCTION,
                                       TEST_KIND_INDEPENDENT,
                                       TEST_KIND_NON_PARAMETRIC,
                                       TEST_KIND_PAIRED, TEST_KIND_PARAMETRIC,
                                       TEST_MANNWHITNEYU, TEST_T_INDEPENDENT,
                                       TEST_T_PAIRED, TEST_WILCOXON)
from utils.textconstants import CHANNEL, PARTICIPANT
from utils.visual_settings import (FIXATION_SELECTION_ALGORITHM,
                                   FIXATION_SELECTION_ALGORITHMS)


def statistical_analysis_for_subjectwise_averages(analysis_data: pd.DataFrame, alternative_hypotheses_per_measure: dict[str, str],
                                                  additional_groupers: list = [], stest_kind: str = TEST_KIND_INDEPENDENT, log: bool = True, independent_variable: str = CONDITION, independent_factors: tuple[str, str] = (CONDITION_CONFUSING, CONDITION_CLEAN, )) -> pd.DataFrame:
    '''Calculates whether there is a significant difference for the measures across all snippets between the conditions
    This is done by aggregating the data on a condition-subjectwise mean and std, and optionally with additional groupers.

    Depending on whether the resulting dataset is pairwise or not, the wilcoxon-test or the mann-whitney-u-test will be performed against the alternative hypothesis.
    if the alternative hypothesis not accepted (null kept), then a test in the other direction is also performed.

    Arguments:
    * analysis_data: contains the measured data with PARTICIPANT, CONDITION, measures and additional groupers
    * alternative_hypotheses_per_measure: contains the primary alternative hypothesis per measure
    * additional_groupers: statistical analysis for each value combination of the columns between conditions

    returns: a dataframe containing the results for each statistical analysis
    '''
    # or (SNIPPET_COLUMN_VARIANT in analysis_data.columns),
    assert independent_variable in analysis_data.columns, f'''There must be a marker for the independent variable in the analysis_data: {
        independent_variable}'''
    assert len(
        independent_factors) == 2, f'''There can only be 2 independent factors, given {independent_factors}'''
    assert set(independent_factors) == set(analysis_data[independent_variable].unique()), f'''The independent factors must only and all be present in the independent variable. Factors: {independent_factors}, 
    values in independent variable column:re must be a condition marker in the analysis_data: {analysis_data[independent_variable].unique()}'''
    assert PARTICIPANT in analysis_data.columns, f'''{
        PARTICIPANT} must be in the analysis_data'''
    subjectwise_averages = calculate_subjectwise_averages(
        analysis_data, alternative_hypotheses_per_measure.keys(), additional_groupers+[independent_variable])
    results = pd.DataFrame([], columns=[*additional_groupers, 'independent variable', MEASURE,
                                        f'normality {independent_factors[0]}', f'''normality {
                                            independent_factors[0]} {PVALUE}''',
                                        f'normality {independent_factors[1]}', f'''normality {
                                            independent_factors[1]} {PVALUE}''',
                                        'test', ALTERNATIVE_HYPOTHESIS, PVALUE, 'alpha', 'decision',
                                        'effect size', 'effect strength'])
    decision_position = list(results.columns).index(
        'decision')-results.shape[1]
    test_settings = subjectwise_averages[additional_groupers].drop_duplicates(
        keep='first')
    # default is 1 group
    if test_settings.empty:
        test_settings.index = [1]
    # test per group
    for i, setting in test_settings.iterrows():
        setting_data = subjectwise_averages
        if log:
            print(setting.to_dict())
        for grouper, setting_value in setting.items():
            setting_data = setting_data[setting_data[grouper] == setting_value]
        # get data
        factor0_data = setting_data[setting_data[independent_variable]
                                    == independent_factors[0]].sort_values(PARTICIPANT)
        factor1_data = setting_data[setting_data[independent_variable] ==
                                    independent_factors[1]].sort_values(PARTICIPANT)
        # elif SNIPPET_COLUMN_VARIANT in analysis_data.columns:
        #     confusing_data = setting_data[setting_data[SNIPPET_COLUMN_VARIANT]
        #                                   == SNIPPET_OBF].sort_values(PARTICIPANT)
        #     clean_data = setting_data[setting_data[SNIPPET_COLUMN_VARIANT]
        #                               == SNIPPET_CLEAN].sort_values(PARTICIPANT)
        # check test kind paired or independent
        if stest_kind == TEST_KIND_PAIRED:
            if not factor0_data[PARTICIPANT].reset_index(drop=True).equals(factor1_data[PARTICIPANT].reset_index(drop=True)):
                print(
                    'For paired test there must be pairwise data. Selecting independent test instead.')
                stest_kind = TEST_KIND_INDEPENDENT
        # per measure on data group
        for measure in alternative_hypotheses_per_measure:
            alternative_hypothesis = alternative_hypotheses_per_measure[measure]
            # test for normality
            if stest_kind == TEST_KIND_PAIRED:
                diff_text = f'diff_{independent_factors[0]}-{independent_factors[1]}'
                diff_normal, diff_normal_p = is_normally_distributed(
                    factor0_data[measure].reset_index(drop=True)-factor1_data[measure].reset_index(drop=True), f'''{measure} {diff_text}''', log)
                normality_data = [measure, diff_normal,
                                  diff_normal_p, diff_text, f'{diff_text} pvalue']
                is_normal = diff_normal
            elif stest_kind == TEST_KIND_INDEPENDENT:
                factor0_normal, factor0_normal_p = is_normally_distributed(
                    factor0_data[measure], f'{measure} {independent_factors[0]}', log)
                factor1_normal, factor1_normal_p = is_normally_distributed(
                    factor1_data[measure], f'{measure} {independent_factors[1]}', log)
                normality_data = [measure, factor0_normal,
                                  factor0_normal_p, factor1_normal, factor1_normal_p]
                is_normal = factor1_normal and factor0_normal
            else:
                raise Exception(
                    f'statistical test kind {stest_kind} not known')
            # decide for parametric or nonparametric test based on normality
            if is_normal:
                test = TEST[TEST_KIND_PARAMETRIC][stest_kind]
            else:
                test = TEST[TEST_KIND_NON_PARAMETRIC][stest_kind]
            # perform test in given direction
            test_data = perform_single_test(
                test, factor0_data[measure], factor1_data[measure], measure, alternative_hypothesis, log)
            results.loc[results.shape[0]] = setting.values.tolist() + [{independent_variable: independent_factors}] +\
                normality_data+test_data
            if test_data[decision_position] == STATISTIC_INFER_H1_NON_ACCEPTED:
                # if not accepted, test out reverse hypothesis
                alternative_hypothesis = get_reversed_alternative_hypothesis(
                    alternative_hypothesis)
                test_data = perform_single_test(
                    test, factor0_data[measure], factor1_data[measure], measure, alternative_hypothesis, log)
                results.loc[results.shape[0]
                            ] = setting.values.tolist() + [{independent_variable: independent_factors}]+normality_data+test_data
    return results


def calculate_subjectwise_averages(data: pd.DataFrame, categories: list[str], additional_groupers: list = []) -> pd.DataFrame:
    # subject-condition-wise mean and the standard deviation
    subjectwise_averages = data.groupby(list(set([CONDITION if CONDITION in data.columns else SNIPPET_COLUMN_VARIANT, PARTICIPANT, *additional_groupers]))).agg({
        c: [MEAN, STD] for c in categories})
    subjectwise_averages.columns = [
        (c if i == MEAN else f'{c} {i}') for c in categories for i in [MEAN, STD]]
    subjectwise_averages = subjectwise_averages.reset_index()
    return subjectwise_averages


def is_normally_distributed(data: pd.Series, description: str, log: bool = True) -> tuple[bool, float]:
    try:
        result = shapiro(data)
    except ValueError:
        if log:
            print(
                f'\t{description} there are too few samples to judge the distribution')
        return False, 1
    if result.pvalue < ALPHA:
        if log:
            print(
                f'\t{description} is not normally distributed due to {round(result.pvalue, 3)} less than alpha {ALPHA}; Result {result}')
        return False, result.pvalue
    if log:
        print(f'''\t{description} might be normally distributed due to {
              round(result.pvalue, 3)} greater equals to alpha {ALPHA}; Result {result}''')
    return True, result.pvalue


def perform_single_test(statistical_test: str, confusing_data: pd.Series, clean_data: pd.Series, measure: str, alternative_hypothesis: str, log: bool = True) -> list:
    if statistical_test == TEST_WILCOXON:
        parameters = {'x': confusing_data,
                      'y': clean_data,
                      'alternative': alternative_hypothesis,
                      'correction': True,
                      }
    elif statistical_test == TEST_MANNWHITNEYU:
        parameters = {'x': confusing_data,
                      'y': clean_data,
                      'alternative': alternative_hypothesis,
                      'use_continuity': True
                      }
    elif statistical_test in TEST[TEST_KIND_PARAMETRIC].values():
        parameters = {'a': confusing_data,
                      'b': clean_data,
                      'alternative': alternative_hypothesis,
                      'nan_policy': 'raise'
                      }
    result = TEST_FUNCTION[statistical_test](**parameters)
    alternative_hypothesis_text = f'''confusing {
        alternative_hypothesis} than clean'''
    decision = (STATISTIC_INFER_H1_ACCEPTED if result.pvalue <
                ALPHA else STATISTIC_INFER_H1_NON_ACCEPTED)
    if log:
        print(
            f'\tFor {measure}, the {statistical_test}\'s stance on the H1 `{alternative_hypothesis_text}` indicates with alpha={ALPHA} and the p-value of {round(result.pvalue, 3)}: {decision}; Result {result}')
    final = [statistical_test,
             alternative_hypothesis_text, result.pvalue, ALPHA, decision]
    if decision == STATISTIC_INFER_H1_ACCEPTED:
        effect_size, effect_strength = calculate_effect_size(
            statistical_test, confusing_data, clean_data)
        if log:
            print(f'\t\tEffect size {effect_size} {effect_strength}')
    else:
        effect_size, effect_strength = 0, 'None'
    return final+[effect_size, effect_strength]


def calculate_effect_size(statistical_test: str, confusing_data: pd.Series, clean_data: pd.Series):
    if statistical_test in TEST[TEST_KIND_PARAMETRIC].values():
        # calculate effect size using cohen's d
        clean_mean, clean_var = clean_data.agg([MEAN, 'var'])
        confusing_mean, confusing_var = confusing_data.agg([MEAN, 'var'])
        if statistical_test == TEST_T_PAIRED:
            # d=(m1−m2)/√((Var1+Var2)/2)
            pooled_std = sqrt((confusing_var+clean_var)/2)
            effect_size = (confusing_mean-clean_mean)/pooled_std
        elif statistical_test == TEST_T_INDEPENDENT:
            # d=(m1−m2)/√(((n1-1)*Var1+(n2-1)*Var2)/(n1+n2-2))
            clean_len_corr, confusing_len_corr = clean_data.shape[0] - \
                1, confusing_data.shape[0]-1
            pooled_std = sqrt((confusing_len_corr*confusing_var +
                              clean_len_corr*clean_var)/(confusing_len_corr+clean_len_corr))
            effect_size = (confusing_mean-clean_mean)/pooled_std
        effect_strength = EFFECT_STRENGTH_NEGLIGIBLE if abs(effect_size) < 0.2 else (
            EFFECT_STRENGTH_SMALL if abs(effect_size) < 0.5 else (EFFECT_STRENGTH_MEDIUM if abs(effect_size) < 0.8 else EFFECT_STRENGTH_LARGE))
    elif statistical_test in TEST[TEST_KIND_NON_PARAMETRIC].values():
        # calculate effect size using cliff's delta
        effect_size, _ = cliffs_delta(confusing_data, clean_data)
        # print(effect_size, effect_size_cliff)
        effect_strength = EFFECT_STRENGTH_NEGLIGIBLE if abs(effect_size) < 0.147 else (
            EFFECT_STRENGTH_SMALL if abs(effect_size) < 0.33 else (EFFECT_STRENGTH_MEDIUM if abs(effect_size) < 0.474 else EFFECT_STRENGTH_LARGE))
    return effect_size, effect_strength


def get_reversed_alternative_hypothesis(alternative_hypothesis: str):
    if alternative_hypothesis == ALTERNATIVE_HYPOTHESIS_GREATER:
        return ALTERNATIVE_HYPOTHESIS_LESS
    elif alternative_hypothesis == ALTERNATIVE_HYPOTHESIS_LESS:
        return ALTERNATIVE_HYPOTHESIS_GREATER
    raise Exception()


def test_significance_average_window(subjectwise_averages: dict[str, dict[str, mne.Evoked]], electrode: str, tmin: float, tmax: float, log: bool = True):
    assert tmin < tmax, f'tmin {tmin}  must be smaller than tmax {tmax}'
    subject_conditionwise_mean = pd.DataFrame(
        [], index=[], columns=[PARTICIPANT, CONDITION, EEG_MEAN_AMPLITUDE])
    for participant, c_averages in subjectwise_averages.items():
        for condition, average in c_averages.items():
            # electrode and time dimension
            electrode_data = average.get_data(
                electrode, tmin=tmin, tmax=tmax,units='uV')[0]
            # mean across time dimension in microvolt
            mean_electrode_data = np.mean(electrode_data)
            subject_conditionwise_mean.loc[subject_conditionwise_mean.shape[0]] = [
                participant, condition, mean_electrode_data]
    results = statistical_analysis_for_subjectwise_averages(subject_conditionwise_mean, {
                                                            EEG_MEAN_AMPLITUDE: ALTERNATIVE_HYPOTHESIS_GREATER}, [], TEST_KIND_PAIRED, log)
    results[CHANNEL] = electrode
    results['tmin'] = tmin
    results['tmax'] = tmax
    return results


def perform_cluster_permutation_test_diff(erp_frp: bool | str, snippet_group: str, correct_data_only: bool, epoch_interval: tuple[float, float], participants: list[str], subinterval: tuple[float, float] = (0, None), downsample_to: int = None, ignore_channels: list[str] = [], each_channel: bool = True, channel_combo: bool = True):
    assert (erp_frp is True or erp_frp in FIXATION_SELECTION_ALGORITHMS), erp_frp
    assert (downsample_to is None or (downsample_to > 0 and downsample_to < EEG_FREQUENCY)
            ), f'downsample_to must be either None or an integer between 0 and {EEG_FREQUENCY}'
    assert (all(channel in EEG_CHANNELS for channel in ignore_channels)
            ), f'all channels to ignore {ignore_channels} must be found in {EEG_CHANNELS}'
    description = get_erp_description(
        erp_frp, correct_data_only, epoch_interval)
    print(description)
    # set subinterval values
    if subinterval == (0, None):
        interval_description = 'allalong'
    else:
        interval_description = f'''{str(subinterval[0]).replace(
            ".", "")}-{str(subinterval[1]).replace(".", "")}'''
    if subinterval[0] is None or epoch_interval[0] > subinterval[0]:
        subinterval = epoch_interval[0], subinterval[1]
    if subinterval[1] is None or epoch_interval[1] < subinterval[1]:
        subinterval = subinterval[0], epoch_interval[1]
    assert (epoch_interval[0] < epoch_interval[1])
    assert (subinterval[0] < subinterval[1])
    # load subjectwise diff data
    subjectwise_diff: dict[str, dict[str, mne.Evoked]] = load_all_erp_averages(erp_frp, snippet_group, correct_data_only, epoch_interval,
                                                                               subjectwise=True, participants=participants, grand=False, diff=True, conditional=False)
    # downsample if required
    example = list(subjectwise_diff.values())[0][CONDITION_DIFF]
    example_info = example.info
    assert example_info[MNE_KEY_FREQUENCY] == EEG_FREQUENCY, example_info[MNE_KEY_FREQUENCY]
    if not downsample_to is None:
        for subject, diff in subjectwise_diff.items():
            subjectwise_diff[subject][CONDITION_DIFF] = diff[CONDITION_DIFF].resample(
                downsample_to)
    else:
        downsample_to = EEG_FREQUENCY

    example = list(subjectwise_diff.values())[0][CONDITION_DIFF]
    example_info = example.info
    # times = np.array([round_time_EEG(time) for time in times])
    times = np.asarray([time for time in example.times if subinterval[0]
                       <= round_time_EEG(time) <= subinterval[1]])
    # times = np.asarray(times[np.where(times <= subinterval[1])])
    # subinterval=subinterval[0]-sys.float_info.min, subinterval[1]+sys.float_info.min

    # temp write file
    all_file_buffer = JSONFileBuffers(get_erp_statistics_path(
        erp_frp, snippet_group, description, f'permutation swise diff {interval_description} {downsample_to}Hz', 'json', False), True)
    positive_file_buffer = JSONFileBuffers(get_erp_statistics_path(
        erp_frp, snippet_group, description, f'permutation swise diff {interval_description} {downsample_to}Hz', 'json', True), True)
    all_file_buffer.start()
    positive_file_buffer.start()
    # test parameters
    # channel-> test-> [cluster_count, positive_cluster_count, positive_clusters -> (positive_p_value, positive_cluster_range/array)]
    channels_to_iterate = []
    possible_channels = [
        channel for channel in EEG_CHANNELS if channel not in ignore_channels]
    if each_channel:
        channels_to_iterate += possible_channels
    if channel_combo:
        channels_to_iterate += [possible_channels]
    for channel in tqdm(channels_to_iterate):
        if isinstance(channel, list):
            channel_description = 'multiple channels' if ignore_channels else 'all channels'
        else:
            channel_description = channel
        print(channel_description)
        # create ndarray with dimensions (subjects x times x electrodes), pairwise via diff values
        subjectwise_diff_data = []
        for participant in sorted(subjectwise_diff.keys()):
            evoked = subjectwise_diff[participant][CONDITION_DIFF]
            times = np.asarray([time for time in evoked.times if subinterval[0]
                               <= round_time_EEG(time) <= subinterval[1]])
            data = evoked.get_data(channel,units='uV')
            new_data = data[:, list(evoked.times).index(
                times[0]):list(evoked.times).index(times[-1])+1]
            if isinstance(channel, list):
                data = np.transpose(new_data)
            else:
                data = new_data[0]
            # print(data)
            subjectwise_diff_data.append(data)
        subjectwise_diff_data = np.asarray(subjectwise_diff_data)
        print('\tsubjects x times (x electrodes)', subjectwise_diff_data.shape)
        assert (subjectwise_diff_data.shape[1] == times.shape[0]
                ), f'({subjectwise_diff_data.shape[1]}, {times}) ({times.shape[0]}, {times})'
        # set up channel adjacency
        channel_adjacency, _ = get_channel_adjacency(
            channel, example_info)

        # perform permutation tests
        test_clusters = {}
        for test_side in PERMUTATION_TEST_PARAMETERS[TEST_KIND_PAIRED]:
            print('\tTest', test_side)
            # incrementally increase number of permutations if pvalue not confident
            permutation_count = PERMUTATION_COUNT_MAX
            test_clusters[test_side] = []
            while True:
                print('\t\tPermutation count', permutation_count)
                T_obs, clusters, cluster_p_values, H0, positive_clusters = perform_permutation_cluster_1samp_test(
                    subjectwise_diff_data, channel_adjacency, **PERMUTATION_TEST_PARAMETERS[TEST_KIND_PAIRED][test_side], n_permutations=permutation_count,
                    max_step=calculate_max_step(downsample_to))
                results = {ERP_PERM_PARAMETER_CHANNEL_DESCRIPTION: channel_description, ERP_PARAMETER_SNIPPET_GROUP: snippet_group, ALTERNATIVE_HYPOTHESIS: test_side,
                           ERP_PERM_PARAMETER_CHANNELS: channel, ERP_PERM_PARAMETER_PERMUTATION_COUNT: H0.shape[0],
                           ERP_PERM_PARAMETER_CLUSTER_COUNT: len(clusters), ERP_PERM_PARAMETER_POSITIVE_CLUSTER_COUNT: len(positive_clusters), ERP_PERM_PARAMETER_POSITIVE_CLUSTERS: [],
                           ERP_PERM_PARAMETER_NEGATIVE_CLUSTER_COUNT: len(clusters)-len(positive_clusters), ERP_PERM_PARAMETER_NEGATIVE_CLUSTERS: [],
                           ERP_PARAMETER_ERP_FRP: erp_frp, ERP_PARAMETER_EPOCH_INTERVAL: list(epoch_interval), ERP_PERM_PARAMETER_SUBINTERVAL: list(subinterval),
                           ERP_PARAMETER_CORRECT_TRIALS_ONLY: correct_data_only, ERP_PARAMETER_PARTICIPANTS: participants,
                           ERP_PERM_PARAMETER_T_STATISTICS: T_obs, ERP_PERM_PARAMETER_H0: H0, ERP_PERM_PARAMETER_P_VALUES_CONFIDENT: False, ERP_PERM_PARAMETER_FREQUENCY: downsample_to}
                if results[ERP_PERM_PARAMETER_CLUSTER_COUNT] > results[ERP_PERM_PARAMETER_POSITIVE_CLUSTER_COUNT]:
                    results[ERP_PERM_PARAMETER_NEXT_P_VALUE] = cluster_p_values[np.where(
                        cluster_p_values > ALPHA)].min()
                else:
                    results[ERP_PERM_PARAMETER_NEXT_P_VALUE] = 'No cluster not accepted'
                # add per cluster p value and range / array

                for cluster_index, cluster in enumerate(clusters):
                    cluster_data = {
                        ERP_PERM_CLUSTER_PARAMETER_P_VALUE: cluster_p_values[cluster_index]}
                    if isinstance(channel, list):
                        cluster_range = np.argwhere(cluster)
                        cluster_data[ERP_PERM_CLUSTER_PARAMETER_TIMES] = [round_time_EEG(
                            times[time]) for time in np.unique(cluster_range[:, 0])]
                        cluster_data[ERP_PERM_CLUSTER_PARAMETER_CHANNELS] = [channel[c]
                                                                             for c in np.unique(cluster_range[:, 1])]
                        cluster_range = * \
                            np.min(cluster_range, axis=0), * \
                            np.max(cluster_range, axis=0)
                        cluster_range = [cluster_range[0], cluster_range[2]], [
                            cluster_range[1], cluster_range[3]]
                        cluster_data[ERP_PERM_CLUSTER_PARAMETER_TIME_RANGE] = [round_time_EEG(
                            times[cluster_range[0][0]]), round_time_EEG(times[cluster_range[0][1]])]
                        cluster_data[ERP_PERM_CLUSTER_PARAMETER_CHANNEL_RANGE] = [
                            channel[cluster_range[1][0]], channel[cluster_range[1][1]]]
                        cluster_data[ERP_PERM_CLUSTER_PARAMETER_CLUSTER] = cluster
                    else:
                        cluster_range = np.argwhere(cluster).reshape((-1,))
                        cluster_data[ERP_PERM_CLUSTER_PARAMETER_TIMES] = [round_time_EEG(
                            times[time]) for time in cluster_range]
                        cluster_range = [
                            np.min(cluster_range), np.max(cluster_range)]
                        cluster_data[ERP_PERM_CLUSTER_PARAMETER_TIME_RANGE] = [round_time_EEG(
                            times[cluster_range[0]]), round_time_EEG(times[cluster_range[1]])]
                    results[ERP_PERM_PARAMETER_POSITIVE_CLUSTERS if cluster_index in positive_clusters else ERP_PERM_PARAMETER_NEGATIVE_CLUSTERS].append(
                        cluster_data)
                test_clusters[test_side].append(results)
                # get the permutation count for which p is a confident result
                confident_permutation_counts = [
                    calculate_required_permutation_count(p) for p in cluster_p_values]
                results[ERP_PERM_PARAMETER_REQUIRED_PERMUTATION_COUNTS] = confident_permutation_counts
                if len(clusters) == 0:
                    results[ERP_PERM_PARAMETER_P_VALUES_CONFIDENT] = True
                    break
                # if exact test (perm count > shape of H0 portraying the actual permutation count)
                if permutation_count > H0.shape[0]:
                    print(
                        '\t\t\t', f'Stop after exact test results, as {permutation_count} exceeds possible {H0.shape[0]}')
                    results[ERP_PERM_PARAMETER_P_VALUES_CONFIDENT] = True
                    break
                # #  select the highest permutation count required for the p values
                # new_permutation_count = ceil(
                #     (max(confident_permutation_counts)+1)/100+1)*100
                # # if lower, then we can be confident and stop
                # if new_permutation_count <= permutation_count:
                #     print(
                #         '\t\t\t', f'Achieved satisfaction in permutation_count, as {permutation_count} exceeds or is equal to required {new_permutation_count}')
                #     results[ERP_PERM_PARAMETER_P_VALUES_CONFIDENT] = True
                #     break
                # # if too high, check the distance
                # elif new_permutation_count > PERMUTATION_COUNT_MAX:
                #     # if distance low, redo with max
                #     if abs(new_permutation_count-permutation_count) > PERMUTATION_COUNT_MAX/10:
                #         permutation_count = PERMUTATION_COUNT_MAX
                #         continue
                #     # otherwise stop
                #     else:
                #         print(
                #             '\t\t\t', f'No satisfaction in permutation_count achievable, as {new_permutation_count} exceeds maximum {PERMUTATION_COUNT_MAX}')
                #         break
                # permutation_count = new_permutation_count
                break
        all_file_buffer.data_chunk(
            test_clusters, channel_description, JSONTypesEncoder)
        # for all positive cases, take the last entry only if that one is positive
        positive_test_clusters = {test_side: test_results[-1] for test_side, test_results in test_clusters.items(
        ) if test_results[-1][ERP_PERM_PARAMETER_POSITIVE_CLUSTER_COUNT] > 0}
        positive_file_buffer.data_chunk(
            positive_test_clusters, channel_description, JSONTypesEncoder)
        # plot results
        if positive_test_clusters:
            fig, fig_dataframes = plot_permutation_clusters(positive_test_clusters, [round_time_EEG(time) for time in times], channel, {
                                            CONDITION_DIFF: subjectwise_diff_data.mean(axis=0)})
            fig_path = get_erp_statistics_path(
                erp_frp, snippet_group, description, 
                f'permutation swise diff {interval_description} {downsample_to}Hz', 'png', True)
            # fig_path = fig_path.with_stem(fig_path.stem+'_'+channel_description)
            # create and store contours
            contours_only_image = add_store_contours(fig)
            # plot
            if len(fig.get_axes())>2:
                fig.get_axes()[2].imshow(contours_only_image)
            plt.show()
            # save all plots
            fig.savefig(fig_path.with_stem(
                fig_path.stem+'_special_contours'))
            plt.close(fig)
            matplotlib.image.imsave(fig_path.with_stem(
                fig_path.stem+'_only_contours'), contours_only_image.copy(order='C'))
            fig_data_path = get_erp_statistics_path(
                erp_frp, snippet_group, description, 
                f'permutation swise diff {interval_description} {downsample_to}Hz', 'csv', True)
            fig_dataframes[0].to_csv(fig_data_path.with_stem('Data Figure2c amplitudes'), sep=SEPARATOR)
            for i, dataframe in enumerate(fig_dataframes[1:]):
                dataframe.to_csv(fig_data_path.with_stem(f'Data Figure2c cluster{i} mask'), sep=SEPARATOR)
    # finish file buffer
    all_file_buffer.end()
    positive_file_buffer.end()


def add_store_contours(fig:plt.figure):
    axes = fig.get_axes()
    # Extract the color data for all entries from the 2nd axis
    cluster_image = axes[1].images[1].make_image(renderer=None, unsampled=True)[0]
    # transform the color data into pixels of image resolution
    cluster_image_pixels = np.kron(cluster_image, 
                                    np.ones((PERMUTATION_PLOT_PIXEL_Y, PERMUTATION_PLOT_PIXEL_X, 1)).astype(np.uint8)).astype(np.uint8)
    print(cluster_image_pixels.shape)
    # Convert the image to a format suitable for OpenCV
    cluster_image_cv2 = cv2.cvtColor(cluster_image_pixels, cv2.COLOR_RGBA2RGB)
    mask = cv2.inRange(cluster_image_cv2, (0,0,0), (0,0,0))
    # Find contours in the mask, including small holes
    contours_with_contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Create an empty image to draw the contours on
    contours_only_image = np.zeros_like(cluster_image_cv2)
    contours_only_image.fill(255)
    cv2.drawContours(contours_only_image, contours_with_contours, -1, (0, 0, 0), 2)
    # correct contours at the borders
    contours_only_image[:,:2] = contours_only_image[:,2:4]
    contours_only_image[:,-2:] = contours_only_image[:,-4:-2]
    contours_only_image[:2,:] = contours_only_image[2:4,:]
    contours_only_image[-2:,:] = contours_only_image[-4:-2,:]
    # add alpha channel
    alpha = (255-contours_only_image[:,:,0]).reshape((*contours_only_image.shape[:2], 1))
    contours_only_image = np.concatenate((contours_only_image, alpha), axis=2)
    # flip for correct orientation
    contours_only_image = np.flipud(contours_only_image)
    return contours_only_image


def get_channel_adjacency(channels, info):
    # set up channel adjacency
    if isinstance(channels, list):
        channel_adjacency, all_channels = mne.channels.find_ch_adjacency(
            info, 'eeg')
        if channels != all_channels:
            channel_indices = [all_channels.index(
                channel) for channel in channels]
            keep_col = np.in1d(
                np.arange(channel_adjacency.shape[1]), channel_indices, assume_unique=True)
            keep_cols = np.tile(keep_col, (keep_col.shape[0], 1))
            keep = np.logical_and(keep_cols, keep_cols.T)
            channel_adjacency = scipy.sparse.csr_matrix(
                channel_adjacency[np.where(keep)].reshape((len(channels), len(channels))))
    else:
        channel_adjacency = scipy.sparse.csr_matrix(np.ones((1, 1)))
        channels = [channels]
    return channel_adjacency, channels


def calculate_max_step(eeg_frequency: int = EEG_FREQUENCY):
    # max_step varies with frequency, bit should be at least 1 to connect adjacent time points
    return max(1, int(PERMUTATION_MAX_STEP_FREQUENCY_FACTOR*eeg_frequency))


def perform_permutation_cluster_1samp_test(data, adjacency, tail, n_permutations=PERMUTATION_COUNT, max_step=int(PERMUTATION_MAX_STEP_FREQUENCY_FACTOR*EEG_FREQUENCY)):
    import warnings
    warnings.filterwarnings('ignore')
    T_obs, clusters, cluster_p_values, H0 = mne.stats.permutation_cluster_1samp_test(data, n_permutations=n_permutations, threshold=None,
                                                                                     tail=tail, adjacency=adjacency, out_type='mask', verbose=True, max_step=max_step)
    warnings.filterwarnings('error')
    positive_clusters = analyze_clusters(clusters, cluster_p_values)
    return T_obs, clusters, cluster_p_values, H0, positive_clusters


def perform_permutation_cluster_test(data, adjacency, tail, n_permutations=PERMUTATION_COUNT, max_step=int(PERMUTATION_MAX_STEP_FREQUENCY_FACTOR*EEG_FREQUENCY)):
    T_obs, clusters, cluster_p_values, H0 = mne.stats.permutation_cluster_test(data, n_permutations=n_permutations,  threshold=None,
                                                                               tail=tail, adjacency=adjacency, out_type='mask', verbose=True, max_step=max_step)
    positive_clusters = analyze_clusters(clusters, cluster_p_values)
    return T_obs, clusters, cluster_p_values, H0, positive_clusters


def analyze_clusters(clusters, cluster_p_values):
    if len(clusters) == 0:
        return []
    # if isinstance(clusters[0], np.ndarray):
    #     print(clusters[0].shape, [np.count_nonzero(cluster*1) for cluster in clusters])
    # else:
    #     print([cluster[0].stop-cluster[0].start for cluster in clusters])
    print('\t\t\t', 'P values', cluster_p_values)
    positive_clusters = np.where(cluster_p_values <= ALPHA)[0]
    print('\t\t\t', 'positive clusters', positive_clusters)
    return positive_clusters


def calculate_required_permutation_count(p_value: float, confidence=PERMUTATION_CONFIDENCE_INTERVAL):
    confidence_ztable = norm.ppf(confidence)
    if abs(p_value-ALPHA) < 1e-8:
        p_value = ALPHA-1e-8
    return (p_value*(1-p_value))/(((ALPHA-p_value)/confidence_ztable)**2)


def plot_permutation_clusters(test_clusters: dict[str, dict[str, Any]], times: np.ndarray, channels: list[str], channel_data: dict[str, np.ndarray] = None):
    if any([test_results[ERP_PERM_PARAMETER_POSITIVE_CLUSTER_COUNT] > 0 for test_results in test_clusters.values()]):
        any_hypothesis = list(test_clusters.keys())[0]
        all_plot = channel_data[CONDITION_DIFF]
        cluster_plot = all_plot.copy()
        if isinstance(test_clusters[any_hypothesis][ERP_PERM_PARAMETER_CHANNELS], list):
            all_positive_clusters = np.full_like(
                test_clusters[any_hypothesis][ERP_PERM_PARAMETER_POSITIVE_CLUSTERS][0][ERP_PERM_CLUSTER_PARAMETER_CLUSTER], False)
            for test_side, test_results in test_clusters.items():
                for positive_clusters in test_results[ERP_PERM_PARAMETER_POSITIVE_CLUSTERS]:
                    all_positive_clusters = np.logical_or(
                        all_positive_clusters, positive_clusters[ERP_PERM_CLUSTER_PARAMETER_CLUSTER])
            cluster_plot[~all_positive_clusters] = np.nan
            fig, ax = plt.subplots(3, 1, figsize=(12, 12), layout='constrained')
            max_value_plot = abs(all_plot.T).max(axis=None)
            plot_2d_cluster_heatmap(
                fig, ax[0], all_plot, cluster_plot, times, channels, max_value_plot)
            # # order electrode channels by highest value in cluster
            # max_values_cluster = pd.Series(
            #     np.nanmax(cluster_plot, axis=0, initial=0)).sort_values().to_frame()
            # max_values_array = np.repeat(max_values_cluster.index.values, len(
            #     times), axis=0).reshape((max_values_cluster.shape[0], len(times))).T
            # cluster_plot2 = np.take_along_axis(
            #     cluster_plot, max_values_array, axis=1)
            # all_plot2 = np.take_along_axis(all_plot, max_values_array, axis=1)
            plot_2d_cluster_heatmap(
                fig, ax[1], all_plot, cluster_plot, times, channels, max_value_plot, color_diff=True)
            all_dataframe = pd.DataFrame(all_plot, index=times, columns=channels)
            cluster_dataframes = [pd.DataFrame(positive_clusters[ERP_PERM_CLUSTER_PARAMETER_CLUSTER], 
                                  index=times, columns=channels) for _, test_results in test_clusters.items() for positive_clusters in test_results[ERP_PERM_PARAMETER_POSITIVE_CLUSTERS]]
            return fig, [all_dataframe, *cluster_dataframes]
        else:
            ms_times = [int(round(time*1000, 0)) for time in times]
            fig, (ax, ax2) = plt.subplots(2, 1, figsize=(8, 4))
            ax.set_title('Channel : ' +
                         test_clusters[any_hypothesis][ERP_PERM_PARAMETER_CHANNELS])
            for condition in channel_data:
                ax.plot(times, channel_data[condition],
                        label=condition, c=CONDITION_COLORS[condition])
            ax.set_ylabel('EEG microV')
            ax.legend()
            legend_handler = [], []
            for test_side, test_results in test_clusters.items():
                for positive_clusters in test_results[ERP_PERM_PARAMETER_POSITIVE_CLUSTERS]:
                    for time in positive_clusters[ERP_PERM_CLUSTER_PARAMETER_TIMES]:
                        h = ax2.axvspan(
                            time, time+1/test_results[ERP_PERM_PARAMETER_FREQUENCY], color=PERMUTATION_TEST_COLORS[test_side], alpha=0.3)
                if test_results[ERP_PERM_PARAMETER_POSITIVE_CLUSTERS]:
                    legend_handler[0].append(h)
                    legend_handler[1].append(test_side)
            _ = plt.plot(ms_times, all_plot, 'k')
            ax2.legend(*legend_handler)
            ax.set_xlabel('Time (ms)')
            ax2.set_ylabel('f-values')
            return fig, [pd.from_dict(channel_data, index=times), *[
                pd.Series(positive_clusters[ERP_PERM_CLUSTER_PARAMETER_TIMES]) 
                for _, test_results in test_clusters.items() 
                for positive_clusters in test_results[ERP_PERM_PARAMETER_POSITIVE_CLUSTERS]]]

def plot_2d_cluster_heatmap(fig, ax, all_plot: np.ndarray, cluster_plot: np.ndarray, 
                            times: np.ndarray, channels: list[str], max_value: float, 
                            color_diff: bool = False, color_all: bool = True):
    assert(color_all or color_diff), 'at least one aspect must be colored'
    channels = list(reversed(channels))
    # Adjust saturation of the color map
    if color_all:
        c1 = ax.imshow(np.flip(all_plot.T, axis=0), cmap='RdBu_r', aspect='auto', origin='lower',
                    norm=plt.Normalize(vmin=-max_value, vmax=max_value),)
    else: 
        # grey background
        new_colors = plt.get_cmap('bwr')(np.linspace(0, 1, 256))
        new_colors[:, :3] = [(0.5,0.5,0.5) for _ in new_colors[:, :3]]
        new_map = LinearSegmentedColormap.from_list('bwr_dull', new_colors)
        c1 = ax.imshow(np.flip(all_plot.T, axis=0), cmap=new_map, aspect='auto', origin='lower',
                    norm=plt.Normalize(vmin=-max_value, vmax=max_value),)
    if color_diff:
        c2 = ax.imshow(np.flip(cluster_plot.T, axis=0), cmap='BrBG_r', aspect='auto',
                    origin='lower', norm=plt.Normalize(vmin=-max_value, vmax=max_value))
    if color_all:
        cbar = fig.colorbar(c1, ax=ax, label='amplitude differences (ambiguous - unambiguous)', )
        cbar.ax.set_title('µV')
    if color_diff:
        cbar = fig.colorbar(c2, ax=ax, label='amplitude differences in significant cluster')
        cbar.ax.set_title('µV')
    if len(times) <= 20:
        ax.set_xticks(np.arange(0, len(times)), [
                      int(round_time_EEG(time*1000)) for time in times])
    else:
        TICK_TIME_DISTANCE = 0.05
        last_tick_name_time = times[0]
        tick_names = [int(round(times[0]*1000, 0))]
        for time in times[1:]:
            rtime = round_time_EEG(time)
            next_tick_time = round_time_EEG(
                last_tick_name_time+TICK_TIME_DISTANCE)
            if rtime >= next_tick_time:
                tick_names.append(int(round(rtime*1000, 0)))
                last_tick_name_time = rtime
            else:
                tick_names.append('')
        ax.set_xticks(np.arange(0, len(times)), tick_names)
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Electrodes')
    ax.set_yticks(np.arange(0, len(channels)), channels)


def analyze_statistics_distribution(erp_frp: bool | str, snippet_group: str, description: str, fixation_analysis_data: pd.DataFrame, analysis_topic: str, analysis_column: str):
    conditional_offset, participant_conditional_offset = statistics_distribution(
        erp_frp, snippet_group, description, fixation_analysis_data, analysis_topic, analysis_column)
    participant_conditional_offset = participant_conditional_offset[['mean']]
    participant_conditional_offset.columns = [analysis_column]
    participant_conditional_offset = participant_conditional_offset.reset_index()
    stat_results = statistical_analysis_for_subjectwise_averages(participant_conditional_offset, {
                                                                 analysis_column: ALTERNATIVE_HYPOTHESIS_GREATER}, [], TEST_KIND_PAIRED)
    stat_results.to_csv(get_erp_fixation_analysis_path(erp_frp, snippet_group,
                        f'{description}_participant_statistics', analysis_topic+'_stat_test'), index=False, sep=SEPARATOR)
    return stat_results
