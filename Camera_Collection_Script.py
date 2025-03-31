import requests
import datetime
import time
import os

snapshot_url = "http://10.114.4.108:8080/?action=snapshot"

def main():
    try:
        start_time = time.time()
        print(f"{datetime.datetime.now()}: Snapshot data collection now in progress...")

        while True:
            current_time = time.time()
            if current_time - start_time >= 1:
                timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S.%fZ")
                path = r'C:\Users\TUPUProject\Desktop\Printer Recording\Camera Screenshots'  # Raw string for file path
                name = f"{timestamp}_snapshot.png"
                name = os.path.join(path, name)

                response = requests.get(snapshot_url, stream=True)
                response.raise_for_status()

                with open(name, 'wb') as file:
                    file.write(response.content)
                print(f"Snapshot saved to {name}.")

                start_time = current_time

                time.sleep(1)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching snapshot: {e}.")
    except KeyboardInterrupt:
        print("Process interrupted by user.")
    except Exception as e:
        print(f"Error processing image: {e}.")

if __name__ == "__main__":
    main()
