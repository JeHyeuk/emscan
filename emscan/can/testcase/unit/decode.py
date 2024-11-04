try:
    from ....core.testcase.case import Case
    from ...rule import naming
except ImportError:
    from emscan.core.testcase.case import Case
    from emscan.can.rule import naming
from pandas import Series


class RxDecode(Case):

    def __init__(self, sig:Series, **override):
        nm = naming(sig)
        sg = sig.SignalRenamed if sig.SignalRenamed else sig.name
        var = f"{sg}_Can"
        unit = '-' if not sig.Unit else sig.Unit
        index = self._index(sig)
        buff = "\n".join([f"{nm.buffer}_[{n}]" for n in index])
        vals = '\n'.join(['Unconcerned'] * len(index))
        expr = f"{index[0]}:{index[-1]}" if len(index) > 1 else f"{index[0]}"
        kwargs = {
            "Category": "UNIT",
            "Group": "CAN",
            "Test Case Name": "Signal Decoding Test",
            "Test Purpose, Description": f"{sg} @{nm}({sig.ID}) Decoding Test",
            "Test Execution (TE) - Description": f"CAN 신호: {sg} @{nm} 송출\n"
                                                 f"- 차량 검증 시: 차량 사양에 따름\n"
                                                 f"- 정적 검증 시: 포괄 범위 동적 신호 송출",
            "TE-Variable": f"{nm.counter}\n"
                           f"{buff}",
            "TE-Compare": "'=",
            "TE-Value": f"△1\n"
                        f"{vals}",
            "Expected Results (ER) - Description": f"신호 수신 시\n"
                                                   f"- Message Counter = △1\n"
                                                   f"- Signal Variable = Buffer[{expr}]\n"
                                                   f"신호 속성 DB 값과 일치",
            "ER-Variable": f"{var}",
            "ER-Compare": "'=",
            "ER-Value": f"{nm.buffer}_[{expr}]",
            "Test Result Description": f"신호 수신 시\n"
                                       f"- {nm.counter} = △1\n"
                                       f"- {var} = {nm.buffer}_[{expr}]\n"
                                       f"  * Length(Bit): {sig.Length}\n"
                                       f"  * Start Bit:  {sig.StartBit}\n\n"
                                       f"신호 속성\n"
                                       f"- Factor: {sig.Factor}\n"
                                       f"- Offset: {sig.Offset}\n"
                                       f"- Min: {sig.Offset} [{unit}]\n"
                                       f"- Max: {sig.Factor * (2 ** sig.Length - 1) + sig.Offset} [{unit}]",
        }
        kwargs.update(override)
        super().__init__(**kwargs)
        self._sig_ = sig
        return

    @staticmethod
    def _index(sig:Series) -> range:
        start_byte = sig.StartBit // 8
        end_bit = sig.StartBit + sig.Length
        end_byte = end_bit // 8
        if (end_bit / 8) > end_byte:
            end_byte += 1
        return range(start_byte, end_byte, 1)

    @property
    def length(self) -> int:
        return self._sig_.Length

    @property
    def address(self) -> int:
        return self._sig_.StartBit

    @property
    def factor(self) -> float:
        return self._sig_.Factor

    @property
    def offset(self) -> float:
        return self._sig_.Offset