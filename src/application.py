from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QFile, QIODevice, QDir

from about import AboutWidget

import json
import scapy.all as scapy
import os
import sys


class Application(QApplication):
    """Application class"""

    def __init__(self, *args, **kwargs):
        super(QApplication,self).__init__(*args, **kwargs)
        print('Application initiated')

        self.about_window = AboutWidget()

        print("Creating menu...")
        # TODO: Create a menu class
        # BODY: Create a menu class to make Application class lighter.
        self.menu = QMenu()
        self.device_menu = QMenu("Devices")
        self.separator = self.menu.addSeparator()
        self.aboutAction = self.menu.addAction("About")
        self.aboutAction.triggered.connect(self.about_window.show)
        self.quitAction = self.menu.addAction("Quit")
        self.quitAction.triggered.connect(self.quit)
        
        prefix_path = "."

        if ":/" in sys.path:
            prefix_path = ":"

        self.databaseFile = QFile(os.path.join(prefix_path,"data","macaddress.io-db.json"))


        # FIXME: Detect Dark/Light mode
        # BODY: Pick light or dark icon to fit contrast and make it visible on different theme
        self.icon = QIcon(os.path.join(prefix_path,"icons","spy-light.png"))
        self.rescanIcon = QIcon(os.path.join(prefix_path,"icons","reload.png"))

        # Create the tray
        self.tray = QSystemTrayIcon(self.icon, None)
        self.tray.setContextMenu(self.menu)

        self.tray.show()

        # We are scanning local IP
        self.scan('192.168.1.0/24')    

    def rescan(self):
        self.device_menu.clear()
        self.scan('192.168.1.0/24')

    def scan(self, ip):
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast/arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]
        
        self.rescanAction = self.device_menu.addAction(self.rescanIcon,"Rescan")
        self.rescanAction.triggered.connect(self.rescan)
        self.device_menu.addSeparator()

        clients_list = []

        self.databaseFile.open(QIODevice.ReadOnly | QIODevice.Text)
        content = self.databaseFile.readAll()
        content = bytes(content).decode().split("\n")
        self.databaseFile.close()

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
