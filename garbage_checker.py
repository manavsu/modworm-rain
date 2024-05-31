from ipaddress import *
from typing import Tuple

def validate_ip(address) -> bool:
    try:
        ip_address(address)
        return True
    except ValueError:
        return False

def validate_port(port) -> bool:
    try:
        port = int(port)
        return 1 <= port <= 65535
    except ValueError:
        return False
    
def validate_cidr(cidr) -> bool:
    try:
        ip_network(cidr, strict=False)
        return True
    except ValueError:
        return False

def validate_modbus_address(address, count) -> bool:
    try:
        address = int(address)
        count = int(count)
        return 0 <= address <= 65535 and address + count <= 65535
    except ValueError:
        return False

def validate_slave_id(slave_id) -> bool:
    try:
        slave_id = int(slave_id)
        return 0 <= slave_id <= 255
    except ValueError:
        return False

def validate_func_code(func_code) -> bool:
    try:
        func_code = int(func_code)
        return 1 <= func_code <= 7 or func_code == 15 or func_code == 16
    except ValueError:
        return False
