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

# Define the main delivery algorithm that assigns and delivers packages using trucks and drivers.
def greedy_delivery_algorithm(package_table):
    # Set up the number of trucks and drivers available for deliveries.
    num_of_trucks = 3
    num_of_drivers = 2
    # Initialize the trucks with unique IDs.
    trucks = [Truck(i) for i in range(num_of_trucks)]
    trucks[0].departure_time = datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0))
    trucks[1].departure_time = datetime.datetime.combine(datetime.date.today(), datetime.time(9, 10))
    trucks[2].departure_time = datetime.datetime.combine(datetime.date.today(), datetime.time(10, 30))
    # Assume drivers are numbered and create a list of them.
    drivers = [i for i in range(num_of_drivers)]

    # Extract packages from the hash table and place them into a list for processing.
    packages = []
    for bucket in package_table.table:
        for PackageKV in bucket:
            packages.append(PackageKV[1])

    # Define the depot location as a constant.
    DEPOT_LOCATION = "HUB"
    # Sort packages first by deadline, then by distance from the depot to prioritize delivery order.
    packages.sort(key=lambda x: (x.deadline, get_distance(DEPOT_LOCATION, x.address)))
    # Set the current time to the start of the delivery day.
    current_time = datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0))
    # Create a list to hold packages that cannot be delivered on the first attempt.
    problematic_packages = []
    # Define a limit to how many packages can be delivered per turn.
    PACKAGE_LIMIT_PER_TURN = 16

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

    # Nested function to handle the delivery of packages for one truck and driver.
    def deliver_packages(driver_id, truck, SkippedInstructionCheck=False):
        nonlocal current_time  # Allows modification of the current_time variable from the outer scope.
        delivered = 0  # Counter for how many packages have been delivered in this turn.

        # Continue delivering packages until there are none left or the turn limit is reached.
        while packages and delivered < PACKAGE_LIMIT_PER_TURN:
            current_location = truck.current_location
            # Get the closest package to the truck's current location.
            package = get_closest_package(current_location)

            # Break the loop if no package is found (all are delivered).
            if not package:
                break
            # If we're not skipping instruction check and there are special instructions that can't be handled, skip the package.
            if not SkippedInstructionCheck:
                if not package.handle_special_instructions(driver_id, current_time):
                    problematic_packages.append(package)
                    continue

            # Calculate distance and delivery time for the current package.
            distance = get_distance(current_location, package.address)
            delivery_time = current_time + datetime.timedelta(hours=distance / AVERAGE_SPEED)

            # Set departure time for the package if the truck is at the depot.
            #if truck.current_location == DEPOT_LOCATION:
                #package.departure_time = current_time

            # If the truck has reached the package limit, it returns to the depot.
            if delivered == PACKAGE_LIMIT_PER_TURN:
                distance_back_to_hub = get_distance(package.address, DEPOT_LOCATION)
                current_time += datetime.timedelta(hours=(distance + distance_back_to_hub) / AVERAGE_SPEED)
                truck.current_location = DEPOT_LOCATION
            # Otherwise, update the package's delivery time and status, and update the truck's location and mileage.
            else:
                package.delivery_time = delivery_time
                package.departure_time = truck.departure_time
                package.status = "Delivered"
                current_time = delivery_time
                truck.current_location = package.address
            truck.mileage += distance
            package.mileage = distance
            delivered += 1

    # Begin the first round of deliveries.
    truck_index = 0
    while packages:
        for driver_id in drivers:
            if truck_index < num_of_trucks:
                truck = trucks[truck_index]
                # If we are using the third truck, update the address for package 9 as per special instruction.
                if truck_index == 2:
                    p9 = package_table.search(9)
                    p9.address = "410 S State St"
                    p9.zip = "84111"
                # Deliver packages using the current truck and driver.
                deliver_packages(driver_id, truck)
                truck_index += 1

    # Re-attempt delivery for packages that had issues on the first attempt.
    packages += problematic_packages
    problematic_packages.clear()

    # Begin the second round of deliveries for any remaining packages,
    # including those that had special instructions or issues on the first attempt.
    truck_index = 0
    while packages:
        for driver_id in drivers:
            if truck_index < num_of_trucks:
                truck = trucks[truck_index]
                # Now deliver packages with SkippedInstructionCheck set to True,
                # indicating that we are attempting to deliver problematic packages
                # which may have had their special instructions resolved.
                deliver_packages(driver_id, truck, True)
                truck_index += 1

    # After all delivery attempts, calculate and print the total mileage covered by all trucks.
    #total_mileage = sum([truck.mileage for truck in trucks])
    #print(f"Total mileage for all trucks: {total_mileage:.2f} miles")
    # Print the mileage for each individual truck.
    # for i, truck in enumerate(trucks):
    #     print(f"Mileage for Truck {i + 1}: {truck.mileage:.2f} miles")

    # Identify and print the status of any packages that have not been successfully delivered.
    undelivered_packages = [pkg for pkg in packages if pkg.status != "Delivered"]
    if not undelivered_packages:
        print("All packages have been delivered!")
    else:
        print(f"{len(undelivered_packages)} packages have not been delivered.")
        for pkg in undelivered_packages:
            print(f"Package {pkg.package_id} at address {pkg.address} is {pkg.status}.")

    # Return the list of trucks, which now contains updated mileage and delivery information.
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

    #print("Get distance: ",get_distance(distance_table[10][0],distance_table[0][0]))


    #greedy_delivery_algorithm(package_table, distance_table)
    greedy_delivery_algorithm(package_table)
    while True:
        print("\nOptions:")
        print("1. Get a single package status with a time")
        print("2. Get all package status with a time")
        print("3. Print all package statuses and total mileage")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            pkg_id = input("Enter package ID: ")
            time_str = input("Enter the time in HH:MM format: ")
            try:
                # Parsing the input time
                time_to_check = dt.datetime.strptime(time_str, '%H:%M').time()

                package = package_table.search(int(pkg_id))
                if package:
                    # Checking if the package is delivered by the input time
                    if time_to_check >= package.delivery_time.time():
                        print(package.time_status("Delivered", package.delivery_time))
                    # Checking if the package has not yet departed
                    elif time_to_check < package.departure_time.time():
                        print(package.time_status("At the hub"))
                    # If the package has departed but not yet delivered
                    else:
                        print(package.time_status("En route"))
                else:
                    print("Package not found.")
            except ValueError:
                print("Invalid time format. Please use HH:MM format.")

        elif choice == '2':
            time_str = input("Enter the time in HH:MM format: ")
            try:
                time_to_check = dt.datetime.strptime(time_str, '%H:%M').time()
                for i in range(1,41):
                    pkg = package_table.search(i)
                    if time_to_check >= pkg.delivery_time.time():
                        print(pkg.time_status("Delivered", pkg.delivery_time))
                    elif time_to_check < pkg.departure_time.time():  # Checking if the package is en route
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
