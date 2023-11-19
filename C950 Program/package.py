import datetime
class Package:
    def __init__(self, package_id, address, city, state, zip, deadline, weight, special_notes=None):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.special_notes = special_notes
        self.status = "At the hub."  # Default status
        self.departure_time = None
        self.delivery_time = None
        self.mileage = 0
        self.truck_id = None
    def __str__(self):
        return f'{self.package_id},{self.address},{self.city},{self.state},{self.zip},{self.deadline},{self.weight},{self.mileage},{self.status},{self.departure_time},{self.delivery_time},Truck: {self.truck_id}'

    def time_status(self,current_status,del_time=""):
        return f'{self.package_id},{self.address},{self.city},{self.state},{self.zip},{self.deadline},{self.weight},{self.mileage},{current_status},{self.departure_time},{del_time},Truck: {self.truck_id}'