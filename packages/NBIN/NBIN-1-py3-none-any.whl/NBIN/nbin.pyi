from typing import NoReturn
from typing import Any

from NBIN.types import *
from NBIN.errors import *

from struct import unpack
from struct import pack


# Maximum length of data in collections (block, command, array, str)
MAX_COLLECTION_LEN = 4
# All NBIN data types as collections
COLLECTIONS_NBIO_DATA = Block | Command | list
# All NBIN data types
NBIO_DATA = Block | Command | str | float | None | int | bool | list


def load(nbinCode: bytes) -> NBIO_DATA:
    '''
    Converts NBIN to Python object

    Here:
    * data - source binary code in NBIN format
    '''


def dump(nbinCode: NBIO_DATA) -> bytes:
    '''
    Converts a Python object to NBIN

    Here:
    * data - source Python object
    '''
