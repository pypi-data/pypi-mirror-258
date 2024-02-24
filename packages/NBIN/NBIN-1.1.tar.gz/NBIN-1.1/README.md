## What is NBIN

NBIN is a data serialization format that aims to make it easier to create and store bytecode for arbitrary programming languages. For this purpose, it has special data types, as well as its own binary file structure

NBIN has its own binary notation format, which can be broadly described as follows:
```bnf
<i8>        ::= 00h <byte>{1}
<i16>       ::= 01h <byte>{2}
<i32>       ::= 02h <byte>{4}
<i64>       ::= 03h <byte>{8}
<u8>        ::= 05h <byte>{1}
<u16>       ::= 06h <byte>{2}
<u32>       ::= 07h <byte>{4}
<u64>       ::= 09h <byte>{8}
<float>     ::= 10h <byte>{4}
<bool>      ::= 11h <byte>
<str>       ::= 12h <lenght> <byte>+
<null>      ::= 13h
<list>      ::= 14h <lenght> <exp>+
<block>     ::= 15h <lenght> <command>+
<command>   ::= 16h <lenght> <byte>+ <lenght> <exp>+


/* unsigned int */
<lenght> ::= <byte>{4}
```

> What is written in "{ ... }" is the number of repetitions

Each version of NBIN defines its own specification, for example the current NBIN (NBIN 1) uses the following specification:
1. Supported data types:
    * i8 - 1 sign byte
    * i16 - 2 sign bytes
    * i32 - 4 sign bytes
    * i64 - 8 sign bytes
    * u8 - 1 unsigned byte
    * u16 - 2 unsigned bytes
    * u32 - 4 unsigned bytes
    * u64 - 8 unsigned bytes
    * str - UNICODE string
    * bool - logical type
    * float - 32-bit fractional number
    * command - command
    * block - block with commands
    * list - not a typed list
    * null - no value
2. The length of any collection NBIN is a 32-bit unsigned number
3. Any NBIN object can be written in a binary file (it is not necessary that everything be wrapped in a block)
4. NBIN tries to support as many types as possible
5. NBIN types should satisfy both low-level and high-level programming needs


## NBIN library

There are two functions here:
1. `load` - accepts bytes in NBIN format as input and returns a Python object
1. `dump` - takes a Python object as input and returns bytes in NBIN format

In general, these two functions deal with object conversion

Usage example:
```python
from NBIN.nbin import *


# An example of an abstract syntax tree in some programming language
code = [
    Command('PRINT', ['Hello world!']),
    [
        'FUNC',
        Block([
            Command('SET', ['a', 14]),
            Command('SET', ['b', 2]),
            Command('SUM', ['a', 'b']),
        ]),
    ],
    Command('CALL', ['FUNC'])
]


# Write to file
with open('test.bin', 'wb') as file:
    result = dump(code)
    file.write()

# Reading from a file
with open('test.bin', 'rb') as file:
    result = load( file.write() )

```


## NBIN data types in Python

NBIN ports the following types to Python:
1. `INT` - data type, for fine-tuning the integer type
2. `Command` - command type
3. `Block` - a type that describes a block


### INT

If you want to create an integer of 1 byte in size, and at the same time so that it can have a sign, then do this:
```python
number = INT('i8', 52)
```

`i8` here is the NBIN data type.
The entire list of these types is stored in the `TYPES_INT` constant, and as an annotation - `LITERAL_TYPES_INT`.
In this case, you need to observe the allowed ranges for each type; they can be taken from the `RANGES_TYPES_INT` constant.


### Command

`Command` allows you to define your variable, with its name and parameters.

Usage example:
```python
cmd = Command('echo', ['Hello world!'])
```

Here: `name` (in the example it is equal to `echo`) is the first parameter of `Command`, and the parameters are passed to the second parameter `Command` in the form of a list, and can be of any type.


### Block

`Block` allows you to combine a list of commands into one block.

Usage example:
```python
func = Block([
    Command('PRINT', ['Hello!']),
    Command('EXIT'),
])
```

**Only a list of commands can be passed into it!**
