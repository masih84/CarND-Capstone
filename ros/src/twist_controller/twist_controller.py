
GAS_DENSITY = 2.858
ONE_MPH = 0.44704


class Controller(object):
    def __init__(self, vehicle_mass ,
                                    fuel_capacity,
                                    brake_deadband,
                                    decel_limit,
                                    accel_limit,
                                    wheel_radius,
                                    wheel_base,
                                    steer_ratio,
                                    max_lat_accel,
                                    max_steer_angle):
        # TODO: Implement
        self.yaw_controller = yaw_controller(wheel_base, steer_ratio, 0.1, max_lat_accel, max_steer_angle)
        kp = 0.3
        ki = .1
        kd =0.
        mn =0. # min throtle value
        mx =.2 # max throtle value

        self.throttle_controller = PID(kp, ki, kd, mn, mx)

        tau = .5
        ts = 0.02
        self.vel_lpf = LowPassFilter(tau, ts)


    def control(self, current_vel, angular_vel, linear_vel, dbw_enabled):
        # TODO: Change the arg, kwarg list to suit your needs
        # Return throttle, brake, steer
        return 1., 0., 0.
