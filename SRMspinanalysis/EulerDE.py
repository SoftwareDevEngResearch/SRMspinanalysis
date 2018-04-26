import numpy as np

def compute_moments(design_params, thrust_motor_1, thrust_motor_2):
    """Computes moment vector given thrust information from each motor and
    specific design parameters.

    `PEP 484`_ type annotations are supported. If attribute, parameter, and
    return types are annotated according to `PEP 484`_, they do not need to be
    included in the docstring:

    Args:
        design_params (np.array()): Array of design parameters.
        [r1, r2, d1, d2, Ixx, Iyy, Izz] where r1 and r2 are the radial locations of
        the solid rocket motors (m), d1 and d2 are the longitudinal locations of the two
        motors (m), and Ixx, Iyy, and Izz are the interia values (kg-m^2).
        thrust_motor_1 (float): Thrust from motor 1 (N).
        thrust_motor_2 (float): Thrust from motor 2 (N).

    Returns:
        moments (np.array()): Moment vector in the x, y, and z directions (N-m).

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/

    """
    r1, r2, d1, d2, Ixx, Iyy, Izz = design_params
    if (design_params >= 0).all():
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