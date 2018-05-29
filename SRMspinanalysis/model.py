import numpy as np

class RocketModel():
    def __init__(self, r1=4.5*0.0254, r2=4.5*0.0254,
                       d1=25.0*0.0254, d2=25.0*0.0254,
                       Ixx=185000.0*0.45359237*0.0254**2,
                       Iyy=185000.0*0.45359237*0.0254**2,
                       Izz=3500.0*0.45359237*0.0254**2,):
        self.r1 = r1 # m
        self.r2 = r2 # m
        self.d1 = d1 # m
        self.d2 = d2 # m
        self.Ixx = Ixx # kg-m^2
        self.Iyy = Iyy # kg-m^2
        self.Izz = Izz # kg-m^2
        
    def create_design_params(self):
        return np.array([self.r1, self.r2, self.d1, self.d2, self.Ixx, self.Iyy, self.Izz])