from abc import abstractmethod
from typing import Protocol, Iterable, Generic, Set, runtime_checkable

from hgraph._types._scalar_types import KEYABLE_SCALAR
from hgraph._types._time_series_types import TimeSeriesInput, TimeSeriesOutput, TimeSeriesDeltaValue
from hgraph._types._ts_type import TS

__all__ = ("SetDelta", "TSS", "TSS_OUT", "TimeSeriesSet", "TimeSeriesSetInput", "TimeSeriesSetOutput")


@runtime_checkable
class SetDelta(Protocol[KEYABLE_SCALAR],Generic[KEYABLE_SCALAR]):

    @property
    @abstractmethod
    def added_elements(self) -> Iterable[KEYABLE_SCALAR]:
        """
        The elements that were added
        """

    @property
    @abstractmethod
    def removed_elements(self) -> Iterable[KEYABLE_SCALAR]:
        """
        The elements that were removed
        """


class TimeSeriesSet(TimeSeriesDeltaValue[KEYABLE_SCALAR, SetDelta[KEYABLE_SCALAR]], Generic[KEYABLE_SCALAR]):
    """
    The representation of a set over time.
    """

    @abstractmethod
    def __contains__(self, item: KEYABLE_SCALAR) -> bool:
        """
        If this time series set contain the value provided.
        """

    @abstractmethod
    def values(self) -> Iterable[KEYABLE_SCALAR]:
        """
        Iterator over all the time-series values of this collection
        """

    @abstractmethod
    def added(self) -> Iterable[KEYABLE_SCALAR]:
        """
        Iterator over the added values
        """

    @abstractmethod
    def was_added(self, item: KEYABLE_SCALAR) -> bool:
        """True if the item was added in this engine cycle."""

    @abstractmethod
    def removed(self) -> Iterable[KEYABLE_SCALAR]:
        """
        Iterator over the removed values
        """

    @abstractmethod
    def was_removed(self, item: KEYABLE_SCALAR) -> bool:
        """True if the item was removed in this engine cycle."""


class TimeSeriesSetInput(TimeSeriesInput, TimeSeriesSet[KEYABLE_SCALAR], Generic[KEYABLE_SCALAR]):
    """
    The input version of the set.
    """


class TimeSeriesSetOutput(TimeSeriesOutput, TimeSeriesSet[KEYABLE_SCALAR], Generic[KEYABLE_SCALAR]):
    """
    The output version of the set
    """

    @abstractmethod
    def get_contains_output(self, item: KEYABLE_SCALAR, requester: object) -> TS[bool]:
        """
        Returns a TS[bool] output reference that ticks True when the item value is present and False otherwise.
        """

    @abstractmethod
    def release_contains_output(self, item: KEYABLE_SCALAR, requester: object):
        """Releases the reference request"""

    @abstractmethod
    def is_empty_output(self) -> TS[bool]:
        """Returns a TS[bool] output that tracks the empty state of the set."""

    @property
    @abstractmethod
    def value(self) -> Set[KEYABLE_SCALAR]:
        ...

    @property
    @abstractmethod
    def delta_value(self) -> SetDelta[KEYABLE_SCALAR]:
        ...

    def add(self, element: KEYABLE_SCALAR):
        """Add an element to the set"""

    def remove(self, element: KEYABLE_SCALAR):
        """Removes the element from the set"""

    def clear(self):
        """Removes all elements from the set"""


TSS = TimeSeriesSetInput
TSS_OUT = TimeSeriesSetOutput
