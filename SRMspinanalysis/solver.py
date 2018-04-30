import numpy as np
from scipy.interpolate import interp1d

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

def interpolate_thrust_data(t, motor_time_data, motor_thrust_data):
    """Performs a linear interpolation on motor thrust data and extracts the value
    at a desired time.

    `PEP 484`_ type annotations are supported. If attribute, parameter, and
    return types are annotated according to `PEP 484`_, they do not need to be
    included in the docstring:

    Args:
        t (float): Desired time (s) at which to compute thrust.
        motor_time_data (np.array()): Time data from a specific motor (s).
        motor_thrust_data (np.array()): Thrust data from a specific motor (N).

    Returns:
        (float): Thrust at the specified time t.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/

    """
    if t < np.min(motor_time_data) or t > np.max(motor_time_data):
        return 0.0
    else:
        interp_thrust = interp1d(motor_time_data, motor_thrust_data)
        return interp_thrust(t).item()

def euler_eom(f, t, design_params, SRM1, SRM2):
    # Update documentation.
    """Computes moment vector given thrust information from each motor and
    specific design parameters.

    `PEP 484`_ type annotations are supported. If attribute, parameter, and
    return types are annotated according to `PEP 484`_, they do not need to be
    included in the docstring:

    Args:
        f (np.array()): Array of variables to be numerically solved.
        [wx, wy, wz, psi, theta, phi] where wx, wy, wz are the body angles of the launch
        vehicle (rad) and psi, theta, and phi are the Eulerian angles (rad).
        t (float): Time (s) to numerically solve equations of motion.
        design_params (np.array()): Array of design parameters.
        [r1, r2, d1, d2, Ixx, Iyy, Izz] where r1 and r2 are the radial locations of
        the solid rocket motors (m), d1 and d2 are the longitudinal locations of the two
        motors (m), and Ixx, Iyy, and Izz are the interia values (kg-m^2).
        SRM1 (SolidRocketMotor()): First solid rocket motor organized into a class.
        SRM2 (SolidRocketMotor()): Second solid rocket motor organized into a class.

    Returns:
        (np.array()): Array of the time derivatives of the function variables f.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/

    """
    wx, wy, wz, psi, theta, phi = f
    r1, r2, d1, d2, Ixx, Iyy, Izz = design_params
    thrust_motor_1 = interpolate_thrust_data(t, SRM1.motor_time_data, SRM1.motor_thrust_data)
    thrust_motor_2 = interpolate_thrust_data(t, SRM2.motor_time_data, SRM2.motor_thrust_data)
    moments = compute_moments(design_params, thrust_motor_1, thrust_motor_2)
    Mx, My, Mz = moments
    # Differential equations of motion
    wx_dot = (Mx - (Izz - Iyy) * wy * wz) / Ixx
    wy_dot = (My - (Ixx - Izz) * wz * wx) / Ixx
    wz_dot = (Mz - (Iyy - Ixx) * wx * wy) / Ixx
    psi_dot = (wy * np.sin(phi) + wz * np.cos(phi)) * np.sec(theta)
    theta_dot = wy * np.cos(phi) - wz * np.sin(phi)
    phi_dot = wx + (wy * np.sin(phi) + wz * np.cos(phi)) * np.tan(theta)
    return np.array([wx_dot, wy_dot, wz_dot, psi_dot, theta_dot, phi_dot])
    
# Add delay function to get_data module?
# Add a model module to set up design params and solid rocket motors with time delay?
# Add delay function to SolidRocketMotor class?