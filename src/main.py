#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
import os

print(sys.path)

from PyQt5.QtCore import QLibraryInfo

print("PrefixPath : " + QLibraryInfo.location(QLibraryInfo.PrefixPath))
print("DocumentationPath : " + QLibraryInfo.location(QLibraryInfo.DocumentationPath))
print("HeadersPath : " + QLibraryInfo.location(QLibraryInfo.HeadersPath))
print("LibrariesPath : " + QLibraryInfo.location(QLibraryInfo.LibrariesPath))
print("LibraryExecutablesPath : " + QLibraryInfo.location(QLibraryInfo.LibraryExecutablesPath))
print("BinariesPath : " + QLibraryInfo.location(QLibraryInfo.BinariesPath))
print("PluginsPath : " + QLibraryInfo.location(QLibraryInfo.PluginsPath))
print("ImportsPath : " + QLibraryInfo.location(QLibraryInfo.ImportsPath))
print("Qml2ImportsPath : " + QLibraryInfo.location(QLibraryInfo.Qml2ImportsPath))
print("ArchDataPath : " + QLibraryInfo.location(QLibraryInfo.ArchDataPath))
print("DataPath : " + QLibraryInfo.location(QLibraryInfo.DataPath))
print("TranslationsPath : " + QLibraryInfo.location(QLibraryInfo.TranslationsPath))
print("ExamplesPath : " + QLibraryInfo.location(QLibraryInfo.ExamplesPath))
print("TestsPath : " + QLibraryInfo.location(QLibraryInfo.TestsPath))
print("SettingsPath : " + QLibraryInfo.location(QLibraryInfo.SettingsPath))

from application import Application


def main():
    print('Starting...')
    app = Application(sys.argv)

    print('Executing...')
    sys.exit(app.exec_())

main()
