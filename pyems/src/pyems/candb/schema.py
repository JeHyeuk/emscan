from pyems.typesys import DataDictionary, metaclass
from pandas import Index


class CanDbSchema(metaclass=metaclass):
    """
    CAN DB의 SCHEMA
    클래스 단위로 사용
    """
    METADATA = __meta__ = DataDictionary({
        "ECU":{
            "synonyms": ["ecu", "controller", "sender", "tx", "송출제어기"],
            "dtype": str,
            "width": 100,
            "align": "center",
        },
        "Message":{
            "synonyms": ["message", "msg"],
            "dtype": str,
            "width": 140,
            "align": "center",
        },
        "ID":{
            "synonyms": ["id"],
            "dtype": str,
            "width": 60,
            "align": "center",
        },
        "DLC":{
            "synonyms": ["dlc"],
            "dtype": int,
            "width": 30,
            "align": "center",
        },
        "Send Type":{
            "synonyms": ["sendtype"],
            "dtype": str,
            "width": 30,
            "align": "center",
        },
        "Cycle Time":{
            "synonyms": ["cycletime"],
            "dtype": int,
            "width": 30,
            "align": "center",
        },
        "Signal":{
            "synonyms": ["signal", "sig"],
            "dtype": str,
            "width": 200,
            "align": "left",
        },
        "Definition":{
            "synonyms": ["definition"],
            "dtype": str,
            "width": 240,
            "align": "left",
        },
        "Length":{
            "synonyms": ["length", "Length\n(Bit)"],
            "dtype": int,
            "width": 30,
            "align": "center",
        },
        "StartBit":{
            "synonyms": ["startbit", "Startbit", "address"],
            "dtype": int,
            "width": 30,
            "align": "center",
        },
        "Sig Receivers":{
            "synonyms": ["Destination", "receiver"],
            "dtype": str,
            "width": 80,
            "align": "left",
        },
        "UserSigValidity":{
            "synonyms": [],
            "dtype": str,
            "width": 60,
            "align": "center",
        },
        "Value Table":{
            "synonyms": ["table"],
            "dtype": str,
            "width": 140,
            "align": "left",
        },
        "Value Type":{
            "synonyms": ["type"],
            "dtype": str,
            "width": 80,
            "align": "center",
        },
        "GenSigStartValue":{
            "synonyms": ["startvalue", "initialValue", "initial"],
            "dtype": str,
            "width": 80,
            "align": "center",
        },
        "Factor":{
            "synonyms": ["factor"],
            "dtype": float,
            "width": 60,
            "align": "center",
        },
        "Offset":{
            "synonyms": ["offset"],
            "dtype": float,
            "width": 60,
            "align": "center",
        },
        "Min":{
            "synonyms": ["min"],
            "dtype": float,
            "width": 60,
            "align": "center",
        },
        "Max":{
            "synonyms": ["max"],
            "dtype": float,
            "width": 60,
            "align": "center",
        },
        "Unit":{
            "synonyms": ["unit"],
            "dtype": str,
            "width": 60,
            "align": "center",
        },
        "Local Network Wake Up Request":{
            "synonyms": [],
            "dtype": str,
            "width": 40,
            "align": "center",
        },
        "Network Request Holding Time":{
            "synonyms": [],
            "dtype": str,
            "width": 30,
            "align": "center",
        },
        "Description":{
            "synonyms": ["description"],
            "dtype": str,
            "width": 100,
            "align": "left",
        },
        "Version":{
            "synonyms": ["version"],
            "dtype": str,
            "width": 80,
            "align": "center",
        },
        "Requirement ID": {
            "synonyms": [],
            "dtype": str,
            "width": 100,
            "align": "center",
        },
        "Required Date": {
            "synonyms": [],
            "dtype": str,
            "width": 60,
            "align": "center",
        },
        "Remark": {
            "synonyms": [],
            "dtype": str,
            "width": 100,
            "align": "center",
        },
        "Status": {
            "synonyms": [],
            "dtype": str,
            "width": 60,
            "align": "center",
        },
        "ByteOrder": {
            "synonyms": [],
            "dtype": str,
            "width": 80,
            "align": "center",
        },
        "ICE Channel":{
            "synonyms": [],
            "dtype": str,
            "width": 60,
            "align": "center",
        },
        "ICE WakeUp":{
            "synonyms": [],
            "dtype": str,
            "width": 60,
            "align": "center",
        },
        "HEV Channel":{
            "synonyms": [],
            "dtype": str,
            "width": 60,
            "align": "center",
        },
        "HEV WakeUp": {
            "synonyms": [],
            "dtype": str,
            "width": 60,
            "align": "center",
        },
        "SystemConstant":{
            "synonyms": [],
            "dtype": str,
            "width": 160,
            "align": "center",
        },
        "Codeword":{
            "synonyms": [],
            "dtype": str,
            "width": 160,
            "align": "center",
        },
        "Formula":{
            "synonyms": [],
            "dtype": str,
            "width": 140,
            "align": "center",
        },
        "SignedProcessing":{
            "synonyms": [],
            "dtype": str,
            "width": 100,
            "align": "center",
        },
        "InterfacedVariable":{
            "synonyms": [],
            "dtype": str,
            "width": 200,
            "align": "left",
        },
        "SignalRenamed":{
            "synonyms": [],
            "dtype": str,
            "width": 200,
            "align": "left",
        },
    })

    __iterable__ = __meta__.items()
    __string__ = str(__meta__)

    def __class_getitem__(cls, item):
        return cls.__meta__[item]

    @classmethod
    def standardize(cls, columns: Index) -> list:
        standard_columns = []
        for col in cls.__meta__:
            if col in columns:
                standard_columns.append(col)
                continue
            for synonym in cls.__meta__[col].synonyms:
                if synonym in columns:
                    standard_columns.append(col)
            if not col in standard_columns:
                raise KeyError(f"Cannot find {col} in columns; {columns}")
        return standard_columns

    @classmethod
    def toJSpreadSheet(cls, columns: Index=None) -> list:
        if columns is None:
            columns = list(cls.__meta__.keys())
        else:
            columns = cls.standardize(columns)

        return [{
            "type": "text",
            "width": cls.__meta__[col].width,
            "title": col,
            "align": cls.__meta__[col].align
        } for col in columns]


if __name__ == "__main__":
    print(CanDbSchema)
    # print(CanDbSchema['ECU'])
    # print(CanDbSchema.toJSpreadSheet())
    # for test in CanDbSchema:
    #     print(test)