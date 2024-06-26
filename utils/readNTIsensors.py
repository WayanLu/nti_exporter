import re
import json
import requests
import logging
from bs4 import BeautifulSoup
from typing import Dict


def get_nti_sensors(nti_address: str) -> Dict[int, float]:
    '''
    Function to get all nti sensors and return a dictionary of
    {sensor_number: sensor_temperature}
    '''

    response = requests.get(nti_address, auth=('root', 'nti'))
    response.raise_for_status()  # Raise an exception for bad responses

    html_soup = BeautifulSoup(response.text, 'html.parser')
    nti_sensors = {}

    for index, sensor_element in enumerate(
            html_soup.find_all(id=re.compile(r'es\d+'))):

        sensor = sensor_element.get_text()
        temperature = re.sub(r'[^\d.]+', '', sensor)
        if temperature != '':
            nti_sensors[index] = float(temperature)
        else:
            logging.info(f'Sensor {index}: No Value')

    return nti_sensors


if __name__ == "__main__":
    print("Test")
    with open("../config.json") as file:
        config_json = file.read()

    config = json.loads(config_json)
    nti_address = config["address"]

    nti = get_nti_sensors(nti_address)
    print(nti)
