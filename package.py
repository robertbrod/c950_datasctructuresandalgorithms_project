from datetime import datetime

class Package:
    def __init__(self, id, address, city, state, zip, deadline, mass):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.mass = mass
        self.loaded = False
        self.status = "AT HUB"
        self.delivery_time = None