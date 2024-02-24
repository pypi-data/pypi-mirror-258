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