#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
import os

# FIXME: Move main.py to src/
# BODY: Move main.py file to source folder.

from application import Application

def main():
    print('Starting...')
    app = Application(sys.argv)

    print('Executing...')
    sys.exit(app.exec_())

main()
