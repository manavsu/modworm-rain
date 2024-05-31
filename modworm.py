
import asyncio
import argparse
import garbage_checker
import enum
import os
from rain import Rain
from kill import kill
import daemon
import subprocess
import sys

PROCESS_NAME = "modworm"
VERSION = "v1.0.0"

parser = argparse.ArgumentParser(prog="modworm", description="Modbus server for testing.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--type", default="random", choices=["echo", "incrementing", "random"], help="The type of server to run.")
parser.add_argument("--host", default="127.0.0.1", help="The host to listen on.")
parser.add_argument("--port", type=int, default=50902, help="The port to listen on.")
parser.add_argument("-d", action='store_true', help="Daemonize the server and run in the background.")
parser.add_argument("-k", action='store_true', help="Kill all daemonized servers.")
parser.add_argument("--version", action='version', version=VERSION)

def main(host, port, server_type, demonize):
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
        
    server_type = server_type.lower()
    if not (server_type == "random" or server_type == "echo" or server_type == "incrementing"):
        print(f"Invalid server type: {server_type}")
        return
    if not demonize:
        Rain(host, port, server_type)
    else:
        subprocess.Popen([sys.executable, "--port", str(port), "--host", host, "--type", server_type])
        print(f"Daemonized server running on {host}:{port} with type {server_type}")

if __name__ == "__main__":
    args = parser.parse_args()
    if args.k:
        kill(PROCESS_NAME)
    else:
        main(host=args.host, port=args.port, server_type=args.type, demonize=args.d)