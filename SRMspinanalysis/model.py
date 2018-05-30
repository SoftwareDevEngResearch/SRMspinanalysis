import numpy as np
import get_data
import solver
import plot
import os

class RocketModel(object):
    """Rocket model includes physical characteristics of launch vehicle.

    Attributes
    ----------
    r1 : Radial location of solid rocket motor for spin-up [m]
    r2 : Radial location of solid rocket motor for spin-up [m]
    d1 : Longitudinal location of solid rocket motor for spin-up [m]
    d2 : Longitudinal location of solid rocket motor for spin-up [m]
    Ixx : Roll inertia of rocket [kg-m^2]
    Iyy : Yaw inertia of rocket [kg-m^2]
    Izz : Pitch inertia of rocket [kg-m^2]
    
    """
    
    def __init__(self, r1=4.5*0.0254, r2=4.5*0.0254,
                       d1=25.0*0.0254, d2=25.0*0.0254,
                       Ixx=185000.0*0.45359237*0.0254**2,
                       Iyy=185000.0*0.45359237*0.0254**2,
                       Izz=3500.0*0.45359237*0.0254**2,):
        """Initalizes the rocket model with user defined values.
        """
        self.r1 = r1 # m
        self.r2 = r2 # m
        self.d1 = d1 # m
        self.d2 = d2 # m
        self.Ixx = Ixx # kg-m^2
        self.Iyy = Iyy # kg-m^2
        self.Izz = Izz # kg-m^2
        
    def create_design_params(self):
        """Packages the design parameters into a numpy array.
        """
        self.design_params = np.array([self.r1, self.r2, self.d1, self.d2, self.Ixx, self.Iyy, self.Izz])
        
    def select_SRM(self, url1, url2=None):
        """Creates SolidRocketMotor object complete with motor information and thrust data.
        """
        if url2 is None:
            url2 = url1
        self.SRM1 = get_data.SolidRocketMotor(url1)
        self.SRM2 = get_data.SolidRocketMotor(url2)
        
    def solve_eom(self, tend, dt=0.0001):
        """Solves equations of motion for a specified duration (s) with an optional time step argument (s).
        """
        ic = np.zeros(6)
        tstart = 0.0
        self.t_span = np.linspace(tstart, tend, tend/dt)
        self.create_design_params()
        self.wx, self.wy, self.wz, self.psi, self.theta, self.phi = solver.integrate_eom(ic, self.t_span, self.design_params, self.SRM1, self.SRM2).T
        self.nutation_angle = solver.compute_nutation_angle(self.theta, self.phi)
        self.precession_angle = solver.compute_precession_angle(self.theta, self.psi)
    
    def plot(self, euler_angles=True, nutation_angle=True, longitudinal_axis=True, show_plot=True, save_plot=True, filepath=os.path.join(os.path.expanduser('~'), 'SpinFigures'), filenames=['Euler.png', 'Nut.png', 'Axis.png']):
        """Plots figures and saves them to file by default. All arguments are optional and can be changed if necessary.
        """
        if euler_angles:
            plot.plot_euler_angles(self.t_span, self.psi, self.theta, self.phi)
            if save_plot:
                if not os.path.exists(filepath):
                    os.makedirs(filepath)
                plot.save_plot(os.path.join(filepath, filenames[0]))
        if nutation_angle:
            plot.plot_nutation_angle(self.t_span, self.nutation_angle)
            if save_plot:
                if not os.path.exists(filepath):
                    os.makedirs(filepath)
                plot.save_plot(os.path.join(filepath, filenames[1]))
        if longitudinal_axis:
            plot.plot_longitudinal_axis(self.t_span, self.nutation_angle, self.precession_angle)
            if save_plot:
                if not os.path.exists(filepath):
                    os.makedirs(filepath)
                plot.save_plot(os.path.join(filepath, filenames[2]))
        if show_plot:
            plot.show_plot()