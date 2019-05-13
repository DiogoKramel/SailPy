import numpy as np
from scipy import interpolate
import csv

def resistance(lwl, bwl, tc, alcb, cp, cm, awp, disp, lcb, lcf, vboat, heel):
    # Delft coefficients
    coefficient_residual = [
        ['FroudeNo' 'a0' 'a1' 'a2' 'a3' 'a4' 'a5' 'a6' 'a7' 'a8'], 
        [0.10, -0.0014, 0.0403, 0.047, -0.0227, -0.0119, 0.0061, -0.0086, -0.0307, -0.0553], 
        [0.15, 0.0004, -0.1808, 0.1793, -0.0004, 0.0097, 0.0118, -0.0055, 0.1721, -0.1728], 
        [0.20, 0.0014, -0.1071, 0.0637, 0.009, 0.0153, 0.0011, 0.0012,0.1021, -0.0648], 
        [0.25, 0.0027, 0.0463, -0.1263, 0.015, 0.0274, -0.0299, 0.011, -0.0595, 0.122], 
        [0.30, 0.0056, -0.8005, 0.4891, 0.0269, 0.0519, -0.0313, 0.0292, 0.7314, -0.3619], 
        [0.35, 0.0032, -0.1011, -0.0813, -0.0382, 0.032, -0.1481, 0.0837, 0.0233, 0.1587], 
        [0.40, -0.0064, 2.3095, -1.5152, 0.0751, -0.0858, -0.5349, 0.1715, -2.455, 1.1865], 
        [0.45, -0.0171, 3.4017, -1.9862, 0.3242, -0.145, -0.8043, 0.2952, -3.5284, 1.3575], 
        [0.50, -0.0201, 7.1576, -6.3304, 0.5829, 0.163, -0.3966, 0.5023, -7.1579, 5.2534], 
        [0.55, 0.0495, 1.5618, -6.0661, 0.8641, 1.1702, 1.761, 0.9176, -2.1191, 5.4281], 
        [0.60, 0.0808, -5.3233, -1.1513, 0.9663, 1.6084, 2.7459, 0.8491, 4.7129, 1.1089]
    ]

    coefficient_residual_heel = [
        ['FroudeNo' 'u0' 'u1' 'u2' 'u3' 'u4' 'u5'], 
        [0.25, -0.0268, -0.0014, -0.0057, 0.0016, -0.007, -0.0017], 
        [0.30, 0.6628, -0.0632, -0.0699, 0.0069, 0.0459, -0.0004], 
        [0.35, 1.6433, -0.2144, -0.164, 0.0199, -0.054, -0.0268], 
        [0.40,-0.8659, -0.0354, 0.2226, 0.0188, -0.58, -0.1133], 
        [0.45, -3.2715, 0.1372, 0.5547, 0.0268, -1.0064, 0.2026], 
        [0.50, -0.1976, -0.148, -0.6593, 0.1862, -0.7489, -0.1648], 
        [0.55, 1.5873, -0.3749, -0.7105, 0.2146, -0.4818, -0.1174]
    ]

    coefficient_viscous_heel = [
        ['phi' 's0' 's1' 's2' 's3'], 
        [5, -4.112, 0.054, -0.027, 6.329], 
        [10, -4.522, -0.132, -0.077, 8.738], 
        [15, -3.291, -0.389, -0.118, 8.949], 
        [20, 1.85, -1.2, -0.109, 5.364], 
        [25, 6.51, -2.305, -0.066, 3.443], 
        [30, 12.334, -3.911, 0.024, 1.767], 
        [35, 14.648, -5.182, 0.102, 3.497]
    ] 

    # for a = 100 and wavelength/lwl = 1
    coefficient_addwave = [
        ['FroudeNo' 'a0' 'a1' 'a2' 'a3' 'a4' 'a5' 'a6' 'a7' 'a8' 'a9'], 
        [0.20, 0.135971706, -0.079712707, 0.011040044, -0.000512737, 0.00177368, -0.000207076, 0.000133095 , 0.252647483, -0.359794615, 0.14069324], 
        [0.25, 0.144740648, -0.087875806, 0.0121882, -0.000563218, 0.00256833, -0.00033302, 5.17839E-05, 0.223659113, -0.160193869, -0.073440481],  
        [0.30, 0.125369414, -0.092281743, 0.012800398, -0.000592109, 0.00119098, -0.000139619, 8.14003E-05, 0.357822779, -0.327040392, -0.020221069], 
        [0.35, 0.139011133, -0.108178384, 0.01491584, -0.000692116, 0.004351508, -0.000336362, 0.000360906, 0.319067432, -0.031271366, -0.332228687], 
        [0.40, 0.125891281, -0.120856359, 0.01672588, -0.0007783, 0.003887939, -0.000272325, 0.00038914, 0.481253166, -0.176587773, -0.344081072], 
        [0.45, 0.139240049, -0.142907914, 0.019939832, -0.000934437, 0.006308615, -0.000543945, 0.000457244, 0.578174665, -0.22452672, -0.390073693]
    ], 

    # Physical constants
    rho = 1025          # Water density [kg/m3]
    ni = 1e-6           # Water kinematic viscosity [m2/s]
    grav = 9.80665      # Gravity acceleration [m/s2]
    
    # Basic parameters
    heel = np.radians(heel)         # Heel angle [rad]
    Fn = vboat/(lwl*grav)**0.5      # Froude [-]
    k_form = 0.09                   # Coefficient form [-] original value from VPPUSP
    kg = 0.5                        # Estimative of centre of gravity [m]
    cb = disp/(lwl*bwl*tc)          # Block coefficient [-]
    cwp = awp/(lwl*bwl)             # Waterplane coefficient [-]
    loa = lwl*1.05                  # Estimation adopted for overall lenght [m]
    boa = bwl*1.15                  # Estimation adopted for maximmum beam [m]
    
    # 1 RESISTANCE
    # 1.1 Viscous Resistance
    Re = (0.7*lwl*(vboat))/ni                                         # Reynolds [-]
    Cf = (0.075/((np.log(Re)/np.log(10))-2)**2)-(1800/Re)             # Friction Coefficient
    Scb = (1.97+0.171*(bwl/tc))*((0.65/cm)**(1/3))*(disp*lwl)**0.5    # Estimation for the canoe body surface area [m2]
    Rv = 0.5*rho*vboat**2*Cf*(1+k_form)*Scb

    # 1.2 Residual resistance
    # vector with delft series coefficients
    vector_residual = np.zeros(9)
    if Fn > 0.6:
        Fn_temp = 0.6
    elif Fn < 0.1:
        Fn_temp = 0.1
    else:
        Fn_temp = Fn
    for k in range(1, 10, 1):
        if float(coefficient_residual[k][0]) <= Fn_temp and Fn_temp <= float(coefficient_residual[k + 1][0]):
            AA = [float(coefficient_residual[k][0]), float(coefficient_residual[k + 1][0])]
            for j in range(1, 10, 1):
                BB = [float(coefficient_residual[k][j]), float(coefficient_residual[k + 1][j])]
                vector_residual[j - 1] = interpolate.interp1d(AA, BB)(Fn_temp)
    # LCB and LCF measured from midsection 
    LCBfpp = (lwl/2)-lcb
    LCFfpp = (lwl/2)-lcf
    Rr = disp*rho*grav*(vector_residual[0] + (vector_residual[1]*LCBfpp/lwl + vector_residual[2]*cp + vector_residual[3]*disp**(2/3)/awp + vector_residual[4]*bwl/lwl)*disp**(1/3)/lwl + (vector_residual[5]*disp**(2/3)/Scb + vector_residual[6]*LCBfpp/LCFfpp + vector_residual[7]*(LCBfpp/lwl)**2 + vector_residual[8]*cp**2)*disp**(1/3)/lwl)
    
    # 1.3 Resistance due to heel
    # 1.3.1 Viscous additional resistance due to hee
    # vector with delft series coefficients
    vector_heel_viscous = np.zeros(4)
    heel_temp = np.degrees(heel)
    if heel_temp > 35:
        heel_temp = 35
    for k in range(1, 7, 1):
        if float(coefficient_viscous_heel[k][0]) <= heel_temp and heel_temp <= float(coefficient_viscous_heel[k + 1][0]):
            CC = [float(coefficient_viscous_heel[k][0]), float(coefficient_viscous_heel[k + 1][0])]
            for j in range(1, 5, 1):
                DD = [float(coefficient_viscous_heel[k][j]), float(coefficient_viscous_heel[k + 1][j])]
                vector_heel_viscous[j - 1] = interpolate.interp1d(CC, DD)(heel_temp)
    if heel_temp < 5:
        Rv_heel = 0
    else:
        Scbincl = Scb*(1+1/100*(vector_heel_viscous[0]+vector_heel_viscous[1]*bwl/tc+vector_heel_viscous[2]*(bwl/tc)**2+vector_heel_viscous[3]*cm))
        Rv_heel = 0.5*rho*vboat**2*Cf*(1+k_form)*Scbincl - Rv

    # 1.3.2 Residual additional resistance due to heel
    # vector with delft series coefficients
    vector_heel_residual = np.zeros(6)
    if Fn > 0.55:
        Fn_temp = 0.55
    if Fn < 0.25:
        Fn_temp = 0.25
    else:
        Fn_temp = Fn
    for k in range(1, 7, 1):
        if float(coefficient_residual_heel[k][0]) <= Fn_temp and Fn_temp <= float(coefficient_residual_heel[k + 1][0]):
            EE = [float(coefficient_residual_heel[k][0]), float(coefficient_residual_heel[k + 1][0])]
            for j in range(1, 7, 1):
                FF = [float(coefficient_residual_heel[k][j]), float(coefficient_residual_heel[k + 1][j])]
                vector_heel_residual[j - 1] = interpolate.interp1d(EE, FF)(Fn_temp)
    vector_heel_residual[:] = [x / 1000 for x in vector_heel_residual]
    if Fn_temp < 0.25:
        Rr_heel = 0
    else:
        Rr_heel_20 = disp*rho*grav*(vector_heel_residual[0]+vector_heel_residual[1]*lwl/bwl+vector_heel_residual[2]*bwl/tc+vector_heel_residual[3]*(bwl/tc)**2+vector_heel_residual[4]*lcb+vector_heel_residual[5]*lcb**2)
        Rr_heel = Rr_heel_20*6*abs(heel)**1.7
    
    # 1.3.3 Total resistance due to heel
    Rheel = Rv_heel + Rr_heel

    # 1.4 Added resistance in waves
    # vector with delft series coefficients
    vector_addwave = np.zeros(10)
    if Fn > 0.45:
        Fn_temp = 0.45
    if Fn < 0.20:
        Fn_temp = 0.20
    else:
        Fn_temp = Fn
    for k in range(1, 7, 1):
        if float(coefficient_addwave[k][0]) <= Fn_temp and Fn_temp <= float(coefficient_addwave[k + 1][0]):
            GG = [float(coefficient_addwave[k][0]), float(coefficient_addwave[k + 1][0])]
            for j in range(1, 11, 1):
                HH = [float(coefficient_addwave[k][j]), float(coefficient_addwave[k + 1][j])]
                vector_addwave[j - 1] = interpolate.interp1d(GG, HH)(Fn_temp)
    vector_addwave[:] = [x / 1000 for x in vector_addwave]
    if Fn_temp < 0.25:
        Raw = 0
    else:
        Raw = vector_addwave[0]+vector_addwave[1]*(lwl/disp**(1/3)) + vector_addwave[2]*(lwl/disp**(1/3))**2 + vector_addwave[3]*(lwl/disp**(1/3))**3 + vector_addwave[4]*(lwl/bwl) + vector_addwave[5]*(lwl/bwl)**2 + vector_addwave[6]*(bwl/tc) + vector_addwave[7]*cp + vector_addwave[8]*cp**2 + vector_addwave[9]*cp**3 

    # 1.5 TOTAL RESISTANCE
    Rt = abs(Rv)+abs(Rr)+abs(Rheel)+abs(Raw)

    # 2 STABILITY
    # OOSSANEN, P. van. A concept exploration model for sailing yachts. Transactions of RINA, p. 17–28, 2003.
    # coefficients b0 and b1 built as fitting polynomials from the plot provided in the paper above
    GZ = np.zeros(19)
    heel_calc = np.zeros(19)
    for i in range (2,17):
        heel_calc[i] = i*5
        b0 = 8*10**(-10)*heel_calc[i]**4 - 3*10**(-7)*heel_calc[i]**3 + 4*10**(-5)*heel_calc[i]**2 - 0.002*heel_calc[i] + 0.0754
        b1 = 5*10**(-12)*heel_calc[i]**5 - 4*10**(-9)*heel_calc[i]**4 + 9*10**(-7)*heel_calc[i]**3 + 9*10**(-5)*heel_calc[i]**2 + 0.0038*heel_calc[i] + 0.0153
        c1 = b0 + b1*(boa/bwl)**2*(tc/bwl)/cb
        bm = c1*bwl**2/tc
        kb = tc*(5/6-cb/(3*cwp))    # WILSON, P. A. Basic Naval Architecture. Springer, 2017
        GZ[i] = (kb + bm - kg)*np.sin(heel_calc)
    GZ[1] = GZ[2]/2                 # GZ at 10 deg is half of GZ at 20 deg
    GZ[17] = GZ[16]/2               # GZ at 170 deg is half of GZ at 160 deg
    
    GZmax = max(GZ)
    # Angle of Vanishing Stability 
    for i in range (2,17):
        if GZ[i] < 0 and GZ[i-1] > 0:
            AVS = (heel_calc[i]*GZ[i-1]+heel_calc[i-1]*GZ[i])/(GZ[i]+GZ[i-1])

    # 3 MOTION COMFORT RATIO
    # BREWER, E. S. Ted Brewer Explains Sailboat Design. International Marine Publishing Company, 1985
    CR = disp*1025*2.20462/((boa*3.28084)**(4/3)*0.65*(0.7*lwl*3.28084+0.3*loa*3.28084))

    # 4 VERTICAL ACCELERATION
    # MARCHAJ, C. A. Sailing Theory and Practice. Dodd, Mead & Company, 1964
    RA = (6.28/tc)**2*(boa-1.5)*(10*np.pi)/(180*32.2)


    return Rt, Rv, Rr, Rheel, Raw, GZmax, AVS, CR, RA, Rv_heel, Rr_heel
