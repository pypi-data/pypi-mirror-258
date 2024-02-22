import os
import fnmatch
import subprocess
import logging
import json
from win32com.shell import shell
import io

# Define Exception Handler
class NotRunningAsAdmin(Exception):
    def __init__(self, *args: object) -> None:
        logging.error(f"Handling exception!")
        super().__init__(*args)


class WDCKitNotFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


# Main Class
class WDCKit:
    def __init__(self, accept_terms: bool = True, retain_logs: bool = False) -> None:
        self.exec_path = self.__find_wdckit()
        if not shell.IsUserAnAdmin():
            raise NotRunningAsAdmin("Not running as admin! Cannot execute!")
        self.retain_logs = retain_logs
        if accept_terms:
            self.__accept_terms()

    def __execute(self, command):
        logging.debug(f'Executing: {command}')
        out, err = subprocess.Popen(
            command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=1
        ).communicate()
        try:
            for line in out.decode('unicode_escape').replace('\r\n\r\n', '\r\n').replace('\r\n', '\n').strip().split('\n'):
                logging.debug(line)
        except:
            for line in out.decode().replace('\r\n\r\n', '\r\n').replace('\r\n', '\n').strip().split('\n'):
                logging.debug(line)
        return out

    def __find_wdckit(self) -> str:
        matches = []
        for root, dirnames, filenames in os.walk("."):
            for filename in fnmatch.filter(filenames, 'wdckit.exe'):
                matches.append(os.path.join(root, filename))

        if len(matches) > 0:
            return matches[0]
        raise WDCKitNotFound('Unable to find path to wdckit.exe')

    def __accept_terms(self):
        self.exec_path
        # return True if file exists
        self.license_file_path = os.path.join(
            "\\".join(self.exec_path.split('\\')[:-1]), ".wdckit_lic")
        if os.path.exists(self.license_file_path):
            logging.info("WDCKit licenses already accepted! ")
        else:
            logging.info("WDCKit licenses doesn't exist! Accepting licenses.")
            with io.open(self.license_file_path, 'w') as stream:
                stream.write('1\n')
            return True

    def __parse_results(self, output: bytes) -> dict:
        try:
            try:
                op = json.loads("".join(output.decode().replace("\\","/").replace("//","/").strip().replace(" ", "").split('\r\n')[5:]))['wdckit']['results']
            except:
                op = json.loads("".join(output.decode('unicode_escape').replace("\\","/").replace("//","/").strip().replace(" ", "").split('\r\n')[5:]))['wdckit']['results']
        except:
            return output.decode()
        return op

    def get_duts(self):
        logging.info("Collecting DUT info")
        output = self.__execute(f'{self.exec_path} s --output json')
        return self.__parse_results(output)

    def get_smart(self, device: str):
        logging.info(f"Getting SMART for {device}")
        output = self.__execute(f'{self.exec_path} getsmart {device} --output json')
        return self.__parse_results(output)
    
    def get_dui(self, device, file_save_path:str = r"C:\Automance\DUI"):
        logging.info("Collecting DUI")
        output = self.__execute(f'{self.exec_path} getdui {device} --no-trace --no-progress --nobanner --save {file_save_path}')
        return self.__parse_results(output)

if __name__ == "__main__":
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
