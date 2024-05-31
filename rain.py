import asyncio
import signal
import sys
from echo_server import EchoServer
from incrementing_server import IncrementingServer
from random_server import RandomServer
import os

async def start_server(host, port, server_type):
    print("start_server", os.getpid())
    def signal_handler(sig, frame):
        print(f"SIGTERM received, shutting down...{host} {port}")
        asyncio.run(server.stop())
        sys.exit(0)
        
    if server_type == "random":
        server = EchoServer(host, port, 1)
    elif server_type == "incrementing":
        server = IncrementingServer(host, port, 1)
    elif server_type == "echo":
        server = RandomServer(host, port, 1)
    signal.signal(signal.SIGTERM, signal_handler)

    await server.start()

def Rain(host, port, server_type):
    print("Rain", os.getpid())
    asyncio.run(start_server(host, port, server_type))