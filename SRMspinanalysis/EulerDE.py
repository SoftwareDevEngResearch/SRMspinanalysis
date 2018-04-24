import numpy as np

def compute_moments(params, thrust_motor_1, thrust_motor_2):
    """ Units:
        r1, r2, d1, d2: m
        Ixx, Iyy, Izz: kg-m^2 """
    r1, r2, d1, d2, Ixx, Iyy, Izz = params
    if (params >= 0).all():
        Mx = 0;
        My = thrust_motor_1*d1 - thrust_motor_2*d2
        Mz = thrust_motor_1*r1 + thrust_motor_2*r2
        moments = np.array([Mx, My, Mz])
    else:
        raise ValueError('All design parameters should be positive values.')
    return moments

"""def f(y,t,params):
    # This is a start to this function. It is not complete.
    wx, wy, wz, psi, theta, phi = y
    r1, r2, d1, d2, Ixx, Iyy, Izz = params"""