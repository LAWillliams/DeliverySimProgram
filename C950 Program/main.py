#Student ID: 005954917
#Student Name: Luke Williams

import csv
import datetime
import datetime as dt
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

    # Nested function to find the closest package to the current truck location.
def get_closest_package(location):
    min_distance = float('inf')
    closest_package = None
    index = -1
    for i, package in enumerate(packages):
        distance = get_distance(location, package.address)
        if distance < min_distance:
            min_distance = distance
            closest_package = package
            index = i
    # Remove the closest package from the list once identified.
    if index != -1:
        packages.pop(index)
    return closest_package

# Set up the number of trucks and drivers available for deliveries.
num_of_trucks = 3
num_of_drivers = 2
trucks = [Truck(i) for i in range(num_of_trucks)]
trucks[0].truck_id = 1
trucks[1].truck_id = 2
trucks[2].truck_id = 3
truck_one = trucks[0]
truck_two = trucks[1]
truck_three = trucks[2]
truck_one.current_packages = [1,2,4,5,7,8,10,11,12,13,14,15,16,17,19,20]
truck_two.current_packages = [3,6,18,21,22,23,24,25,26,27,28,29,30,32,36,38]
truck_three.current_packages = [9,31,33,34,35,37,39,40]
truck_one.departure_time = datetime.timedelta(hours=8,minutes=0)
truck_two.departure_time = datetime.timedelta(hours=9,minutes=10)
truck_three.departure_time = datetime.timedelta(hours=10, minutes=20)

# This function defines the algorithmic logic for the greedy algorithm to deliver packages
def deliver_packages(truck):
    current_time = truck.departure_time
    current_location = truck.current_location
    not_delivered = []

    # Load packages into not_delivered list
    for package_id in truck.current_packages:
        package = package_table.search(package_id)
        not_delivered.append(package)

    # Clear the truck's current packages since they are now in the not_delivered list
    truck.current_packages.clear()

    # Deliver packages
    while len(not_delivered) > 0:
        closest_package = None
        min_distance = float('inf')

        # Find the closest package
        for package in not_delivered:
            distance = get_distance(current_location, package.address)
            package.mileage = distance

            if distance < min_distance:
                min_distance = distance
                closest_package = package

        if closest_package is not None:

            # Simulate delivery
            current_location = closest_package.address
            not_delivered.remove(closest_package)

            truck.mileage += distance

            # Calculate the time to deliver
            travel_time = datetime.timedelta(hours=min_distance / AVERAGE_SPEED)
            current_time += travel_time  # Update current_time with travel time only
            if closest_package.package_id == 9:
                if current_time < datetime.timedelta(hours=10, minutes=20):
                    closest_package.address = "Waiting for update"
                    closest_package.zip = "Waiting for update"
                else:
                    closest_package.address = "410 S State St"
                    closest_package.zip = "84111"
            closest_package.departure_time = truck.departure_time
            closest_package.delivery_time = current_time
            closest_package.status = "Delivered"
            closest_package.truck_id = truck.truck_id

    # Update truck's final location and time
    truck.current_location = current_location
    truck.return_time = current_time
    return truck



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
# Convert the hashtable of packages into a list for easier access
packages = [PackageKV[1] for bucket in package_table.table for PackageKV in bucket]



def main():

    deliver_packages(truck_one)
    deliver_packages(truck_two)
    deliver_packages(truck_three)

    while True:
        print("\nOptions:")
        print("1. Get a single package status with a time")
        print("2. Get all package status with a time")
        print("3. Print all package statuses and total mileage")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            pkg_id = input("Enter package ID: ")
            h,m = input("Enter the time in HH:MM format: ").split(':')
            try:
                # Parsing the input time
                time_to_check = datetime.timedelta(hours=int(h),minutes=int(m))

                package = package_table.search(int(pkg_id))

                if time_to_check < datetime.timedelta(hours=10,minutes=20):
                    p9 = package_table.search(9)
                    p9.address = "Wrong address listed waiting on update"
                    p9.zip = "Wrong zip listed waiting on update"
                if time_to_check >= datetime.timedelta(hours=10, minutes=20):
                    p9.address = "410 S State St"
                    p9.zip = "84111"

                if package:
                    # Checking if the package is delivered by the input time
                    if time_to_check >= package.delivery_time:
                        print(package.time_status("Delivered", package.delivery_time))
                    # Checking if the package has not yet departed
                    elif time_to_check < package.departure_time:
                        print(package.time_status("At the hub"))
                    # If the package has departed but not yet delivered
                    else:
                        print(package.time_status("En route"))
                else:
                    print("Package not found.")
            except ValueError:
                print("Invalid time format. Please use HH:MM format.")

        elif choice == '2':
            h,m = input("Enter the time in HH:MM format: ").split(':')
            try:
                time_to_check = datetime.timedelta(hours=int(h),minutes=int(m))
                for i in range(1,41):
                    pkg = package_table.search(i)

                    if time_to_check < datetime.timedelta(hours=10, minutes=20):
                        p9 = package_table.search(9)
                        p9.address = "Wrong address listed waiting on update"
                        p9.zip = "Wrong zip listed waiting on update"
                    if time_to_check >= datetime.timedelta(hours=10, minutes=20):
                        p9.address = "410 S State St"
                        p9.zip = "84111"

                    if time_to_check >= pkg.delivery_time:
                        print(pkg.time_status("Delivered", pkg.delivery_time))
                    elif time_to_check < pkg.departure_time:  # Checking if the package is en route
                        print(pkg.time_status("At the hub"))
                    else:
                        print(pkg.time_status("En route"))
            except ValueError:
                print("Invalid time format. Please use HH:MM format.")

        elif choice == '3':
            total_mileage = 0
            for i in range(1,41):
                pkg = package_table.search(i)
                print(f"Package ID {i}: {pkg.status} ")
                total_mileage += pkg.mileage
            print(f"Total mileage is  {total_mileage.__round__()}")
        elif choice == '4':
                break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
