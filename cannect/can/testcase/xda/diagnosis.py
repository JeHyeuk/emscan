from pyems.mdf import MdfReader
from pyems.environ import ENV
from cannect.can.rule import naming

from datetime import datetime
from io import StringIO
from xml.etree.ElementTree import ElementTree, Element
from xml.dom import minidom
import os


class XdaDiagnosis(ElementTree):

    def __init__(self, dat:str, message:str):
        super().__init__(file=ENV["CAN"]["CAN_TestCase/Template/XDA.xda"])
        self.dat = dat
        self.mdf = MdfReader(dat)
        self.msg = message
        self.nm = naming(message)
        return

    @property
    def path(self) -> str:
        return self.dat.encode('ascii', 'xmlcharrefreplace').decode('ascii')

    def _serialize(self) -> str:
        stream = StringIO()
        self.write(
            file_or_filename=stream,
            encoding='unicode',
            xml_declaration=False,
            method='xml',
        )
        dom = f'{minidom.parseString(stream.getvalue()).toprettyxml(indent="  ")}' \
            .replace('<?xml version="1.0" ?>', '<?xml version="1.0" encoding="ISO-8859-1"?>')
        rejoin = []
        for line in dom.splitlines():
            if line.replace(" ", "").replace("\t", ""):
                line = line.replace("&amp;", "&")
                if "/>" in line and not any([key in line for key in [
                    "STRINGCHANNELS",
                    "SEGMENTLIST",
                    "BOOKMARKS",
                    "LAYOUT_LIST",
                    "HEADLINE_LIST"
                ]]):
                    line = line.replace("/", "") + line.replace(" ", "").replace("<", "</").replace("/>", ">")
                if "&lt;![CDATA" in line:
                    line = line.replace("&lt;![CDATA", "<![CDATA")
                if "]]&gt;" in line:
                    line = line.replace("]]&gt;", "]]>")
                rejoin.append(line)
        return "\n".join(rejoin)

    def change_reference_dat(self):
        for elem in self.iter():
            if elem.text is None:
                continue
            if '.dat' in elem.text:
                find = elem.text.find('.dat') + len('.dat')
                elem.text = elem.text.replace(elem.text[:find], self.path)
        return

    def change_timespan(self):
        for elem in self.iter('TimeEnd'):
            elem.text = str(self.mdf.index[-1])
        return

    def change_variables(self):
        def _replace(elem:Element, prev:str, curr:str):
            if elem.text and prev in elem.text:
                elem.text = elem.text.replace(prev, curr)


        for elem in self.iter():
            _replace(elem, "CanD_tiMonDetAbs_C", self.nm.detectionThresholdTime)
            _replace(elem, "CanD_cEnaDetAbsEsc01", self.nm.detectionEnable)
            _replace(elem, "CanD_cEnaDiagAbsEsc01", self.nm.diagnosisEnable)
            _replace(elem, "CanD_ctDetAbsEsc01", self.nm.detectionCounter)
            _replace(elem, "EEP_stFDABSESC01", self.nm.eep)
            _replace(elem, "FD_cVldAbsEsc01Msg", self.nm.messageCountValid)
            _replace(elem, "FD_cVldAbsEsc01Crc", self.nm.crcValid)
            _replace(elem, "FD_cVldAbsEsc01Alv", self.nm.aliveCountValid)
            _replace(elem, "CanD_tiFltAbsEsc01Msg", self.nm.debounceTimerMsg)
            _replace(elem, "CanD_tiFltAbsEsc01Crc", self.nm.debounceTimerCrc)
            _replace(elem, "CanD_tiFltAbsEsc01Alv", self.nm.debounceTimerAlv)
            _replace(elem, "CanD_cErrAbsEsc01Msg", self.nm.diagnosisMsg)
            _replace(elem, "CanD_cErrAbsEsc01Crc", self.nm.diagnosisCrc)
            _replace(elem, "CanD_cErrAbsEsc01Alv", self.nm.diagnosisAlv)
            _replace(elem, "DEve_FDAbs01Msg", self.nm.deveMsg)
            _replace(elem, "DEve_FDAbs01Crc", self.nm.deveCrc)
            _replace(elem, "DEve_FDAbs01Alv", self.nm.deveAlv)
            _replace(elem, "Fid_FDABSESC01D", self.nm.fid)
        return


    def create(self, path:str=''):
        self.change_reference_dat()
        self.change_timespan()
        self.change_variables()
        self.export(path)
        return

    def export(self, path:str=''):
        if not path:
            path = os.path.join(ENV['DOWNLOADS'], 'XDA')
        timestamp = datetime.now().timestamp()
        os.makedirs(path, exist_ok=True)
        os.utime(path, (timestamp, timestamp))
        filename = os.path.join(path, f'{self.msg}.xda')
        self.find('MEASUREFILES/ConfigName').text = \
             filename.encode('ascii', 'xmlcharrefreplace').decode('ascii')
        self.find('PRINT/COMMENT').text = f"<![CDATA[{self.find('PRINT/COMMENT').text}]]>"
        with open(file=filename, mode='w', encoding='utf-8') as f:
            f.write(self._serialize())
        return



if __name__ == "__main__":
    diag = DiagnosisDisplay(
        r"\\kefico\keti\ENT\Softroom\Temp\J.H.Lee\00 CR\CR10785931 J1979-2 CAN 진단 대응 ICE CANFD\08_Verification\Data\CanFDABSD_Det_Diag.dat",
        "WHL_01_10ms"
    )
    diag.create(r'\\kefico\keti\ENT\Softroom\Temp\J.H.Lee\00 CR\CR10785931 J1979-2 CAN 진단 대응 ICE CANFD\08_Verification\xda')
