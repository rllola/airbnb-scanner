#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
import os
import configparser

from application import Application

def main():
    """
    main function to launch the program
    """
    print('Create ~/.config/AirbnbScanner/config.ini if it doesn\'t exist')
    config_path = os.path.join(os.path.expanduser('~'), '.config', 'AirbnbScanner')
    config_file = os.path.join(config_path, 'config.ini')
    if not os.path.exists(config_file):
        os.mkdir(config_path)
        with open(config_file, "x") as file:
            file.write('[theme]\nDarkMode = false')

    config = configparser.ConfigParser()
    config.read(config_file)

    print('Starting...')
    app = Application(config, sys.argv)

    print('Executing...')
    sys.exit(app.exec_())

main()
