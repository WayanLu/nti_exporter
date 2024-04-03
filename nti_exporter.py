import time
import json
import logging
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
    # Set logger
    set_logger()
    # Read Config
    filepath = "config.json"
    address, interval, port = read_config(filepath)
    # Start up the server to expose the metrics.
    start_http_server(port)
    logging.info('NTI exporter started listening on port %s...', port)
    # Generate some requests.
    while True:
        logging.info('Retrieving data from NTI sensors...')
        process_request(interval, address)

