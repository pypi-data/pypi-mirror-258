class DefunctCommandError(Exception):
    def __init__(self, command: bytes):
        super().__init__(f'The command with the opcode "{command}" does not exist.')


class UnsupportedTypeError(Exception):
    def __init__(self, typeN):
        super().__init__(f'NBIN does not support data type "{typeN}"')


class NBINFormatIsBroken(Exception):
    def __init__(self):
        super().__init__('The storage format of binary files NBIN is broken: There may be a fingerprint in the source dam')
