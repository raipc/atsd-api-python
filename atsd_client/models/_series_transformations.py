import numbers
from ._data_queries import set_if_type_is_valid, set_if_has_attr, set_if_interval


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


class Smooth:
    """
    Class representing transformation param 'smooth'
    """

    def __init__(self, smoothType, count=None, interval=None, minimumCount=None, incompleteValue=None):
        if smoothType is None:
            raise ValueError("Type is required parameter for Smooth")
        self.set_type(smoothType)
        if count is not None:
            self.set_count(count)
        if interval is not None:
            self.set_interval_dict(interval)
        if minimumCount is not None:
            self.set_minimum_count(minimumCount)
        if incompleteValue is not None:
            self.set_incomplete_value(incompleteValue)

    def set_type(self, smooth_type):
        set_if_has_attr(self, "type", smooth_type, SmoothType)

    def set_count(self, count):
        set_if_type_is_valid(self, "count", count, numbers.Number)

    def set_interval(self, count, unit):
        self.set_interval_dict({'count': count, 'unit': unit})

    def set_interval_dict(self, interval):
        set_if_interval(self, "interval", interval)

    def set_minimum_count(self, minimum_count):
        set_if_type_is_valid(self, "minimumCount", minimum_count, numbers.Number)

    def set_incomplete_value(self, incomplete_value):
        set_if_type_is_valid(self, "incompleteValue", incomplete_value, str)


class Downsample:
    """
    Class representing transformation param 'downsample'
    """

    def __init__(self, algorithm=None, difference=None, ratio=None, gap=None):
        if algorithm is not None:
            self.set_algorithm(algorithm)
        if difference is not None:
            self.set_difference(difference)
        if ratio is not None:
            self.set_ratio(ratio)
        if gap is not None:
            self.set_gap_dict(gap)

    def set_algorithm(self, algorithm):
        set_if_has_attr(self, "algorithm", algorithm, DownsampleAlgorithm)

    def set_difference(self, difference):
        set_if_type_is_valid(self, "difference", difference, numbers.Number)

    def set_ratio(self, ratio):
        set_if_type_is_valid(self, "ratio", ratio, numbers.Number)

    def set_gap(self, count, unit):
        self.set_gap_dict({'count': count, 'unit': unit})

    def set_gap_dict(self, gap):
        set_if_interval(self, "gap", gap)


class Evaluate:
    """
    Class representing transformation param 'evaluate'
    """

    def __init__(self, mode=None, libs=None, expression=None, script=None, order=None, timezone=None):
        if mode is not None:
            self.set_mode(mode)
        if libs is not None:
            self.set_libs(libs)
        if expression is not None:
            self.set_expression(expression)
        if script is not None:
            self.set_script(script)
        if order is not None:
            self.set_order(order)
        if timezone is not None:
            self.set_timezone(timezone)

    def set_mode(self, mode):
        set_if_has_attr(self, "mode", mode, EvaluateMode)

    def set_libs(self, libs):
        self.libs = [libs] if not isinstance(libs, list) else libs

    def set_expression(self, expression):
        set_if_type_is_valid(self, "expression", expression, str)

    def set_script(self, script):
        set_if_type_is_valid(self, "script", script, str)

    def set_order(self, order):
        set_if_type_is_valid(self, "order", order, numbers.Number)

    def set_timezone(self, timezone):
        set_if_type_is_valid(self, "timezone", timezone, str)


# =======================================================================
# Forecast Transformation
# =======================================================================
class ForecastTransformation:

    def __init__(self, autoAggregate=None, aggregationFunction=None, include=None, scoreInterval=None, min_range=None, max_range=None,
                    holtwinters=None, arima=None, ssa=None, horizon=None, baseline=None):
        if autoAggregate is not None:
            self.set_auto_aggregate(autoAggregate)
        if aggregationFunction is not None:
            self.set_aggregation_function(aggregationFunction)
        if include is not None:
            self.set_include(include)
        if scoreInterval is not None:
            self.set_score_interval_dict(scoreInterval)
        if min_range is not None and max_range is not None:
            self.set_range(min_range, max_range)
        if holtwinters is not None:
            self.set_holtwinters(holtwinters)
        if arima is not None:
            self.set_arima(arima)
        if ssa is not None:
            self.set_ssa(ssa)
        if horizon is not None:
            self.set_horizon(horizon)
        if baseline is not None:
            self.set_baseline(baseline)

    def set_auto_aggregate(self, auto_aggregate):
        set_if_type_is_valid(self, "autoAggregate", auto_aggregate, bool)

    def set_aggregation_function(self, aggregation_function):
        if not (hasattr(StatisticalFunction, aggregation_function) or aggregation_function.upper().startswith("PERCENTILE")):
            raise ValueError('Expected one of StatisticalFunction attributes or PERCENTILE, found: ' + str(aggregation_function))
        self.aggregationFunction = aggregation_function

    def set_include(self, include):
        self.include = [include] if not isinstance(include, list) else include

    def set_score_interval(self, count, unit):
        self.set_score_interval_dict({'count': count, 'unit': unit})

    def set_score_interval_dict(self, score_interval):
        set_if_interval(self, "scoreInterval", score_interval)

    def set_range(self, minRange, maxRange):
        if not isinstance(minRange, numbers.Number):
            raise ValueError('Expected min to be a number, found: ' + unicode(type(minRange)))
        if not isinstance(maxRange, numbers.Number):
            raise ValueError('Expected max to be a number, found: ' + unicode(type(maxRange)))
        self.range = {'min': minRange, 'max': maxRange}

    def set_holtwinters(self, holtwinters):
        set_if_type_is_valid(self, "hw", holtwinters, HoltWinters)

    def set_arima(self, arima):
        set_if_type_is_valid(self, "arima", arima, Arima)

    def set_ssa(self, ssa):
        set_if_type_is_valid(self, "ssa", ssa, Ssa)

    def set_horizon(self, horizon):
        set_if_type_is_valid(self, "horizon", horizon, Horizon)

    def set_baseline(self, baseline):
        set_if_type_is_valid(self, "baseline", baseline, Baseline)


class HoltWinters:

    def __init__(self, auto=None, period=None, alpha=None, beta=None, gamma=None):
        if auto is not None:
            self.set_auto(auto)
        if period is not None:
            self.set_period_dict(period)
        if alpha is not None:
            self.set_alpha(alpha)
        if beta is not None:
            self.set_beta(beta)
        if gamma is not None:
            self.set_gamma(gamma)

    def set_auto(self, auto):
        set_if_type_is_valid(self, "auto", auto, bool)

    def set_period(self, count, unit):
        self.set_period_dict({'count': count, 'unit': unit})

    def set_period_dict(self, period):
        set_if_interval(self, "period", period)

    def set_alpha(self, alpha):
        set_if_type_is_valid(self, "alpha", alpha, numbers.Number)

    def set_beta(self, beta):
        set_if_type_is_valid(self, "beta", beta, numbers.Number)

    def set_gamma(self, gamma):
        set_if_type_is_valid(self, "gamma", gamma, numbers.Number)


class Horizon:

    def __init__(self, interval=None, length=None, endDate=None, startDate=None):
        if interval is not None:
            self.set_interval_dict(interval)
        if length is not None:
            self.set_length(length)
        if endDate is not None:
            self.set_end_date(endDate)
        if startDate is not None:
            self.set_start_date(startDate)

    def set_interval(self, count, unit):
        self.set_interval_dict({'count': count, 'unit': unit})

    def set_interval_dict(self, interval):
        set_if_interval(self, "interval", interval)

    def set_length(self, length):
        set_if_type_is_valid(self, "length", length, numbers.Number)

    def set_end_date(self, endDate):
        set_if_type_is_valid(self, "endDate", endDate, str)

    def set_start_date(self, startDate):
        set_if_type_is_valid(self, "startDate", startDate, str)


class Arima:

    def __init__(self, auto=None, autoRegressionInterval=None, p=None, d=None):
        if auto is not None:
            self.set_auto(auto)
        if autoRegressionInterval is not None:
            self.set_auto_regression_interval_dict(autoRegressionInterval)
        if p is not None:
            self.set_p(p)
        if d is not None:
            self.set_d(d)

    def set_auto(self, auto):
        set_if_type_is_valid(self, "auto", auto, bool)

    def set_auto_regression_interval(self, count, unit):
        self.set_auto_regression_interval_dict({'count': count, 'unit': unit})

    def set_auto_regression_interval_dict(self, auto_regression_interval):
        set_if_interval(self, "autoRegressionInterval", auto_regression_interval)

    def set_p(self, p):
        set_if_type_is_valid(self, "p", p, numbers.Number)

    def set_d(self, d):
        set_if_type_is_valid(self, "d", d, numbers.Number)


class Baseline:

    def __init__(self, period=None, count=None, function=None):
        if period is not None:
            self.set_period_dict(period)
        if count is not None:
            self.set_count(count)
        if function is not None:
            self.set_function(function)

    def set_period(self, count, unit):
        self.set_period_dict({'count': count, 'unit': unit})

    def set_period_dict(self, period):
        set_if_interval(self, "period", period)

    def set_count(self, count):
        set_if_type_is_valid(self, "count", count, numbers.Number)

    def set_function(self, function):
        if not (hasattr(StatisticalFunction, function) or function.upper().startswith("PERCENTILE")):
            raise ValueError('Function expected to be one of StatisticalFunction attributes or PERCENTILE, but found: ' + function)
        self.function = function


class Ssa:

    def __init__(self, decompose=None, group=None, reconstruct=None, ssaForecast=None):
        if decompose is not None:
            self.set_decompose(decompose)
        if group is not None:
            self.set_group(group)
        if reconstruct is not None:
            self.set_reconstruct(reconstruct)
        if ssaForecast is not None:
            self.set_forecast(ssaForecast)

    def set_decompose(self, decompose):
        set_if_type_is_valid(self, "decompose", decompose, Decompose)

    def set_reconstruct(self, reconstruct):
        set_if_type_is_valid(self, "reconstruct", reconstruct, Reconstruct)

    def set_forecast(self, ssaForecast):
        set_if_type_is_valid(self, "forecast", ssaForecast, SsaForecast)

    def set_group(self, group):
        set_if_type_is_valid(self, "group", group, SsaGroup)


class Decompose:

    def __init__(self, eigentripleLimit=None, method=None, windowLength=None, singularValueThreshold=None):
        if eigentripleLimit is not None:
            self.set_eigentriple_limit(eigentripleLimit)
        if method is not None:
            self.set_method(method)
        if windowLength is not None:
            self.set_window_length(windowLength)
        if singularValueThreshold is not None:
            self.set_singular_value_threshold(singularValueThreshold)

    def set_eigentriple_limit(self, eigentripleLimit):
        set_if_type_is_valid(self, "eigentripleLimit", eigentripleLimit, numbers.Number)

    def set_method(self, method):
        set_if_has_attr(self, "method", method, DecomposeMethod)

    def set_window_length(self, windowLength):
        set_if_type_is_valid(self, "windowLength", windowLength, numbers.Number)

    def set_singular_value_threshold(self, singularValueThreshold):
        set_if_type_is_valid(self, "singularValueThreshold", singularValueThreshold, numbers.Number)


class Reconstruct:

    def __init__(self, averagingFunction=None, fourier=None):
        if averagingFunction is not None:
            self.set_averaging_function(averagingFunction)
        if fourier is not None:
            self.set_fourier(fourier)

    def set_averaging_function(self, averagingFunction):
        set_if_has_attr(self, "averagingFunction", averagingFunction, ReconstructAveragingFunction)

    def set_fourier(self, fourier):
        set_if_type_is_valid(self, "fourier", fourier, bool)


class SsaForecast:

    def __init__(self, method=None, base=None):
        if method is not None:
            self.set_method(method)
        if base is not None:
            self.set_base(base)

    def set_method(self, method):
        set_if_has_attr(self, "method", method, SsaForecastMethod)

    def set_base(self, base):
        set_if_has_attr(self, "base", base, SsaForecastBase)


class SsaGroup:

    def __init__(self, auto=None, manual=None):
        if auto is not None:
            self.set_auto(auto)
        if manual is not None:
            self.set_manual(manual)

    def set_auto(self, auto):
        set_if_has_attr(self, "auto", auto, SsaGroupAuto)

    def set_manual(self, manual):
        set_if_has_attr(self, "manual", manual, SsaGroupManual)


class SsaGroupAuto:

    def __init__(self, count=None, stack=None, union=None, clustering=None):
        if count is not None:
            self.set_count(count)
        if stack is not None:
            self.set_stack(stack)
        if union is not None:
            self.set_union(union)
        if clustering is not None:
            self.set_clustering(clustering)

    def set_count(self, count):
        set_if_type_is_valid(self, "count", count, numbers.Number)

    def set_stack(self, stack):
        set_if_type_is_valid(self, "stack", stack, bool)

    def set_union(self, union):
        set_if_type_is_valid(self, "union", union, list)

    def set_clustering(self, clustering):
        set_if_type_is_valid(self, "clustering", clustering, SsaGroupAutoClustering)


class SsaGroupAutoClustering:

    def __init__(self, method=None, params=None):
        if method is not None:
            self.set_method(method)
        if params is not None:
            self.set_params(params)

    def set_method(self, method):
        set_if_has_attr(self, "method", method, SsaGroupAutoClusteringMethod)

    def set_params(self, params):
        set_if_type_is_valid(self, "params", params, dict)


class SsaGroupManual:

    def __init__(self, groups=None):
        if groups is not None:
            self.set_groups(groups)

    def set_groups(self, groups):
        set_if_type_is_valid(self, "groups", groups, list)
