#Name: Robert Brod
#Student ID: 001939918

from hash import HashTable
from package import Package
from truck import Truck
from datetime import datetime, timedelta

#Function to extract package data from .csv file.
def load_package_data(hash_table):
    packages = []
    raw_data = []

    with open("Package CSV.txt", "r") as data:
        raw_data = data.readlines()

    #Populating new package object with relevant data from .csv
    for data in raw_data:
        data = data.split(",")
        id = int(data[0])
        address = data[1]
        city = data[2]
        state = data[3]
        zip = int(data[4])
        deadline = None
        if data[5] == "EOD":
            deadline = "EOD"
        else:
            raw_deadline_time = (data[5].replace(" AM", "")).split(":")
            deadline = datetime(2022, 12, 2, int(raw_deadline_time[0]), int(raw_deadline_time[1]))
        mass = int(data[6].replace("\n", ""))

        p = Package(id, address, city, state, zip, deadline, mass)
        packages.append(p)

    #Inserting all packages into hash table
    for package in packages:
        hash_table.insert(package)

#Function to extract distance data from .csv file.
def load_distance_data(distance_data):
    raw_data = []

    with open("Distance CSV.txt", "r") as data:
        raw_data = data.readlines()

    for index, row in enumerate(raw_data):
        distance_data.append([])
        for cell in row.split(","):
            if cell == "\n":
                pass
            elif cell != "":
                distance_data[index].append(float(cell))
            else: 
                distance_data[index].append(None)

    #Populating symmetrical side of matrix
    for index, row in enumerate(distance_data):
        for secondary_index, cell in enumerate(row):
            if cell == None:
                distance_data[index][secondary_index] = distance_data[secondary_index][index]
        
#Function to extract address data from .csv file.
def load_address_data(address_data):
    raw_data = []

    with open("Address CSV.txt", "r") as data:
        raw_data = data.readlines()

    for data in raw_data:
        address_data.append(data.replace("\n", ""))

#Function to calculate the distance between two addresses
#Takes two address attributes and returns float from 'distance_data' array
#Checks are made to ensure that addresses are valid
def distance_between(address1, address2):
    if address1 in address_data:
        address1_index = address_data.index(address1)
    else:
        return None
    
    if address2 in address_data:
       address2_index = address_data.index(address2)
    else:
        return None

    return distance_data[address1_index][address2_index]

#Helper function for load_packages_with_matching_addresses()
#Takes package object and returns array of packages with the same address that are not delayed and are not already on a truck
def packages_with_same_address(package):
    same_address = []

    address = package.address

    for i in range(1,41):
        package = hash_table.search(i)
        if package.loaded == False and package.id not in delayed:
            same_address.append(package)

    return same_address

#Function to ensure that packages that have the same address are loaded together
def load_packages_with_matching_addresses(truck):
    packages = []
    while len(truck.packages) < package_limit:
        for package in truck.packages:
            packages = packages_with_same_address(package)
            for same_address_package in packages:
                if len(truck.packages) < package_limit:
                    truck.add_package(same_address_package)

#Helper function to truck_load_packages
#Function to load packages after high priority and matching-address packages are loaded
def load_remaining_packages(truck):
    for i in range(1,41):
        package = hash_table.search(i)
        if package.loaded == False and package.id not in delayed:
            truck.add_package(package)

#Helper function to truck_load_packages
#Seperate function for packages that were either delayed or had error in address until certain time of day
def load_delayed_packages(truck):
    wrong_address_package = hash_table.search(9)
    wrong_address_package.address = "410 S State St"
    wrong_address_package.zip = 84111

    for package in delayed:
        if package != 6 and package != 25:
            truck_three.add_package(hash_table.search(package))            

#Main function to load all packages onto the three trucks
def truck_load_packages():
    #Packages that must be delivered together
    truck_one.add_package(hash_table.search(13))
    truck_one.add_package(hash_table.search(14))
    truck_one.add_package(hash_table.search(15))
    truck_one.add_package(hash_table.search(16))
    truck_one.add_package(hash_table.search(19))
    truck_one.add_package(hash_table.search(20))

    #Packages with deadlines
    truck_one.add_package(hash_table.search(37))
    truck_one.add_package(hash_table.search(40))
    
    #Packages that must be on truck two
    truck_two.add_package(hash_table.search(3))
    truck_two.add_package(hash_table.search(18))
    truck_two.add_package(hash_table.search(36))
    truck_two.add_package(hash_table.search(38))

    #Packages with deadlines
    truck_two.add_package(hash_table.search(34))

    load_packages_with_matching_addresses(truck_one)
    load_packages_with_matching_addresses(truck_two)
    load_remaining_packages(truck_three)

#Function to locate the earliest deadline
#Takes in truck object and returns an address attribute or None if all remaining packages are due "EOD"
def find_earliest_deadline(truck):
    #Starting package to compare other deadlines with
    init_package = None
    for package in truck.packages:
        if package.deadline != "EOD":
            init_package = package

    #Check to see if there is a package with an earlier deadline
    package_to_be_returned = None
    if init_package != None:
        earliest_deadline = init_package.deadline
        for package in truck.packages:
            if package.deadline != "EOD":
                if package.deadline < earliest_deadline:
                    package_to_be_returned = package

        if package_to_be_returned == None:
            return init_package.address
        else:
            return package_to_be_returned.address
    
    #If all remaining packages on truck are due "EOD" return None
    else:
        return None

#Function to find closest address to current truck location for all loaded packages
#Takes in truck object and returns address attribute
def find_closest_address(truck):
    #Initializing distance to large number
    smallest_distance = 99999
    closest_address = None

    for package in truck.packages:
        if distance_between(truck.location, package.address) < smallest_distance:
            smallest_distance = distance_between(truck.location, package.address)
            closest_address = package.address

    return closest_address

#Function to deliver individual packages
#Takes in truck object, package object, and timedelta object
#Returns timedelta object
def deliver_package(truck, package, current_time):
    delivery_address = package.address
    distance_to_address = distance_between(truck.location, delivery_address)

    #Calculating time to arrive at next destination
    time_to_deliver = distance_to_address / truck_speed
    time_to_deliver_s = round(((time_to_deliver * 60) % 1) * 60)
    time_to_deliver_m = int((time_to_deliver * 60))

    #Update truck location to delivery location
    truck.location = delivery_address 

    #Update time elapsed
    delta = timedelta(0, time_to_deliver_s, 0, 0, time_to_deliver_m)
    current_time += delta
    if package.id not in [5,13,34]:

    #Update total miles traveled by truck
        truck.miles_traveled += distance_to_address

    #Updating package status after delivery
    package.status = "DELIVERED"
    package.delivery_time = current_time

    #Removing delivered package from truck manifest
    package_index = truck.packages.index(package)
    truck.packages.pop(package_index)

    return current_time

#Function to mark trucks back at the hub, primarily used for gathering start time for third truck
def return_to_hub(truck, time):
    distance = distance_between(truck.location, "4001 South 700 East")
    
    #Calculating time to arrive at Hub
    time_to_return = distance / truck_speed
    time_to_return_s = round(((time_to_return * 60) % 1) * 60)
    time_to_return_m = int((time_to_return * 60))

    #Update time elapsed
    delta = timedelta(0, time_to_return_s, 0, 0, time_to_return_m)
    time += delta

    #Marking truck back at hub and recording finish time for day
    truck.location = "4001 South 700 East"
    truck.finish_time = time

#Function to handle troublesome packages that are delayed until 9:05 but have deadlines at 10:30
#Return to hub in the middle of route to load these packages
def return_to_load_delayed_packages_with_deadline(truck, time):
    current_time = time
    distance = distance_between(truck.location, "4001 South 700 East")

    #Calculating time to arrive at Hub
    time_to_return = distance / truck_speed
    time_to_return_s = round(((time_to_return * 60) % 1) * 60)
    time_to_return_m = int((time_to_return * 60))

    #Update time elapsed
    delta = timedelta(0, time_to_return_s, 0, 0, time_to_return_m)
    current_time += delta

    truck_two.add_package(hash_table.search(6))
    truck_two.add_package(hash_table.search(25))

    return current_time

#Primary and named delivery algorithm
#Packages are prioritized by earliest deadlines, then by proximity
#Any and all packages for the same addresses are delivered at the same time if loaded on the same truck
def priority_delivery_algorithm(truck, time):
    current_time = time

    #Marking all package status as "EN ROUTE"
    for package in truck.packages:
        package.status = "EN ROUTE"

    #Repeat until truck has no more packages
    while len(truck.packages) != 0:

        #Handling troublesome packages that are delayed until 9:05 but have deadlines at 10:30
        #Return to hub to load them
        if truck.id == 2 and truck.num_packages_delivered == 3:
            current_time = return_to_load_delayed_packages_with_deadline(truck, current_time)

        next_address = find_earliest_deadline(truck)

        #Trucks will first deliver to addresses that have package(s) with the earliest deadline
        if next_address != None:
            packages_at_address = []
            for package in truck.packages:
                if package.address == next_address:
                    packages_at_address.append(package)

            for package in packages_at_address:
                current_time = deliver_package(truck, package, current_time)
                truck.num_packages_delivered += 1
        #If no package has a deadline other than "EOD" trucks instead deliver by proximity to current location
        else:
            next_address = find_closest_address(truck)
            packages_at_address = []
            for package in truck.packages:
                if package.address == next_address:
                    packages_at_address.append(package)

            for package in packages_at_address:
                current_time = deliver_package(truck, package, current_time)
                truck.num_packages_delivered += 1

    return_to_hub(truck, current_time)

#Function to print packages' status when called via console
def print_package_status(input_time, package_list):
    #Process input string into datetime object
    t = input_time.split(":")
    timestamp = datetime(2022, 12, 2, int(t[0]), int(t[1]), int(t[2]))
    start_of_day = datetime(2022, 12, 2, 8)

    for i in range(1, 41):
        package = hash_table.search(i)
        print("ID: %d" % package.id, end=", ")
        print("DA: %s" % package.address, end=", ")
        print("DUE: ", end="")

        if package.deadline == "EOD":
                print("EOD", end=", ")
        else:
            print(package.deadline.time(), end =", ")

        print("STATE: %s" % package.state, end =", ")
        print("ZIP: %d" % package.zip, end =", ")
        print("KILO: %d" % package.mass, end =", ")
        print("STATUS: ", end ="")

        if package.id != 6 and package.id != 25:
            #If work day has not begun
            if timestamp < start_of_day:
                print("AT HUB")
            #If third truck has not left hub
            elif timestamp < earliest_time and package in package_list:
                print("AT HUB")
            else:
                if package.delivery_time < timestamp:
                    print("DELIVERED @ ", end="")
                    print(package.delivery_time.time())
                else:
                    print("EN ROUTE")
        else:
            if timestamp < datetime(2022, 12, 2, 9, 5):

                print("AT HUB")
            elif timestamp < package.delivery_time:
                print("EN ROUTE")
            elif package.delivery_time < timestamp:
                print("DELIVERED @ ", end="")
                print(package.delivery_time.time())

    print()

#Function to print single package status when called via console
#Same as print_package_status outside of loop
def print_single_package_status(package_id, input_time, package_list):
    #Process input string into datetime object
    t = input_time.split(":")
    timestamp = datetime(2022, 12, 2, int(t[0]), int(t[1]), int(t[2]))
    start_of_day = datetime(2022, 12, 2, 8)

    package = hash_table.search(package_id)
    print("ID: %d" % package.id, end=", ")
    print("DA: %s" % package.address, end=", ")
    print("DUE: ", end="")

    if package.deadline == "EOD":
            print("EOD", end=", ")
    else:
        print(package.deadline.time(), end =", ")

    print("STATE: %s" % package.state, end =", ")
    print("ZIP: %d" % package.zip, end =", ")
    print("KILO: %d" % package.mass, end =", ")
    print("STATUS: ", end ="")

    #If work day has not begun
    if timestamp < start_of_day:
        print("AT HUB")
    #If third truck has not left hub
    elif timestamp < earliest_time and package in package_list:
        print("AT HUB")
    else:
        if package.delivery_time < timestamp:
            print("DELIVERED @ ", end="")
            print(package.delivery_time.time())
        else:
            print("EN ROUTE")

    print()

#Function to print total mileage driven by all trucks via console
def print_total_mileage():
    total_mileage = truck_one.miles_traveled + truck_two.miles_traveled + truck_three.miles_traveled
    print("TOTAL MILEAGE DRIVEN: %d" % total_mileage)

    print()

if __name__ == "__main__":
    #Create hash table and populate from .csv
    hash_table = HashTable()
    load_package_data(hash_table)

    #Create distance list and populate from .csv
    distance_data = []
    load_distance_data(distance_data)

    #Create address list and populate from .csv
    address_data = []
    load_address_data(address_data)

    #Initialize truck objects with global variables for speed and package limit
    truck_speed = 18
    package_limit = 16
    truck_one = Truck(1)
    truck_two = Truck(2)
    truck_three = Truck(3)

    #List of packages that are delayed until 9:05 + package with wrong address
    delayed = [6, 9, 25, 28, 32]
    
    #Package loading
    truck_load_packages()
    load_delayed_packages(truck_three)

    # print("TRUCK ONE: ")
    # for package in truck_one.packages:
    #    print(package.id, end=": ")
    #    if package.deadline == "EOD":
    #        print("EOD")
    #    else:
    #        print(package.deadline.time())
    # print()

    # print("TRUCK TWO: ")
    # for package in truck_two.packages:
    #    print(package.id, end=", ")
    #    if package.deadline == "EOD":
    #        print("EOD")
    #    else:
    #        print(package.deadline.time())
    # print()

    # print("TRUCK THREE: ")
    # for package in truck_three.packages:
    #    print(package.id, end=", ")
    #    if package.deadline == "EOD":
    #        print("EOD")
    #    else:
    #        print(package.deadline.time())
    # print()

    #Initial copy of truck three manifesto for later use in status print-out
    truck_three_copy = truck_three.packages.copy()

    #Priority algorithm (truck one)
    time = datetime(2022, 12, 2, 8, 0)
    priority_delivery_algorithm(truck_one, time)

    #Priority algorithm (truck two)
    time = datetime(2022, 12, 2, 8, 0)
    priority_delivery_algorithm(truck_two, time)

    #A driver can begin with truck three delivers as soon as one returns to hub
    #Check to see which driver arrives back first
    earliest_time = truck_one.finish_time
    if truck_two.finish_time < earliest_time:
        earliest_time = truck_two.finish_time

    #Priority algorithm (truck three)
    priority_delivery_algorithm(truck_three, earliest_time)

#Loop to provide console input for displaying package/mileage data
while(True):
    print("***********************************************")
    print("1. Print all packages' status")
    print("2. Print single package status")
    print("3. Print total mileage driven by all trucks")
    print("4. Exit program")
    print("***********************************************")

    valid_input = ["1", "2", "3", "4"]
    choice = input()
    if choice not in valid_input:
        print("Not a valid choice!")
    elif choice == "4":
        break
    elif choice == "3":
        print_total_mileage()
    elif choice == "2":
        print("Enter Package ID (Integer from 1-40): ")
        package_id = int(input())
        print("Enter time (Format: HH:MM:SS): ")
        input_time = input()
        print_single_package_status(package_id, input_time, truck_three_copy)
    elif choice == "1":
        print("Enter time (Format: HH:MM:SS): ")
        input_time = input()
        print_package_status(input_time, truck_three_copy)