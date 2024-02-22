from hgraph import compute_node, TSL, TIME_SERIES_TYPE, SIZE, SCALAR, TS, graph, AUTO_RESOLVE, NUMBER, REF, TSD

__all__ = ("flatten_tsl_values", "merge")

from hgraph.nodes._const import const
from hgraph.nodes._analytical import sum_
from hgraph.nodes._operators import len_


@compute_node
def flatten_tsl_values(tsl: TSL[TIME_SERIES_TYPE, SIZE], all_valid: bool=False) -> TS[tuple[SCALAR, ...]]:
    """
    This will convert the TSL into a time-series of tuples. The value will be the value type of the time-series
    provided to the TSL. If the value has not ticked yet, the value will be None.
    The output type must be defined by the user.

    Usage:
    ```Python
        tsl: TSL[TS[float], Size[3]] = ...
        out = flatten_tsl[SCALAR: float](tsl)
    ```
    """
    return tsl.value if not all_valid or tsl.all_valid else None


@compute_node
def merge(tsl: TSL[TIME_SERIES_TYPE, SIZE]) -> TIME_SERIES_TYPE:
    """
    Selects and returns the first of the values that tick (are modified) in the list provided.
    If more than one input is modified in the engine-cycle, it will return the first one that ticked in order of the
    list.
    """
    return next(tsl.modified_values()).delta_value


@graph(overloads=len_)
def tsl_len(ts: TSL[TIME_SERIES_TYPE, SIZE], _sz: type[SIZE] = AUTO_RESOLVE) -> TS[int]:
    return const(_sz.SIZE)


@compute_node(overloads=sum_)
def sum_tsl(ts: TSL[TS[NUMBER], SIZE], _sz: type[SIZE] = AUTO_RESOLVE) -> TS[NUMBER]:
    return sum(t.value for t in ts.valid_values())


@compute_node
def tsl_to_tsd(tsl: TSL[REF[TIME_SERIES_TYPE], SIZE], keys: tuple[str, ...]) -> TSD[str, REF[TIME_SERIES_TYPE]]:
    """
    Converts a time series into a time series dictionary with the keys provided.
    """
    return {k: ts.value for k, ts in zip(keys, tsl) if ts.modified}
