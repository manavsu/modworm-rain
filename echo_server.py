
import asyncio
import logging

from pymodbus.datastore import ModbusSequentialDataBlock, ModbusServerContext, ModbusSlaveContext
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server import ModbusTcpServer

from constants import *

logging.basicConfig()
log = logging.getLogger("EchoServer")
log.setLevel(logging.WARNING)


class EchoServer:
    """
    A simple echoing server for testing.

    Discrete Output Coils
    Addr:0 (0x0000) -> toggled continuously
    Addr:1-1000 (0x0001-0x03E7) -> echoed to Addr:1001-2000 (0x03E8-0x07D0)
    
    Analog Output Holding Registers
    Addr:0 (0x0000) -> incremented continuously
    Addr:1-1000 (0x0001-0x03E7) -> echoed to Addr:1001-2000 (0x03E8-0x07D0)

    Discrete Input Contacts (Readonly)
    Addr:0 (0x0000) -> toggled continuously
    Addr:1-1000 (0x0001-0x03E7) -> echoed from Discrete Output Coils Addr:1-1000 (0x0001-0x03E7)

    Analog Input Registers (Readonly)
    Addr:0 (0x0000) -> incremented continuously
    Addr:1-1000 (0x0001-0x03E7) -> echoed from Analog Output Holding Registers Addr:1-1000 (0x0001-0x03E7)
    """

    def __init__(self, host:str, port:int, num_clients:int, interval_seconds:int=1):
        self.interval_seconds = interval_seconds
        self.address = (host, port)
        self.running = False
        create_datablock = lambda cnt : ModbusSequentialDataBlock(0x0000, [0x0000] * cnt)
        slave_contexts = {}
        for i in range(num_clients):
            slave_contexts[i] = ModbusSlaveContext(
                di=create_datablock(1000),
                co=create_datablock(2000),
                hr=create_datablock(2000),
                ir=create_datablock(1000),
                zero_mode=True,
            )
        self.identity = ModbusDeviceIdentification(
            info_name={
                "VendorName": "Modworm",
                "ProductCode": "ES",
                "VendorUrl": "https://modworm.com",
                "ProductName": "Echo Server",
                "MajorMinorRevision": VERSION,
            })
        self.context = ModbusServerContext(slaves=slave_contexts, single=False)
        self.server = ModbusTcpServer(context=self.context, identity=self.identity, address=(host, port))
        log.info(f"echo modbus server listening on {host}:{port}")


    async def start(self):
        '''start the Modbus server and begin echoing.'''

        self.running = True
        await asyncio.gather(self.__echo_loop(), self.server.serve_forever())

    async def stop(self):
        '''stop the Modbus server.'''
        self.running = False
        await self.server.shutdown()
    
    async def __echo_loop(self) -> None:
        log.info("starting echo function")
        while self.running:
            for slave_id in self.context.slaves():
                slave:ModbusSlaveContext = self.context[slave_id]
                slave.setValues(OUTPUT_COILS, 0, [slave.getValues(OUTPUT_COILS, 0, 1)[0] ^ 0x01])
                slave.setValues(INPUT_CONTACTS, 0, slave.getValues(OUTPUT_COILS, 0, 1))
                slave.setValues(HOLDING_REGISTERS, 0, [slave.getValues(HOLDING_REGISTERS, 0, 1)[0] + 1])
                slave.setValues(INPUT_REGISTERS, 0, slave.getValues(HOLDING_REGISTERS, 0, 1))

                values = slave.getValues(HOLDING_REGISTERS, 1, 999)

                slave.setValues(HOLDING_REGISTERS, 1000, values)
                slave.setValues(INPUT_REGISTERS, 1, values)

                values = slave.getValues(OUTPUT_COILS, 1, 999)
                slave.setValues(OUTPUT_COILS, 1000, values)
                slave.setValues(INPUT_CONTACTS, 1, values)
            await asyncio.sleep(self.interval_seconds)
