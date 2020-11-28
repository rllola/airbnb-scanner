from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QFile, QIODevice, QDir
import json
import scapy.all as scapy
import os
import data
import sys


class Application(QApplication):
    """Application class"""

    def __init__(self, *args, **kwargs):
        super(QApplication,self).__init__(*args, **kwargs)
        print('Application initiated')

        print("Creating menu...")
        self.menu = QMenu()
        self.separator = self.menu.addSeparator()
        self.quitAction = self.menu.addAction("Quit")
        self.quitAction.triggered.connect(self.quit)

        prefix_path = "."

        if ":/" in sys.path:
            prefix_path = ":"

        # FIXME: Detect Dark/Light mode
        # BODY: Pick light or dark icon to fit contrast and make it visible on different theme
        self.icon = QIcon(os.path.join(prefix_path,"icons","spy-light.png"))

        # Create the tray
        self.tray = QSystemTrayIcon(self.icon, None)
        self.tray.setContextMenu(self.menu)

        self.tray.show()

        # We are scanning local IP
        self.scan('192.168.1.0/24')

    def scan(self, ip):
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast/arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]

        self.device_menu = QMenu("Devices")

        clients_list = []

        # FIXME: Path for macaddress.io-db.json for dev
        # BODY: If doing dev we need to specify the path using another method
        if "DEV" in os.environ:
            qf = QFile(os.path.join("data","macaddress.io-db.json"))
        else:
            qf = QFile(data.__file__.replace("__init__.pyo", "macaddress.io-db.json"))
        qf.open(QIODevice.ReadOnly | QIODevice.Text)
        content = qf.readAll()
        content = bytes(content).decode().split("\n")
        qf.close()

        # Remove last empty item
        del content[-1]

        for element in answered_list:
            print(element[1].hwsrc)
            client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}

            company_name = "Unknown"
            for x in content:
                entry = json.JSONDecoder().decode(x.strip())
                if element[1].hwsrc.startswith(entry["oui"].lower()):
                    print(entry)
                    company_name = entry["companyName"]
                    break

            self.device_menu.addAction(company_name + "\n" + element[1].psrc)

            clients_list.append(client_dict)

        self.print_result(clients_list)



        self.menu.insertMenu(self.separator, self.device_menu)

    def print_result(self, results_list):
        print("IP\t\t\tMAC Address")
        print("----------------------------------------------------")
        for client in results_list:
            print(client["ip"] + "\t\t" + client["mac"])
