# pylint: disable=import-error
import scapy.all as scapy

def get_ip_mask():
    """Get the ip mask to scan on"""
    ip_interface = scapy.get_if_addr(scapy.conf.iface).split('.')
    ip_interface[3] = "0"
    ip_mask = '.'.join(ip_interface) + '/24'

    return ip_mask
