import nmap
import logging
import xml.etree.ElementTree as ET
import time

logging.basicConfig()
log = logging.getLogger("ServerScanner")
log.setLevel(logging.WARNING)

def scan_network(cidr, port='502'):
    '''
    Scan a network or host using nmap.

    cidr: CIDR notation for the network or host to scan.
    port: Port to scan, default is 502.
    '''
    start_time = time.time()
    nm = nmap.Nmap()
    hosts = __parse_nmap_xml(nm.scan(cidr, port))
    log.debug(f"scan_network {cidr}:{port} completed in {time.time() - start_time:.2f} seconds")
    return hosts

def __parse_nmap_xml(xml_string):
    tree = ET.fromstring(xml_string)
    hosts = []
    for host in tree.findall('host'):
        status = host.find('status').get('state')
        address = host.find('address').get('addr')
        if status != 'up':
            continue
        ports = host.find('ports')
        if ports is None:
            continue
        for port in ports.findall('port'):
            port_id = port.get('portid')
            state = port.find('state').get('state')
            if state == 'open':
                hosts.append({"address" : address, "port" : port_id})
    return hosts

