def compute_total_impulse(spin_rate, roll_inertia, radial_distance):
    """ Computes total impulse required to spin rocket at desired rate.
        Units are as follows:
        spin_rate: rad/s
        roll_inertia: kg-m^2
        radial_distance: m """
    if spin_rate <= 0 or roll_inertia <= 0 or radial_distance <= 0:
        raise ValueError('Spin rate, roll inertia, and radial distance must be positive values.')
    total_impulse = roll_inertia*spin_rate/float(radial_distance)
    return total_impulse
    
def compute_impulse_per_motor(total_impulse):
    if total_impulse <= 0:
        raise ValueError('Total impulse must be a positive value.')
    return total_impulse/2.0