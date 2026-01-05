from typing import Any, SupportsBytes, Union
import os, string


class SddReader:

    def __init__(self, sdd:Union[Any, str, SupportsBytes]):
        self.fullpath = ''
        if sdd.endswith('.rtf'):
            self.fullpath = sdd
        else:
            for path, _, files in os.walk(sdd):
                for file in files:
                    if not file == "FunctionDefinition.rtf":
                        continue
                    self.fullpath = os.path.join(path, file)
        if not self.fullpath:
            raise FileExistsError(f'{sdd} NOT FOUND')

        self.version_doc = ''
        self._n_doc = -1
        self.version_log = ''
        self.font = r'\f1'

        self.syntax = []
        with open(self.fullpath, "r", encoding='ansi') as f:
            for n, line in enumerate(f.readlines()):
                if "Arial" in line:
                    clip = line[:line.find('Arial')]
                    self.font = clip[clip.rfind('{') + 1:][:3]
                if not self.version_doc and "[" in line and "]" in line:
                    if r"\f1" in line:
                        line = line.replace(r"\f1", "")
                    self.version_doc = line[line.find('[') + 1:line.find(']')].replace(" ", "")
                    self._n_doc = n

                if self.version_doc and not self.version_log and "[" in line and "]" in line:
                    if r"\f1" in line:
                        line = line.replace(r"\f1", "")
                    self.version_log = line[line.find('[') + 1:line.find(']')].replace(" ", "")

                self.syntax.append(line)
        return

    def update(self, log:str):

        def to_rtf(text: str, fallback: str = "?") -> str:
            out = []
            for ch in text:
                if ch in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] or \
                        ch in ["[", "]", ".", ",", "-", "_", ">", "<", " "] or \
                        ch.lower() in string.ascii_lowercase:
                    out.append(ch)
                else:
                    code = ord(ch)
                    code = str(code)
                    out.append(f"\\u{code}{fallback}")
            return "".join(out)

        if self._n_doc == -1:
            return "FAILED TO UPDATE SDD"
        split = self.version_doc.split(".")
        split[-1] = str(int(split[-1]) + 1).zfill(3)
        self.version_doc = ".".join(split)

        doc = self.syntax[self._n_doc]
        prefix = doc[:doc.find('[') + 1]
        suffix = doc[doc.find(']'): ]
        self.syntax[self._n_doc] = f'{prefix}{self.version_doc}{suffix}'

        log = to_rtf(log)
        syntax = []
        for line in self.syntax:
            if self.version_log in line:
                syntax.append(rf'\wpparid0\plain{self.font}\fs20 [{self.version_doc}] {log} \par' + '\n')
            syntax.append(line)

        self.version_log = self.version_doc
        with open(self.fullpath, "w", encoding="ansi") as f:
            f.write("".join(syntax))
        return ''


if __name__ == "__main__":

    sdd = SddReader(
        r'D:\SDD\Notes\Files\040g1ngg01a01p070g504vva30e2i\FunctionDefinition.rtf'
    )
    status = sdd.update('testing')
    if status:
        print(status)