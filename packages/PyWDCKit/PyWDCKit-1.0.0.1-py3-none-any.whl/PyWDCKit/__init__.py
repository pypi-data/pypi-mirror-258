VERSION = "1.0.0.1"
if not __name__ == "__main__":
    from .main import WDCKit, NotRunningAsAdmin, WDCKitNotFound
else:
    from main import WDCKit, NotRunningAsAdmin, WDCKitNotFound
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