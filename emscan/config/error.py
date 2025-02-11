class AmdFormatError(FileExistsError):
    pass

class BaselineError(OSError):
    pass

class ColumnError(KeyError):
    pass

class MdaNotFound(OSError):
    pass

class MessageError(ReferenceError):
    pass

class ObjectIDError(ReferenceError):
    pass

class PathNotFoundError(FileNotFoundError):
    pass

class SignalError(TypeError):
    pass

class TestCaseError(AttributeError):
    pass
