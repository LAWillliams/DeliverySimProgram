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
