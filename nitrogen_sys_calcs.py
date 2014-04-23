# This document will contain the calculations for the Refrigerator system using LN2.


import CoolProp
import CoolProp.CoolProp as CP


# Defined Heat Loads
Q_camera = 540 		# watts, total camera power consumption, including contingency for heaters
T_operation = 100 	# degrees K, (-135 deg C)

X_max = 0.01		# Max allowable quality NEEDS TO BE VERIFIED BY EXPERIENCE OF DECAM


#Defined Mass Flow Data

m_dot = 300			# grams/second
D = .0334-.00377*2
print D			# meter, inside diameter of tubing



#Derived Heat Loads

L_pipe = 80			# Meters of vacuum insulated hose
L_hose = 30 		# Meters of vacuum insulated hose

loss_pipe = .452	# W/m, loss rate per unit length @ LN2 temps with 1.0" pipe. Ref: Technifab
loss_hose = .9		# W/m, estimate


Q_pipes =  loss_pipe*L_pipe
Q_hose =  loss_hose*L_hose

Q_valves = 25		# watts, Heat leak from valves throughout the system. Equal to value from DECAM
Q_pump = 150		# watts, 3X value from DECAM, assumes that we might need tripple the flow.



Q_net = Q_pipes + Q_hose + Q_camera + Q_pump + Q_valves
print "Q_net = ", '%.1f' % Q_net


# Compute the pressure drop from the maximum vertical rise in the system.
cam_height = 18.6	# meters, height difference from the utility room to the camera high spot
g = 9.81 			# m/s^2, gravity

#Density of Nitrogen at T_operation as a liquid.
rho = CP.Props('D','T', T_operation, 'Q', 0,"Nitrogen") 

dP_head = rho*g*cam_height/1000	# kPa, static pressure head from util room to camera

#Computing dynamics losses

# velocity = 

# Re = 


# def dP():
# 	dP = f_D*L/D*rho*V
# 	return dP
# # dP_flow_hose   = 
# # dP_flow_smooth = 

print "dP_head = " '%.1f' % dP_head



