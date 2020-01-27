from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon
import json
import scapy.all as scapy
import os

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

        self.icon = QIcon("./icons/spy-light.png")

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
        macaddress_file = os.path.join("data", "macaddress.io-db.json")
        print(macaddress_file)
        print(os.path.isfile(macaddress_file))
        with open(macaddress_file, encoding='utf-8') as f:
            print(f)
            content = f.readlines()
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
