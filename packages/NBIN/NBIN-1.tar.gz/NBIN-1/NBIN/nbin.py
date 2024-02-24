from typing import NoReturn
from typing import Any

from NBIN.types import *
from .errors import *

from struct import unpack
from struct import pack


# Maximum length of data in collections (block, command, array, str)
MAX_COLLECTION_LEN = 4
# All NBIN data types as collections
COLLECTIONS_NBIO_DATA = Block | Command | list
# All NBIN data types
NBIO_DATA = Block | Command | str | float | None | int | bool | list


def __parseBlock(nbinCode: bytes) -> tuple[Block, int]:
    commands: list[Command] = []
    lenght: int = 0
    i = 0
    
    while i < len(nbinCode):
        result, lenght = __parseNextCommand(nbinCode[i:])
        i += lenght + 1
        commands.append(result)

    return Block(commands), i


def __parseNextCommand(nbinCode: bytes) -> tuple[Any, int]:
    # Lenght command
    lenght: int

    match nbinCode[0]:
        ## BLOCK ##
        case 0x15:
            offset: int = int.from_bytes(nbinCode[1 : MAX_COLLECTION_LEN + 1], signed=True)
            result, lenght = __parseBlock(
                nbinCode[MAX_COLLECTION_LEN + 1 : MAX_COLLECTION_LEN + offset]
            )
            return result, lenght + 4
        
        ## INT ##
        case 0x00:
            return int.from_bytes(nbinCode[1 : 2]), 1
        
        case 0x01:
            return int.from_bytes(nbinCode[1 : 3]), 2
        
        case 0x02:
            return int.from_bytes(nbinCode[1 : 5]), 4
        
        case 0x03:
            return int.from_bytes(nbinCode[1 : 9]), 8
        
        ## UNSIGNED INT ##
        case 0x05:
            return int.from_bytes(nbinCode[1 : 2], signed=True), 1
        
        case 0x06:
            return int.from_bytes(nbinCode[1 : 3], signed=True), 2
        
        case 0x07:
            return int.from_bytes(nbinCode[1 : 5], signed=True), 4
        
        case 0x09:
            return int.from_bytes(nbinCode[1 : 9], signed=True), 8

        ## FLOAT ##
        case 0x10:
            float_number = unpack('f', nbinCode[1 : 5])[0]
            return float_number, 4
        
        ## BOOL ##
        case 0x11:
            return nbinCode[1] != 0, 1
        
        ## STR ##
        case 0x12:
            offset: int = int.from_bytes(nbinCode[1 : MAX_COLLECTION_LEN + 1], signed=True)
            separat = nbinCode[MAX_COLLECTION_LEN + 1 : MAX_COLLECTION_LEN + offset + 1]
            return separat.decode(), len(separat) + MAX_COLLECTION_LEN
        
        ## NULL ##
        case 0x13:
            return None, 0
        
        ## LIST ##
        case 0x14:
            resultList: list = []
            offset: int = int.from_bytes(nbinCode[1 : MAX_COLLECTION_LEN + 1], signed=True)
            listAsBytes: bytes = nbinCode[1 + MAX_COLLECTION_LEN : 1 + MAX_COLLECTION_LEN + offset]

            i = 0
            while i < len(listAsBytes):
                result, lenght = __parseNextCommand(listAsBytes[i:])
                i += lenght + 1
                resultList.append(result)

            return resultList, MAX_COLLECTION_LEN + offset + len(listAsBytes)
        
        ## COMMAND ##
        case 0x16:
            nameSize: int = int.from_bytes(nbinCode[1 : MAX_COLLECTION_LEN + 1], signed=True)
            name: str = nbinCode[1 + MAX_COLLECTION_LEN : nameSize + MAX_COLLECTION_LEN + 1].decode('utf-8')
            offset: int = int.from_bytes(nbinCode[nameSize + MAX_COLLECTION_LEN + 2 : nameSize + MAX_COLLECTION_LEN + 5], signed=True)
            commandAsBytes: bytes = nbinCode[nameSize + MAX_COLLECTION_LEN + 5 : nameSize + MAX_COLLECTION_LEN*2 + 5 + offset]
            commands: list = []

            i = 0
            while i < len(commandAsBytes):
                result, lenght = __parseNextCommand(commandAsBytes[i:])
                i += lenght + 1
                commands.append(result)
            
            return Command(name, commands), len(commandAsBytes) + MAX_COLLECTION_LEN*2 + nameSize
    
        case _:
            raise DefunctCommandError(nbinCode[0])


def load(data: bytes) -> NBIO_DATA:
    '''
    Converts NBIN to Python object

    Here:
    * data - source binary code in NBIN format
    '''
    return __parseNextCommand(data)[0]
    

#######################################################
###                     DUMP                        ###
#######################################################


def __parseNBINObj(data: NBIO_DATA) -> bytes:
    T = type(data)
    result: bytes = b''
    size: int = 0

    if T == Block:
        for command in data.commands:
           pastResult = __parseNBINObj(command)
           result += pastResult
        
        result = b'\x15' + len(pastResult).to_bytes(4, signed=True) + result
        return result

    elif T == Command:
        i = 0
        name: bytes = data.name.encode()

        for node in data.nodes:
           result += __parseNBINObj(node)
           i += 1

        result = b'\x16' + len(name).to_bytes(4, signed=True) + name + len(result).to_bytes(4, signed=True) + result
        return result

    elif T == list:
        for literal in data:
           result += __parseNBINObj(literal)

        result = b'\x14' + len(result).to_bytes(4, signed=True) + result
        return result

    elif T == int:
        return b'\x03' + data.to_bytes(8)
    
    elif T == float:
        return b'\x10' + pack('f', data)
    
    elif T == bool:
        return b'\x11' + b'\x01' if data else b'\x00'
    
    elif T == str:
        return b'\x12' + len(data).to_bytes(4, signed=True) + data.encode()
    
    elif T == None:
        return b'\x13'
    
    else:
        raise UnsupportedTypeError(T)
    

def dump(data: NBIO_DATA) -> bytes:
    '''
    Converts a Python object to NBIN

    Here:
    * data - source Python object
    '''
    try:
        return __parseNBINObj(data)
    except IndexError:
        NBINFormatIsBroken()


__all__ = [
    dump,
    load,
    MAX_COLLECTION_LEN,
    NBIO_DATA,
    COLLECTIONS_NBIO_DATA,
]
