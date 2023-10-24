import datetime

class Package:
    def __init__(self,package_id,address,deadline,city,zip,weight,status) -> None:
        self.package_id = package_id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip = zip
        self.weight = weight
        self.status = "At the hub." #This is the default status of a package
        self.departure_time = None
        self.delivery_time = None

    def update_status(self,current_time) -> None:
        if self.delivery_time and current_time > self.delivery_time:
            self.status = "Package is delivered"
        elif self.departure_time and self.delivery_time and self.departure_time <= current_time <= self.delivery_time:
            self.status = "On the way"
        else:
            self.status = "At the hub"

    def __str__(self):
        return ("Address: {}\n"
                "Deadline: {}\n"
                "City: {}\n"
                "Zip Code: {}\n"
                "Weight: {}\n"
                "Status: {}\n").format(self.address,self.deadline,self.city,self.zip,self.weight,self.status)

    def update_address(self,new_address):
        self.address = new_address

    def handle_special_instructions(self,current_driver_id,current_time):
        # If the package is delayed
        if "Delayed on flight---will not arrive to depot until 9:05 am" in self.special_notes:
            #Extract the time from the special note
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
                print(f"Package {self.package_id} must be delivered with packages {self.special_notes.split('with ')[1]}")
                break
        
        # If there's a wrong address listed
        if "Wrong address listed" in self.special_notes and self.package_id == 9:
            if current_time.time() < datetime.time(10,20):
                print(f"Package {self.package_id} has a wrong address listed.")
                return False
            else:
                print(f"Package {self.package_id}'s address has been corrected to 410 S. State St., Salt Lake City, UT 84111")
                self.address = "410 S. State St."
        
        return True
