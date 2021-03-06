from typing import Mapping, Union
from .data import Data
from .order import Order
from .trade import Trade
from ...config import EventType
from ...common import _in_cpp

try:
    from aat.binding import EventCpp  # type: ignore
    _CPP = _in_cpp()
except ImportError:
    _CPP = False


class Event(object):
    __slots__ = [
        "__type",
        "__target",
    ]

    # for convenience
    Types = EventType

    def __new__(cls, *args, **kwargs):
        if _CPP:
            return EventCpp(*args, **kwargs)
        return super(Event, cls).__new__(cls)

    def __init__(self, type: EventType, target: Union[Data, Order, Trade, None]):
        self.__type = type
        self.__target = target

    # ******** #
    # Readonly #
    # ******** #
    @property
    def type(self) -> EventType:
        return self.__type

    @property
    def target(self) -> Union[Data, Order, Trade]:
        return self.__target  # type: ignore
        # ignore None type so typing is happy in other parts

    def __repr__(self):
        return f'Event(type={self.type}, target={self.target})'

    def to_json(self) -> Mapping[str, Union[str, int, float]]:
        target = {'target.' + k: v for k, v in self.target.to_json().items()} if self.target else {'target': ''}

        ret = {'type': self.type.value}

        ret.update(target)
        return ret
