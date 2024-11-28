import json

import numpy as np
import pandas as pd
import rpy2


LMEM_FAMILY_BINOMIAL = 'binomial'
LMEM_FAMILY_GAUSSIAN = 'gaussian'
LMEM_FAMILY_GAMMA = 'Gamma'
LMEM_FAMILY_POISSON = 'Poisson'
LMEM_ERROR_IDENTITY = 'identity'
LMEM_ERROR_LOG = 'log'

LMEM_RESULT_MODEL = 'model'
LMEM_RESULT_SUMMARY = 'summary'
LMEM_RESULT_ANOVA = 'anova'
LMEM_RESULT_FIXED_EFFECTS = 'fixed effects'
LMEM_RESULT_TERMS = 'terms'
LMEM_RESULT_RANDOM_EFFECTS = 'random effects'
LMEM_RESULT_COEFFICIENTS = 'coefficients'
LMEM_RESULT_FORMULA = 'formula'
LMEM_RESULT_FAMILY = 'family'
LMEM_RESULT_CONF_INT = 'confidence intervals'
LMEM_RESULTS = [LMEM_RESULT_MODEL,
                LMEM_RESULT_SUMMARY,
                LMEM_RESULT_ANOVA,
                LMEM_RESULT_FIXED_EFFECTS,
                LMEM_RESULT_TERMS,
                LMEM_RESULT_RANDOM_EFFECTS,
                LMEM_RESULT_COEFFICIENTS,
                LMEM_RESULT_FORMULA,
                LMEM_RESULT_FAMILY,
                LMEM_RESULT_CONF_INT]

ENCODING_CP1252 = 'cp1252'


def cchar_to_str(c, encoding: str = ENCODING_CP1252) -> str:
    s = rpy2.rinterface_lib.openrlib.ffi.string(c).decode(encoding)
    return s


def cchar_to_str_with_maxlen(c, maxlen: int, encoding: str = ENCODING_CP1252) -> str:
    s = rpy2.rinterface_lib.openrlib.ffi.string(
        c, maxlen).decode(ENCODING_CP1252)
    return s


class RTypesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, pd.DataFrame):
            return obj.to_dict(orient='index')
        if isinstance(obj, pd.Series):
            return obj.to_dict()
        if isinstance(obj, rpy2.robjects.Vector):
            return [i for i in obj.items()]
        if isinstance(obj, rpy2.rinterface_lib.sexp.NULLType):
            return None
        if isinstance(obj, rpy2.robjects.language.LangVector):
            return repr(obj)
        if isinstance(obj, rpy2.robjects.Environment):
            return [k for k in obj.keys()]
        if isinstance(obj, rpy2.robjects.Formula) or isinstance(obj, rpy2.robjects.methods.RS4):
            obj_dict = {}
            for k, value in obj.slots.items():
                # print(k, type(value))
                obj_dict[k] = self.default(value)
            return obj_dict
        print(type(obj))
        return json.JSONEncoder.default(self, obj)
