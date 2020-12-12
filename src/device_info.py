import webbrowser
import os

from urllib.parse import urlencode
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from info import __email__, __github__

class DeviceInfoWidget(QWidget):
    """
    DeviceInfoWidget class
    """

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

        self.company_name = None
        self.mac_address = None

        layout.addWidget(self.label)
        layout.addWidget(self.report_email_button)
        layout.addWidget(self.report_github_button)
        self.setWindowTitle("Device Info")
        self.setLayout(layout)

    #pylint: disable=invalid-name
    def closeEvent(self, event):
        """
        override close event
        """
        # Just hide the widget
        event.ignore()
        self.hide()

    def open_email(self):
        """
        open default email application with ready to use template
        """
        os.system("""
            xdg-email \
                --subject 'Report device' \
                --body 'Hi, \r Reporting the following manufacturer as a company producing IP camera. \r Manufacturer: {} \r MAC: {}' \
                {}
        """.format(self.company_name, self.mac_address, __email__))

    def open_github(self):
        """
        open default browser application and redirect to github issue
        """
        body = """
            Reporting the following manufacturer as a company producing IP camera. \r Manufacturer: {} \r MAC: {}
        """.format(self.company_name, self.mac_address)
        github_arg = {
            "title": "[Report] {}".format(self.company_name),
            "body": body,
            "labels": "report"
            }
        webbrowser.open("{}/issues/new?{}".format(__github__, urlencode(github_arg)))


    def show_info(self, ip, mac_address, company_name):
        """
        open device info window
        """
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
