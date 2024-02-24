from typing import NoReturn
from typing import Any
from typing import Literal


# Integer data types
TYPES_INT = Literal['i8', 'i16', 'i32', 'i64', 'u8', 'u16', 'u32', 'u64']
# Acceptable ranges for them
RANGES_TYPES_INT = {
    'i8': range(-127, 127),
    'i16': range(-32_767, 32_767),
    'i32': range(-2_147_483_647, 2_147_483_647),
    'i64': range(-9_223_372_036_854_775_807, 9_223_372_036_854_775_807),
    'u8': range(0, 255),
    'u16': range(0, 65_535),
    'u32': range(0, 4_294_967_295),
    'u64': range(0, 18_446_744_073_709_551_615),
}


class Command:
    '''
    Command (machine) - a type used to describe one-line commands.

    Here:
    * name - command name
    * nodes - command parameters
    '''
    __slots__= ('name', 'nodes')

    def __init__(self, name: str,  nodes: list[Any]) -> None:
        if not isinstance(name, str):
            raise TypeError('The command name must be of type "str"')
        
        if not isinstance(nodes, list):
            raise TypeError('Command values ​​must be in the list')
        
        self.name = name
        self.nodes = nodes


class Block:
    '''
    A block is a data type that stores a list of commands of the "Command" type.

    Here:
    * commands - list of commands
    '''
    __slots__= ('commands')
    
    def __init__(self, commands: list[Command]) -> None:
        if not isinstance(commands, list):
            raise TypeError('The value passed must be of type "list", and it must contain values ​​of type "Command" or nothing')
        
        self.commands = commands


class INT:
    '''
    This is an integer type for interfacing with NBIN.

    Here:
    * value - value
    * typeInt - number type (the list of allowed types can be found in the "TYPES_INT" variable)
    '''
    __slots__= ('value', 'typeInt')
    
    def __init__(self, typeInt: TYPES_INT, value) -> None:
        if typeInt not in TYPES_INT:
            raise TypeError(f'Value "{value}" not in the list "TYPES_INT" of allowed types')
        
        if value in RANGES_TYPES_INT[typeInt]:
            self.value = value
        else:
            raise ValueError(f'The passed value "{value}" of type "{typeInt}" is out of range {RANGES_TYPES_INT[typeInt]}')


__all__ = [
    TYPES_INT,
    RANGES_TYPES_INT,
    Block,
    INT,
    Command,
]
