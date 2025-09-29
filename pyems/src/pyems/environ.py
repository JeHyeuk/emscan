from pyems.dtypes import DataDictionary, Path
from dotenv import load_dotenv
import os


load_dotenv()
if os.getenv('SVN_PATH', None) is None:
    raise OSError('SVN_PATH environment variable is not set')

__path__ = os.getenv('SVN_PATH')
__root__ = Path(__path__, readonly=True)

SVN = DataDictionary(
    SVN=__path__,
    ROOT=__root__,
    CONF=__root__[r'GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename'],
    MODEL=__root__[r'model\ascet\trunk']
)


if __name__ == "__main__":
    print(SVN)
