from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
import csv

# Define the function to validate if the file is .bin
def validate_bin(file_path):
    """ Validate if the given file path ends with .bin"""
    return file_path.strip().lower().endswith(".bin")

# Define the function to check for .pkg and .conf files in the router's flash:
def check_files_in_flash(connection):
    """Check if .pkg and .conf files exist in the router's flash and return the list of these files"""
    command = "dir flash:"
    output = connection.send_command(command)
    print("Flash directory contents:\n{}".format(output))

    pkg_files = []
    conf_files = []

    # Parse the output to find .pkg and .conf files
    for line in output.splitlines():
        if ".pkg" in line:
            pkg_files.append(line.split()[-1])  # Get the file name (last item in the line)
        elif ".conf" in line:
            conf_files.append(line.split()[-1])  # Get the file name (last item in the line)

    return pkg_files, conf_files

# Define the function to process each router
def process_router(router_details, success_file):
    try:
        # Attempt to connect to the router
        connection = ConnectHandler(**router_details)
        print("Connected to {}.".format(router_details['host']))

        # Check the system image file
        output = connection.send_command("show version | include image file")
        print("System image output on {}: {}".format(router_details['host'], output))

        # Extract the file path
        if "System image file is" in output:
            file_path = output.split("is")[-1].strip().strip('"')
            if validate_bin(file_path):
                print("The system image file '{}' is valid (.bin).".format(file_path))
            else:
                print("System image file '{}'. Skipping file deletion on {}.".format(file_path, router_details['host']))
                return
        else:
            print("Could not determine the system image file on {}.".format(router_details['host']))
            return

        # Check if .pkg or .conf files are present in flash: before attempting to delete
        pkg_files, conf_files = check_files_in_flash(connection)

        # Display the complete list of files found in flash:
        if pkg_files:
            print("Found .pkg files in flash: on {}:".format(router_details['host']))
            for pkg in pkg_files:
                print(pkg)

        if conf_files:
            print("Found .conf files in flash: on {}:".format(router_details['host']))
            for conf in conf_files:
                print(conf)

        # Check if there are any .pkg or .conf files to delete
        if pkg_files or conf_files:
            # Commands to delete files
            commands = [
                "cd flash:",  # Navigate to the appropriate directory
                "delete /recursive *.pkg"
            ]

            for command in commands:
                if "delete" in command:  # Handle delete command interactively
                    print("Executing command: {}".format(command))
                    
                    # Send the delete command
                    output = connection.send_command(command, expect_string=r"Delete filename")
                    print(output)

                    # Confirm the filename deletion prompt
                    if "Delete filename" in output:
                        output = connection.send_command("", expect_string=r"confirm")
                        print(output)
                    
                    # Confirm the final deletion prompt
                    if "confirm" in output:
                        output = connection.send_command("y", expect_string=r"#")
                        print(output)
                else:
                    # Handle non-delete commands
                    output = connection.send_command(command, expect_string=r"#")
                    print(output)  # Print the output of the command

            print("Files deleted successfully on {}.".format(router_details['host']))

            # Log successful operation
            with open(success_file, "a") as file:
                file.write("{} - Success\n".format(router_details['host']))
        else:
            print("No .pkg or .conf files found in flash: on {}. Skipping deletion.".format(router_details['host']))

    except NetMikoTimeoutException as e:
        print("Timeout while connecting to router {}: {}".format(router_details['host'], e))
    except NetMikoAuthenticationException as e:
        print("Authentication failed for router {}: {}".format(router_details['host'], e))
    except Exception as e:
        print("An error occurred on {}: {}".format(router_details['host'], e))
    finally:
        # Ensure the connection is closed
        try:
            connection.disconnect()
            print("Connection closed for {}.".format(router_details['host']))
        except NameError:
            print("No connection to close for {}.".format(router_details['host']))
        except Exception as e:
            print("Failed to close connection for {}: {}".format(router_details['host'], e))

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
    filename = "routers_with_pkg.txt"
    success_file = "success.txt"

    # Clear or create the success file
    open(success_file, "w").close()

    # Get the list of routers
    router_list = read_routers_from_file(filename)

    # Process each router
    for router in router_list:
        process_router(router, success_file)
