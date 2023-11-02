from package import Package
from datetime import datetime

class Truck:
    def __init__(self, id, location="4001 South 700 East"):
        self.id=id
        self.packages = []
        self.location = location
        self.miles_traveled = 0
        self.finish_time = None
        self.num_packages_delivered = 0

    def add_package(self, package):
        self.packages.append(package)
        package.loaded = True