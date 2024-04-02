import random
import time
from datetime import datetime
from prometheus_client import start_http_server, Gauge
from readNTIsensors import get_nti_sensors

# Interval for pulling data
INTERVAL = 5
PORT = 8103
ADDRESS = 'http://10.0.0.11'

# Add more variables if you want to exporter more metrics
temperature_gauge = Gauge('nti_sensor_temperature', 'Temperature of NTI sensors', ['sensor_id'])

def process_request(t):
    '''
    Get data from NTI sensors and update exporter
    '''

    nti_data = get_nti_sensors(ADDRESS)
    print(f'{datetime.now()} nti_sensor_data: {nti_data}')
    for (sensor_id, temperature) in nti_data.items():
        temperature_gauge.labels(sensor_id=sensor_id).set(temperature)

    time.sleep(t)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(PORT)
    print(f'{datetime.now()} Start nti_exporter listening on port {PORT}...')
    # Generate some requests.
    while True:
        print(f'{datetime.now()} Retrieving data from NTI sensors...')
        process_request(INTERVAL)
