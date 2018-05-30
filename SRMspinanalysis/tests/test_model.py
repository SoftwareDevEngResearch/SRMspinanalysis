from .. import model

def test_RocketModel():
    # Tests several functions in the RocketModel class to span multiple modules.
    url = 'http://www.thrustcurve.org/simfilesearch.jsp?id=51'
    tend = 7.0
    delay = 0.02
    RocketModel = model.RocketModel()
    RocketModel.create_design_params()
    RocketModel.select_SRM(url)
    RocketModel.SRM1.motor_number_of_grains = 3.0
    RocketModel.SRM2.motor_number_of_grains = 3.0
    RocketModel.SRM2.add_delay(delay)
    RocketModel.SRM1.motor_thrust_data = RocketModel.SRM1.compute_thrust_per_grain() # I200 have three grains.
    RocketModel.SRM2.motor_thrust_data = RocketModel.SRM2.compute_thrust_per_grain() # I200 have three grains.
    RocketModel.solve_eom(tend)
    RocketModel.plot()