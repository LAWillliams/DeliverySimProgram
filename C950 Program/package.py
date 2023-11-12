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
    def __str__(self):
        return f'{self.package_id},{self.address},{self.city},{self.state},{self.zip},{self.deadline},{self.weight},{self.mileage},{self.status},{self.departure_time},{self.delivery_time}'

    def time_status(self,current_status,del_time=""):
        return f'{self.package_id},{self.address},{self.city},{self.state},{self.zip},{self.deadline},{self.weight},{self.mileage},{current_status},{self.departure_time},{del_time}'

    def handle_special_instructions(self, current_driver_id, current_time):
        # If the package is delayed
        if "Delayed on flight---will not arrive to depot until 9:05 am" in self.special_notes:
            # Extract the time from the special note
            delay_time_str = self.special_notes.split('until ')[1]
            delay_time = datetime.datetime.strptime(delay_time_str, '%I:%M %p').time()

            # If the current time is before the delay time, the package won't be ready for delivery
            if current_time.time() < delay_time:
                print(f"Package {self.package_id} is delayed and will not be available until after {delay_time_str}")
                return False

        # If the package can only be on a specific truck
        if "Can only be on truck 2" in self.special_notes and current_driver_id != 2:
            print(f"Package {self.package_id} can only be on {self.special_notes}")
            return False

        # If the package must be delivered with other packages
        delivery_conditions = ["Must be delivered with 15, 19",
                               "Must be delivered with 13, 19",
                               "Must be delivered with 13, 15"]
        for condition in delivery_conditions:
            if condition in self.special_notes:
                print(
                    f"Package {self.package_id} must be delivered with packages {self.special_notes.split('with ')[1]}")
                break

        # If there's a wrong address listed
        if "Wrong address listed" in self.special_notes and self.package_id == 9:
            if current_time.time() < datetime.time(10, 20):
                print(f"Package {self.package_id} has a wrong address listed.")
                return False
            else:
                print(
                    f"Package {self.package_id}'s address has been corrected to 410 S. State St., Salt Lake City, UT 84111")
                self.address = "410 S State St"

        return True