try:
    from emscan.can.db.objs import MessageObj
    from .msg import messageAttribute
    from .sig import signalAttribute
except ImportError:
    from emscan.can.db.objs import MessageObj
    from emscan.can.module.attr.msg import messageAttribute
    from emscan.can.module.attr.sig import signalAttribute
from pandas import DataFrame, concat


class Attributes(DataFrame):

    def __init__(self, message:MessageObj):
        _m_attr = [messageAttribute(message)]
        _s_attr = [signalAttribute(sig) for sig in message]
        super().__init__(concat(_m_attr + _s_attr, axis=0, ignore_index=True))
        if not message.hasCRC():
            self.drop(index=self[self["type"].astype(str).str.startswith("crc")].index, inplace=True)
        if not message.hasAliveCounter():
            self.drop(index=self[self["type"].astype(str).str.startswith("aliveCount")].index, inplace=True)
        return

    def setOID(self, ):
        # TODO
        return

if __name__ == "__main__":
    from emscan.can.db.db import DB
    from pandas import set_option

    set_option('display.expand_frame_repr', False)

    m = DB("SMK_02_200ms")
    print(Attributes(m))