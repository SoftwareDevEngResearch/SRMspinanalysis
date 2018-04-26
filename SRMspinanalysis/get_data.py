# Handles RASP File Formats from thrustcurve.org

from bs4 import BeautifulSoup
import urllib2
import numpy as np
import re

class SolidRocketMotor():
    def __init__(self, motor_header_line, motor_time_data, motor_thrust_data):
        self.motor_name = motor_header_line[0]
        self.motor_diameter = motor_header_line[1]
        self.motor_length = motor_header_line[2]
        self.motor_delays = motor_header_line[3]
        self.motor_propellant_weight = motor_header_line[4]
        self.motor_total_weight = motor_header_line[5]
        self.motor_manufacturer = motor_header_line[6]
        self.motor_time_data = motor_time_data
        self.motor_thrust_data = motor_thrust_data

def extract_RASP_data(url):
    """Provide this function with a RASP engine url from thrustcurve.org to
    retrieve thrust data and other important motor information in a class via
    html parsing using BeautifulSoup.
    
    `PEP 484`_ type annotations are supported. If attribute, parameter, and
    return types are annotated according to `PEP 484`_, they do not need to be
    included in the docstring:

    Args:
        url (str): URL from thrustcurve.org containing RASP engine data.

    Returns:
        SolidRocketMotor: Class returned containing motor information and
        thrust data.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/

    """
    # Opens and reads the raw html
    response = urllib2.urlopen(url)
    raw_html = response.read()
    # Sets up BeautifulSoup to help parse html
    parsed_html = BeautifulSoup(raw_html, 'html.parser')
    # Find and extract the desired string from the <TEXTAREA> block.
    RASP_raw_data = ''.join(parsed_html.find('textarea').get_text()).split('\n')
    RASP_raw_data = [re.sub('\r', '', line) for line in RASP_raw_data]
    RASP_raw_data = [line.lstrip() for line in RASP_raw_data]
    RASP_raw_data = [re.sub(' +', ' ', line) for line in RASP_raw_data]
    # This line encodes the unicode data to utf-8. It is optional.
    #RASP_raw_data = [item.encode('utf-8') for item in RASP_raw_data]
    RASP_raw_data = [line for line in RASP_raw_data if not is_comment(line)]
    if RASP_raw_data[-1] == u'':
        RASP_raw_data = RASP_raw_data[:-1]
    # Separate raw string into header line (containing motor information),
    # a time vector, and a thrust vector.
    motor_header_line = RASP_raw_data[0].split(' ')
    RASP_raw_thrust_time_data = [line.split(' ') for line in RASP_raw_data[1:]]
    motor_time_data = np.zeros(len(RASP_raw_thrust_time_data)+1)
    motor_thrust_data = np.zeros(len(RASP_raw_thrust_time_data)+1)
    for index, data_point in enumerate(RASP_raw_thrust_time_data, 1):
        motor_time_data[index] = float(data_point[0])
        motor_thrust_data[index] = float(data_point[1])
    return SolidRocketMotor(motor_header_line, motor_time_data, motor_thrust_data)
    
def is_comment(line):
    """This function simply checks to see if a line in a RASP file is a comment. 
    Comments begin with a ';' character.
    
    `PEP 484`_ type annotations are supported. If attribute, parameter, and
    return types are annotated according to `PEP 484`_, they do not need to be
    included in the docstring:

    Args:
        line (str): Line from html text.

    Returns:
        bool: Whether or not a line is a comment.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/

    """
    return line.startswith(';')