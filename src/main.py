#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys

from application import Application

def main():
    """
    main function to launch the program
    """
    print('Starting...')
    app = Application(sys.argv)

    print('Executing...')
    sys.exit(app.exec_())

main()
