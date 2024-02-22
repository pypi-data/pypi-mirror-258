# PyWDCKit - Python
UNOFFICIAL Python bindings for Western Digital's WDCKit drive utility

A package that allows you to utilize and get data from Western Digital's WDCKit drive utility.

To download WDCKit visit the [official page](https://support-en.wd.com/app/answers/detailweb/a_id/50708/~/wdckit-drive-utility-download-and-instructions-for-internal-drives).

## Usage
```Python
from PyWDCKit import WDCKit, NotRunningAsAdmin, WDCKitNotFound
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%d-%b-%y %H:%M:%S'
)
wdckit = WDCKit()
try:
    logging.info(f'Found wdckit.exe at {wdckit.exec_path}')
except WDCKitNotFound as e:
    logging.error(e)
print(wdckit.get_duts())
```

Note: The package will automatically try to search for wdckit.exe within the current working directory.