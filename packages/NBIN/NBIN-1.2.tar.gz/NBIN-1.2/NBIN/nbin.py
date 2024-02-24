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
            offset: int = int.from_bytes(nbinCode[1 : MAX_COLLECTION_LEN + 1], signed=False)
            commands: list[Command] = []
            lenght = 0
            
            i = 0
            while i < offset:
                result, lenght = __parseBlock(
                    nbinCode[i + MAX_COLLECTION_LEN + 1 : i + MAX_COLLECTION_LEN + 1 + offset]
                )
                commands.append(result)
                i += lenght + 1

            return Block(commands), lenght + MAX_COLLECTION_LEN
        
        ## INT ##
        case 0x00 | 0x01 | 0x02 | 0x03 | 0x05 | 0x06 | 0x07 | 0x09:
            intSizeBytes = {
                b'\x00': (1, 'i8'),
                b'\x01': (2, 'i16'),
                b'\x02': (4, 'i32'),
                b'\x03': (8, 'i64'),
                b'\x05': (1, 'u8'),
                b'\x06': (2, 'u16'),
                b'\x07': (4, 'u32'),
                b'\x09': (8, 'u64'),
            }
            responce = intSizeBytes[ nbinCode[0] ]
            resultNumber = int.from_bytes(
                bytes=nbinCode[1 : responce[0] + 1],
                signed=( responce[1] in ('i8', 'i16', 'i32', 'i64') )
            )

            return INT(responce[1], resultNumber), responce[0] + 1

        ## FLOAT ##
        case 0x10:
            float_number = unpack('f', nbinCode[1 : 5])[0]
            return float_number, 4
        
        ## BOOL ##
        case 0x11:
            return nbinCode[1] != 0, 1
        
        ## STR ##
        case 0x12:
            offset: int = int.from_bytes(nbinCode[1 : MAX_COLLECTION_LEN + 1], signed=False)
            separat = nbinCode[MAX_COLLECTION_LEN + 1 : MAX_COLLECTION_LEN + offset + 1]
            return separat.decode(), len(separat) + MAX_COLLECTION_LEN
        
        ## NULL ##
        case 0x13:
            return None, 0
        
        ## LIST ##
        case 0x14:
            resultList: list = []
            offset: int = int.from_bytes(nbinCode[1 : MAX_COLLECTION_LEN + 1], signed=False)
            listAsBytes: bytes = nbinCode[1 + MAX_COLLECTION_LEN : 1 + MAX_COLLECTION_LEN + offset]

            i = 0
            while i < len(listAsBytes):
                result, lenght = __parseNextCommand(listAsBytes[i:])
                i += lenght + 1
                resultList.append(result)

            return resultList, MAX_COLLECTION_LEN + offset + len(listAsBytes)
        
        ## COMMAND ##
        case 0x16:
            nameSize: int = int.from_bytes(nbinCode[1 : MAX_COLLECTION_LEN + 1], signed=False)
            name: str = nbinCode[1 + MAX_COLLECTION_LEN : nameSize + MAX_COLLECTION_LEN + 1].decode('utf-8')
            offset: int = int.from_bytes(nbinCode[1 + nameSize + MAX_COLLECTION_LEN : 1 + nameSize + MAX_COLLECTION_LEN*2], signed=False)
            commandAsBytes: bytes = nbinCode[1 + nameSize + MAX_COLLECTION_LEN*2 : 1 + nameSize + MAX_COLLECTION_LEN*2 + offset]
            commands: list = []

            i = 0
            while i < len(commandAsBytes):
                result, lenght = __parseNextCommand(commandAsBytes[i:])
                i += lenght + 1
                commands.append(result)
            
            # 13
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

    ### Block ###
    if T == Block:
        for command in data.commands:
           pastResult = __parseNBINObj(command)
           result += pastResult
        
        result = b'\x15' + len(result).to_bytes(4, signed=False) + result
        return result

    ### Command ###
    elif T == Command:
        i = 0
        name: bytes = data.name.encode()

        for node in data.nodes:
           result += __parseNBINObj(node)
           i += 1

        result = b'\x16' + len(name).to_bytes(4, signed=False) + name + len(result).to_bytes(4, signed=False) + result
        return result
    
    ### INT ###
    elif T == INT:
        intSizeBytes = {
            'i8':  (1, b'\x00'),
            'i16': (2, b'\x01'),
            'i32': (4, b'\x02'),
            'i64': (8, b'\x03'),
            'u8':  (1, b'\x05'),
            'u16': (2, b'\x06'),
            'u32': (4, b'\x07'),
            'u64': (8, b'\x09'),
        }
        responce = intSizeBytes[data.typeInt]
        resultNumber = data.value.to_bytes(
            responce[0],
            signed=( data.typeInt in ('i8', 'i16', 'i32', 'i64') )
        )

        return responce[1] + resultNumber

    ### OTHER ###
    elif T == list:
        for literal in data:
           result += __parseNBINObj(literal)

        result = b'\x14' + len(result).to_bytes(4, signed=False) + result
        return result
    
    elif T == int:
        return b'\x03' + data.to_bytes(8, signed=True)
    
    elif T == float:
        return b'\x10' + pack('f', data)
    
    elif T == bool:
        return b'\x11' + b'\x01' if data else b'\x00'
    
    elif T == str:
        return b'\x12' + len(data).to_bytes(4, signed=False) + data.encode()
    
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
    'dump',
    'load',
    'MAX_COLLECTION_LEN',
    'NBIO_DATA',
    'COLLECTIONS_NBIO_DATA',
]
