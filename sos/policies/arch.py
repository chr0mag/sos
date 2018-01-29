import os
from sos.policies import PackageManager, LinuxPolicy
from sos.plugins import Plugin
from sos.utilities import shell_out


class ArchPolicy(LinuxPolicy):

    distro = "Arch Linux"
    vendor = "Arch Linux"
    vendor_url = "https://www.archlinux.org/"
    vendor_text = ""
    # package_manager = PackageManager(
    #   "pacman --query | awk 'BEGIN {OFS = \"|\"} {print $1,$2}'")
    valid_subclasses = [Plugin]

    def __init__(self, sysroot=None):
        super(LinuxPolicy, self).__init__(sysroot=sysroot)
        self.package_manager = Pacman()

    @classmethod
    def check(cls):
        """This method checks to see if we are running on Arch.
            It returns True or False."""
        try:
            with open('/etc/os-release', 'r') as f:
                return "archlinux" in f.read()
        except:
            return False


class Pacman(PackageManager):
    # this subclass is only needed because sos_get_command_output()
    # in utilities.py sets shell=False so the pipe to awk in the
    # command below used to format pacman output does not work
    # pacman --query | awk 'BEGIN {OFS = \"|\"} {print $1,$2}'

    def get_pkg_list(self):
        cmd = "pacman --query"
        pkg_list = shell_out(
            cmd, timeout=0, chroot=self.chroot
        ).splitlines()

        for pkg in pkg_list:
            name, version = pkg.split()
            self.packages[name] = {
                'name': name,
                'version': version.split(".")
            }

        return self.packages

# vim: set et ts=4 sw=4 :