try:
    from emscan.core.ascet.module.tag.attr import ascetAttribute
    from emscan.can.db.objs import MessageObj
    from emscan.can.module.core.namingrule import naming
except ImportError:
    from emscan.core.ascet.module.tag.attr import ascetAttribute
    from emscan.can.db.objs import MessageObj
    from emscan.can.module.core.namingrule import naming
from pandas import DataFrame


class messageAttribute(DataFrame):

    def __init__(self, message:MessageObj):
        xcp = naming(message)

        timerFormula = f"Ti_q{message.astype(str).taskTime}_s" \
                       .replace(".", "p") \
                       .replace('p0_s', '_s')
        if message.timeoutTime % message.taskTime:
            timeoutTime = message.taskTime * (message.timeoutTime // message.taskTime + 1)
        else:
            timeoutTime = message.taskTime * (message.timeoutTime // message.taskTime)
        identifier = f"{message['Message']}({message['ID']})"

        objs = [
            ascetAttribute.unsigned(
                type="counter",
                name=xcp.counter,
                Comment=f"{identifier} Message Counter",
            ),
            ascetAttribute.unsigned(
                type="counterCalc",
                name=xcp.counterCalc,
                kind="variable",
                scope="local",
                Comment=f"{identifier} Message Counter Calculated",
            ),
            ascetAttribute.array(
                type="buffer",
                name=xcp.buffer,
                Comment=f"{identifier} Buffer",
                maxSizeX=f'{message["DLC"]}',
                value=f'{[0] * message["DLC"]}'
            ),
            ascetAttribute.unsigned(
                type="dlc",
                name=xcp.dlc,
                kind="variable",
                scope="local",
                Comment=f"{identifier} DLC",
            ),
            ascetAttribute.continuous(
                type="timerThreshold",
                name=xcp.thresholdTime,
                Comment=f"{identifier} Timeout Threshold",
                unit="s",
                kind="parameter",
                volatile="false",
                write="false",
                formula=timerFormula,
                physMax=message['taskTime'] * 255,
                value=timeoutTime,
            ),
            ascetAttribute.continuous(
                type="messageCountTimer",
                name=xcp.messageCountTimer,
                Comment=f"{identifier} Counter Timeout Timer",
                unit="s",
                kind="variable",
                scope="local",
                formula=timerFormula,
                physMax=message['taskTime'] * 255,
            ),
            ascetAttribute.continuous(
                type="crcTimer",
                name=xcp.crcTimer,
                Comment=f"{identifier} CRC Timeout Timer",
                unit="s",
                kind="variable",
                scope="local",
                formula=timerFormula,
                physMax=message['taskTime'] * 255,
            ),
            ascetAttribute.continuous(
                type="aliveCountTimer",
                name=xcp.aliveCountTimer,
                Comment=f"{identifier} Alive Counter Timeout Timer",
                unit="s",
                kind="variable",
                scope="local",
                formula=timerFormula,
                physMax=message['taskTime'] * 255,
            ),
            ascetAttribute.logic(
                type="messageCountValid",
                name=xcp.messageCountValid,
                Comment=f"{identifier} Counter Validity"
            ),
            ascetAttribute.logic(
                type="crcValid",
                name=xcp.crcValid,
                Comment=f"{identifier} CRC Validity"
            ),
            ascetAttribute.logic(
                type="aliveCountValid",
                name=xcp.aliveCountValid,
                Comment=f"{identifier} Alive Counter Validity"
            )
        ]
        super().__init__(data=objs, dtype=str)
        return


if __name__ == "__main__":
    from emscan.can.db.db import DB
    from pandas import set_option

    set_option('display.expand_frame_repr', False)

    m = DB("SMK_02_200ms")
    myTags = messageAttribute(m)
    print(myTags)
