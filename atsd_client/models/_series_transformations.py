import numbers
from ._data_queries import Interval, is_interval, TimeUnit


unicode = str


# ------------------------------------------------------------------------------
class StatisticalFunction:
    MIN = "MIN"
    MAX = "MAX"
    AVG = "AVG"
    SUM = "SUM"
    COUNT = "COUNT"
    FIRST = "FIRST"
    LAST = "LAST"
    DELTA = "DELTA"
    COUNTER = "COUNTER"
    MEDIAN = "MEDIAN"
    STANDARD_DEVIATION = "STANDARD_DEVIATION"
    MEDIAN_ABS_DEV = "MEDIAN_ABS_DEV"
    SLOPE = "SLOPE"
    INTERCEPT = "INTERCEPT"
    WAVG = "WAVG"
    WTAVG = "WTAVG"
    THRESHOLD_COUNT = "THRESHOLD_COUNT"
    THRESHOLD_DURATION = 'THRESHOLD_DURATION'
    THRESHOLD_PERCENT = 'THRESHOLD_PERCENT'
    MIN_VALUE_TIME = "MIN_VALUE_TIME"
    MAX_VALUE_TIME = "MAX_VALUE_TIME"
    VARIANCE = "VARIANCE"
    POPULATION_VARIANCE = "POPULATION_VARIANCE"


# ------------------------------------------------------------------------------
class SmoothType:
    AVG = "AVG"
    COUNT = "COUNT"
    SUM = "SUM"
    WAVG = "WAVG"
    WTAVG = "WTAVG"
    EMA = "EMA"


# ------------------------------------------------------------------------------
class DownsampleAlgorithm:
    DETAIL = "DETAIL"
    INTERPOLATE = "INTERPOLATE"


# ------------------------------------------------------------------------------
class EvaluateMode:
    STRICT = "STRICT"
    NOT_STRICT = "NOT_STRICT"


# ------------------------------------------------------------------------------
class DecomposeMethod:
    FULL = "FULL"
    TRUNCATED = "TRUNCATED"
    AUTO = "AUTO"


# ------------------------------------------------------------------------------
class ReconstructAveragingFunction:
    AVG = "AVG"
    MEDIAN = "MEDIAN"


# ------------------------------------------------------------------------------
class SsaForecastMethod:
    RECURRENT = "RECURRENT"
    VECTOR = "VECTOR"


# ------------------------------------------------------------------------------
class SsaForecastBase:
    RECONSTRUCTED = "RECONSTRUCTED"
    ORIGINAL = "ORIGINAL"


# ------------------------------------------------------------------------------
class SsaGroupAutoClusteringMethod:
    HIERARCHICAL = "HIERARCHICAL"
    XMEANS = "XMEANS"
    NOVOSIBIRSK = "NOVOSIBIRSK"


def set_if_type_is_valid(obj, name, value, expected_type):
    if not isinstance(value, expected_type):
        raise ValueError(name + " expected to be a " + str(expected_type) + " found: " + unicode(type(value)))
    setattr(obj, name, value)


def set_if_has_attr(obj, name, value, expected_attr_owner):
    if not hasattr((expected_attr_owner, value)):
        raise ValueError(name + " expected to be one of " + expected_attr_owner + " attributes, found: " + str(value))
    setattr(obj, name, value)


def set_if_interval(obj, name, value):
    if not is_interval(value):
        raise ValueError(name + " expected to be an Interval instance, found: " + unicode(type(value)))
    setattr(obj, name, value)


class Smooth:
    """
    Class representing transformation param 'smooth'
    """

    def __init__(self, smoothType, count=None, interval=None, minimumCount=None, incompleteValue=None):
        if not hasattr(SmoothType, smoothType):
            raise ValueError('Invalid type parameter, expected SmoothType, found: ' + unicode(type(smoothType)))
        self.type = smoothType
        if count is not None:
            self.count = count
        if interval is not None:
            self.interval = interval
        if minimumCount is not None:
            self.minimumCount = minimumCount
        if incompleteValue is not None:
            self.incompleteValue = incompleteValue

    def set_type(self, smoothType):
        if not hasattr(SmoothType, smoothType):
            raise ValueError('Invalid type parameter, expected SmoothType, found: ' + unicode(type(smoothType)))
        self.type = smoothType

    def set_count(self, count):
        if not isinstance(count, numbers.Number):
            raise ValueError('Count must be a number, found: ' + unicode(type(count)))
        self.count = count

    def set_interval(self, count, unit):
        if not isinstance(count, numbers.Number):
            raise ValueError('Interval count must be a number, found: ' + unicode(type(count)))
        if not hasattr(TimeUnit, unit):
            raise ValueError('Invalid interval unit')
        self.interval = {'count': count, 'unit': unit}

    def set_interval(self, interval):
        if not is_interval(interval):
            raise ValueError('Interval expected to be of Interval instance, found: ' + unicode(type(interval)))
        self.interval = interval

    def set_minimumCount(self, minimumCount):
        if not isinstance(minimumCount, numbers.Number):
            raise ValueError('Minimum count must be a value, found: ' + unicode(type(minimumCount)))
        self.minimumCount = minimumCount

    def set_incompleteValue(self, incompleteValue):
        if not isinstance(incompleteValue, str):
            raise ValueError('Incomplete value must be string, found: ' + unicode(type(incompleteValue)))
        self.incompleteValue = incompleteValue


class Downsample:
    """
    Class representing transformation param 'downsample'
    """

    def __init__(self, algorithm=None, difference=None, ratio=None, gap=None):
        if algorithm is not None:
            self.algorithm = algorithm
        if difference is not None:
            self.difference = difference
        if ratio is not None:
            self.ratio = ratio
        if gap is not None:
            self.gap = gap

    def set_algorithm(self, algorithm):
        if not hasattr(DownsampleAlgorithm, algorithm):
            raise ValueError('Invalid algorithm parameter, expected DownsampleAlgorithm, found: ' + str(algorithm))
        self.algorithm = algorithm

    def set_difference(self, difference):
        if not isinstance(difference, numbers.Number):
            raise ValueError('Invalid difference parameter, expected number, found: ' + unicode(type(difference)))
        self.difference = difference

    def set_ratio(self, ratio):
        if not isinstance(ratio, numbers.Number):
            raise ValueError('Invalid ratio parameter, expected number, found: ' + unicode(type(ratio)))
        self.ratio = ratio

    def set_gap(self, count, unit):
        if not isinstance(count, numbers.Number):
            raise ValueError('Gap count must be a number, found: ' + unicode(type(count)))
        if not hasattr(TimeUnit, unit):
            raise ValueError('Invalid gap unit ' + str(unit))
        self.gap = {'count': count, 'unit': unit}

    def set_gap(self, gap):
        if not is_interval(gap):
            raise ValueError("Gap expected to be an Interval, found: " + unicode(type(gap)))
        self.gap = gap


class Evaluate:
    """
    Class representing transformation param 'evaluate'
    """

    def __init__(self, mode=None, libs=None, expression=None, script=None, order=None, timezone=None):
        if mode is not None:
            self.mode = mode
        if libs is not None:
            self.libs = [libs] if not isinstance(libs, list) else libs
        if expression is not None:
            self.expression = expression
        if script is not None:
            self.script = script
        if order is not None:
            self.order = order
        if timezone is not None:
            self.timezone = timezone

    def set_mode(self, mode):
        if not hasattr(EvaluateMode, mode):
            raise ValueError('Mode must be one of EvaluateMode attributes, found: ' + str(mode))
        self.mode = mode

    def set_libs(self, libs):
        self.libs = [libs] if not isinstance(libs, list) else libs

    def set_expression(self, expression):
        self.expression = expression

    def set_script(self, script):
        self.script = script

    def set_order(self, order):
        if not isinstance(order, numbers.Number):
            raise ValueError('Order must be a number, found: ' + unicode(type(order)))
        self.order = order

    def set_timezone(self, timezone):
        self.timezone = timezone


# =======================================================================
# Forecast Transformation
# =======================================================================
class ForecastTransformation:

    def __init__(self, autoAggregate=None, aggregationFunction=None, include=None, scoreInterval=None, forecastRange=None,
                    holtwinters=None, arima=None, ssa=None, horizon=None, baseline=None):
        if autoAggregate is not None:
            self.autoAggregate = autoAggregate
        if aggregationFunction is not None:
            self.aggregationFunction = aggregationFunction
        if include is not None:
            self.include =[include] if not isinstance(include, list) else include
        if scoreInterval is not None:
            self.scoreInterval = scoreInterval
        if forecastRange is not None:
            self.range = forecastRange
        if holtwinters is not None:
            self.hw = holtwinters
        if arima is not None:
            self.arima = arima
        if ssa is not None:
            self.ssa = ssa
        if horizon is not None:
            self.horizon = horizon
        if baseline is not None:
            self.baseline = baseline

    def set_auto_aggregate(self, autoAggregate):
        if not isinstance(autoAggregate, bool):
            raise ValueError('AutoAggregate expected to be bool, found: ' + unicode(type(autoAggregate)))
        self.autoAggregate = autoAggregate

    def set_aggregation_function(self, aggregationFunction):
        if not (hasattr(StatisticalFunction, aggregationFunction) or aggregationFunction.upper().startswith("PERCENTILE")):
            raise ValueError('Expected one of StatisticalFunction attributes or PERCENTILE, found: ' + str(aggregationFunction))
        self.aggregationFunction= aggregationFunction

    def set_include(self, include):
        self.include =[include] if not isinstance(include, list) else include

    def set_score_interval(self, count, unit):
        if not isinstance(count, numbers.Number):
            raise ValueError('Score Interval count must be a number, found: ' + unicode(type(count)))
        if not hasattr(TimeUnit, unit):
            raise ValueError('Invalid score interval unit, found: ' + str(unit))
        self.scoreInterval = {'count': count, 'unit': unit}

    def set_score_interval(self, score_interval):
        if not is_interval(score_interval):
            raise ValueError("Score Interval expected to be an Interval instance, found: " + unicode(type(score_interval)))
        self.scoreInterval = score_interval

    def set_range(self, minRange, maxRange):
        if not isinstance(minRange, numbers.Number):
            raise ValueError('Expected min to be a number, found: ' + unicode(type(minRange)))
        if not isinstance(minRange, numbers.Number):
            raise ValueError('Expected max to be a number, found: ' + unicode(type(maxRange)))
        self.range = {'min': minRange, 'max': maxRange}

    def set_holtwinters(self, holtwinters):
        if not isinstance(holtwinters, HoltWinters):
            raise ValueError('Expected HolwWinters class instance, found: ' + unicode(type(holtwinters)))
        self.hw = holtwinters

    def set_arima(self, arima):
        if not isinstance(arima, Arima):
            raise ValueError('Expected Arima class instance, found: ' + unicode(type(arima)))
        self.arima = arima

    def set_ssa(self, ssa):
        if not isinstance(ssa, Ssa):
            raise ValueError('Expected Ssa class instance, found: ' + unicode(type(ssa)))
        self.ssa = ssa

    def set_horizon(self, horizon):
        if not isinstance(horizon, Horizon):
            raise ValueError('Expected Horizon class instance, found: ' + unicode(type(horizon)))
        self.horizon = horizon

    def set_baseline(self, baseline):
        if not isinstance(baseline, Baseline):
            raise ValueError('Expected Baseline class instance, found: ' + unicode(type(baseline)))
        self.baseline = baseline


class HoltWinters:

    def __init__(self, auto=None, period=None, alpha=None, beta=None, gamma=None):
        if auto is not None:
            self.auto = auto
        if period is not None:
            self.period = period
        if alpha is not None:
            self.alpha = alpha
        if beta is not None:
            self.beta = beta
        if gamma is not None:
            self.gamma = gamma

    def set_auto(self, auto):
        if not isinstance(auto, bool):
            raise ValueError('Auto expected to be a bool, found: ' + unicode(type(auto)))
        self.auto = auto

    def set_period(self, count, unit):
        if not isinstance(count, numbers.Number):
            raise ValueError('Period count must be a number, found: ' + unicode(type(count)))
        if not hasattr(TimeUnit, unit):
            raise ValueError('Invalid period unit ' + str(unit))
        self.period = {'count': count, 'unit': unit}

    def set_period(self, period):
        if not is_interval(period):
            raise ValueError('Period expected to be an interval, found: ' + unicode(type(period)))
        self.period = period

    def set_alpha(self, alpha):
        if not isinstance(alpha, numbers.Number):
            raise ValueError("Alpha expected to be a number, found: " + unicode(type(alpha)))
        self.alpha = alpha

    def set_beta(self, beta):
        if not isinstance(beta, numbers.Number):
            raise ValueError("Beta expected to be a number, found: " + unicode(type(beta)))
        self.beta = beta

    def set_gamma(self, gamma):
        if not isinstance(gamma, numbers.Number):
            raise ValueError("Gamma expected to be a number, found: " + unicode(type(gamma)))
        self.gamma = gamma


class Horizon:

    def __init__(self, interval=None, length=None, endDate=None, startDate=None):
        if interval is not None:
            self.interval = None
        if length is not None:
            self.length = length
        if endDate is not None:
            self.endDate = endDate
        if startDate is not None:
            self.startDate = startDate

    def set_interval(self, count, unit):
        if not isinstance(count, numbers.Number):
            raise ValueError('Interval count must be a number, found: ' + unicode(type(count)))
        if not hasattr(TimeUnit, unit):
            raise ValueError('Invalid interval unit, found: ' + str(unit))
        self.interval = {'count': count, 'unit': unit}

    def set_length(self, length):
        if not isinstance(length, numbers.Number):
            raise ValueError('Length expected to be a number, found: ' + unicode(type(length)))
        self.length = length

    def set_end_date(self, endDate):
        self.endDate = endDate

    def set_start_date(self, startDate):
        self.startDate = startDate


class Arima:

    def __init__(self, auto=None, autoRegressionInterval=None, p=None, d=None):
        if auto is not None:
            self.auto = auto
        if autoRegressionInterval is not None:
            self.autoRegressionInterval = autoRegressionInterval
        if p is not None:
            self.p = p
        if d is not None:
            self.d = d

    def set_auto(self, auto):
        if not isinstance(auto, bool):
            raise ValueError('Auto parameter must be bool, but found: ' + unicode(type(auto)))
        self.auto = auto

    def set_auto_regression_interval(self, count, unit):
        if not isinstance(count, numbers.Number):
            raise ValueError('Interval count must be a number, found: ' + unicode(type(count)))
        if not hasattr(TimeUnit, unit):
            raise ValueError('Invalid interval unit, found: ' + str(unit))
        self.autoRegressionInterval = {'count': count, 'unit': unit}

    def set_p(self, p):
        if not isinstance(p, numbers.Number):
            raise ValueError('P must be a number, but found: ' + unicode(type(p)))
        self.p = p

    def set_d(self, d):
        if not isinstance(d, numbers.Number):
            raise ValueError('D must be a number, but found: ' + unicode(type(d)))
        self.d = d


class Baseline:

    def __init__(self, period=None, count=None, function=None):
        if period is not None:
            self.period = period
        if count is not None:
            self.count = count
        if function is not None:
            self.function = function

    def set_period(self, count, unit):
        if not isinstance(count, numbers.Number):
            raise ValueError('Period count must be a number, found: ' + unicode(type(count)))
        if not hasattr(TimeUnit, unit):
            raise ValueError('Invalid period unit ' + str(unit))
        self.period = {'count': count, 'unit': unit}

    def set_count(self, count):
        if not isinstance(count, numbers.Number):
            raise ValueError('Count must be a number, found: ' + unicode(type(count)))
        self.count = count

    def set_function(self, function):
        if not (hasattr(StatisticalFunction, function) or function.upper().startswith("PERCENTILE")):
            raise ValueError('Function expected to be one of StatisticalFunction attributes or PERCENTILE, but found: ' + function)
        self.function = function


class Ssa:

    def __init__(self, decompose=None, group=None, reconstruct=None, ssaForecast=None):
        if decompose is not None:
            self.decompose = decompose
        if group is not None:
            self.group = group
        if reconstruct is not None:
            self.reconstruct = reconstruct
        if ssaForecast is not None:
            self.forecast = ssaForecast

    def set_decompose(self, decompose):
        if not isinstance(decompose, Decompose):
            raise ValueError('Expected Decompose class instance, found: ' + unicode(type(decompose)))
        self.decompose = decompose

    def set_reconstruct(self, reconstruct):
        if not isinstance(reconstruct, Reconstruct):
            raise ValueError('Expected Reconstruct class instance, found: ' + unicode(type(reconstruct)))
        self.reconstruct = reconstruct

    def set_forecast(self, ssaForecast):
        if not isinstance(ssaForecast, SsaForecast):
            raise ValueError('Expected SsaForecast class instance, found: ' + unicode(type(ssaForecast)))
        self.forecast = ssaForecast

    def set_group(self, group):
        if not isinstance(group, SsaGroup):
            raise ValueError('Expected SsaGroup class instance, found: ' + unicode(type(group)))
        self.group = group


class Decompose:

    def __init__(self, eigentripleLimit=None, method=None, windowLength=None, singularValueThreshold=None):
        if eigentripleLimit is not None:
            self.eigentripleLimit = eigentripleLimit
        if method is not None:
            self.method = method
        if windowLength is not None:
            self.windowLength = windowLength
        if singularValueThreshold is not None:
            self.singularValueThreshold = singularValueThreshold

    def set_eigentriple_limit(self, eigentripleLimit):
        if not isinstance(eigentripleLimit, numbers.Number):
            raise ValueError('Expected a number on eigentripleLimit, but found: ' + unicode(type(eigentripleLimit)))
        self.eigentripleLimit = eigentripleLimit

    def set_method(self, method):
        if not hasattr(DecomposeMethod, method):
            raise ValueError('Expected attribute from DecomposeMethod, but found' + str(method))
        self.method = method

    def set_window_length(self, windowLength):
        if not isinstance(windowLength, numbers.Number):
            raise ValueError('Expected a number on windowLength, but found: ' + unicode(type(windowLength)))
        self.windowLength = windowLength

    def set_singular_value_threshold(self, singularValueThreshold):
        if not isinstance(singularValueThreshold, numbers.Number):
            raise ValueError('Expected a number on singularValueThreshold, but found: ' + unicode(type(singularValueThreshold)))
        self.singularValueThreshold = singularValueThreshold


class Reconstruct:

    def __init__(self, averagingFunction=None, fourier=None):
        if averagingFunction is not None:
            self.averagingFunction = averagingFunction
        if fourier is not None:
            self.fourier = fourier

    def set_averaging_function(self, averagingFunction):
        if not hasattr(ReconstructAveragingFunction, averagingFunction):
            raise ValueError('Expected attribute of ReconstructAveragingFunction, found: ' + str(averagingFunction))
        self.averagingFunction = averagingFunction

    def set_fourier(self, fourier):
        if not isinstance(fourier, bool):
            raise ValueError('Expected fourier to be bool, found: ' + unicode(type(fourier)))
        self.fourier = fourier


class SsaForecast:

    def __init__(self, method=None, base=None):
        if method is not None:
            self.method = method
        if base is not None:
            self.base = base

    def set_method(self, method):
        if not hasattr(SsaForecastMethod, method):
            raise ValueError('Expected attribute of SsaForecastMethod, found: ' + str(method))
        self.method = method

    def set_base(self, base):
        if not hasattr(SsaForecastBase, base):
            raise ValueError('Expected attribute of SsaForecastBase, found: ' + str(base))
        self.base = base


class SsaGroup:

    def __init__(self, auto=None, manual=None):
        if auto is not None:
            self.auto = auto
        if manual is not None:
            self.manual = manual

    def set_auto(self, auto):
        if not isinstance(auto, SsaGroupAuto):
            raise ValueError('Expected SsaGroupAuto class instance, found: ' + unicode(type(auto)))
        self.auto = auto

    def set_manual(self, manual):
        if not isinstance(manual, SsaGroupManual):
            raise ValueError('Expected SsaGroupManual class instance, found: ' + unicode(type(manual)))
        self.manual = manual


class SsaGroupAuto:

    def __init__(self, count=None, stack=None, union=None, clustering=None):
        if count is not None:
            self.count = count
        if stack is not None:
            self.stack = stack
        if union is not None:
            self.union = union
        if clustering is not None:
            self.clustering = clustering

    def set_count(self, count):
        if not isinstance(count, numbers.Number):
            raise ValueError('Expected count to be a number, found: ' + unicode(type(count)))
        self.count = count

    def set_stack(self, stack):
        if not isinstance(stack, bool):
            raise ValueError('Expected stack to be bool, found: ' + unicode(type(stack)))
        self.stack = stack

    def set_union(self, union):
        if not isinstance(union, list):
            raise ValueError('Expected union to be list, found: ' + unicode(type(union)))
        self.union = union

    def set_clustering(self, clustering):
        if not isinstance(clustering, SsaGroupAutoClustering):
            raise ValueError('Expected stack to be SsaGroupAutoClustering, found: ' + unicode(type(clustering)))
        self.clustering = clustering


class SsaGroupAutoClustering:

    def __init__(self, method=None, params=None):
        if method is not None:
            self.method = method
        if params is not None:
            self.params = params

    def set_method(self, method):
        if not hasattr(SsaGroupAutoClusteringMethod, method):
            raise ValueError('Expected attribute of SsaGroupAutoClusteringMethod, found: ' + str(method))
        self.method = method

    def set_params(self, params):
        if not isinstance(params, dict):
            raise ValueError('Expected params to be a dictionary, found: ' + unicode(type(params)))
        self.params = params


class SsaGroupManual:

    def __init__(self, groups=None):
        if groups is not None:
            self.groups = groups

    def set_groups(self, groups):
        if not isinstance(groups, list):
            raise ValueError('Expected groups to be a list, found: ' + unicode(type(groups)))
        self.groups = groups