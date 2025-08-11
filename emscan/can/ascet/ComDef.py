from emscan.env import PATH
from emscan.core.ascet.amd import AmdIO
from emscan.can.db.db import db as canDB
from emscan.can.ascet.db2elem import SignalElement, MessageElement, crcClassElement


class ComDef:

    def __init__(self, db:canDB, engineType:str, resource:str=''):
        self.db = db

        """
        베이스 모델 설정
        @resource가 주어진 경우 해당 모델을 사용히며 주어지지 않은 경우
        SVN의 최신 모델을 베이스로 사용
        """
        self.name = name = 'ComDef_HEV' if engineType == 'HEV' else 'ComDef'
        self.path = path = PATH.makedir(f'{PATH.DOWNLOADS}/{name}')
        if not resource:
            resource = PATH.SVN.CANMODEL.findfile(f'{name}.zip')
        if resource.endswith('.zip'):
            PATH.unzip(resource, path)
        # if resource.endswith('.main.amd'):
        #
        #     for file
        self.resource = resource


        """
        CAN DB가 개발 모드가 아닌 경우 개발 모드로 변환 후 모델 생성
        - 송출 제어기: EMS 및 특수 사양 LOCAL-CAN 통신 제어기 제외
        """
        if not db.isDevMode:
            EXCLUDE = ["EMS", "CVVD", "MHSG", "NOx"]
            if engineType == "ICE":
                EXCLUDE += ["BMS", "LDC"]

            DB.dev_mode(engineType)
            DB.constraint(~DB["ECU"].isin(EXCLUDE))



        self.main = AmdIO(rf'{path}\{name}.main.amd')
        self.impl = AmdIO(rf'{path}\{name}.implementation.amd')
        self.data = AmdIO(rf'{path}\{name}.data.amd')
        self.spec = AmdIO(rf'{path}\{name}.specification.amd')

        elements = self.main.dataframe('Element')
        methods = self.main.dataframe('MethodSignature')
        oids = dict(zip(elements['name'], elements['OID']))
        oids.update(dict(zip(methods['name'], methods['OID'])))
        self.oids = oids

        """
        DB 메시지 기반의 요소 생성
        """
        self.ME = {name: MessageElement(obj, oids=oids) for name, obj in db.messages.items()}
        self.SE = [SignalElement(sig, oids=oids) for sig in db.signals]
        return

    def no_name(self, amd:str, tag:str):
        alignment = [
            "counter",
            "buffer",
            "size",
            "counterCalc",
            "timerThreshold",
            "messageCountTimer",
            "aliveCountTimer",
            "crcTimer",
            "messageCounterValidity",
            "aliveCounterValidity",
            "crcValidity",
            "aliveCounterCalc",
            "crcCalc"
        ]
        amd:AmdIO = self.__getattribute__(amd)

        elem = amd.strictFind(tag)[0]
        parent = amd.findParent(elem)[elem]
        parent.clear()

        for se in self.SE:
            parent.append(getattr(se, tag))

        for key in alignment:
            for name, obj in self.db.messages.items():
                if "alive" in key and not obj.hasAliveCounter():
                    continue
                if "crc" in key and not obj.hasCRC():
                    continue

                me = self.ME[name]
                attr = getattr(me, key)
                parent.append(getattr(attr, tag))
        parent.append(crcClassElement(8).Element)
        parent.append(crcClassElement(16).Element)
        return


if __name__ == "__main__":
    from emscan.can.db.db import DB
    from pandas import set_option

    set_option('display.expand_frame_repr', False)


    model = ComDef(DB, 'ICE')
    print(model.resource)
    old = model.main.dataframe('Element').copy().set_index(keys=['name', 'OID'])

    # print(model.main.dataframe('Element'))
    model.no_name('main', 'Element')
    # print(model.main.dataframe('Element'))
    new = model.main.dataframe('Element').copy().set_index(keys=['name', 'OID'])

    add = new[~new.index.isin(old.index)]
    deleted = old[~old.index.isin(new.index)]

    print(add)
    print(deleted)

