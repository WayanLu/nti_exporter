import time
import json
from datetime import datetime
from prometheus_client import start_http_server, Gauge
from readNTIsensors import get_nti_sensors

# Add more variables if you want to exporter more metrics
temperature_gauge = Gauge('nti_sensor_temperature', 'Temperature of NTI sensors', ['sensor_id'])

def read_config(filepath):
    '''
    Process yaml file to get config
    '''
    with open(filepath, 'r') as file:
        config_json = file.read()

    config = json.loads(config_json)
    print(config)
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
    print(f'{datetime.now()} nti_sensor_data: {nti_data}')
    for (sensor_id, temperature) in nti_data.items():
        temperature_gauge.labels(sensor_id=sensor_id).set(temperature)

    time.sleep(t)

if __name__ == '__main__':

    filepath = "config.json"
    address, interval, port = read_config(filepath)
    
    # Start up the server to expose the metrics.
    start_http_server(port)
    print(f'{datetime.now()} Start nti_exporter listening on port {port}...')
    # Generate some requests.
    while True:
        print(f'{datetime.now()} Retrieving data from NTI sensors...')
        process_request(interval)


