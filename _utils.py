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
            print("Installing missing packages...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing_packages])
