# This document contains calculations for the Refrigerator system using LN2.


import CoolProp
import CoolProp.CoolProp as CP
import numpy as np
from cryo_flow import flowLN as flowLN


#Physical Parameters
P_pump = 400				# kPa
m_dot  = 1				# mass flow rate, DECAM
X_0    = 0.0 				# Initial quality, pure liquid
D =.0254 	#meter, Hydraulic diameter of 1.0" pipe/hose
epsilon_pipe = 0.0001		# meter, surface roughness of piping
epsilon_hose = 0.00635		# meter, referenced from Swagelok convoluted flex hoses

pipe_loss = .452			# watts/meter of 1" VJ pipe
hose_loss = pipe_loss*2 	# watts/meter of 1" VJ hose


# Segments of Cryogenics Plumbing
theta = 0.			#radians, rotational anglual distance from horizon pointing


# Utilities room to maypole, Fixed
dzRigid1 = 0.
dxRigid1 = 10.0
heat_leak1 = 0.0
args = [P_pump, m_dot, X_0, D, epsilon_pipe, dxRigid1, dzRigid1, pipe_loss, heat_leak1]
P_out, X_out, Q_net, T_in, T_out = flowLN(args)
print X_out

# Maypole flex hose, (z fixed)
dzFlex1 = 6.3
dxFlex1 = 16.0

# Rigid Lines to altitude articulation, (z fixed)
dzRigid2 = 7.6
dxRigid2 = 15.0

# Altitude flex hose, (z movement of outlet)
radius_art = 46.0*.0254	
dzFlex2 = np.sin(theta)*radius_art
dxFlex2 = 9.75

# Rigid to camera polar axis, (z moves with altitude pointing)
radius_polar = 7.8
dzRigid3 = np.sin(theta)*radius_polar
dxRigid3 = 10.0

# Zenith rotation axis flex lines, (z moves with altitude pointing, zenith has negligible effect)
dzFlex3 = 0.0
dxFlex3 = 4.25

# Camera heat exchanger, (z moves with altitude pointing)
camera_length = 4			#meter, length with tubing
dzRigid4 = -np.sin(theta)*camera_length
dxRigid4 = camera_length


