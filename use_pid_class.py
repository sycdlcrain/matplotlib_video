
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

from pid_class import PID

np.random.seed(3)

target = 0

steps = 1000
dt = 0.02
maxtime = steps*dt

noise = np.random.uniform(-.01,.01,steps)
noise[0:500]+=.02
# noise[200:300]+=.02
noise[700:900]-=.02

x0 = np.atleast_2d([0.1, 0.01]).transpose() # position, velocity, acceleration


def transition(x, control, noise): 
	# kinematics (this describes motion)
	# xf = x0 + v*t + 0.5a*t*t

	# Spring Mass Damper
	# ma + cv + kx = u (each of these is a force)
	m = 1
	c = 0.05
	k = 20

	period = 200 # steps
	w = (2*np.pi)/period # 0.06

	damping = 0.4

	# T = np.asarray([[1, dt, 0.5*dt*dt],
	# 				[0, 1,  dt],
	# 				[0, 0,  0]]) # dynamics 
	
	A = np.asarray([[   0,            1],
					[-w*w, -2*damping*w]]) # dynamics 

	b = np.asarray([[   0],
					[1/m]])

	F = control+noise

	dx = np.dot(A,x)+b*F

	x += dx 

	return x

VIDEO = 1
im_count = 0


x1 = x0 + 0.0
x2 = x0 + 0.0
x3 = x0 + 0.0
spring_history =  np.zeros((2,steps))
noise_history = np.zeros((2,steps))
pid_history = np.zeros((2,steps))
pid = PID(dt)

target = np.ones(steps)
target[:100] = 0
target[100:300] = -5.0
target[300:500] = 10.0
target[500:] = 0

for t in range(steps):
	
	x1 = transition(x1, 0, noise[t])
	# x3 = transition(x3, control, noise[t])
	control = pid.control(x3[0], target[t])
	x3 = transition(x3, control, noise[t])
	# spring_history[:,t] = x1.ravel()
	noise_history[:,t] = x1.ravel()
	pid_history[:,t] = x3.ravel()
	
	if VIDEO:
		# plot
		plt.clf()
		plt.plot(np.linspace(0,maxtime,steps), target, label='Target')
		plt.plot(np.linspace(0,maxtime,steps), pid_history[0,:], label='PID')
		plt.plot(np.linspace(0,maxtime,steps), noise_history[0,:], label='Without control')
		plt.legend()
		plt.show(block=False)
		plt.pause(0.0000000001)

		# record 
		mystring = 'video/' + str(im_count) + '.png'
		im_count += 1
		plt.savefig(mystring)


if not VIDEO:
	plt.plot(np.linspace(0,maxtime,steps),target, label='Target')
	plt.plot(np.linspace(0,maxtime,steps),noise_history[0,:], label='Without control')
	plt.plot(np.linspace(0,maxtime,steps),pid_history[0,:], label='PID')
	plt.legend()
	plt.show()
