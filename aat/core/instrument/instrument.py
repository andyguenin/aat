from .db import InstrumentDB
from ..exchange import ExchangeType
from ...config import InstrumentType
from ...common import _in_cpp

try:
    from ...binding import InstrumentCpp  # type: ignore
    _CPP = _in_cpp()
except ImportError:
    _CPP = False


class Instrument(object):
    _instrumentdb = InstrumentDB()

    __slots__ = [
        "__name",
        "__type",
        "__exchanges"
    ]

    def __new__(cls, *args, **kwargs):
        if cls._instrumentdb.instruments(*args, **kwargs):
            return cls._instrumentdb.get(*args, **kwargs)

        if _CPP:
            # construct with C++
            instrument = InstrumentCpp(*args, **kwargs)
        else:
            # pure python
            instrument = super(Instrument, cls).__new__(cls)

        return instrument

    def __init__(self, name, type: InstrumentType = InstrumentType.EQUITY, exchange: ExchangeType = ExchangeType("")):
        assert isinstance(name, str)
        assert isinstance(type, InstrumentType)
        assert isinstance(exchange, ExchangeType) or not exchange
        self.__name = name
        self.__type = type
        self.__exchanges = [] if exchange else [exchange]

        # install into instrumentdb, noop if already there
        self._instrumentdb.add(self)

    # ******** #
    # Readonly #
    # ******** #
    @property
    def name(self) -> str:
        return self.__name

    @property
    def type(self) -> InstrumentType:
        return self.__type

    @property
    def exchanges(self):
        return self.__exchanges

    def __eq__(self, other):
        return self.name == other.name and self.type == other.type

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return f'Instrument({self.name}-{self.type})'
