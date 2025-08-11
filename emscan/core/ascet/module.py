from emscan.env import PATH
import os


class Module:

    def __init__(self, file:str):
        self.name = name = os.path.basename(file).split('.')[0]
        if file.endswith('.zip'):
            PATH.unzip(file, PATH.ETASDATA.BIN)
            self.path = path = PATH.ETASDATA.BIN
            self.file = file = path.file(f'{name}.main.amd')
        elif file.endswith('.main.amd'):
            self.path = os.path.dirname(file)
            self.file = file
        # else:
        #     raise FileFormatError
        self.main = file
        self.impl = file.replace(".main.amd", ".implementation.amd")
        self.data = file.replace(".main.amd", ".data.amd")
        self.spec = file.replace(".main.amd", ".specification.amd")
        return
