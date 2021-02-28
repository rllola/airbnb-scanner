import sys
import os
import platform
import configparser
from PyQt5.QtCore import QDir

from application import Application

def main():
    """
    main function to launch the program
    """
    # use os.getenv('APPDATA') for windows
    
    # By default path if Linux user path
    config_path = os.path.join(os.path.expanduser('~'), '.config', 'AirbnbScanner')
    if platform.system() == "Windows":
        config_path = os.path.join(os.getenv('APPDATA'), 'AirbnbScanner')

    config_file = os.path.join(config_path, 'config.ini')
    print('Create {} if it doesn\'t exist'.format(config_file))
    if not os.path.exists(config_file):
        os.makedirs(config_path, exist_ok=True)
        with open(config_file, "x") as file:
            file.write('[theme]\nDarkMode = false')

    config = configparser.ConfigParser()
    config.read(config_file)

    print('Starting...')
    print(sys.argv)
    app = Application(config, config_file, sys.argv)

    print('Executing...')
    sys.exit(app.exec_())


if __name__ == '__main__':    
    main()
