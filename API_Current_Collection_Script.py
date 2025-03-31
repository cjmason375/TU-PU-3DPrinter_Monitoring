import os
import csv
import requests
import datetime
import time
from xml.etree import ElementTree as ET

def create_dir(directory):
    try:
        if not os.path.exists(directory):
            print("Current directory:", directory)
            os.makedirs(directory)
    except OSError:
        print("Error: Creating directory. " + directory)

def get_mtconnect_data(url, retries=5, delay=5):
    """method to get MTConnect data with exception"""
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # raise error if happens..
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}. Retrying in {delay} seconds... (Attempt {attempt+1}/{retries})")
            time.sleep(delay)
    print(f"Failed to retrieve data after {retries} attempts.")
    return None

# Main execution code inside the if __name__ block
if __name__ == "__main__":  # Ensure the code runs only when the script is executed directly
    agent = "10.114.4.110:5000"
    print(datetime.datetime.now(), "MTConnect-current csv collection started...")
    now = datetime.datetime.now(datetime.timezone.utc)
    now_ts = now.strftime("%Y%m%d_%H%M%S.%fz")

    # Set the directory where you want to save the CSV files
    path = "C:\\Users\\TUPUProject\\Desktop\\Printer Recording\\xml_access"
    create_dir(path)  # Ensure the directory exists

    while True:
        # Change working directory to where you want the files to be saved
        directory = os.path.join(path, "mtconnect_data")
        create_dir(directory)  # Create subfolder for saving data if it doesn't exist
        os.chdir(directory)

        url_current = "http://" + agent + "/current"  # Current Request

        # Get MTConnect data
        mtconnect_content = get_mtconnect_data(url_current)
        if mtconnect_content is None:
            # If data retrieval failed, retry
            continue

        try:
            MTCONNECT_STR = ET.fromstring(mtconnect_content).tag.split("}")[0] + "}"
        except ET.ParseError as e:
            print(f"XML parsing failed: {e}. Skipping this iteration.")
            time.sleep(5)  # Retry after a time sleep
            continue

        now = datetime.datetime.now(datetime.timezone.utc)
        ts = now.strftime("%Y-%m-%d %H:%M:%S.%fz")
        d = {"timestamp": ts}  # Data dictionary
        root = ET.fromstring(mtconnect_content)

        # XML parsing
        for device in root.iter(MTCONNECT_STR + "DeviceStream"):
            uuid = device.get('uuid')
            filename = "_".join([now_ts, uuid]) + ".csv"  # YYYYmmdd_machineuuid.csv

            try:
                with open(filename, 'a', newline='') as csvfile:
                    for event in device.iter(MTCONNECT_STR + "Events"):
                        for elem in event:
                            dId = elem.get("dataItemId")  # Data item id
                            text = elem.text.replace(",", " ")  # Replace commas with spaces
                            d[dId] = text  # Add {dataItemId:value} pairs

                    for sample in device.iter(MTCONNECT_STR + "Samples"):
                        for elem in sample:
                            dId = elem.get("dataItemId")  # Data item id
                            d[dId] = elem.text

                    for condition in device.iter(MTCONNECT_STR + "Condition"):
                        for elem in condition:
                            d[elem.get("dataItemId")] = elem.tag.replace(MTCONNECT_STR, "")

                    field_name = list(d.keys())
                    writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n', fieldnames=field_name)

                    if os.stat(filename).st_size == 0:  # If file exists, skip header generation
                        writer.writeheader()

                    writer.writerow(d)  # Insert a new row
                    print(d)  # Print to check

            except OSError as e:  # Handle writing errors
                print(f"Error writing to file {filename}: {e}")
                time.sleep(1)  # Retry after 1 sec.

        time.sleep(1)  # Wait before the next iteration

