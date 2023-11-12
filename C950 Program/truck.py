class Truck:
    AVERAGE_SPEED = 18
    MAX_CAPACITY = 16
    speed = AVERAGE_SPEED
    total_trucks = 3
    total_drivers = 2

    def __init__(self, driver_id) -> None:
        self.current_packages = []
        self.current_location = "HUB"
        self.mileage = 0
        self.driver_id = driver_id
        self.status = "idle"
        self.special_note = None
        self.departure_time = None

    def __str__(self):
        return ("Capacity: %s, Speed: %s mph, Load: %s, Packages: %d, Mileage: %s miles, Address: %s, Status: %s, Departure Time: %s"
                % (Truck.MAX_CAPACITY, Truck.speed, len(self.current_packages), len(self.current_packages), self.mileage, self.current_location, self.status, self.departure_time))
