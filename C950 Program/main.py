#Student ID: 005954917
#Student Name: Luke Williams

import csv
import datetime

from truck import Truck
from package import Package
from hashtable import ChainingHashTable

AVERAGE_SPEED = 18

def getaddressindex(location):
    index = 0
    for row in distance_table:
        if row[0] == location:
            return index
        index += 1
    return -1
def get_distance(current_location, destination):
    current_index = getaddressindex(current_location)
    destination_index = getaddressindex(destination)
    if current_index > destination_index:
        distance = distance_table[current_index][destination_index+1]
    else:
        distance = distance_table[destination_index][current_index+1]
    return float(distance)

    # Function to print the status at each checkpoint


import datetime


def print_checkpoint_status(checkpoint_num=None):
    # Define default checkpoints
    checkpoints = [
        datetime.datetime.combine(datetime.date.today(), datetime.time(8, 35)),
        datetime.datetime.combine(datetime.date.today(), datetime.time(9, 35)),
        datetime.datetime.combine(datetime.date.today(), datetime.time(12, 3)),
    ]

    # If checkpoint_num is not provided or is invalid, print an error message
    if checkpoint_num is None or checkpoint_num < 1 or checkpoint_num > len(checkpoints):
        print("Invalid checkpoint number.")
        return

    # Get the desired checkpoint time
    checkpoint_time = checkpoints[checkpoint_num - 1]

    # Collect all the packages from the package_table into a list
    packages = []
    for bucket in package_table.table:
        for PackageKV in bucket:
            packages.append(PackageKV[1])

    # Print the status of the packages at the specified checkpoint
    print(f"Status of packages at {checkpoint_time.time()}:")
    for package in packages:
        print(f"Package {package.package_id}: Status: {package.status} Delivery Time: {package.delivery_time}")


def greedy_delivery_algorithm(package_table, distance_table):
    # Create trucks and assign them drivers
    num_of_trucks = 3
    num_of_drivers = 2
    trucks = [Truck(i) for i in range(num_of_trucks)]
    drivers = [i for i in range(num_of_drivers)]

    # Collect all the packages from the package_table into a list
    packages = []
    #while len(package_table) > 0:
    for bucket in package_table.table:
        for PackageKV in bucket:
            packages.append(PackageKV[1])
        #package_table.remove(PackageID)

    # Sort the packages by their deadline
    packages.sort(key=lambda x: x.deadline)

    # Initialize the current_time as 8:00 am
    current_time = datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0))

    # List to keep track of problematic packages
    problematic_packages = []

    def deliver_packages(driver_id, truck):
        nonlocal current_time
        while packages:
            current_location = truck.current_location

            # Select the closest package for delivery
            package = packages.pop(0)

            # Check if the package can be delivered based on special conditions
            if not package.handle_special_instructions(driver_id, current_time):
                problematic_packages.append(package)
                continue

            # Calculate distance and update delivery details
            distance = get_distance(current_location,destination=package.address)
            if distance == float('inf') or AVERAGE_SPEED == 0:
                print(f"Error: Invalid distance ({distance}) or speed ({AVERAGE_SPEED})")
                return
            else:
                delivery_time = current_time + datetime.timedelta(hours=distance / AVERAGE_SPEED)
            package.delivery_time = delivery_time
            package.status = "Delivered"
            current_time = delivery_time
            truck.current_location = package.address
            truck.mileage += distance
            package.mileage = distance
            print(current_location,',',package.address,',',package)
    # Assign each driver a specific truck and start delivering packages
    for i in range(num_of_drivers):
        truck = trucks[i]
        driver_id = drivers[i]
        deliver_packages(driver_id, truck)

    # Handle problematic packages
    for driver_id in drivers:
        for truck in trucks:
            deliver_packages(driver_id, truck)

    return trucks


package_table = ChainingHashTable()
def load_package_data():
    headers = "PackageID,Address,City,State,Zip,DeliveryDeadline,WeightKILO,Special Notes".split(",")

    with open('WGUPSPackageFile.csv', mode='r') as csv_file:
        #print("File opened successfully!")

        lines = list(csv_file)
        start_idx = -1
        for idx, line in enumerate(lines):
            if '"PackageID"' in line:  # Using the unique identifier in the header
                start_idx = idx
                break

        # Print the line where we found the header
        #print(f"Found header line at index {start_idx}: {lines[start_idx] if start_idx != -1 else 'Not Found'}")

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
                package_table.insert(package.package_id, package)  # assuming HashTable has an insert method

                # For debugging purposes, printing the package details
                inserted_package = package_table.search(package.package_id)  # assuming HashTable has a lookup method
                #print(inserted_package)
        else:
            print("Header not found in the CSV file.")

    return package_table


def is_float_convertible(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

distance_table = []
def load_distance_data():
    with open('WGUPSDistanceTable.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            distance_table.append(row)

package_table = load_package_data()
load_distance_data()
def main():

    #print("Get distance: ",get_distance(distance_table[10][0],distance_table[0][0]))


    #greedy_delivery_algorithm(package_table, distance_table)
    trucks = greedy_delivery_algorithm(package_table, distance_table)
    while True:
        print("Total mileage: ",trucks[0].mileage+trucks[1].mileage+trucks[2].mileage )
        print("\nOptions:")
        print("1. Check package status")
        print("2. Check package checkpoints")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            pkg_id = input("Enter package ID: ")
            package = package_table.search(int(pkg_id))
            if package:
                print(package)
            else:
                print("Package not found.")
        elif choice == '2':
            print("\nOptions:")
            print("1. Checkpoint at 8:35 AM")
            print("2. Checkpoint at 9:35 AM")
            print("3. Checkpoint at 12:03 PM")

            checkpoint_choice = input("Choose a checkpoint: ")

            if checkpoint_choice == '1':
                print_checkpoint_status(1)
            elif checkpoint_choice == '2':
                print_checkpoint_status(2)
            elif checkpoint_choice == '3':
                print_checkpoint_status(3)
            else:
                print("Invalid option")

        elif choice == '3':
                break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
