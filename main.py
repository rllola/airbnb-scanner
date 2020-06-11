#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
import os

from src.application import Application

def main():
    print('Starting...')
    app = Application(sys.argv)

    print('Executing...')
    sys.exit(app.exec_())

main()
