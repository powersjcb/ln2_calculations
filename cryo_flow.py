# This file is a function for computing flows of liquid Nitrogen.

# args = [500,.4,.005,.0254,.0001,30,1,0.2,0]

def flowLN(args):

	import CoolProp
	import CoolProp.CoolProp as CP
	import numpy as np


	if len(args)!=9:
		print "INCORRECT NUMBER OF ARGUMENTS"
	#Inputs
	P = args[0]					# kPa, pressure inlet
	m_dot = args[1]				# kg/s, mass flow
	X = args[2]					# quality
	D = args[3]					# meter, diameter of tubing
	epsilon = args[4]			# 
	dX = args[5]				# meter, length of tubing
	dZ = args[6]				# meter, height difference of tubing
	loss_per_lg = args[7]		# watts/m, loss per length tubing
	heat_in = args[8]			# watts, misc loss or loads

	# Constants
	g = 9.81 			# m/s^2, gravity


	# start flow solver functions:

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

	# end flow solver functions




	# CoolProp @ input
	T_in 	= CP.Props('T','P',P,'Q', X,"Nitrogen")				#Temp, Kelvin
	rho 	= CP.Props('D','P',P,'Q', X,"Nitrogen")				#density, kg/m^3
	H 		= CP.Props('H','P',P,'Q', X,"Nitrogen")				#inlet enthalpy, kJ/kg
	# print T_in, "T_in"
	# print rho, "Rho"
	# print H, "H"

	# Start solving for variables

	Q_net =	dX*loss_per_lg + heat_in 				# watts, total loss 

		# Flow characeristics of system
	A_flow = np.pi*D**2/4		# meters^2

		# Mean velocity of flow in the system
	U_mean = m_dot/(A_flow*rho)	# meters/second

		#Dynamic viscosity of saturated LN2 @ T_op
	mu  = CP.Props('V','P',P, 'Q', X,"Nitrogen") # Pascal-second

	Re =  rho*U_mean*D/mu
	# print Re, "Re"

	friction = DarcyWeisbach(Re,epsilon,D)		#Friction factor for tubes
	P_head = rho*g*dZ/1000	# Pa, static pressure head from util room to camera
	P_flow = friction*dX/(D*2)*rho*U_mean**2/1000
	P_out = (P - P_flow - P_head)			#kPa


	# print friction, "f"
	# print P_flow, "dynamic pressure"
	# print P_head, "static pressure"
	# print P_out, "pressure out"


	H_isenthalpic = CP.Props('H','P',P_out, 'Q', X,"Nitrogen") # isenthalpic expansion
	T_isenthalpic = CP.Props('T','P',P_out, 'Q', X,"Nitrogen") # isenthalpic expansion
	# print T_in, "T_in"
	# print T_isenthalpic, "T_isenthalpic"

	H_out = H_isenthalpic + Q_net/(m_dot)/1000	#outlet enthalpy, kJ/kg. 


	X_out = CP.Props('Q','P',P_out, 'H', H_out,"Nitrogen") # isobaric heating
	T_out = CP.Props('T','P',P_out, 'H', H_out,"Nitrogen") # isenthalpic expansion



	# print Q_net, "Q_net"
	# print H
	# print H_isenthalpic, "Enthalpy isochoric"
	# print H_out, "Enthalpy out"
	# print X, "inlet quality"
	# print X_out, "outlet quality"
	# print T_out, "T_out"




	return P_out, X_out, Q_net, T_in, T_out
