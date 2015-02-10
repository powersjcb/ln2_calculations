import CoolProp
import CoolProp.CoolProp as CP
import numpy as np
from cryo_flow import flowLN as flowLN
import matplotlib.pyplot as plt
import scipy.optimize as op


	# start flow solver functions:

def friction(Re,epsilon,diam):
	from scipy.optimize import fixed_point			
	def friction_funct(friction, Re, epsilon, diam):

		LHS = - 2.*np.log10(epsilon/(3.7*diam) + 2.51/(Re*np.sqrt(friction)))
		return 1/LHS**2

	return fixed_point(friction_funct, 0.2, args=(Re,epsilon,diam))


# Solver for friction factor for arbitrary Reynolds number
def DarcyWeisbach(Re,epsilon,diam):
	if Re < 2100:
		friction_laminar = 64/Re
		return friction_laminar
	else:
		return friction(Re,epsilon,diam)

# end flow solver functions

def flow_rate(V_dot):
	#solving setup
	D = 0.020*.0254

	V_dot = float(V_dot)/(60*1000)				# m^3/s, guess
	P = (105+14.7)*6.89475729			# kPa, inlet pressure ref inlet P
	P_mean = (P-101.3)/2+101.3 			# kPa, mean pressure Ref P mean
	T = 22+273							# K, inlet temperature
	epsilon = .1*10**-6
	dX = 9*12*.0254


	rho   = CP.Props('D','P',P_mean,'T', T,"Nitrogen")				#density, kg/m^3

	# Flow characeristics of system
	A_flow = np.pi*D**2/4		# meters^2
	m_dot = rho*V_dot						# kg/s, mass flow rate

		# Mean velocity of flow in the system
	U_mean = m_dot/(A_flow*rho)	# meters/second

		#Dynamic viscosity of saturated LN2 @ T_op
	mu  = CP.Props('V','P',P_mean, 'T', T,"Nitrogen") # Pascal-second
	SoS  = CP.Props('A','P',P_mean, 'T', T,"Nitrogen") # m/s

	Re =  rho*U_mean*D/mu
	# print Re, "Re"

	friction = DarcyWeisbach(Re,epsilon,D)		#Friction factor for tubes


	P_flow = friction*dX/D*rho/2*(U_mean**2)/1000

	if SoS < U_mean:
		print "Error: choked flow."
	# else:
	print V_dot, " Volumetric flow rate"
	print "%.2f" % dX, "m, length of tube"
	print "%.3f" % rho, " kg/m^3, mean density"
	print mu, " Pa-s, dynamic viscosity"
	print "%.2f" % SoS, "speed of sound, m/s"
	print V_dot, "m^3/s, Volumetric flow rate"
	print "%.4f" % U_mean, " m/s"
	print "%.f" % Re, "Reynold's number"
	print "%.4f" % friction, " friction factor (Darcy Weisbach)"
	print "%.f" % P, "kPa, desired"
	print "%.f" % P_flow, "kPa flow p drop"

	residual =  P-P_flow
	# print P_flow, P
	# print residual
	return residual

res = op.root(flow_rate,x0=1.)
flow_rate(res.x)
print res.x, 'l/min'
