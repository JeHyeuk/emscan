class AmdFormatError(FileExistsError):
    pass

class AscetPathError(FileExistsError):
    pass

class BCNotFoundError(FileExistsError):
    pass

class AuthorizeError(OSError):
    pass