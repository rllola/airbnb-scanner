from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt

from info import __version__, __author__, __email__, __github__

class AboutWidget(QWidget):
    """AboutWiget class"""

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setOpenExternalLinks(True)
        self.label.setTextFormat(Qt.TextFormat.RichText)
        self.label.setText(
            """
            <center>
                <b>Airbnb Scanner</b><br/>
                Version v{version}
                <br/><br/>
                Created and maintained by {author} (<a href="mailto:{email}">{email}</a>).
                <br/><br/>
            </center>
                Source code : <a href="{github}">{github}</a><br/>
                Report an issue : <a href="{github}/issues">{github}/issues</a> <br/><br/>
                Under <a href="http://www.wtfpl.net/">
                    Do What the Fuck You Want to Public License
                </a>.
            """.format(version=__version__, author=__author__, email=__email__, github=__github__)
        )
        layout.addWidget(self.label)
        self.setWindowTitle("About")
        self.setLayout(layout)

    #pylint: disable=invalid-name
    def closeEvent(self, event):
        """ Triggered when closing about window """
        # Just hide the widget
        event.ignore()
        self.hide()
