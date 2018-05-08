# SRMspinanalysis

## About
SRMspinanalysis package contains modules for analyzing dynamic effects of small launch vehicles in zero gravity utilizing solid rocket motors for spin-stabilization.

## Module Descriptions

### get\_data.py
Pulls data from thrustcurve.org url for RASP engine data and organizes data into a class.

#### class SolidRocketMotor()

Contains information about the chosen solid rocket motor. Output of the extract_RASP_data function.
* motor name
* motor diameter (mm)
* motor length (mm)
* motor delays
* motor propellant weight (kg)
* motor total weight (kg)
* motor manufacturer

Also contains the thrust-time data.
* thrust vector (N)
* time vector (s)

Contains function to add an ignition delay to the chosen motor.

#### def extract\_RASP\_data(url)
Given a url for RASP engine data from thrustcurve.org, this function parses the html and extracts the appropriate data into a SolidRocketMotor class.

#### def is\_comment(line)
Determines if a string is a RASP file comment. Comments begin with a ';' character.

### solver.py
Contains dynamic model and necessary functions to solve equations of motion.

#### def compute\_moments(params, thrust\_motor\_1, thrust\_motor\_2)
Computes moment vector given thrust information from two oppositely pointed SRM's and a set of design parameters.

#### def interpolate\_thrust\_data(t, motor\_time\_data, motor\_thrust\_data):
Performs a linear interpolation on motor thrust data and extracts the value at a desired time.

#### def euler\_eom(f, t, design\_params, SRM1, SRM2):
Numerically computes the time derivatives of the specified function variables. To be used for numerical integration.

### sizing.py
Simple module that can be used to size a motor given design constraints.

#### def compute\_total\_impulse(spin\_rate, roll\_inertia, radial\_distance)
Computes total impulse required to spin a rocket design (i.e. known roll inertia and radial location of motors) at a desired spin rate.

#### def compute\_impulse\_per\_motor(total\_impulse)
Computes impulse for a single motor from the total impulse.