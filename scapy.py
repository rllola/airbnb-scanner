from pyqtdeploy import Component, PythonPackage

class scapyComponent(Component):
    """ The scapy component. """

    def get_archive_name(self):
        """ Return the filename of the source archive. """

        return 'scapy-{}.tar.gz'.format(self.version)

    def get_archive_urls(self):
        """ Return the list of URLs where the source archive might be
        downloaded from.
        """

        return self.get_pypi_urls('scapy')

    def verify(self):
        """ Verify the component. """

        # Make sure any installed version is the one specified.
        if not self.install_from_source:
            self._verify_installed_version()

    def install(self):
        """ Install for the target. """

        if not self.install_from_source:
            self.error("need install from source")
            return

        else:

            self.unpack_archive(self.get_archive())
            self.copy_dir('.', os.path.join(self.target_include_dir))

    def _verify_installed_version(self):

        from scapy import VERSION
        if str(self.version) > VERSION:

            self.error("Incomplatible version %s < %s" %
                       (VERSION, self.version))

    @property
    def provides(self):
        """ The dict of parts provided by the component. """

        parts = {
            'scapy': PythonPackage(
                deps=('Python:ctypes', 'Python:ctypes.util'),
            ),
        }

        return parts