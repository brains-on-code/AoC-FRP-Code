import numpy as np
import seaborn as sns

SNIPPET_CLEAN = 'clean'
SNIPPET_OBF = 'obf'

CONDITION = 'Condition'
CONDITION_CLEAN = 'unambiguous'
CONDITION_CONFUSING = 'ambiguous'
CONDITION_DIFF = f'diff_{CONDITION_CONFUSING}-{CONDITION_CLEAN}'

CONDITION_VARIANT_MATCH = {
    SNIPPET_CLEAN: CONDITION_CLEAN,
    SNIPPET_OBF: CONDITION_CONFUSING
}

SNIPPET_NUMBERS = [
    0, *range(4, 18+1), 30, 49, 54, 57, *range(60, 63+1)
]
SNIPPET_GROUP_ALL = 'all'

CONDITION_COLORS = {CONDITION_CONFUSING: '#c55a11',  # RGB: (197,90,17), dark orange
                    # RGB: (47,85,151), dark blue
                    CONDITION_CLEAN: '#2f5597',
                    CONDITION_DIFF: '#54822b'}  # RGB: (84,130,53), dark green
sns.set_palette([
    CONDITION_COLORS[CONDITION_CLEAN],
    CONDITION_COLORS[CONDITION_CONFUSING],
    CONDITION_COLORS[CONDITION_DIFF]])

RATING_EASY = 'easy'
RATING_HARD = 'hard'
RATINGS = [RATING_EASY, RATING_HARD, np.nan]


ANSWER_CORRECTNESS = [True, False, np.nan]

PANDAS_DESCRIPTION_AGG_FUNCTIONS = ['count', 'mean', 'std', 'min', lambda x: np.percentile(
    x, q=25), 'median', lambda x: np.percentile(x, q=75), 'max']
PANDAS_DESCRIPTION_AGG_NAMES = [
    'count', 'mean', 'std', 'min', '25%', 'median', '75%', 'max']
