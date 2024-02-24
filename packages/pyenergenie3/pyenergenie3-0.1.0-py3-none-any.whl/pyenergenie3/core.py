import getpass
import re

import requests
from bs4 import BeautifulSoup


class PyEnergenie3:
    def __init__(self, device_ip, password):
        self.device_ip = device_ip
        self.password = password
        self.base_url = f"http://{device_ip}"
        self.session = requests.Session()

    def authenticate(self):
        login_url = f"{self.base_url}/login.html"
        login_data = {"pw": self.password}
        try:
            response = self.session.post(login_url, data=login_data)
            response.raise_for_status()

            # Check for additional conditions indicating unsuccessful authentication
            if response.text == "" or "EnerGenie Web:" in response.text:
                raise RuntimeError(f"Authentication failed")
        
        except requests.ConnectionError:
            raise RuntimeError("Failed to connect to the device. Check your network connection.")  
        except requests.HTTPError as http_err:
            # This captures specific HTTP status errors.
            raise RuntimeError(f"HTTP error occurred: {http_err}")
        except requests.RequestException as e:
            # This is for catching any other requests-related exceptions.
            raise RuntimeError(f"An error occurred while handling the request: {str(e)}")

    def get_all_outlet_states(self):
        status_url = f"{self.base_url}/status"
        try:
            response = self.session.get(status_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            script_content = ""
            scripts = soup.find_all("script")
            for script in scripts:
                if "sockstates" in script.text:
                    script_content = script.text
                    break;
            
            if not script_content:
                raise RuntimeError("Failed to find 'sockstates' in the page.")

            # Pattern to find 'sockstates' and its value in the script text
            match = re.search(r'.*var sockstates = \[(.*)\];.*', script.text)
            if not match:
                raise RuntimeError("Failed to extract 'sockstates' from the script content.")

            # convert the matched group to a list of integers
            #states = [int(state) for state in match.group(1).split(',')]
            states = list(map(int, match.group(1).split(',')))

        except requests.ConnectionError:
            raise RuntimeError("Failed to connect to the device. Check your network connection.")
        except requests.HTTPError as http_err:
            raise RuntimeError(f"HTTP error occurred: {http_err}")
        except requests.RequestException as req_err:
            raise RuntimeError(f"Error occurred while fetching outlet states: {req_err}")
        except ValueError as val_err:
            raise RuntimeError(f"Error parsing outlet states: {val_err}")
        
        
    def get_outlet_state(self, outlet_number):
        try:
            all_states = self.get_all_outlet_states()
            return all_states[outlet_number - 1]
        except IndexError:
            raise ValueError(f"Invalid outlet number: {outlet_number}")

    def set_outlet_state(self, outlet_number, state):
        if state not in [0, 1]:
            raise ValueError("State should be 0 (off) or 1 (on)")

        control_url = f"{self.base_url}/"
        data = {f"cte{outlet_number}": state}
        try:
            response = self.session.post(control_url, data=data)
            response.raise_for_status()

        except requests.ConnectionError:
            raise RuntimeError("Failed to connect to the device. Check your network connection.")  
        except requests.HTTPError as http_err:
            # This captures specific HTTP status errors.
            raise RuntimeError(f"HTTP error occurred: {http_err}")
        except requests.RequestException as e:
            # This is for catching any other requests-related exceptions.
            raise RuntimeError(f"An error occurred while setting outlet states: {str(e)}")

    def set_all_outlets(self, state):
        if state not in [0, 1]:
            raise ValueError("State should be 0 (off) or 1 (on)")

        control_url = f"{self.base_url}/"

        for outlet_number in range(1, 5):
            data = {f"cte{outlet_number}": state}

            try:
                response = self.session.post(control_url, data=data)
                response.raise_for_status()
            except requests.RequestException as e:
                raise RuntimeError(f"Failed to set state for outlet {outlet_number}: {str(e)}")


def main():
    # Replace with the IP address of your device
    device_ip = input("Enter the IP address of the device: ")
    password = getpass.getpass("Enter the password for the device: ")

    energenie = PyEnergenie3(device_ip, password)

    try:
        # Authenticate
        energenie.authenticate()
        print("Authentication successful.")

        # Get all outlet states
        all_states = energenie.get_all_outlet_states()
        print("All outlet states:", all_states)

        # Get state of a specific outlet
        outlet_number = int(input("Enter the outlet number (1-4) to get its state: "))
        outlet_state = energenie.get_outlet_state(outlet_number)
        print(f"State of outlet {outlet_number}: {outlet_state}")

        # Set state of a specific outlet
        outlet_number = int(input("Enter the outlet number (1-4) to set its state (0 or 1): "))
        outlet_state = int(input("Enter the state (0 for off, 1 for on): "))
        energenie.set_outlet_state(outlet_number, outlet_state)
        print(f"State of outlet {outlet_number} set to {outlet_state}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
