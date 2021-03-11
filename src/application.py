import json
import os
import sys
import platform

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QFile, QIODevice

# pylint: disable=no-name-in-module
from scapy.all import ARP, Ether, srp

from about import AboutWidget
from preferences import PreferencesWidget
from device_info import DeviceInfoWidget
from utils import get_ip_mask

# pylint: disable=too-many-instance-attributes
class Application(QApplication):
    """Application class"""

    # pylint: disable=too-many-statements
    def __init__(self, config, config_file, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('Application initiated')

        self.config = config
        self.config_file = config_file
        self.dark_mode = self.config['theme'].getboolean('DarkMode')

        self.about_window = AboutWidget()
        self.preferences_window = PreferencesWidget(config, self.handle_dark_mode_change)
        self.device_info = DeviceInfoWidget()

        # Get Ip mask to scan on
        self.ip_mask = get_ip_mask()

        print("Creating menu...")
        # TODO: Create a menu class
        # BODY: Create a menu class to make Application class lighter.
        self.menu = QMenu()
        self.device_menu = QMenu("Devices")
        self.separator = self.menu.addSeparator()
        self.about_action = self.menu.addAction("About")
        self.about_action.triggered.connect(self.about_window.show)
        self.preferences_action = self.menu.addAction("Preferences")
        self.preferences_action.triggered.connect(self.preferences_window.show)
        self.quit_action = self.menu.addAction("Quit")
        self.quit_action.triggered.connect(self.quit)

        prefix_path = "."

        if ":/" in sys.path:
            prefix_path = ":"
        elif platform.system() == "Windows":
            prefix_path = ""

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

        if self.dark_mode:
            dark_stylesheet = """
            QMenu {background-color: #19FFFFFF; color: white; padding: 20px 1px; min-width: 200px; border: 1px solid white;}
            QMenu::item {padding: 8px 20px;}
            QMenu::icon {margin-right: 20px;}
            QMenu::item:selected {background: rgba(100, 100, 100, 150);}
            """

            if platform.system() == "Windows":
                self.menu.setStyleSheet(dark_stylesheet)
                self.device_menu.setStyleSheet(dark_stylesheet)

            self.icon = QIcon(os.path.join(prefix_path, "icons", "spy-light.svg"))
            self.rescan_icon = QIcon(os.path.join(prefix_path, "icons", "reload-light.svg"))
            self.warning_icon = QIcon(os.path.join(prefix_path, "icons", "warning-light.svg"))
        else:
            self.icon = QIcon(os.path.join(prefix_path, "icons", "spy.svg"))
            self.rescan_icon = QIcon(os.path.join(prefix_path, "icons", "reload.svg"))
            self.warning_icon = QIcon(os.path.join(prefix_path, "icons", "warning.svg"))

        # Create the tray
        self.tray = QSystemTrayIcon(self.icon, None)
        self.tray.setContextMenu(self.menu)

        self.tray.show()

        # We are scanning local IP
        self.scan(self.ip_mask)

    def handle_dark_mode_change(self):
        """
        handle theme changes in the applicatino
        """

        self.config['theme']['DarkMode'] = 'true'
        # Update config file
        with open(self.config_file, 'w') as file:
            self.config.write(file)

        self.dark_mode = not self.dark_mode
        prefix_path = "."
        if ":/" in sys.path:
            prefix_path = ":"

        if self.dark_mode:
            self.icon = QIcon(os.path.join(prefix_path, "icons", "spy-light.svg"))
            self.rescan_icon = QIcon(os.path.join(prefix_path, "icons", "reload-light.svg"))
            self.warning_icon = QIcon(os.path.join(prefix_path, "icons", "warning-light.svg"))
        else:
            self.icon = QIcon(os.path.join(prefix_path, "icons", "spy.svg"))
            self.rescan_icon = QIcon(os.path.join(prefix_path, "icons", "reload.svg"))
            self.warning_icon = QIcon(os.path.join(prefix_path, "icons", "warning.svg"))

        for action in self.device_menu.actions():
            if action.iconText() == 'Rescan':
                action.setIcon(self.rescan_icon)
            elif not action.icon().isNull():
                action.setIcon(self.warning_icon)

        self.tray.setIcon(self.icon)

    def rescan(self):
        """
        rescan the network
        """
        self.device_menu.clear()
        self.scan(self.ip_mask)

    # pylint: disable=too-many-locals
    def scan(self, ip_mask):
        """
        scan local network
        """
        # pylint: disable=no-member
        arp_request = ARP(pdst=ip_mask)
        # pylint: disable=no-member
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast/arp_request
        answered_list = srp(arp_request_broadcast, timeout=2, verbose=False)[0]

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

            def triggered_info(client_ip, client_mac, company):
                self.device_info.show_info(
                    client_ip,
                    client_mac,
                    company)

            device_action.triggered.connect(
                lambda x,
                       client_ip=client_dict["ip"],
                       client_mac=client_dict["mac"],
                       company=company_name:
                triggered_info(client_ip, client_mac, company)
            )


            clients_list.append(client_dict)

        self.menu.insertMenu(self.separator, self.device_menu)


def print_result(results_list):
    """
    Print the IP/MAC table
    """
    print("IP\t\t\tMAC Address")
    print("----------------------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])
