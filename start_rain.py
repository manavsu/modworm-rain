import asyncio
import signal
import sys
from echo_server import EchoServer
from incrementing_server import IncrementingServer
from random_server import RandomServer
import os

async def start_server(host, port, server_type):
    def signal_handler(sig, frame):
        loop = asyncio.get_event_loop()
        loop.create_task(server.stop())
        sys.exit(0)
        
    if server_type == "echo":
        server = EchoServer(host, port, 1)
    elif server_type == "incrementing":
        server = IncrementingServer(host, port, 1)
    elif server_type == "random":
        server = RandomServer(host, port, 1)
    signal.signal(signal.SIGTERM, signal_handler)

    await server.start()

def start_rain(host, port, server_type):
    asyncio.run(start_server(host, port, server_type))