A Prometheus exporter for NTI ENVIROMUX® Environment Monitoring System (EMS) with 1-Wire Sensor Interface. 
Made using Python3.10

The script looks for the ip address of the EMS and uses a webscraper to convert data into prometheus metrics. At the moment it only scrapes for internal sensors. 
If there are future requests for external sensor pulling I can implement that.

## Notes
There is a config.json that users need to configure. The ` "address" ` parameter is empty by default and needs to be updated to your sensor IP address. Also by default,
the port for this script runs on 8103, if you want to change that port to something else, feel free. Lastly, you can modify the interval for updates with the `"interval"` parameter.

## Setup
- Clone the repository: `git clone git@github.com:WayanLu/nti_exporter.git`

- Inside the folder, create a virtual environment with Python3.10: `python3.10 -m venv your_venv_name`

- Activate the environment: `source your_venv_name/bin/activate`

- Install the required packages for this script: `pip install -r requirements.txt`

- Finally, you can run `python nti_exporter.py`

## Creating a Linux systemd service file to automate the script
