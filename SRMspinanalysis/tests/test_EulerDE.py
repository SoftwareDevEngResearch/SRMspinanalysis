from .. import EulerDE
import numpy as np

def test_compute_moments_1():
    params = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0])
    thrust_motor_1 = 25.0
    thrust_motor_2 = 6.0
    # Computed by hand
    exp = np.array([0.0, 51.0, 37.0])
    obs = EulerDE.compute_moments(params, thrust_motor_1, thrust_motor_2)
    assert np.allclose(exp, obs)