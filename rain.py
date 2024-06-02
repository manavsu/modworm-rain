
import argparse
import garbage_checker
import os
from start_rain import start_rain
from kill import kill
import subprocess
import sys
import logging
import port_scanner

PROCESS_NAME = "rain"
VERSION = "v1.0.0"

logging.basicConfig(level=logging.WARNING)

parser = argparse.ArgumentParser(prog="rain", description="modbus server manager for testing.", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--version", action='version', version=VERSION)
parser.add_argument("-k", "--kill", action='store_true', help="kill all active servers.")
parser.add_argument("-d", "--daemonize", action='store_true', help="daemonize the server and run in the background.")
parser.add_argument("-q", "--quiet", action='store_true', help="suppress output.")
parser.add_argument("--host", default="127.0.0.1", help="the host to listen on. default=127.0.0.1")
parser.add_argument("--port", type=int, default=50902, help="the port to listen on. default=50902")
parser.add_argument("--type", default="incrementing", help="the type of server to run. default=incrementing" +
                    "\n" + 
                    "\n-- server types --" +
                    "\nincrementing:" +
                    "\n\tincrements registers every second." +
                    "\n" +
                    "\n\tdiscrete output coils" +
                    "\n\tdiscrete input contacts (readonly)" +
                    "\n\taddr:0-1000 (0x0000-0x03E7) -> toggled continuously" +
                    "\n" +
                    "\n\tanalog output holding registers" +
                    "\n\tanalog input registers (readonly)" +
                    "\n\taddr:0-1000 (0x0000-0x03E7) -> incremented continuously at various rates, echo, incrementing" +
                    "\n"
                    "\nrandom:" +
                    "\n\tgenerates 999 random values and updates them every second." +
                    "\n" +
                    "\n\tdiscrete output coils" +
                    "\n\tdiscrete input contacts (readonly)" +
                    "\n\taddr:0 (0x0000) -> toggled continuously" +
                    "\n\taddr:1-999 (0x0001-0x03E7) -> random mod 2" +
                    "\n" +
                    "\n\tanalog output holding registers" +
                    "\n\tanalog input registers (readonly)" +
                    "\n\taddr:0 (0x0000) -> incremented continuously" +
                    "\n\taddr:1-999 (0x0001-0x03E7) -> random" +
                    "\n" +
                    "\necho:" +
                    "\n\techoes values from one register to another." +
                    "\n\tdiscrete output coils" +
                    "\n\taddr:0 (0x0000) -> toggled continuously" +
                    "\n\taddr:1-1000 (0x0001-0x03E7) -> echoed to addr:1001-2000 (0x03E8-0x07D0)" +
                    "\n" +
                    "\n\tanalog output holding registers" +
                    "\n\taddr:0 (0x0000) -> incremented continuously" +
                    "\n\taddr:1-1000 (0x0001-0x03E7) -> echoed to addr:1001-2000 (0x03E8-0x07D0)" +
                    "\n" +
                    "\n\tdiscrete input contacts (readonly)" +
                    "\n\taddr:0 (0x0000) -> toggled continuously" +
                    "\n\taddr:1-1000 (0x0001-0x03E7) -> echoed from discrete output coils addr:1-1000 (0x0001-0x03E7)" +  
                    "\n" +
                    "\n\tanalog input registers (readonly)" +
                    "\n\taddr:0 (0x0000) -> incremented continuously" +
                    "\n\taddr:1-1000 (0x0001-0x03E7) -> echoed from analog output holding registers addr:1-1000 (0x0001-0x03E7)")

def main(host, port, server_type, demonize, quiet):
    if not garbage_checker.validate_ip(host):
        print(f"Invalid host: {host}")
    if not garbage_checker.validate_port(port):
        print(f"Invalid port: {port}")
        return
    port = int(port)
    if port < 1024:
        if os.getuid() != 0:
                print("You must be a root user to use a port below 1024.")
                return
    
    if port_scanner.check_port(host, port):
        print(f"Port {port} is already in use.")
        return
        
    server_type = server_type.lower()
    if not (server_type == "random" or server_type == "echo" or server_type == "incrementing"):
        print(f"Invalid server type: {server_type}")
        return
    if not demonize:
        if not quiet:
            print(f"Starting server on {host}:{port} type -> {server_type}")
        start_rain(host, port, server_type)
    else:
        subprocess.Popen([sys.executable, "--port", str(port), "--host", host, "--type", server_type, "--quiet"])
        if not quiet:
            print(f"Daemonized server created on {host}:{port} type -> {server_type}")

if __name__ == "__main__":
    args = parser.parse_args()
    if args.kill:
        kill(PROCESS_NAME)
    else:
        main(host=args.host, port=args.port, server_type=args.type, demonize=args.daemonize, quiet=args.quiet)