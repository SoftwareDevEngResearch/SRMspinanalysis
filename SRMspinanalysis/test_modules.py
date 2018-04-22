import numpy as np

import get_data
import sizing
import EulerDE

def test_extract_RASP_data_1():
    # Standard url of RASP data from thrustcurve.org.
    url1 = 'http://www.thrustcurve.org/simfilesearch.jsp?id=1247'
    # From thrustcurve.org
    url1_time = np.array([0.016, 0.044, 0.08, 0.088, 0.096, 0.105, 0.116,
                          0.129, 0.131, 0.135, 0.139, 0.143, 0.149, 0.157, 
                          0.173, 0.187, 0.194, 0.197, 0.202, 0.206, 0.213,
                          0.218, 0.227, 0.236, 0.241, 0.25])
    # From function
    SRM1 = get_data.extract_RASP_data(url1)
    assert np.array_equal(url1_time, SRM1.motor_time_data[1:])
    
def test_extract_RASP_data_2():
    # Standard url of RASP data from thrustcurve.org.
    url2 = 'http://www.thrustcurve.org/simfilesearch.jsp?id=641'
    # From thrustcurve.org
    url2_thrust = np.array([16.299, 21.959, 30.785, 35.774, 37.577, 38.220,
                            37.357, 37.577, 35.093, 32.378, 27.168, 26.938,
                            25.125, 21.729, 16.980, 12.682, 7.471, 3.169,
                            1.584, 0.679, 0.000])
    # From function
    SRM2 = get_data.extract_RASP_data(url2)
    assert np.array_equal(url2_thrust, SRM2.motor_thrust_data[1:])
    
def test_compute_total_impulse_1():
    spin_rate = 25.0
    roll_inertia = 1.0
    radial_distance = 0.175
    # Computed by hand
    exp = 142.857
    obs = sizing.compute_total_impulse(spin_rate, roll_inertia, radial_distance)
    assert np.allclose(exp, obs)
    
def test_compute_total_impulse_2():
    spin_rate = 1.0
    roll_inertia = 1.0
    radial_distance = 1.0
    # Computed by hand
    exp = 1.0
    obs = sizing.compute_total_impulse(spin_rate, roll_inertia, radial_distance)
    assert np.allclose(exp, obs)
    
def test_compute_moments_1():
    params = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0])
    thrust_motor_1 = 25.0
    thrust_motor_2 = 6.0
    # Computed by hand
    exp = np.array([0.0, 51.0, 37.0])
    obs = EulerDE.compute_moments(params, thrust_motor_1, thrust_motor_2)
    assert np.allclose(exp, obs)