import json
import os
import sys

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QFile, QIODevice

# pylint: disable=import-error
import scapy.all as scapy

from about import AboutWidget
from device_info import DeviceInfoWidget

# pylint: disable=too-many-instance-attributes
class Application(QApplication):
    """Application class"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('Application initiated')

        self.about_window = AboutWidget()
        self.device_info = DeviceInfoWidget()

        print("Creating menu...")
        # TODO: Create a menu class
        # BODY: Create a menu class to make Application class lighter.
        self.menu = QMenu()
        self.device_menu = QMenu("Devices")
        self.separator = self.menu.addSeparator()
        self.about_action = self.menu.addAction("About")
        self.about_action.triggered.connect(self.about_window.show)
        self.quit_action = self.menu.addAction("Quit")
        self.quit_action.triggered.connect(self.quit)

        self.keks = []

        prefix_path = "."

        if ":/" in sys.path:
            prefix_path = ":"

        database_file = QFile(os.path.join(prefix_path, "data", "macaddress.io-db.json"))
        database_file.open(QIODevice.ReadOnly | QIODevice.Text)
        self.mac_address_database = database_file.readAll()
        self.mac_address_database = bytes(self.mac_address_database).decode().split("\n")
        database_file.close()

        reported_file = QFile(os.path.join(prefix_path, "data", "reported.txt"))
        reported_file.open(QIODevice.ReadOnly | QIODevice.Text)
        content = reported_file.readAll()
        self.reported = bytes(content).decode().split("\n")
        reported_file.close()

        del self.mac_address_database[-1]

        # FIXME: Detect Dark/Light mode
        # BODY: Pick light or dark icon to fit contrast and make it visible on different theme
        self.icon = QIcon(os.path.join(prefix_path, "icons", "spy-light.png"))
        self.rescan_icon = QIcon(os.path.join(prefix_path, "icons", "reload.png"))
        self.warning_icon = QIcon(os.path.join(prefix_path, "icons", "warning.png"))

        # Create the tray
        self.tray = QSystemTrayIcon(self.icon, None)
        self.tray.setContextMenu(self.menu)

        self.tray.show()

        # We are scanning local IP
        self.scan('192.168.1.0/24')

    def rescan(self):
        """
        rescan the network
        """
        self.device_menu.clear()
        self.scan('192.168.1.0/24')

    def scan(self, ip_mask):
        """
        scan local network
        """
        # pylint: disable=no-member
        arp_request = scapy.ARP(pdst=ip_mask)
        # pylint: disable=no-member
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast/arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]

        self.rescan_action = self.device_menu.addAction(self.rescan_icon, "Rescan")
        self.rescan_action.triggered.connect(self.rescan)
        self.device_menu.addSeparator()

        clients_list = []

        for element in answered_list:
            client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}

            company_name = "Unknown"
            warning = False
            for mac_address_line in self.mac_address_database:
                entry = json.JSONDecoder().decode(mac_address_line.strip())
                if element[1].hwsrc.startswith(entry["oui"].lower()):
                    company_name = entry["companyName"]
                    if entry["oui"].lower() in self.reported:
                        warning = True
                    break

            action_text = "{}\n{}".format(company_name, client_dict["ip"])
            device_action = self.device_menu.addAction(action_text)
            if warning:
                device_action.setIcon(self.warning_icon)

            device_action.triggered.connect(
                lambda: self.device_info.show_info(
                    client_dict["ip"],
                    client_dict["mac"],
                    company_name))


            clients_list.append(client_dict)

        print_result(clients_list)

        self.menu.insertMenu(self.separator, self.device_menu)


def print_result(results_list):
    """
    Print the IP/MAC table
    """
    print("IP\t\t\tMAC Address")
    print("----------------------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])
