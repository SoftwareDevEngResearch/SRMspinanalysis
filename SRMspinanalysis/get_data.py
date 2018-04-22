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

def get_RASP_data(url):
    """ This function takes in a specific thrustcurve.org url for a RASP data file 
        and extracts the desired html text into a list of strings for each line in
        the data file. """
    response = urllib2.urlopen(url)
    raw_html = response.read()
    parsed_html = BeautifulSoup(raw_html, 'html.parser')
    RASP_raw_data = ''.join(parsed_html.find('textarea').get_text()).split('\n')
    RASP_raw_data = [re.sub('\r', '', line) for line in RASP_raw_data]
    RASP_raw_data = [line.lstrip() for line in RASP_raw_data]
    RASP_raw_data = [re.sub(' +', ' ', line) for line in RASP_raw_data]
    # This line encodes the unicode data to utf-8.
    #RASP_raw_data = [item.encode('utf-8') for item in RASP_raw_data]
    RASP_raw_data = [line for line in RASP_raw_data if not is_comment(line)]
    if RASP_raw_data[-1] == u'':
        RASP_raw_data = RASP_raw_data[:-1]
    return RASP_raw_data
    
def is_comment(line):
    """ This function simply checks to see if a line in a RASP file is a comment. 
        Comments begin with a ';' character. """
    return line.startswith(';')
    
def extract_RASP_data(url):
    """ This function takes the raw RASP data and organizes it into a class. """
    RASP_raw_data = get_RASP_data(url)
    motor_header_line = RASP_raw_data[0].split(' ')
    RASP_raw_thrust_data = [line.split(' ') for line in RASP_raw_data[1:]]
    motor_time_data = np.zeros(1)
    motor_thrust_data = np.zeros(1)
    for data_point in RASP_raw_thrust_data:
    #    print data_point
        motor_time_data = np.append(motor_time_data, float(data_point[0]))
        motor_thrust_data = np.append(motor_thrust_data, float(data_point[1]))
    return SolidRocketMotor(motor_header_line, motor_time_data, motor_thrust_data)
    
"""if __name__ == '__main__':
    url ='http://www.thrustcurve.org/simfilesearch.jsp?id=641'
    url2 = 'http://www.thrustcurve.org/simfilesearch.jsp?id=1247'
    SRM = extract_RASP_data(url2)"""