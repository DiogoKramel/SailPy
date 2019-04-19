import numpy as np
from scipy import interpolate
import csv

def resistance(lwl, bwl, tc, alcb, cp, cm, awp, disp, lcb, lcf, vboat, heel):
    # coeficientes da serie de delft
    coeffDelf = [['FroudeNo' 'a0' 'a1' 'a2' 'a3' 'a4' 'a5' 'a6' 'a7' 'a8'], [0.10, -0.0014, 0.0403, 0.047, -0.0227, -0.0119, 0.0061, -0.0086, -0.0307, -0.0553], [0.15, 0.0004, -0.1808, 0.1793, -0.0004, 0.0097, 0.0118, -0.0055, 0.1721, -0.1728], [0.20, 0.0014, -0.1071, 0.0637, 0.009, 0.0153, 0.0011, 0.0012,0.1021, -0.0648], [0.25, 0.0027, 0.0463, -0.1263, 0.015, 0.0274, -0.0299, 0.011, -0.0595, 0.122], [0.30, 0.0056, -0.8005, 0.4891, 0.0269, 0.0519, -0.0313, 0.0292, 0.7314, -0.3619], [0.35, 0.0032, -0.1011, -0.0813, -0.0382, 0.032, -0.1481, 0.0837, 0.0233, 0.1587], [0.40, -0.0064, 2.3095, -1.5152, 0.0751, -0.0858, -0.5349, 0.1715, -2.455, 1.1865], [0.45, -0.0171, 3.4017, -1.9862, 0.3242, -0.145, -0.8043, 0.2952, -3.5284, 1.3575], [0.50, -0.0201, 7.1576, -6.3304, 0.5829, 0.163, -0.3966, 0.5023, -7.1579, 5.2534], [0.55, 0.0495, 1.5618, -6.0661, 0.8641, 1.1702, 1.761, 0.9176, -2.1191, 5.4281], [0.60, 0.0808, -5.3233, -1.1513, 0.9663, 1.6084, 2.7459, 0.8491, 4.7129, 1.1089]]
    coeffIncli = [['FroudeNo' 'u0' 'u1' 'u2' 'u3' 'u4' 'u5'], [0.25, -0.0268, -0.0014, -0.0057, 0.0016, -0.007, -0.0017], [0.30, 0.6628, -0.0632, -0.0699, 0.0069, 0.0459, -0.0004], [0.35, 1.6433, -0.2144, -0.164, 0.0199, -0.054, -0.0268], [0.40,-0.8659, -0.0354, 0.2226, 0.0188, -0.58, -0.1133], [0.45, -3.2715, 0.1372, 0.5547, 0.0268, -1.0064, 0.2026], [0.50, -0.1976, -0.148, -0.6593, 0.1862, -0.7489, -0.1648], [0.55, 1.5873, -0.3749, -0.7105, 0.2146, -0.4818, -0.1174]]
    coeffVisc = [['phi' 's0' 's1' 's2' 's3'], [5, -4.112, 0.054, -0.027, 6.329], [10, -4.522, -0.132, -0.077, 8.738], [15, -3.291, -0.389, -0.118, 8.949], [20, 1.85, -1.2, -0.109, 5.364], [25, 6.51, -2.305, -0.066, 3.443], [30, 12.334, -3.911, 0.024, 1.767], [35, 14.648, -5.182, 0.102, 3.497]] 

    # constantes fisicas
    rho = 1025          # water density [kg/m3]
    ni = 1e-6           # water kinematic viscosity [m2/s]
    grav = 9.80665      # gravity acceleration [m/s2]
    pi = np.pi			# pi

    # parametros essenciais do vpp
    leeway = np.radians(10)			# adopted by the author
    leeway = abs(leeway)
    heel = np.radians(heel)
    vboat = abs(vboat)
    alfaK = np.arcsin(np.sin(leeway)*np.cos(heel))
    Fn = vboat/(lwl*grav)**0.5
    
    # 1 RESISTENCIA VISCOSA
    Recb = (0.7*lwl*(vboat))/ni
    Cfcb = (0.075/((np.log(Recb)/np.log(10))-2)**2)-(1800/Recb)
    kcb = 0.09
    scb=(1.97+0.171*(bwl/tc))*((0.65/cm)**(1/3))*(disp*lwl)**0.5
    Rvcb = 0.5*rho*vboat**2*Cfcb*(1+kcb)*scb

    # 2 RESISTENCIA INDUZIDA
    Sfcb = 0.5*rho*(vboat**2)*(0.5*pi*tc**2+1.8*alcb*abs(alfaK))*alfaK
    AReCb = 2*tc/(0.75*lwl)
    Ri = (Sfcb/np.cos(heel))**2/(0.5*rho*vboat**2*alcb*pi*AReCb)

    # 3 RESITENCIA RESIDUAL
    vector_delf = np.zeros(9)         # delft series
    vector_incli = np.zeros(6)    	  # delta hull - inclinacao do casco
    vector_inclivisc = np.zeros(4)    # delta hull viscous
    # procura e interpola os coeficientes de Delft
    if Fn > 0.6:
        Fn1 = 0.6
    elif Fn < 0.1:
        Fn1 = 0.1
    else:
        Fn1 = Fn
    for k in range(1, 10, 1):
        if float(coeffDelf[k][0]) <= Fn1 and Fn1 <= float(coeffDelf[k + 1][0]):
            XX = [float(coeffDelf[k][0]), float(coeffDelf[k + 1][0])]
            for j in range(1, 10, 1):
                YY = [float(coeffDelf[k][j]), float(coeffDelf[k + 1][j])]
                vector_delf[j - 1] = interpolate.interp1d(XX, YY)(Fn1)

    if Fn > 0.55:
        Fn2 = 0.55
    if Fn < 0.25:
        Fn2 = 0.25
    else:
        Fn2 = Fn
    for k in range(1, 7, 1):
        if float(coeffIncli[k][0]) <= Fn2 and Fn2 <= float(coeffIncli[k + 1][0]):
            SS = [float(coeffIncli[k][0]), float(coeffIncli[k + 1][0])]
            for j in range(1, 7, 1):
                TT = [float(coeffIncli[k][j]), float(coeffIncli[k + 1][j])]
                vector_incli[j - 1] = interpolate.interp1d(SS, TT)(Fn2)
    vector_incli[:] = [x / 1000 for x in vector_incli]

    if (abs(heel)) > 0.35:
        heel2 = 0.35
    else:
        heel2 = abs(heel)
    heel2 = np.degrees(heel2)
    for k in range(1, 7, 1):
        if float(coeffVisc[k][0]) <= heel2 and heel2 <= float(coeffVisc[k + 1][0]):
            UU = [float(coeffVisc[k][0]), float(coeffVisc[k + 1][0])]
            for j in range(1, 5, 1):
                VV = [float(coeffVisc[k][j]), float(coeffVisc[k + 1][j])]
                vector_inclivisc[j - 1] = interpolate.interp1d(UU, VV)(heel2)

    # entrada LCB e contada pela secao central, preciso da conta da a partir da secao frontal
    LCBfpp = (lwl/2)-lcb
    LCFfpp = (lwl/2)-lcf
    Rr = disp*rho*grav*(vector_delf[0]+(vector_delf[1]*LCBfpp/lwl+vector_delf[2]*cp+vector_delf[3]*disp**(2/3)/awp+vector_delf[4]*bwl/lwl)*disp**(1/3)/lwl+(vector_delf[5]*disp**(2/3)/scb+vector_delf[6]*LCBfpp/LCFfpp+vector_delf[7]*(LCBfpp/lwl)**2+vector_delf[8]*cp**2)*disp**(1/3)/lwl)

    # Acrescimo da Resistencia residual devido a inclinacao
    if Fn2 < 0.25:
        Rincli20 = 0
    else:
        Rincli20 = disp*rho*grav*(vector_incli[0]+vector_incli[1]*lwl/bwl+vector_incli[2]*bwl/tc+vector_incli[3]*(bwl/tc)**2+vector_incli[4]*lcb+vector_incli[5]*lcb**2)
    Rincli = Rincli20*6*abs(heel)**1.7

    # Acrescimo da resistencia viscosa devido a inclinacao
    if abs(heel) < np.radians(5):
        Scbincl = scb
    else:
        Scbincl = scb*(1+1/100*(vector_inclivisc[0]+vector_inclivisc[1]*bwl/tc+vector_inclivisc[2]*(bwl/tc)**2+vector_inclivisc[3]*cm))
    Rvcb = 0.5*rho*vboat**2*Cfcb*(1+kcb)*Scbincl
    Rv = Rvcb

    # 4 RESISTENCIA TOTAL E CONFORTO
    Rt = abs(Rv)+abs(Ri)+abs(Rr)+abs(Rincli)
    loa = 11
    boa = bwl*1.2
    CR = disp*1025*2.20462/((boa*3.28084)**(4/3)*0.65*(0.7*lwl*3.28084+0.3*loa*3.28084))
    

    return Rt, Rv, Ri, Rr, Rincli, CR
