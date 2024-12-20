class AmdFormatError(FileExistsError):
    pass

class PathNotFoundError(FileNotFoundError):
    pass

class ColumnError(KeyError):
    pass

class MessageError(ReferenceError):
    pass

class SignalError(TypeError):
    pass

class TestCaseError(AttributeError):
    pass

class MdaNotFound(OSError):
    pass

class BaselineError(OSError):
    pass