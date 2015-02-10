# This document contains 1-D calculations for the Refrigerator system using HFE 7100.
import CoolProp
import CoolProp.CoolProp as CP
import numpy as np
from scipy.optimize import fixed_point


#Physical Parameters

D =.0254 	#meter, Hydraulic diameter of 1.0" pipe/hose
DC = 0.0254*(.5-.025*2)	#meter, diameter of tubing in cryoplate
epsilon_pipe = 0.0001		# meter, surface roughness of piping
epsilon_hose = 0.00635		# meter, referenced from Swagelok convoluted flex hoses


#Flow Parameters

m_dot = .6		# kg/second, NEEDS TO BE OPTIMIZED

#T_operation = 193.15 	# degree K

# Heat Loads
Q_camera = 540 		# watt, total camera power consumption, including contingency for heaters

L_pipe = 80*2		# Meters of vacuum insulated hose
L_hose = 30*2 		# Meters of vacuum insulated hose
L_cryoplate = 8.0 		# length of tubing in cryoplate

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

	#Density of HFE at 1atm as liquid
rho = 1825 #CP.Props('D','T', T_operation, 'P', 101.3, "HFE") #kg/m^3, density 

dP_head = rho*g*cam_height	# kPa, static pressure head from util room to camera
# Flow characeristics of system
A_flow = np.pi*D**2/4
A_flowC = np.pi*DC**2/4

	# Mean velocity of flow in the system
U_mean = m_dot/(A_flow*rho)	# m/s
U_meanC = m_dot/(A_flowC*rho)


#Dynamic viscosity
nu = 20*10**-6
mu = nu*rho #CP.Props('V','T', T_operation, 'P', 101.3,"HFE") # Pa-s


Re =  rho*U_mean*D/mu  # Reynolds number for pipes/hoses
Re_cryo = rho*U_meanC*DC/mu

# Friction factor solver for internal flows
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
friction_cryoplate = DarcyWeisbach(Re_cryo, epsilon_pipe,DC)

dP_flow_pipe = friction_pipe*L_pipe/D*rho*U_mean**2/2
dP_flow_hose = friction_hose*L_hose/D*rho*U_mean**2/2
dP_cryoplate = friction_cryoplate*L_cryoplate/D*rho*U_meanC**2/2
dP_pump = dP_flow_pipe+dP_flow_hose+dP_head+dP_cryoplate

#dP_head = rho*g*delta_height/1000	# kPa, static pressure head from util room to camera

#print "Operating pressure", p_top
#dT_movement = CP.Props('T','P', p_top, 'Q', 0,"HFE")-CP.Props('T','P', (p_top-dP_head), 'Q', 0,"HFE")  # Pa-s

#specific heat
cp=950 		# j/(kg*K)

#print "dP movement", dP_head
#print "Temperature shift from movement, degrees K", dT_movement
print 'Dynamic viscosity of HFE-7100 is %.6f' % mu, 'Pa-s'
print "Mass flow of %.1f" % m_dot, 'kg/s with flow diameter of %.2f' % (D*1000), 'mm' 
print "Pressure drop from height of camera is %.f" % dP_head, 'kPa'
print"Pressure drop from pipes is %.f" % dP_flow_pipe, " Pa"
print"Pressure drop from hoses is %.f" % dP_flow_hose, " Pa"
print "Total flow pressure drop is %.f" % dP_pump, " Pa"
print "Total flow pressure drop is %.f" % (dP_pump/101300*14.5), " psi"
print 'dT across camera: %.3f' % (Q_camera/(m_dot*cp)), 'C'
print 'dT across system: %.3f' % (Q_net/(m_dot*cp)), 'C'


print U_mean

## Results
# Q_net =  841.3
# Mass flow of 0.6 kg/s with flow diameter of 25.40 mm
# Pressure drop from height of camera is 300150 kPa
# Pressure drop from pipes is 92228  Pa
# Pressure drop from hoses is 184601  Pa
# Total flow pressure drop is 687315  Pa
# Total flow pressure drop is 98  psi
# dT across camera: 0.947 C
# dT across system: 1.476 C
# [Finished in 1.1s]

