
import asyncio
import logging

from pymodbus.datastore import ModbusSequentialDataBlock, ModbusServerContext, ModbusSlaveContext
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server import ModbusTcpServer

from constants import *

from random import randint

logging.basicConfig()
log = logging.getLogger("IncrementingServer")
log.setLevel(logging.INFO)

class IncrementingServer:
    """
    A simple incrementing server for testing.

    Increments registers every second.

    Discrete Output Coils
    Discrete Input Contacts (Readonly)
    Addr:0-1000 (0x0000-0x03E7) -> toggled continuously
    
    Analog Output Holding Registers
    Analog Input Registers (Readonly)
    Addr:0-1000 (0x0000-0x03E7) -> incremented continuously at various rates
    """

    def __init__(self, host:str, port:int, num_clients:int, interval_seconds:int=1):
        self.interval_seconds = interval_seconds
        self.address = (host, port)
        self.running = False
        create_datablock = lambda cnt : ModbusSequentialDataBlock(0, [0x0000] * cnt)
        slave_contexts = {}
        for i in range(num_clients):
            slave_contexts[i] = ModbusSlaveContext(
                di=create_datablock(1000),
                co=create_datablock(1000),
                hr=create_datablock(1000),
                ir=create_datablock(1000),
                zero_mode=True,
            )
        self.identity = ModbusDeviceIdentification(
            info_name={
                "VendorName": "Modworm",
                "ProductCode": "RS",
                "VendorUrl": "https://modworm.com",
                "ProductName": "Random Server",
                "MajorMinorRevision": VERSION,
            })
        self.context = ModbusServerContext(slaves=slave_contexts, single=False)
        self.server = ModbusTcpServer(context=self.context, identity=self.identity, address=(host, port))
        log.info(f"random modbus server listening on {host}:{port}")


    async def start(self):
        '''start the modbus server and begin generating numbers.'''

        self.running = True
        await asyncio.gather(self.__increment_loop(), self.server.serve_forever())

    async def stop(self):
        '''stop the modbus server.'''
        self.running = False
        await self.server.shutdown()
    
    async def __increment_loop(self) -> None:
        log.info("starting incrementing function")
        while self.running:
            for slave_id in self.context.slaves():
                slave:ModbusSlaveContext = self.context[slave_id]
                slave.setValues(OUTPUT_COILS, 0, [slave.getValues(OUTPUT_COILS, 0, 1)[0] ^ 0x01])
                slave.setValues(INPUT_CONTACTS, 0, slave.getValues(OUTPUT_COILS, 0, 1))
                slave.setValues(HOLDING_REGISTERS, 0, [slave.getValues(HOLDING_REGISTERS, 0, 1)[0] + 1])
                slave.setValues(INPUT_REGISTERS, 0, slave.getValues(HOLDING_REGISTERS, 0, 1))

                cnts = list(range(1, 1000))
                slave.setValues(OUTPUT_COILS, 1, [(a + i) ^ 0x01 for a, i in zip(slave.getValues(OUTPUT_COILS, 1, 999), cnts)])
                slave.setValues(INPUT_CONTACTS, 1, slave.getValues(OUTPUT_COILS, 1, 999))
                slave.setValues(HOLDING_REGISTERS, 1, [(a + i & 0xFFFF) for i, a in zip(slave.getValues(HOLDING_REGISTERS, 1, 999), cnts)])
                slave.setValues(INPUT_REGISTERS, 1, slave.getValues(HOLDING_REGISTERS, 1, 999))
            await asyncio.sleep(self.interval_seconds)
