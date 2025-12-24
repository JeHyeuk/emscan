from pyems.ascet import Amd
from pandas import DataFrame
from typing import List


class AmdDiff:

    def __init__(
        self,
        prev:str,
        post:str,
        exclude_imported:bool=True
    ):
        prev = Amd(prev)
        post = Amd(post)

        self.prev_elem = prev.main.dataframe('Element')
        self.post_elem = post.main.dataframe('Element')
        if exclude_imported:
            self.prev_elem = self.prev_elem[self.prev_elem['scope'] != 'imported']
            self.post_elem = self.post_elem[self.post_elem['scope'] != 'imported']

        self.prev_data = prev.data.dataframe('DataEntry')
        self.post_data = post.data.dataframe('DataEntry')
        return

    @property
    def deleted(self) -> List[str]:
        return list(set(self.prev_elem['name']) - set(self.post_elem['name']))

    @property
    def added(self) -> List[str]:
        return list(set(self.post_elem['name']) - set(self.prev_elem['name']))

    @property
    def added_parameters(self) -> DataFrame:
        elem = self.post_elem[
            self.post_elem['name'].isin(self.added) &
            (self.post_elem['kind'] == 'parameter')
        ]
        elem.set_index(keys='OID', inplace=True)
        data = self.post_data[self.post_data['elementName'].isin(elem['name'])]
        data.set_index(keys='elementOID', inplace=True)
        elem = elem.join(data[['value']], how='left')
        elem = elem[["name", "comment", "model", "value"]]
        elem.columns = ['Name', 'Description', 'Module', 'Recommendation Cal']
        elem['Default Cal'] = elem['Recommendation Cal']
        elem['Disable Cal'] = '-'
        elem['Remark'] = '-'
        elem.index = [""] * len(elem)
        return elem


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    diff = AmdDiff(
        r"D:\Archive\00_프로젝트\2017 통신개발-\2025\DS1201 IUMPR 미표출 ICE CANFD\02_Model\Prev\CanBMSD_48V.main.amd",
        r"D:\Archive\00_프로젝트\2017 통신개발-\2025\DS1201 IUMPR 미표출 ICE CANFD\02_Model\Post\CanBMSD_48V\CanBMSD_48V.main.amd",
    )
    print(diff.added_parameters)