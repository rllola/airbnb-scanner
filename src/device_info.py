from __init__ import __email__, __github__
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
import webbrowser
from urllib.parse import urlencode
import os

class DeviceInfoWidget(QWidget):
    """DeviceInfoWidget class"""
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setOpenExternalLinks(True)
        self.label.setTextFormat(Qt.RichText)
        
        self.report_email_button = QPushButton("Report by email")
        self.report_email_button.clicked.connect(self.open_email)
        self.report_github_button = QPushButton("Report on github")
        self.report_github_button.clicked.connect(self.open_github)

        layout.addWidget(self.label)
        layout.addWidget(self.report_email_button)
        layout.addWidget(self.report_github_button)
        self.setWindowTitle("Device Info")
        self.setLayout(layout)

    def closeEvent(self, event):
        # Just hide the widget
        event.ignore()
        self.hide()
        
    def open_email(self):
        os.system("""
            xdg-email \
                --subject 'Report device' \
                --body 'Hi, \r Reporting the following manufacturer as a company producing IP camera. \r Manufacturer: {} \r MAC: {}' \
                {}
        """.format(self.company_name, self.mac_address, __email__)) 
        
    def open_github(self):
        github_arg = {
            "title": "[Report] {}".format(self.company_name),
            "body": "Reporting the following manufacturer as a company producing IP camera. \r Manufacturer: {} \r MAC: {}".format(self.company_name, self.mac_address),
            "labels": "report"
            }
        webbrowser.open("{}/issues/new?{}".format(__github__, urlencode(github_arg)))


    def show_info(self, ip, mac_address, company_name):
        self.company_name = company_name
        self.mac_address = mac_address
        self.label.setText(
            """
             IP: <br/>
             {ip}
             <br/><br/>
             Device MAC address: <br/> 
             {mac_address}
             <br/><br/>
             Manufacturer: <br/>
             {company_name}
             <br/><br/>
            """.format(ip=ip, mac_address=mac_address, company_name=company_name)
        )
        self.show()