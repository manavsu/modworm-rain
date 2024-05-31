import logging
import xml.etree.ElementTree as ET
import time
import subprocess
import shutil

logging.basicConfig()
log = logging.getLogger("nmap")
log.setLevel(logging.WARNING)

class Nmap:
    '''
    Wrapper for the nmap command line tool, make sure nmap is installed and in PATH. Check https://nmap.org for more info.
    '''
    def __init__(self) -> None:
        self.command = 'nmap'
        self.__check_path()
    
    def __check_path(self):
        if shutil.which(self.command) is None:
            raise FileNotFoundError(f"Could not find {self.command} in PATH")
    
    def scan(self, cidr, ports=None, args=None):
        '''
        Scan a network or host using nmap.

        cidr: CIDR notation for the network or host to scan.
        ports: Port range to scan, e.g. '1-1000'.
        args: Additional arguments to pass to nmap, separated by spaces.
        '''
        start_time = time.time()
        command = [self.command, cidr]
        if ports:
            command.append(f'-p{ports}')
        if args:
            command.extend(args.split())
        command.extend('-oX -'.split())

        result = subprocess.run(command, capture_output=True, text=True)
        result.check_returncode()
        result.stdout
        log.debug(f"{command} completed in {time.time() - start_time:.2f} seconds")
        return result.stdout