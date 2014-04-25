# This document contains 1-D calculations for the Refrigerator system using LN2.


import CoolProp
import CoolProp.CoolProp as CP
import numpy as np
from scipy.optimize import fixed_point

#Physical Parameters

D =.0254 	#meter, Hydraulic diameter of 1.0" pipe/hose
epsilon_pipe = 0.0001		# meter, surface roughness of piping
epsilon_hose = 0.00635		# meter, referenced from Swagelok convoluted flex hoses


#Flow Parameters

m_dot = 0.400		# kg/second, NEEDS TO BE OPTIMIZED

T_operation = 90 	# degree K, (-135 deg C)
X_max = 0.01		# Max allowable quality NEEDS TO BE VERIFIED BY EXPERIENCE OF DECAM

# Heat Loads
Q_camera = 540 		# watt, total camera power consumption, including contingency for heaters

L_pipe = 80			# Meters of vacuum insulated hose
L_hose = 30 		# Meters of vacuum insulated hose

loss_pipe = .452	# W/m, loss rate per unit length @ LN2 temps with 1.0" pipe. Ref: Technifab
loss_hose = .9		# W/m, estimate


Q_pipes =  loss_pipe*L_pipe
Q_hose =  loss_hose*L_hose

Q_valves = 25		# watt, Heat leak from valves throughout the system. Equal to value from DECAM
Q_pump = 150		# watt, 3X value from DECAM, assumes that we might need tripple the flow.



Q_net = Q_pipes + Q_hose + Q_camera + Q_pump + Q_valves
print "Q_net = ", '%.1f' % Q_net


# Compute the pressure drop from the maximum vertical rise in the system.
cam_height = 18.6	# meters, height difference from the utility room to the camera high spot
g = 9.81 			# m/s^2, gravity

	#Density of Nitrogen at 100K as a liquid.
rho = CP.Props('D','T', T_operation, 'Q', 0,"Nitrogen")

dP_head = rho*g*cam_height/1000	# kPa, static pressure head from util room to camera
print "Pressure drop from height of cam", dP_head

# Flow characeristics of system
A_flow = np.pi*D**2/4

	# Mean velocity of flow in the system
U_mean = m_dot/(A_flow*rho)	# m/s

	#Dynamic viscosity of saturated LN2 @ T_op
mu  = CP.Props('V','T', T_operation, 'Q', 0,"Nitrogen") # Pa-s


Re =  rho*U_mean*D/mu

	#Friction factor solver for internal flows

# Solving for friction factor for next Darcy Weisbach
def friction(Re,epsilon,diam):
	from scipy.optimize import fixed_point			
	def friction_funct(friction, Re, epsilon, diam):

		LHS = - 2.*np.log10(epsilon/(3.7*diam)+ 2.51/(Re*np.sqrt(friction)))
		return 1/LHS**2

	return fixed_point(friction_funct, 0.2, args=(Re,epsilon,diam))


# Solver for friction factor for arbitrary Reynolds number
def DarcyWeisbach(Re,epsilon,diam):
	if Re < 2100:
		friction_laminar = 64/Re
		return friction_laminar
	else:
		return friction(Re,epsilon,diam)

friction_pipe = DarcyWeisbach(Re,epsilon_pipe,D)
friction_hose = DarcyWeisbach(Re,epsilon_hose,D)

print friction_pipe

dP_flow_pipe = friction_pipe*L_pipe/D*rho*U_mean**2/2
dP_flow_hose = friction_hose*L_hose/D*rho*U_mean**2/2
print"Pressure drop from pipes is %.f" % dP_flow_pipe, " Pa"
print"Pressure drop from hoses is %.f" % dP_flow_hose, " Pa"

dP_pump = dP_flow_pipe+dP_flow_hose
print "Total flow pressure drop is %.f" % dP_pump, " Pa"


delta_height = 7.9		#meter, change in ht of camera
dP_head = rho*g*delta_height/1000	# kPa, static pressure head from util room to camera

p_top= CP.Props('P','T', T_operation, 'Q', 0,"Nitrogen") # Pa-s
print "Operating pressure", p_top
dT_movement = CP.Props('T','P', p_top, 'Q', 0,"Nitrogen")-CP.Props('T','P', (p_top-dP_head), 'Q', 0,"Nitrogen")  # Pa-s



print "dP movement", dP_head
print "Temperature shift from movement, degrees K", dT_movement
