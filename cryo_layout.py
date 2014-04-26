# This document contains calculations for the Refrigerator system using LN2.


import CoolProp
import CoolProp.CoolProp as CP
import numpy as np
from cryo_flow import flowLN as flowLN
import matplotlib.pyplot as plt


#Physical Parameters
P_pump = 500				# kPa
m_dot  = .4				# mass flow rate, DECAM
X_0    = 0.00 				# Initial quality, pure liquid
D =.030 	#meter, Hydraulic diameter of 1.0" pipe/hose
epsilon_pipe = 0.0001		# meter, surface roughness of piping
epsilon_hose = 0.00635		# meter, referenced from Swagelok convoluted flex hoses

pipe_loss = .452			# watts/meter of 1" VJ pipe
hose_loss = pipe_loss*2 	# watts/meter of 1" VJ hose


# Segments of Cryogenics Plumbing
theta = 0.			#radians, rotational anglual distance from horizon pointing

P_out = []
X_out = []
Q_net = []
T_in  = []
T_out = []
distance=[]
d=0

#1 Utilities room to maypole, Fixed
dzRigid1 = 0.
dxRigid1 = 10.0
heat_leak1 = 0.0

#2 Maypole flex hose, (z fixed)
dzFlex1 = 6.3
dxFlex1 = 16.0
heat_leak2 = 0.0

#3 Rigid Lines to altitude articulation, (z fixed)
dzRigid2 = 7.6
dxRigid2 = 15.0
heat_leak3 = 0.0

#4 Altitude flex hose, (z movement of outlet)
radius_art = 46.0*.0254	
dzFlex2 = np.sin(theta)*radius_art
dxFlex2 = 9.75
heat_leak4 = 0.0

#5 Rigid to camera polar axis, (z moves with altitude pointing)
radius_polar = 7.8
dzRigid3 = np.sin(theta)*radius_polar
dxRigid3 = 10.0
heat_leak5 = 0.0

#6 Zenith rotation axis flex lines, (z moves with altitude pointing, zenith has negligible effect)
dzFlex3 = 0.0
dxFlex3 = 4.25
heat_leak6 = 0.0

#7 Camera heat exchanger, (z moves with altitude pointing)
camera_length = 4			#meter, length with tubing
dzRigid4 = -np.sin(theta)*camera_length
dxRigid4 = camera_length
heat_leak7 = 550

# tabulating variables
epsilon = [epsilon_pipe,epsilon_hose,epsilon_pipe,epsilon_hose,epsilon_pipe,epsilon_hose,epsilon_pipe,
	epsilon_hose,epsilon_pipe,epsilon_hose,epsilon_pipe,epsilon_hose,epsilon_pipe]

dX = [dxRigid1,dxFlex1,dxRigid2,dxFlex2,dxRigid3,dxFlex3,dxRigid4,
	dxFlex3,dxRigid3,dxFlex2,dxRigid2,dxFlex1,dxRigid1]


dZ = [dzRigid1,dzFlex1,dzRigid2,dzFlex2,dzRigid3,dzFlex3,dzRigid4,
	-dzFlex3,-dzRigid3,-dzFlex2,-dzRigid2,-dzFlex1,-dzRigid1]


loss = [pipe_loss,hose_loss,pipe_loss,hose_loss,pipe_loss,hose_loss,pipe_loss,
		hose_loss,pipe_loss,hose_loss,pipe_loss,hose_loss,pipe_loss]
heat_leak = [heat_leak1,heat_leak2,heat_leak3,heat_leak4,heat_leak5,heat_leak6,heat_leak7,
		heat_leak6,heat_leak5,heat_leak4,heat_leak3,heat_leak2,heat_leak1]


print "epsilon", epsilon
print "dX", dX
print "dZ", dZ
print "loss", loss
print "heat_leak", heat_leak


for i in range(0,12):
	if i==0:
		args = [P_pump, m_dot, X_0, D, epsilon[i], dX[i], dZ[i], loss[i], heat_leak[i]]
	else:
		args = [P, m_dot, X, D, epsilon[i], dX[i], dZ[i], loss[i], heat_leak[i]]

	P,X,Q,Ti,To = flowLN(args)

	d = dX[i]+d
	distance.append(d)
	P_out.append(P)
	X_out.append(X)
	Q_net.append(Q)
	T_in.append(Ti)
	T_out.append(To)

	# print i+1, "i"
print P_out, "kPa"
print X_out
print T_in
print T_out

#plotting

fig,ax1 = plt.subplots()

ax2 = ax1.twinx()
ax3 = ax1.twinx()
ax3.set_frame_on(True)
ax3.patch.set_visible(False)

fig.subplots_adjust(right=0.75)

ax1.plot(distance,X_out,color='Green')
ax1.set_ylabel("X, Vapor Quality")
ax1.set_xlabel("Length of plumbing, meters")


ax2.plot(distance,P_out,color='Blue')
ax2.set_ylabel("Pressure, kPa")


ax3.plot(distance,T_out,color='Red')
ax3.spines['right'].set_position(('axes', 1.2))
ax3.set_ylabel("Temperature, Kelvin")
plt.title("Flow characteristics with mass flow of %.2f kg/s" % m_dot)

plt.show()

