from yaw_controller import YawController
from pid import PID
from lowpass import LowPassFilter

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
        self.yaw_controller = YawController(wheel_base, steer_ratio, 0.1, max_lat_accel, max_steer_angle)
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
    	if dbw_enabled:
    		self.throttle_controller.reset()
    		return 0., 0., 0.

    	current_vel = self.vel_lpf.filt(current_vel)

    	steering = self.yaw_controller.get_ste=eering(linear_vel, angular_vel, current_vel)

    	vel_error = linear_vel - current_vel
    	self.last_vel = current_vel

    	current_time = rospy.get_time()
    	sample_time = current_time - self.last_time
    	self.last_time = current_time

    	throttle = self.throttle_controller.step(vel_error, sample_time)
		print(f'vel_error is {vel_error}, sample_time is {sample_time}, throttle is {throttle}.')
    	if linear_vel == 0 and current_vel < 0.1 :
    		throttle = 0
    		brake = 400 # Nm
    	elif throttle < 0.1 and vel_error < 0:
    		throttle = 0
    		decel = max(vel_error, self.decel_limit)
    		brake = abs(decel)*self.vehicle_mass*self.wheel_radius

        return throttle, brake, steering
