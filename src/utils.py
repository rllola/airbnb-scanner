# pylint: disable=import-error
import scapy.all as scapy

def get_ip_mask():
    ip = scapy.get_if_addr(scapy.conf.iface).split('.')
    ip[3] = "0"
    ip_mask = '.'.join(ip) + '/24'
    
    return ip_mask        