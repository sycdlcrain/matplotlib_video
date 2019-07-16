
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

np.random.seed(3)

class PID:
	def __init__(self, dt):
		self.integral_buffer = deque()
		self.max_buffer = 1000 # must be large 10000
		self.dt = dt

		# Ziegler Nichols Tuning
		# https://en.wikipedia.org/wiki/Ziegler%E2%80%93Nichols_method
		self.Kp = 1.2*0.02 # I don't really get oscillations, but it goes unstable above 0.02
		Tu = 40*self.dt # no oscillations from Kp, but small Tu's give osc, but this is a single number to tune
		self.Ki = self.Kp/(Tu/2) #0.001 # stable I only = 0.001  # Kp/(Tu/2) = 0.03
		self.Kd = self.Kp*(Tu/8) #.3 #1 #Kp*(Tu/8)

		# Tuning Notes
		# There should be a Kp that gives a control that steady states (probably not the desired steady state though)
		# Set this then add in I and D terms: Lower Tu to get fastest stable response
		# Lower Kp reduce over shoot
		# increase/tune Tu

	def control(self, x, target):
		error = target - x

		if len(self.integral_buffer)>0:
			derivative = (error - self.integral_buffer[-1])/self.dt
		else: 
			derivative = 0

		self.integral_buffer.append(error)
		if len(self.integral_buffer)>self.max_buffer:
			self.integral_buffer.popleft()
		integral = np.sum(np.asarray(self.integral_buffer))*self.dt

		# # wind up
		# self.max_integral = 50
		# if np.abs(integral)>self.max_integral:
		# 	integral = np.sign(integral)*self.max_integral

		pid = self.Kp*error + self.Ki*integral + self.Kd*derivative 
		return pid

	def tune(self):
		# TODO
		pass
