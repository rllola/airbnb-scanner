from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCheckBox

class PreferencesWidget(QWidget):
    """PreferencesWidget class"""

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.dark_mode_button = QCheckBox("Dark mode (will change the icons to light version)")
        layout.addWidget(self.dark_mode_button)
        self.setWindowTitle("Prefrences")
        self.setLayout(layout)

    #pylint: disable=invalid-name
    def closeEvent(self, event):
        """ Triggered when closing about window """
        # Just hide the widget
        event.ignore()
        self.hide()
