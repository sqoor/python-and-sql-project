import sys
import subprocess
import pkg_resources

""" Documentation
    Description:
        InstallPackages class by making an instance of this call it will install all the packages passed 
        to the constructor using pip on the OS.

    Constructor Parameters:
      packages_to_install (array of string): list of packages you want to install to run this script

"""


class InstallPackages:
    def __init__(self, packages_to_install):
        required_packages = {'pyodbc', 'pandas', 'argparse'}
        installed_packages = {package.key for package in pkg_resources.working_set}
        missing_packages = required_packages - installed_packages

        if missing_packages:
            # implement pip as a subprocess:
            Verbose.print_ln("Installing missing packages...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing_packages])


class Verbose:
    _show_messages = False

    @staticmethod
    def print_ln(message, name=''):
        if not Verbose._show_messages:
            return

        if name:
            print(name)
        print(message)

    @staticmethod
    def show_messages(status=None):
        if status:
            Verbose._show_messages = True
        else:
            Verbose._show_messages = False
