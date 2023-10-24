#Student ID: 005954917
#Student Name: Luke Williams

import csv
import datetime

from truck import Truck
from package import Package
from hashtable import HashTable

AVERAGE_SPEED = 18

def greedy_delivery_algorithm(package_table, distance_table):
    trucks = [Truck(i) for i in range(3)]
    drivers = [i for i in range(2)]

    # Convert hash table values to a list of packages
    packages = [package for package in package_table.values()]

    # Sort the packages by their deadline
    packages.sort(key=lambda x: x.deadline)

    # Initialize the current_time as 8:00 am
    current_time = datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0))

    # Creating a list for packages that can't be delivered yet due to special instructions
    problematic_packages = []

    def deliver_packages(truck, pkg_list):
        nonlocal current_time
        while pkg_list:
            current_location = truck.current_location

            # If truck is empty, return to depot to load up to 16 packages
            if not truck.current_packages:
                distance_to_hub = get_distance(truck.current_location, 'HUB', distance_table)
                time_to_hub = datetime.timedelta(hours=distance_to_hub / AVERAGE_SPEED)
                current_time += time_to_hub
                truck.mileage += distance_to_hub
                truck.current_location = 'HUB'
                continue

            # Find the nearest package based on the distance from the current location
            nearest_package = min(pkg_list, key=lambda p: get_distance(current_location, p.address, distance_table))

            # Check special instructions; if the package doesn't meet criteria, remove it and continue
            if not nearest_package.handle_special_instructions(current_time):
                if pkg_list == problematic_packages:
                    # Handle packages that still can't be delivered here
                    # For now, we will just remove them from the problematic_packages list
                    pkg_list.remove(nearest_package)
                    continue
                problematic_packages.append(nearest_package)
                pkg_list.remove(nearest_package)
                continue

            # Load the package onto the truck
            truck.current_packages.append(nearest_package)

            # Update the truck's mileage based on the distance to the nearest package
            truck.mileage += get_distance(current_location, nearest_package.address, distance_table)

            # "Deliver" the package by setting the truck's current location to the package's address
            truck.current_location = nearest_package.address

            # Remove the delivered package from the list
            pkg_list.remove(nearest_package)

            # Update the current time based on the distance traveled
            distance_to_package = get_distance(current_location, nearest_package.address, distance_table)
            time_to_package = datetime.timedelta(hours=distance_to_package / AVERAGE_SPEED)
            current_time += time_to_package

            # If the truck is empty or full, return to depot
            if not truck.current_packages or len(truck.current_packages) == Truck.MAX_CAPACITY:
                distance_to_hub = get_distance(truck.current_location, 'HUB', distance_table)
                time_to_hub = datetime.timedelta(hours=distance_to_hub / AVERAGE_SPEED)
                current_time += time_to_hub
                truck.mileage += distance_to_hub
                truck.current_location = 'HUB'
    for driver_id in drivers:
        for truck in trucks:
            # Delivering the initial package list
            deliver_packages(driver_id, truck, packages)
            
            # Retry delivery for problematic packages
            deliver_packages(driver_id, truck, problematic_packages)

    return trucks




def get_distance(current_location, destination, distance_table):
    # Get the distance from the current location to the destination using the distance_table
    distance = distance_table.get((current_location, destination))
    if distance is None:
        distance = distance_table.get((destination, current_location))
    return float(distance) if distance else float('inf')


def load_data():
    package_table = HashTable(size=50)
    with open('C:\\Users\\lukea\\OneDrive\\Desktop\\WGU\\C950\\WGUPS Package File.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            p = Package(row['package_id'], row['Address'], row['deadline'], row['city'], row['zip'], row['weight'], row['status'], row.get('special_instructions', None))
            package_table.insert(p.package_id, p)

    distance_table = HashTable(size=200)
    with open('C:\\Users\\lukea\\OneDrive\\Desktop\\WGU\\C950\\WGUPS Distance Table.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            key = (row['from'], row['to'])
            distance_table.insert(key,row['distance'])
    
    return package_table,distance_table

def main():
    package_table, distance_table = load_data()

    greedy_delivery_algorithm(package_table, distance_table)

if __name__ == "__main__":
    main()
