#Student ID: 005954917
#Student Name: Luke Williams

import csv
import datetime
import re

from truck import Truck
from package import Package
from hashtable import HashTable

AVERAGE_SPEED = 18

def preprocess_address(address):
    # Use regular expressions to extract the numeric part of the address (assuming it's a postal code)
    postal_code_match = re.search(r'\b\d{5}\b', address)
    if postal_code_match:
        # If a postal code is found, remove it from the address
        address = address.replace(postal_code_match.group(), '').strip()
    return address

def extract_zip(s):
    matches = re.findall(r'\((\d{5})\)', s)
    if matches:
        return matches[0]
    else:
        return None

def get_distance(current_location, destination, distance_table):
    # Preprocess the addresses to remove extraneous information
    current_location = preprocess_address(current_location)
    destination = preprocess_address(destination)

    # Get the distance from the current location to the destination using the distance_table
    distance = distance_table.get((current_location, destination))
    if distance is None:
        distance = distance_table.get((destination, current_location))
    
    if distance is None:
        print(f"WARNING: Could not find distance for addresses '{current_location}' to '{destination}'")
        return float('inf')
    
    try:
        return float(distance)
    except ValueError:
        print(f"WARNING: Could not convert distance '{distance}' for addresses '{current_location}' to '{destination}' to float. Skipping...")
        return float('inf')

def greedy_delivery_algorithm(package_table, distance_table):
    # Create trucks and assign them drivers
    num_of_trucks = 3
    num_of_drivers = 2
    trucks = [Truck(i) for i in range(num_of_trucks)]
    drivers = [i for i in range(num_of_drivers)]

    # Collect all the packages from the package_table into a list
    packages = []
    for ll in package_table.table:
        current = ll.head
        while current:
            packages.append(current.value)
            current = current.next

    # Sort the packages by their deadline
    packages.sort(key=lambda x: x.deadline)

    # Initialize the current_time as 8:00 am
    current_time = datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0))

    # List to keep track of problematic packages
    problematic_packages = []

    # Define checkpoints for status reporting
    checkpoints = [
        datetime.datetime.combine(datetime.date.today(), datetime.time(8, 35)),
        datetime.datetime.combine(datetime.date.today(), datetime.time(9, 35)),
        datetime.datetime.combine(datetime.date.today(), datetime.time(12, 3)),
    ]

    # Function to print the status at each checkpoint
    def print_checkpoint_status():
        for package in packages:
            print(f"Package {package.package_id}: Status: {package.status} Delivery Time: {package.delivery_time}")

    def deliver_packages(driver_id, truck):
        nonlocal current_time
        while packages:
            current_location = truck.current_location

            # Select the closest package for delivery
            # (For simplicity, you can use the first package in the list)
            # Alternatively, implement a function to find the closest package using the distance_table
            package = packages.pop(0)

            # Check if the package can be delivered based on special conditions
            if not package.handle_special_instructions(driver_id, current_time):
                problematic_packages.append(package)
                continue

            # Calculate distance and update delivery details here
            # For now, as an example:
            distance = get_distance(current_location, package.address, distance_table)
            if distance == float('inf') or AVERAGE_SPEED == 0:
                # Handle this case, perhaps log an error or provide a default value
                print(f"Error: Invalid distance ({distance}) or speed ({AVERAGE_SPEED})")
                return  # or continue or provide a default value
            else:
                delivery_time = current_time + datetime.timedelta(hours=distance / AVERAGE_SPEED)
            package.delivery_time = delivery_time
            package.status = "Delivered"
            current_time = delivery_time
            truck.current_location = package.address

            # Check if any checkpoint is reached
            for checkpoint in checkpoints:
                if current_time >= checkpoint:
                    print(f"Status at {checkpoint.time()}:")
                    print_checkpoint_status()
                    checkpoints.remove(checkpoint)

    # Assign each truck to a driver and start delivering packages
    for driver_id in drivers:
        for truck in trucks:
            deliver_packages(driver_id, truck)

    # Handle problematic packages
    # Ideally, we should handle problematic packages during the first pass itself.
    # But in this simulation, we're treating it separately.
    for driver_id in drivers:
        for truck in trucks:
            deliver_packages(driver_id, truck)

    return trucks


def load_package_data():
    package_table = HashTable(size=50)
    headers = "PackageID,Address,City,State,Zip,DeliveryDeadline,WeightKILO,Special Notes".split(",")

    with open('WGUPSPackageFile.csv', mode='r') as csv_file:
        print("File opened successfully!")

        lines = list(csv_file)
        start_idx = -1
        for idx, line in enumerate(lines):
            if '"PackageID"' in line:  # Using the unique identifier in the header
                start_idx = idx
                break

        # Print the line where we found the header
        print(f"Found header line at index {start_idx}: {lines[start_idx] if start_idx != -1 else 'Not Found'}")

        if start_idx != -1:
            csv_reader = csv.DictReader(lines[start_idx + 1:], fieldnames=headers)

            for row in csv_reader:
                package = Package(
                    int(row['PackageID']),
                    row['Address'],
                    row['City'],
                    row['State'],
                    row['Zip'],
                    row['DeliveryDeadline'],
                    int(row['WeightKILO']),
                    row['Special Notes']
                )
                package_table.set(package.package_id, package)  # assuming HashTable has an insert method

                # For debugging purposes, printing the package details
                print(package)
                inserted_package = package_table.lookup(package.package_id)  # assuming HashTable has a lookup method
                print(inserted_package)
        else:
            print("Header not found in the CSV file.")

    return package_table


def is_float_convertible(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def load_distance_data():
    distance_table = HashTable(size=200)

    with open('WGUPSDistanceTable.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)

        # Skip the header rows (including multi-line headers)
        for _ in range(8):
            next(reader)

        # Read the main header for destinations
        destinations_header = next(reader)
        half_len = len(destinations_header) // 2

        # Splitting the destinations' headers into two halves
        destinations_without_zip = destinations_header[1:half_len + 1]
        destinations_with_zip_distance = destinations_header[half_len + 1:]

        for row in reader:
            origin = row[0]
            for idx, distance in enumerate(row[half_len + 1:]):
                destination = destinations_without_zip[idx]

                if distance.strip() == '':
                    continue  # If the distance is empty, skip the iteration

                if not is_float_convertible(distance):
                    raise ValueError(
                        f"Unexpected data: '{distance}' from {origin} to {destination}. Expected a distance value.")

                distance_float = float(distance)
                key = (origin, destination)
                distance_table.set(key,distance_float)

    return distance_table

def main():
    package_table = load_package_data()
    distance_table = load_distance_data()

    print("Checking problematic addresses...")
    for current_location, destination in distance_table.keys():
        get_distance(current_location, destination, distance_table)
    print("Done checking problematic addresses.")

    greedy_delivery_algorithm(package_table, distance_table)
    trucks = greedy_delivery_algorithm(package_table, distance_table)
    while True:
        print("\nOptions:")
        print("1. Check package status")
        print("2. Check total mileage")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            pkg_id = input("Enter package ID: ")
            package = package_table.get(pkg_id)
            if package:
                print(f"Package {pkg_id}: Status: {package.status} Delivery Time: {package.delivery_time}")
            else:
                print("Package not found.")
        elif choice == '2':
            total_mileage = sum([truck.mileage for truck in trucks])
            print(f"Total Mileage: {total_mileage}")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
