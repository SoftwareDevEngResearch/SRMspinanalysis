# SRMspinanalysis
Repository for the SRMspinanalysis python package.

## Module Descriptions:

### Module #1
'''python
get_data.py
'''
'''python
class SolidRocketMotor()
'''
Contains information about the chosen solid rocket motor.
* motor name
* motor diameter in mm
* motor length in mm
* motor delays
* motor propellant weight in kg
* motor total weight in kg
* motor manufacturer

Also contains the thrust-time data.
* thrust vector
* time vector

'''python
def extract_RASP_data(url)
'''
Given a url for RASP data from thrustcurve.org, this function parses the html and extracts the appropriate data into a SolidRocketMotor() class.

'''python
def is_comment(line)
'''
Determines if a string is a RASP file comment. Comments begin with a ';' character.

### Module #2
'''python
EulerDE.py
'''
'''python
def compute_moments(params, thrust_motor_1, thrust_motor_2)
'''
Computes moment vector given thrust information from two opposite pointed SRM's and a set of design parameters.

### Module #3
'''python
sizing.py
'''
'''python
def compute_total_impulse(spin_rate, roll_inertia, radial_distance)
'''
Computes total impulse required to spin a rocket design (known roll inertia and radial location of motors) at a desired spin rate.

'''python
def compute_impulse_per_motor(total_impulse)
'''
Computes impulse for each single motor from the total impulse.