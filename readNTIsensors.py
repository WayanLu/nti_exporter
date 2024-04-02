import re
import requests
from bs4 import BeautifulSoup
from typing import Dict

nti_address='http://10.0.0.11'

def get_nti_sensors(nti_address: str) -> Dict[int, float]:
    '''
    Function to get all nti sensors and return a dictionary of
    {sensor_number: sensor_temperature}
    '''

    response = requests.get(nti_address, auth=('root', 'nti'))
    response.raise_for_status()  # Raise an exception for bad responses

    html_soup = BeautifulSoup(response.text, 'html.parser')
    nti_sensors = {}

    for index, sensor_element in enumerate(html_soup.find_all(id=re.compile(r'es\d+'))):

        sensor = sensor_element.get_text()
        temperature = re.sub(r'[^\d.]+', '', sensor)
        nti_sensors[index] = float(temperature)

    return nti_sensors

if __name__ == "__main__":
    print("Test")
    nti = get_nti_sensors(nti_address)
    print(nti)
