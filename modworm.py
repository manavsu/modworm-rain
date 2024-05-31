from echo_server import EchoServer
from incrementing_server import IncrementingServer
from random_server import RandomServer
import asyncio
import argparse
import garbage_checker
import enum

parser = argparse.ArgumentParser(prog="modworm", description="Modbus server for testing.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--type", default="random", choices=["echo", "incrementing", "random"], help="The type of server to run.")
parser.add_argument("--host", default="127.0.0.1", help="The host to listen on.")
parser.add_argument("--port", type=int, default=502, help="The port to listen on.")

async def main(host, port, server_type):
    if not garbage_checker.validate_ip(host):
        print(f"Invalid host: {host}")
        return
    if not garbage_checker.validate_port(port):
        print(f"Invalid port: {port}")
        return
    port = int(port)
    if server_type.lower() == "random":
        server = EchoServer(host, port, 1)
    elif server_type.lower() == "incrementing":
        server = IncrementingServer(host, port, 1)
    elif server_type.lower() == "echo":
        server = RandomServer(host, port, 1)
    else:
        print(f"Invalid server type: {server_type}")
        return
    await server.start()

if __name__ == "__main__":
    args = parser.parse_args()
    asyncio.run(main(host=args.host, port=args.port, server_type=args.type))