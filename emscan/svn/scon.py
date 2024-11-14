try:
    from ..config import PATH
except ImportError:
    from emscan.config import PATH
import subprocess


class SourceControl:

    @classmethod
    def update(cls, *path):
        for _path in path:
            try:
                result = subprocess.run(
                    ['svn', 'update', _path],
                    capture_output=True,
                    text=True,
                    check=True
                )
                print("SVN Update Successful!")
                print(result.stdout)
            except subprocess.CalledProcessError as e:
                print("Error:", e.stderr)


if __name__ == "__main__":
    sc = SourceControl
    sc.update(PATH.SVN.BUILD.IR)