import time
import os
import json
import logging
import sys
from prometheus_client import start_http_server, Gauge
from utils.readNTIsensors import get_nti_sensors
from utils.log import set_logger


# Add more variables if you want to export more metrics
temperature_gauge = Gauge('nti_sensor_temperature',
                          'Temperature of NTI sensors', ['sensor_id'])


def read_config(filepath):
    '''
    Process yaml file to get config
    '''
    logging.info('config.json filepath: %s', filepath)
    with open(filepath, 'r') as file:
        config_json = file.read()

    config = json.loads(config_json)
    logging.info('Config loaded: %s', config)

    (address, interval, port) = (
            config["address"],
            int(config["interval"]),
            int(config["port"])
    )

    return address, interval, port


def process_request(t, addr):
    '''
    Get data from NTI sensors and update exporter
    '''
    nti_data = get_nti_sensors(addr)
    logging.info('NTI sensor data: %s', nti_data)
    for (sensor_id, temperature) in nti_data.items():
        temperature_gauge.labels(sensor_id=sensor_id).set(temperature)

    time.sleep(t)


if __name__ == '__main__':
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python nti_exporter.py <config_path>")
        sys.exit(1)

    # Access the argument value
    config_path = sys.argv[1]
    # Parse config_path to get working directory
    working_directory = os.path.dirname(config_path)
    # Set logger
    set_logger(working_directory)
    # Read Config
    address, interval, port = read_config(config_path)
    # Start up the server to expose the metrics.
    start_http_server(port)
    logging.info('NTI exporter started listening on port %s...', port)
    # Generate some requests.
    while True:
        logging.info('Retrieving data from NTI sensors...')
        process_request(interval, address)
