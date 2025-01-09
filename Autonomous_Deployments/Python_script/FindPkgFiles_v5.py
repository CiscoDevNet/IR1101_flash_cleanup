from netmiko import ConnectHandler
import csv

# Define the function to process each router
def process_router(router_details, output_file, failed_file):
    try:
        # Connect to the router
        connection = ConnectHandler(**router_details)
        print("Connected to {}.".format(router_details['host']))

        # Navigate to the flash: directory
        command = "dir flash:"
        output = connection.send_command(command)
        print("Flash directory contents on {}:\n{}".format(router_details['host'], output))

        # Check for .pkg files in the output
        if ".pkg" in output:
            print("Found .pkg files in flash: on {}.".format(router_details['host']))

            # Append the router's details to the output file as plain text with comma separation
            with open(output_file, mode="a") as file:
                file.write("{},{},{},{}\n".format(
                    router_details['host'],
                    router_details['username'],
                    router_details['password'],
                    router_details['device_type']
                ))
        else:
            print("No .pkg files found in flash: on {}.".format(router_details['host']))

    except Exception as e:
        print("An error occurred on {}: {}".format(router_details['host'], e))

        # Append failed connection details to the failed file
        with open(failed_file, mode="a") as file:
            file.write("{} - Error: {}\n".format(router_details['host'], e))

    finally:
        # Ensure the connection is closed if it was established
        if 'connection' in locals():
            connection.disconnect()
            print("Connection closed for {}.".format(router_details['host']))

# Read router details from the text file
def read_routers_from_file(filename):
    routers = []
    try:
        with open(filename, mode="r") as file:
            csv_reader = csv.DictReader(file, fieldnames=["host", "username", "password", "device_type"])
            for row in csv_reader:
                routers.append(row)
    except Exception as e:
        print("Error reading file {}: {}".format(filename, e))
    return routers

# Main logic
if __name__ == "__main__":
    # Specify the filename containing router details
    input_file = "routers.txt"

    # Specify the output file to store routers with .pkg files in comma-separated format
    output_file = "routers_with_pkg.txt"

    # Specify the output file for failed connections
    failed_file = "failed_connections.txt"

    # Clear the output and failed files at the start
    # with open(output_file, mode="w") as file:
    #    file.write("Host,Username,Password,Device Type\n")

    with open(failed_file, mode="w") as file:
        file.write("Failed connections:\n")

    # Get the list of routers
    router_list = read_routers_from_file(input_file)

    # Process each router
    for router in router_list:
        process_router(router, output_file, failed_file)