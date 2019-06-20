'''
-------------------------
SETUP THE MODEL
-------------------------
A) Environmental parameters
B) True wind angle and velocity range 
C) Initial guess for solving the VPP
D) Delft coefficients for resistance estimation
E) Derivated elementary dimensions

-------------------------
VPP MAIN ROUTINE
-------------------------
1 PRE-CALCULATION

2 LIFT FORCES AND MOMENTS
  A) Keel lift force
  B) Bulb lift force
  C) Rudder lift force
  D) Canoe body side force
  E) GZ estimation
  F) Righting Moment
  G) Munk moment
  H) Centre of Effort (CE)

3 RESISTANCE CALCULATION
3.1 Viscous Resistance
  A) Parameters 
  B) Canoe body resistance 
  C) Keel and bulb resistance
  D) Rudder resistance
  E) Total viscous resistance
3.2 Residual Resistance
  A) Canoe body resitance
  B) Keel residual resistance
  C) Total residual resistance
3.3 Induced resistance
  A) Canoe body induced resistance
  B) Keel induced resistance
  C) Rudder induced resistance
  D) Total induced resistance
3.4 Resistance increase due to heel
  A) Canoe body viscous resistance
  B) Canoe body residual resistance
  C) Keel residual resistance
  D) Total heel resistance
3.5 Added resistance in waves
3.6 Total resistance

4) AERODYNAMIC MODELING
4.1) Sail area and centre of effort
  A) Main sail
  B) Jib and foretriangle
  C) Spinnaker
  D) Mizzen
  E) Nominal area
  F) Centre of effort above deck line
4.2) Lift and drag coefficients for each sail
  A) Main sail
  B) Jib sail
  C) Spinnaker
  D) Mast drag coefficient
  E) Lift and drag for all sails combined
4.3) Lift and drag forces and centre of efforts

5 FORCES AND MOMENTS IN GLOBAL COORDINATES [X, Y, Z]
5.1 Coordinates matrix
  A) Leeway
  B) Heel angle
  C) Keel angle attack due to heel
  D) Rudder angle due to heel
  E) Rudder angle attack due to rudder angle
  F) Rudder angle attack due to rudder with no lift
  G) Sail angle attack due to heel
5.2 Forces
  A) Total resistance
  B) Lift force keel
  C) Lift force rudder
  D) Lift force rudder for delta = 0
  E) Bulb side force
  F) Canoe body side force
  G) Sail lift force
  H) Sail drag force 
5.3 Centre of effort
  A) Aerodynamic CE
  B) Hydrodynamic CE
  C) Rudder hydrodynamic CE
5.4 Moments
  A) Munk Moment
  B) Righting Moment
  C) Aerodrynamic moment
  D) Hydrodynamic moment
  E) Rudder moment
5.5 Resulting forces and moments
5.6 Equilibrium system to be solved

-------------------------
NOMENCLATURE & ACRONYMS
-------------------------
- Variables' name are composed of "attribute" + "_" + "object", e.g. velocity_boat, angle_rudder
- Dimensions are given in radians and meters per second, otherwise a suffix will be added, e.g. angle_tw_deg

tw: true wind
aw: apparent wind
cb: canoe body
deg: degrees
temp: temporary
avg: average

-------------------------
REFERENCES
-------------------------
Gerritsma, J. Sailing yacht performance in calm water and in waves. The 11th Chesapeake Sailing Yacht Symposium SNAME, Jan. 1993.
Keuning, J. A., and U. B. Sonnenberg. Approximation of the hydrodynamic forces on a sailing yacht based on the 'Delft Systematic Yacht Hull Series'. Delft University of Technology, Faculty of Mechanical Engineering and Marine Technology, Ship Hydromechanics Laboratory, 1998.
Keuning, J. A., K. J. Vermeulen, and H. P. ten Have. An approximation Method for the added resistance in waves of a sailing yacht. 2 nd International Symposium on Design and Production of Motor and Sailing Yachts MDY ‘06, Madrid, Spain. 2006.
Oossanen, P. van. Predicting the speed of sailing yachts, 1993.
Oossanen, P. van. A concept exploration model for sailing yachts. Transactions of RINA, p. 17–28, 2003.
Wilson, Philip A. Basic Naval Architecture: Ship Stability. Springer, 2018.

'''


### IMPORT PACKAGES
import numpy as np                          # high-level mathematical functions
from scipy import optimize                  # optimization functions to solve the VPP's system of equations
from scipy import interpolate               # interpolatation methods applied to obtain the Delft coefficients
import csv                                  # export the results as CSV
import codecs, json                         # export the results as JSON
import re, os, os.path                      # uxiliary package to build the JSON files                       
from _ctypes import PyObj_FromPtr           # see https://stackoverflow.com/a/15012814/355230


def vpp_solve(sailset, loa, lwl, boa, bwl, tc, lcb, lcf, cb, cm, cp, cwp, lat_surface_cb, KG, free_board, lead_rudder, lead_sail, \
    mass_crew, height_mainsail, base_mainsail, height_foretriangle, base_foretriangle, boom_heigth_deck, length_spinnaker, \
    perpendicular_jib, span_rudder, tip_chord_rudder, root_chord_rudder, tip_thickness_rudder, root_thickness_rudder, \
    sweep_rudder_deg, span_keel, tip_chord_keel, root_chord_keel, tip_thickness_keel, root_thickness_keel, sweep_keel_deg, \
    naca_keel, naca_rudder, height_mast, diameter_mast, height_surface_rudder, height_mizzen, base_mizzen, boom_height_mizzen, \
    chord_bulb_keel, diameter_bulb, surface_area_bulb, minimum_tw_knots, maximum_tw_knots): 
    

    ### SETUP THE MODEL
    # A) Environmental parameters
    density_air = 1.3           # air density [kg/m3]
    density_water = 1025        # water density [kg/m3]
    viscosity_water = 1e-6      # water kynematic viscosity [m2/s]
    gravity = 9.80665           # gravity acceleration [m/s2]

    # B) True wind angle and velocity range 
    pi = np.pi                                       # pi number
    step_angle = 5                                   # true wind angle step [degrees] 
    step_velocity = 1.02889                          # true wind speed step [m/s] equivalent to 2 knots 
    minimum_tw = minimum_tw_knots*0.514444           # true wind speed range [m/s]
    maximum_tw = maximum_tw_knots*0.514444
    if (maximum_tw - minimum_tw) < step_velocity:    # in case the range of wind speed is lower than its step
        step_velocity = (maximum_tw - minimum_tw)*0.99

    # Arrays for true wind angle and velocity 
    angle_tw_deg = np.arange(30, 181, step_angle)    # polar diagram ranging from 30 to 180 degrees
    angle_tw = np.radians(angle_tw_deg)
    velocity_tw = np.arange(minimum_tw, maximum_tw, step_velocity)
    
    # Matrix to store the boat velocity for each true wind angle and speed
    angle_tw_matrix = np.zeros((np.size(velocity_tw), np.size(angle_tw_deg)))
    velocity_boat_matrix = np.zeros((np.size(velocity_tw), np.size(angle_tw_deg)))
    vmg_matrix = np.zeros((np.size(velocity_tw), np.size(angle_tw_deg)))

    # C) Initial guess for solving the VPP 
    # Velocity [m/s], leeway [rad], heel [rad], rudder angle [rad])
    initial_guess = np.array([4, np.radians(5), np.radians(15) ,np.radians(-4)])
 
    # D) Delft coefficients for resistance estimation (Keuning et al, 1998)
    # Residual resistance - bare hull
    coefficient_residual_hull = [
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
    # Residual resistance - keel
    coefficient_residual_keel = [
        ['FroudeNo' 'A0' 'A1' 'A2' 'A3'], 
        [0.2, -0.00104, 0.00172, 0.00117, -0.00008], 
        [0.25, -0.0055, 0.00597, 0.0039, -0.00009], 
        [0.3, -0.0111, 0.01421, 0.00069, 0.00021], 
        [0.35, -0.00713, 0.02632, -0.00232, 0.00039], 
        [0.4, -0.03581, 0.08649, 0.00999, 0.00017], 
        [0.45, -0.0047, 0.11592, -0.00064, 0.00035], 
        [0.5, 0.00553, 0.07371, 0.05991, -0.00114], 
        [0.55, 0.04822, 0.0066, 0.07048, -0.00035], 
        [0.6, 0.01021, 0.14173, 0.06409, -0.00192]
    ]
    # Residual resistance increase due to heel
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
    # Viscous resistance increase due to heel
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
    # Added resistance in waves for a = 100 and wavelength/lwl = 1
    coefficient_waves = [
        ['FroudeNo' 'a0' 'a1' 'a2' 'a3' 'a4' 'a5' 'a6' 'a7' 'a8' 'a9'], 
        [0.20, 0.135971706, -0.079712707, 0.011040044, -0.000512737, 0.00177368, -0.000207076, 0.000133095 , 0.252647483, -0.359794615, 0.14069324], 
        [0.25, 0.144740648, -0.087875806, 0.0121882, -0.000563218, 0.00256833, -0.00033302, 5.17839E-05, 0.223659113, -0.160193869, -0.073440481],  
        [0.30, 0.125369414, -0.092281743, 0.012800398, -0.000592109, 0.00119098, -0.000139619, 8.14003E-05, 0.357822779, -0.327040392, -0.020221069], 
        [0.35, 0.139011133, -0.108178384, 0.01491584, -0.000692116, 0.004351508, -0.000336362, 0.000360906, 0.319067432, -0.031271366, -0.332228687], 
        [0.40, 0.125891281, -0.120856359, 0.01672588, -0.0007783, 0.003887939, -0.000272325, 0.00038914, 0.481253166, -0.176587773, -0.344081072], 
        [0.45, 0.139240049, -0.142907914, 0.019939832, -0.000934437, 0.006308615, -0.000543945, 0.000457244, 0.578174665, -0.22452672, -0.390073693]
    ]

    # E) Derivated elementary dimensions
    # Displacement [m3]
    disp = cb*lwl*bwl*tc

    # Waterplane area [m2]
    awp = cwp*lwl*bwl
    # awp = lwl*bwl*(1.313*cp - 0.0857*cp*lwl/disp**(1/3) + 0.0371*lwl/disp**(1/3))

    # Rudder and keel sweep angle [rad]
    sweep_rudder = np.radians(sweep_rudder_deg)
    sweep_keel = np.radians(sweep_keel_deg)

    # Rudder and keel average chord [m]
    avg_chord_keel = (root_chord_keel + tip_chord_keel)/2
    avg_chord_rudder = (root_chord_rudder + tip_chord_rudder)/2

    # Surface area for canoe body, keel, and rudder [m2]
    surface_area_cb = (1.97 + 0.171*bwl/tc)*(0.65/cm)**(1/3)*(disp*lwl)**0.5    # Gerritsma et al (1992)
    lat_surface_keel = avg_chord_keel*span_keel
    surface_area_keel = 2*lat_surface_keel
    lat_surface_rudder = avg_chord_rudder*span_rudder
    surface_area_rudder = 2*lat_surface_rudder

    # Rudder and keel average thickness [m]
    avg_thickness_rudder = (tip_thickness_rudder + root_thickness_rudder)/2
    avg_thickness_keel = (tip_thickness_keel + root_thickness_keel)/2

    # Taper ratio: ratio of the chord length at the tip to that at the root [-]
    taper_ratio_keel = tip_chord_keel/root_chord_keel
    taper_ratio_rudder = tip_chord_rudder/root_chord_rudder

    # Effective aspect ratio [-]
    aspect_ratio_keel = 2*(span_keel+diameter_bulb/5)**2/lat_surface_keel
    
    # Canoe body ratio [-]
    ratio_cb = 2*tc/(0.75*lwl)

    # Keel displacement and volumetric centre, if not provide [m3]
    kb_keel = span_keel*(2*tip_chord_keel + root_chord_keel)/(3*(tip_chord_keel + root_chord_keel))
    disp_keel = 0.6*span_keel*avg_thickness_keel*avg_chord_keel**2

    # LCB and LCF measured from the stern's perpendicular [m]
    LCBfpp = lwl/2 + lcb 
    LCFfpp = lwl/2 + lcf

    # Form coefficient [-]
    form_coeff_cb = 0.09
    if naca_keel == '6digit':
        form_coeff_keel = 2*(avg_thickness_keel) + 60*(avg_thickness_keel)**4
        visc_keel = 1 # efeito da viscosidade na inclinacao da curva de sustentacao do escoamento 2D
    else:
        form_coeff_keel = 1.2*(avg_thickness_keel) + 70*(avg_thickness_keel)**4
        visc_keel = 0.9
    if naca_rudder == '6digit':
        form_coeff_rudder = 2*(avg_thickness_rudder) + 60*(avg_thickness_rudder)**4
        visc_rudder = 1
    else:
        form_coeff_rudder = 1.2*(avg_thickness_rudder) + 70*(avg_thickness_rudder)**4
        visc_rudder = 0.9

    # Cross-flow drag coefficient [-]
    crossflow_coeff_rudder = 0.1 + 0.7*taper_ratio_rudder
    if chord_bulb_keel > 0:
        crossflow_coeff_keel = 0
    else:
        crossflow_coeff_keel = 0.1 + 0.7*taper_ratio_keel      # faired tip
        # crossflow_coeff_keel = 0.1 + 1.6*taper_ratio_keel    # squared tip


    ### VELOCITY PREDICTION PROGRAMME
    def vpp_solve_main(solution):
        
        ### 1 PRE-CALCULATION
        # The solution for the VPP routine optimization is given in terms of four parameters
        velocity_boat = solution[0]         # Boat velocity [m/s]
        leeway = solution[1]                # Leeway angle [radians]
        heel = solution[2]                  # Heel angle [radians]
        angle_rudder = solution[3]          # Rudder angle [radians]
        
        # Velocity and leeway will be positive
        velocity_boat = abs(velocity_boat)
        leeway = abs(leeway)

        # Froude number
        Fn = (velocity_boat)/(gravity * lwl)**0.5                   # Froude number hull [-]
        Fn_rudder = velocity_boat/(gravity*avg_chord_rudder)**0.5   # Froude number rudder [-]
        
        # Apparent wind calculation
        velocity_aw = (velocity_boat**2 + velocity_tw[t]**2 - 2*velocity_boat*velocity_tw[t]*np.cos(pi - leeway - angle_tw[u]))**0.5
        angle_aw = np.arctan2((velocity_tw[t]*np.sin(angle_tw[u]) - velocity_boat*np.sin(leeway)), (velocity_tw[t]*np.cos(angle_tw[u]) + velocity_boat*np.cos(leeway)))
        
        # Heel and leeway shall have opposite signs
        if leeway > 0 and heel > 0:
            heel = -heel
        if leeway < 0 and heel < 0:
            heel = -heel


        ### 2 LIFT FORCES AND MOMENTS
        # Lift forces calculated according to Oossanen, 1993, page 27
        # A) Keel lift force [N]
        angle_keel = np.arctan2(np.cos(heel)*np.sin(leeway), np.cos(leeway))
        # Keel lift force influencing factors
        keel_linear_factor = 2*pi*visc_keel*aspect_ratio_keel/(2*visc_keel + np.cos(sweep_keel)*(4 + aspect_ratio_keel**2/(np.cos(sweep_keel))**4)**0.5)
        keel_quad_factor = crossflow_coeff_keel/aspect_ratio_keel
        keel_tip_factor = 1 - 0.135/aspect_ratio_keel**(2/3)        # faired tip
        #keel_tip_factor = 1                                        # squared tip
        keel_cb_factor = 1
        keel_bulb_factor = (1 + 0.4*diameter_bulb/span_keel)**2
        keel_factor_total = keel_linear_factor*keel_tip_factor*keel_cb_factor*keel_bulb_factor + keel_quad_factor*abs(angle_keel)
        # Keel lift force
        lift_keel = - 0.5*density_water*(velocity_boat**2)*angle_keel*lat_surface_keel*keel_factor_total

        # B) Bulb lift force [N]
        if chord_bulb_keel > 0 and surface_area_bulb > 0: 
            side_force_bulb = - 0.5*density_water*(velocity_boat**2)*(pi*diameter_bulb**2/2 + 1.8*surface_area_bulb*abs(angle_keel))*angle_keel
        else:
            side_force_bulb = 0

        # C) Rudder lift force [N]
        # Free-surface influence factor of the rudder
        fsr = 1 - 4*height_surface_rudder/(avg_chord_rudder)
        if fsr > 0:
            if Fn_rudder <= 0.5:
                factor_aspect_ratio_rudder = 2
            elif Fn_rudder > 0.5 and Fn_rudder < 0.6413:
                factor_aspect_ratio_rudder = 4.246*Fn_rudder - 0.1230
            else:
                factor_aspect_ratio_rudder = 1 + 0.422/(Fn_rudder)**3
            aspect_ratio_rudder = fsr*factor_aspect_ratio_rudder*(span_rudder**2/lat_surface_rudder)
        else:
            aspect_ratio_rudder = 2*(span_rudder**2/lat_surface_rudder)
        # Taylor wake fraction [-]
        w = 0.10 + 4.5*(tc/(height_surface_rudder + span_rudder))*cb*cp*bwl/(lwl*(7*cwp - 6*cb)*(2.8 - 1.8*cp))
        # Induced flow angle at the keel [rad]
        angle_induced_keel = 1.5*(lead_rudder/(3*avg_chord_keel))**0.25*keel_factor_total*angle_keel/(pi*aspect_ratio_keel)
        # Induced flow angle at the rudder due to the downwash of the keel [rad]
        angle_rudder_attack = - angle_induced_keel + np.arctan2(-np.cos(leeway)*np.sin(angle_rudder) + np.cos(heel)*np.sin(leeway)*np.cos(angle_rudder), np.cos(leeway)*np.cos(angle_rudder) + np.cos(heel)*np.sin(leeway)*np.sin(angle_rudder))
        angle_rudder_delta0 = angle_keel - angle_induced_keel
        # Rudder lift force influencing factors
        rudder_linear_factor = 2*pi*visc_rudder*aspect_ratio_rudder/(2*visc_rudder + np.cos(sweep_rudder)*(4 + aspect_ratio_rudder**2/(np.cos(sweep_rudder))**4)**0.5)
        rudder_quad_factor = crossflow_coeff_rudder/aspect_ratio_rudder
        rudder_tip_factor = 1 - 0.135/aspect_ratio_rudder**(2/3)
        rudder_factor_total = rudder_linear_factor*rudder_tip_factor + rudder_quad_factor*abs(angle_rudder_attack)
        rudder_factor_delta0_total = rudder_linear_factor*rudder_tip_factor + rudder_quad_factor*abs(angle_rudder_delta0)
        # Rudder lift force
        lift_rudder = - 0.5*density_water*((1 - w)*velocity_boat)**2*lat_surface_rudder*rudder_factor_total*angle_rudder_attack
        lift_rudder_delta0 = - 0.5 * density_water * ((1 - w) * velocity_boat)**2 * lat_surface_rudder * rudder_factor_delta0_total * angle_rudder_delta0
        
        # D) Canoe body side force [N]
        side_force_cb = - 0.5*density_water*(velocity_boat**2)*(0.5*pi*tc**2 + 1.8*lat_surface_cb*abs(angle_keel))*angle_keel

        # E) GZ estimation (Oossanen, 2003)
        # coefficients b0 and b1 built as fitting polynomials from the plot provided in the paper above
        b0 = 8*10**(-10)*np.degrees(heel)**4 - 3*10**(-7)*np.degrees(heel)**3 + 4*10**(-5)*np.degrees(heel)**2 - 0.002*np.degrees(heel) + 0.0754
        b1 = 5*10**(-12)*np.degrees(heel)**5 - 4*10**(-9)*np.degrees(heel)**4 + 9*10**(-7)*np.degrees(heel)**3 + 9*10**(-5)*np.degrees(heel)**2 + 0.0038*np.degrees(heel) + 0.0153
        c1 = b0 + b1*(boa/bwl)**2*(tc/bwl)/cb
        BM = c1*bwl**2/tc
        KB = tc*(5/6-cb/(3*cwp))        # Wilson, 2018
        GZ = (KB + BM - KG)*np.sin(heel)

        # F) Righting moment
        # Tranversal righting moment [N*m]
        M_hull_trans = GZ*disp*density_water*gravity

        # Righting moment of crew sitting on weather rail [N*m]
        factor_esc = 1
        if abs(angle_tw[u]) <= (pi/3):
            arm_crew = factor_esc*(0.475*boa - 0.305)
        elif abs(angle_tw[u]) < (2*pi/3):
            arm_crew = factor_esc*(0.475*boa - 0.305)*np.cos(abs(angle_tw[u])*3/2 - pi/2)
        else:
            arm_crew = 0
        M_crew = np.sign(M_hull_trans)*abs(mass_crew*gravity*arm_crew*np.cos(heel))

        # Total righting moment [N*m]
        M_righting = M_hull_trans + M_crew

        # G) Munk moment [N*m]
        # Slender bodies in near-axial flow experience a destabilising moment
        M_munk = - 0.9*disp*density_water*leeway*velocity_boat**2

        # H) Centre of Effort (CE)
        # Rudder hydrodynamic CE [m]
        CE_rudder_x = -lwl/2 - root_chord_rudder/4 - np.tan(sweep_rudder)*span_rudder/3*(1 + 2*taper_ratio_rudder)/(1 + taper_ratio_rudder)
        CE_rudder_z = height_surface_rudder + span_rudder/3*(1 + 2*taper_ratio_rudder)/(1 + taper_ratio_rudder)
        
        # Global hydrodynamic CE [m]
        CE_hydro_x = CE_rudder_x + lead_rudder
        CE_hydro_z = 0.45*(span_keel + tc)
        

        ### 3 RESISTANCE CALCULATION
        ### 3.1 Viscous Resistance
        # A) Parameters
        # Reynolds number [-]
        reynolds_cb = (velocity_boat*0.7*lwl)/viscosity_water
        reynolds_keel = (velocity_boat*avg_chord_keel)/viscosity_water
        reynolds_rudder = (velocity_boat*avg_chord_rudder)/viscosity_water
        reynolds_bulb = (velocity_boat*chord_bulb_keel)/viscosity_water

        # Friction coefficient [-]
        friction_coeff_cb = (0.075/((np.log(reynolds_cb)/np.log(10)) - 2)**2) - (1800/reynolds_cb)
        friction_coeff_keel = (0.075/((np.log(reynolds_keel)/np.log(10)) - 2)**2) - (1800/reynolds_keel)
        friction_coeff_rudder = (0.075/((np.log(reynolds_rudder)/np.log(10)) - 2)**2) - (1800/reynolds_rudder)
        if chord_bulb_keel > 0:
            friction_coeff_bulb = (0.075/((np.log(reynolds_bulb)/np.log(10)) - 2)**2) - (1800/reynolds_bulb)
        else: 
            friction_coeff_bulb = 0
        
        # B) Canoe body resistance [N]
        Rv_cb = 0.5*density_water*velocity_boat**2*friction_coeff_cb*(1 + form_coeff_cb)*surface_area_cb

        # C) Keel and bulb resistance [N]
        Rv_keel = 0.5*density_water*velocity_boat**2*friction_coeff_keel*(1 + form_coeff_keel)*surface_area_keel
        Rv_bulb = 0.5*density_water*velocity_boat**2*friction_coeff_bulb*surface_area_bulb

        # D) Rudder resistance [N]
        Rv_rudder = 0.5*density_water*velocity_boat**2*friction_coeff_rudder*(1 + form_coeff_rudder)*surface_area_rudder

        # E) Total viscous resistance [N]
        R_viscous = Rv_cb + Rv_keel + Rv_rudder + Rv_bulb
        
        ### 3.2 Residual resistance
        # A) Canoe Body resistance [N]
        vector_res_cb = np.zeros(9)
        if Fn > 0.6:
            Fn_temp = 0.6
        elif Fn < 0.1:
            Fn_temp = 0.1
        else:
            Fn_temp = Fn
        for k in range (1, 10, 1):
            if float(coefficient_residual_hull[k][0]) <= Fn_temp and Fn_temp <= float(coefficient_residual_hull[k + 1][0]):
                CC = [float(coefficient_residual_hull[k][0]), float(coefficient_residual_hull[k + 1][0])]
                for j in range (1, 10, 1):
                    DD = [float(coefficient_residual_hull[k][j]), float(coefficient_residual_hull[k + 1][j])]
                    vector_res_cb[j - 1] = interpolate.interp1d(CC, DD)(Fn_temp)
        
        if Fn_temp < 0.1:
            Rr_cb = 0
        else:
            Rr_cb = disp*density_water*gravity*(vector_res_cb[0] + (vector_res_cb[1]*LCBfpp/lwl + vector_res_cb[2]*cp + vector_res_cb[3]*disp**(2/3)/awp + \
                vector_res_cb[4]*bwl/lwl)*disp**(1/3)/lwl + (vector_res_cb[5]*disp**(2/3)/surface_area_cb + vector_res_cb[6]*LCBfpp/LCFfpp + \
                vector_res_cb[7]*(LCBfpp/lwl)**2 + vector_res_cb[8]*cp**2)*disp**(1/3)/lwl)

        # B) Keel residual resitance [N]
        vector_res_keel = np.zeros(4)
        if Fn > 0.6:
            Fn3 = 0.6
        elif Fn < 0.2:
            Fn3 = 0.2
        else:
            Fn3 = Fn
            
        for k in range (1, 9, 1):
            if float(coefficient_residual_keel[k][0]) <= Fn3 and Fn3 <= float(coefficient_residual_keel[k + 1][0]):
                GG = [float(coefficient_residual_keel[k][0]), float(coefficient_residual_keel[k + 1][0])]
                for j in range (1, 5, 1):
                    HH = [float(coefficient_residual_keel[k][j]), float(coefficient_residual_keel[k + 1][j])]
                    vector_res_keel[j - 1] = interpolate.interp1d(GG, HH)(Fn3)
        
        if Fn3 < 0.2:
            Rr_keel = 0
        else:
            Rr_keel = disp_keel*density_water*gravity*(vector_res_keel[0] + vector_res_keel[1]*((tc + span_keel)/bwl) + \
                vector_res_keel[2]*((tc + kb_keel)**3/disp_keel) + vector_res_keel[3]*(disp/disp_keel))

        # C) Total residual resistance
        R_residual = Rr_cb + Rr_keel

        ### 3.3 Induced resistance
        # Fator de correcao para folios de carregamento nao-eliptico
        tr_cb = 0.3         # razao de afilamento do casco
        sig_keel = aspect_ratio_keel*(0.012 - 0.057*taper_ratio_keel + 0.095*taper_ratio_keel**2 - 0.04*taper_ratio_keel**3)
        sig_rudder = aspect_ratio_rudder*(0.012 - 0.057*taper_ratio_rudder + 0.095*taper_ratio_rudder**2 - 0.04*taper_ratio_rudder**3)
        sig_cb = ratio_cb*(0.012 - 0.057*tr_cb + 0.095*tr_cb**2 - 0.04*tr_cb**3)

        # A) Canoe body induced resistance [N]
        Ri_cb = (side_force_cb/np.cos(heel))**2*(1 + sig_cb)/(0.5*density_water*velocity_boat**2*lat_surface_cb*pi*ratio_cb)
        
        # B) Keel induced resistance [N]
        Ri_keel = ((lift_keel**2)*(1 + sig_keel))/(0.5*density_water*(velocity_boat**2)*lat_surface_keel*pi*aspect_ratio_keel)

        # C) Rudder induced resistance [N]
        Ri_rudder = ((lift_rudder**2)*(1 + sig_rudder))/(0.5*density_water*(velocity_boat**2)*lat_surface_rudder*pi*aspect_ratio_rudder)

        # D) Total induced resistance [N]
        R_induced = Ri_cb + Ri_keel + Ri_rudder

        ### 3.4 Resitance increase due to heel
        # A) Canoe body viscous resitance [N]
        vector_heel_visc = np.zeros(4)
        if (abs(heel)) > 0.35:
            heel_temp = 0.35
        else:
            heel_temp = abs(heel)
        heel_temp = np.degrees(heel_temp)

        for k in range (1, 7, 1):
            if float(coefficient_viscous_heel[k][0]) <= heel_temp and heel_temp <= float(coefficient_viscous_heel[k + 1][0]):
                AA = [float(coefficient_viscous_heel[k][0]), float(coefficient_viscous_heel[k + 1][0])]
                for j in range (1, 5, 1):
                    BB = [float(coefficient_viscous_heel[k][j]), float(coefficient_viscous_heel[k + 1][j])]
                    vector_heel_visc[j - 1] = interpolate.interp1d(AA, BB)(heel_temp)
        
        if abs(heel) < np.radians(5):
            surface_area_cb_incl = surface_area_cb
        else:
            surface_area_cb_incl = surface_area_cb*(1 + 1/100*(vector_heel_visc[0] + vector_heel_visc[1]*bwl/tc + vector_heel_visc[2]*(bwl/tc)**2 + vector_heel_visc[3]*cm))
        
        Rv_heel_cb = 0.5*density_water*velocity_boat**2*friction_coeff_cb*surface_area_cb_incl - Rv_cb

        # B) Canoe body residual resistance increase [N]
        vector_heel_cb = np.zeros(6)
        if Fn > 0.55:
            Fn_temp = 0.55
        elif Fn < 0.25:
            Fn_temp = 0.25
        else:
            Fn_temp = Fn

        for k in range (1, 7 , 1):
            if float(coefficient_residual_heel[k][0]) <= Fn_temp and Fn_temp <= float(coefficient_residual_heel[k + 1][0]):
                EE = [float(coefficient_residual_heel[k][0]), float(coefficient_residual_heel[k + 1][0])]
                for j in range(1, 7, 1):
                    FF = [float(coefficient_residual_heel[k][j]), float(coefficient_residual_heel[k + 1][j])]
                    vector_heel_cb[j - 1] = interpolate.interp1d(EE, FF)(Fn_temp)
        vector_heel_cb[:] = [x / 1000 for x in vector_heel_cb]

        # Extrapolating resistance from 20 degrees to the real heel angle
        if Fn_temp < 0.25:
            Rincli20 = 0
        else:
            Rincli20 = disp*density_water*gravity*(vector_heel_cb[0] + vector_heel_cb[1]*lwl/bwl + vector_heel_cb[2]*bwl/tc + \
                vector_heel_cb[3]*(bwl/tc)**2 + vector_heel_cb[4]*lcb + vector_heel_cb[5]*lcb**2)
        Rr_heel_cb = Rincli20*6*abs(heel)**1.7

        # C) Keel residual resistance increase [N]
        CH = -3.5837*(tc/(tc + span_keel)) - 0.0518*(bwl/tc) + 0.5958*(bwl/(tc+span_keel)) + 0.2055*(lwl/disp**(1/3))
        Rr_heel_keel = density_water*gravity*disp_keel*Fn**2*abs(heel)*CH

        # D) Total heel resistance [N]
        R_heel = Rv_heel_cb + Rr_heel_cb + Rr_heel_keel

        ### 3.5 Added resistance in waves (Keuning et al, 2006)
        vector_addwave = np.zeros(10)
        if Fn > 0.45:
            Fn_temp = 0.45
        if Fn < 0.20:
            Fn_temp = 0.20
        else:
            Fn_temp = Fn
        for k in range(1, 6, 1):
            if float(coefficient_waves[k][0]) <= Fn_temp and Fn_temp <= float(coefficient_waves[k + 1][0]):
                GG = [float(coefficient_waves[k][0]), float(coefficient_waves[k + 1][0])]
                for j in range(1, 11, 1):
                    HH = [float(coefficient_waves[k][j]), float(coefficient_waves[k + 1][j])]
                    vector_addwave[j - 1] = interpolate.interp1d(GG, HH)(Fn_temp)
        
        # Added resistance in waves for Froude > 0.25
        if Fn_temp < 0.25:
            R_addwaves = 0
        else:
            R_addwaves = vector_addwave[0]+vector_addwave[1]*(lwl/disp**(1/3)) + vector_addwave[2]*(lwl/disp**(1/3))**2 + \
                vector_addwave[3]*(lwl/disp**(1/3))**3 + vector_addwave[4]*(lwl/bwl) + vector_addwave[5]*(lwl/bwl)**2 + \
                vector_addwave[6]*(bwl/tc) + vector_addwave[7]*cp + vector_addwave[8]*cp**2 + vector_addwave[9]*cp**3 
        wave_amplitude = 0.3
        R_addwaves = R_addwaves*gravity*density_water*lwl*wave_amplitude**2
        
        ### 3.6 Total resistance [N]
        R_total = abs(R_viscous) + abs(R_residual) + abs(R_induced) + abs(R_heel) + abs(R_addwaves)


        ### 4 AERODYNAMIC MODELING
        ### 4.1 Sail area and centre of effort
        # A) Main sail (m)
        Am = 0.5*height_mainsail*base_mainsail
        CEm = (0.39*height_mainsail) + boom_heigth_deck
        
        # B) Jib (j) and Foretriangle (f)
        if sailset == 'main+genoa' or sailset == 'main+genoa+spinnaker':
            Aj = perpendicular_jib*(height_foretriangle**2 + base_foretriangle**2)**0.5/2
            CEj = 0.39*height_foretriangle
            Af = 0.5*height_foretriangle*base_foretriangle
        else:
            Aj = 0
            CEj = 0
            Af = 0
        
        # C) Spinnaker (s)
        if (sailset == 'main+spinnaker' and angle_tw[u] > (2*pi/3)) or (sailset == 'main+genoa+spinnaker' and angle_tw[u] > (2*pi/3)):
            As = 1.15*length_spinnaker*base_foretriangle
            CEs = 0.59*height_foretriangle
        else:
            As = 0
            CEs = 0
            
        # D) Mizzen (mz)
        Amz = 0.5*height_mizzen*base_mizzen
        Cbase_mizzen = 0.39*height_mizzen + boom_height_mizzen

        # E) Nominal area
        An = Af + Am/1.16

        # F) Centre of effort above deck line
        CE_sail = (CEm*Am +  CEj*Aj + CEs*As + Cbase_mizzen*Amz)/An

        ### 4.2 Lift and drag coefficients for each sail
        angle_sail = np.arctan2(np.cos(heel)*np.sin(angle_aw), np.cos(angle_aw))

        # A) Main sail (full)
        # coefficients of clm (y) and cdm (z)
        x = [0.0, 0.12211111, 0.157, 0.20933333, 1.04666667, 1.57, 2.09333333, 2.61666667, 3.14]
        y = [0, 1.15, 1.4,1.55, 1.44, 0.96, 0.58, 0.25, -0.1]
        z = [0.027, 0.027, 0.027, 0.027, 0.103, 0.275, 0.671, 1.11, 1.2]
        Clm = np.interp(angle_sail, x, y)
        Cdm = np.interp(angle_sail, x, z)

        # B) Jib
        # coefficients of clj (y) and cdj (z)
        x = [0.12211111, 0.26166667, 0.34888889, 0.471, 0.87222222, 1.04666667, 1.74444444, 2.61666667, 3.14]
        y = [0.0, 1.0, 1.375, 1.45, 1.43, 1.25, 0.4, 0.0, -0.1] 
        z = [0.05, 0.023, 0.031, 0.037, 0.25, 0.35, 0.73, 0.95, 0.9]
        Clj = np.interp(angle_sail, x, y)
        Cdj = np.interp(angle_sail, x, z)

        # C) Spinnaker
        # coefficients of cls (y) and cds (z)
        x = [0.48844444, 0.72, 0.8, 1.05, 1.31, 1.74, 2.27, 2.62, 3.14]
        y = [0.0, 1.31, 1.56, 1.71, 1.69, 1.4, 0.83, 0.5, 0.0]
        z = [0.1, 0.15, 0.2, 0.4, 0.7, 1.0, 1.1, 1.1, 1.1]
        Cls = np.interp(angle_sail, x, y)
        Cds = np.interp(angle_sail, x, z)

        # Coefficient drag separacao
        KPm = 0.016
        KPj = 0.016
        KPs = 0.019

        # D) Mast drag coefficient
        coeff_drag_mast = 1.13*((boa*free_board) + (height_mast*diameter_mast))/An 

        # E) Lift and drag for all sails combined
        # Sail aspect ratio
        if (angle_tw[u]) < (pi/3):
            aspect_ratio_sail = (1.1*(height_mast + free_board))**2/An
        else:
            aspect_ratio_sail = (1.1*height_mast)**2/An
        if sailset == 'main' or sailset == 'main+genoa' or (sailset == 'main+spinnaker' and angle_tw[u] < (2*pi/3)) or (sailset == 'main+genoa+spinnaker' and angle_tw[u] < (2*pi/3)):
            coeff_lift = (Clm*Am + Clj*Aj)/An
            coeff_drag_par = (Cdm*Am + Cdj*Aj)/An
            coeff_drag_ind = (Clm**2*Am + Clj**2*Aj)/(An*pi*aspect_ratio_sail)
            coeff_drag_sep = (Clm**2*Am*KPm + Clj**2*Aj*KPj)/An
            coeff_drag_global = coeff_drag_par + coeff_drag_ind + coeff_drag_sep + coeff_drag_mast
        elif (sailset == 'main+spinnaker' or sailset == 'main+genoa+spinnaker') and angle_tw > (2*pi/3):
            coeff_lift = (Clm*Am + Cls*As)/An
            coeff_drag_par = (Cdm*Am + Cds*As)/An 
            coeff_drag_ind = (Clm**2*Am + Cls**2*As)/(An*pi*aspect_ratio_sail)
            coeff_drag_sep = (Clm**2*Am*KPm + Cls**2*As*KPs)/An
            coeff_drag_global = coeff_drag_par + coeff_drag_ind + coeff_drag_sep + coeff_drag_mast

        ### 4.3 Lift and draf forces and centre of efforts
        # Forces
        lift_force_sail = 0.5*density_air*velocity_aw**2*(1 - np.sin(heel)**2*np.sin(angle_aw)**2)*coeff_lift*An*np.sign(angle_sail)
        drag_force_sail = - 0.5*density_air*velocity_aw**2*(1 - np.sin(heel)**2*np.sin(angle_aw)**2)*coeff_drag_global*An
        
        # Centre of effort
        CE_aero_x = CE_hydro_x + lead_sail
        CE_aero_z = - CE_sail - free_board
        heel = abs(heel)


        ### 5 FORCES AND MOMENTS IN GLOBAL COORDINATES [X, Y, Z]
        ### 5.1 Coordinates matrix
        # A) Leeway
        Mrot_leeway = np.matrix([
            [np.cos(leeway), -np.sin(leeway), 0], 
            [np.sin(leeway), np.cos(leeway), 0], 
            [0, 0, 1]
        ])
        # B) Heel angle
        Mrot_heel = np.matrix([
            [1, 0, 0], 
            [0, np.cos(heel), - np.sin(heel)], 
            [0, np.sin(heel), np.cos(heel)]
        ])
        # C) Keel angle attack due to heel
        Mrot_keel_heel = np.matrix([
            [np.cos(angle_keel), -np.sin(angle_keel), 0], 
            [np.sin(angle_keel), np.cos(angle_keel), 0], 
            [0, 0, 1]
        ])
        # D) Rudder angle due to heel
        Mrot_rudder_heel = np.matrix([
            [np.cos(angle_rudder), -np.sin(angle_rudder), 0], 
            [np.sin(angle_rudder), np.cos(angle_rudder), 0], 
            [0, 0, 1]
        ])
        # E) Rudder angle attack due to rudder angle
        Mrot_rudder_attack = np.matrix([
            [np.cos(angle_rudder_attack), -np.sin(angle_rudder_attack), 0], 
            [np.sin(angle_rudder_attack), np.cos(angle_rudder_attack), 0], 
            [0, 0, 1]
        ])
        # F) Rudder angle attack due to rudder with no lift
        Mrot_rudder_delta0 = np.matrix([
            [np.cos(angle_rudder_delta0), -np.sin(angle_rudder_delta0), 0], 
            [np.sin(angle_rudder_delta0), np.cos(angle_rudder_delta0), 0], 
            [0, 0, 1]
        ])
        # G) Sail angle attack due to heel
        Mrot_sail_heel = np.matrix([
            [np.cos(angle_sail), np.sin(angle_sail), 0], 
            [-np.sin(angle_sail), np.cos(angle_sail), 0], 
            [0, 0, 1]
        ])

        ### 5.2 Forces [N]
        # A) Total resistance
        R_total_xyz = Mrot_leeway*np.array([R_total, 0, 0]).reshape(-1, 1)
        # B) Lift force keel
        lift_keel_xyz = Mrot_heel*Mrot_keel_heel*np.array([0, lift_keel, 0]).reshape(-1, 1)
        # C) Lift force rudder
        lift_rudder_xyz = Mrot_heel*Mrot_rudder_heel*Mrot_rudder_attack*np.array([0, lift_rudder, 0]).reshape(-1, 1)
        # D) Lift force rudder for delta = 0
        lift_rudder_delta0_xyz = Mrot_heel*Mrot_rudder_delta0*np.array([0, lift_rudder_delta0, 0]).reshape(-1, 1)
        # E) Bulb side force
        side_force_bulb_xyz = Mrot_leeway*np.array([0, side_force_bulb, 0]).reshape(-1, 1)
        # F) Canoe body side force
        side_force_cb_xyz = Mrot_leeway*np.array([0, side_force_cb, 0]).reshape(-1, 1)
        # G) Sail lift force
        lift_force_sail_xyz = Mrot_heel*Mrot_sail_heel*np.array([0, lift_force_sail, 0]).reshape(-1, 1)
        # H) Sail drag force 
        drag_force_sail_xyz = Mrot_heel*Mrot_sail_heel*np.array([drag_force_sail, 0, 0]).reshape(-1, 1)

        ### 5.3 Centre of effort [m]
        # A) Aerodynamic CE
        CE_aero_xyz = Mrot_heel*np.array([CE_aero_x, 0, CE_aero_z]).reshape(-1, 1)
        # B) Hydrodynamic CE
        CE_hydro_xyz = Mrot_heel*np.array([CE_hydro_x, 0, CE_hydro_z]).reshape(-1, 1)
        # C) Rudder hydrodynamic CE
        CE_rudder_xyz = Mrot_heel*np.array([CE_rudder_x, 0, CE_rudder_z]).reshape(-1, 1)

        ### 5.4 Moments [N.m]
        # A) Munk Moment
        M_munk_xyz = np.array([0, 0, M_munk])
        # B) Righting Moment
        M_righting_xyz = np.array([M_righting, 0, 0])
        # C) Aerodrynamic moment
        x = [np.float(CE_aero_xyz[0]), np.float(CE_aero_xyz[1]), np.float(CE_aero_xyz[2])]
        y = [np.float(lift_force_sail_xyz[0]) + np.float(drag_force_sail_xyz[0]), np.float(lift_force_sail_xyz[1]) + np.float(drag_force_sail_xyz[0]), np.float(lift_force_sail_xyz[2]) + np.float(drag_force_sail_xyz[0])] 
        M_aero_xyz = np.cross(x,y)
        # D) Hydrodynamic moment
        x = [np.float(CE_hydro_xyz[0]), np.float(CE_hydro_xyz[1]), np.float(CE_hydro_xyz[2])]
        y = [np.float(-R_total_xyz[0]) + np.float(lift_keel_xyz[0]) + np.float(lift_rudder_xyz[0]) + np.float(side_force_cb_xyz[0]) + np.float(side_force_bulb_xyz[0]), \
            np.float(-R_total_xyz[1]) + np.float(lift_keel_xyz[1]) + np.float(lift_rudder_xyz[1]) + np.float(side_force_cb_xyz[1]) + np.float(side_force_bulb_xyz[1]), \
            np.float(-R_total_xyz[2]) + np.float(lift_keel_xyz[2]) + np.float(lift_rudder_xyz[2]) + np.float(side_force_cb_xyz[2]) + np.float(side_force_bulb_xyz[2])]
        M_hydro_xyz = np.cross(x,y)
        # E) Rudder moment
        x = [np.float(CE_rudder_xyz[0]) - np.float(CE_hydro_xyz[0]), np.float(CE_rudder_xyz[1]) - np.float(CE_hydro_xyz[1]), np.float(CE_rudder_xyz[2]) - np.float(CE_hydro_xyz[2])]
        y = [np.float(lift_rudder_xyz[0]) - np.float(lift_rudder_delta0_xyz[0]), np.float(lift_rudder_xyz[1]) - np.float(lift_rudder_delta0_xyz[1]), np.float(lift_rudder_xyz[2]) - np.float(lift_rudder_delta0_xyz[2])]
        M_rudder_xyz = np.cross(x,y)

        ### 5.5 Resulting forces and moments
        forces_resulting = lift_force_sail_xyz + drag_force_sail_xyz + lift_keel_xyz + lift_rudder_xyz + side_force_cb_xyz + side_force_bulb_xyz - R_total_xyz
        moments_resulting = M_munk_xyz + M_righting_xyz + M_aero_xyz + M_hydro_xyz + M_rudder_xyz

        ### 5.6 Equilibrium system to be solved for Surge, Sway, Roll, and Yaw, in this order
        equilibrium_system = np.array([np.float(forces_resulting[0]), np.float(forces_resulting[1]), np.float(moments_resulting[0]), np.float(moments_resulting[2])])


        return equilibrium_system


    ### RUNNING THE VPP FOR EVERY COMBINATION OF WIND ANGLE AND WIND SPPED
    for t in range (0, np.size(velocity_tw), 1):
        for u in range (0, np.size(angle_tw), 1):
            # solve for Powell hybrid method (hybr) or Levenber-Marquart (lb)
            sol = optimize.root(vpp_solve_main, initial_guess)
            velocity_boat_matrix[t, u] = abs(sol.x[0])
            angle_tw_matrix[t, u] = np.degrees(angle_tw[u])
            vmg_matrix[t, u] = abs(sol.x[0])*np.cos(abs(sol.x[1]) + angle_tw[u])
            print(sol)


    # Average velocity [kn]
    average_velocity = np.float(np.mean(velocity_boat_matrix))

    # Average velocity upwind [kn]
    max_angle = np.int((120-30)/step_angle + 1)
    angle_tw_matrix_upwind = np.zeros((np.size(velocity_tw), max_angle))
    velocity_boat_matrix_upwind = np.zeros((np.size(velocity_tw), max_angle))
    for t in range (0, np.size(velocity_tw), 1):
        for u in range (0, max_angle, 1):
            velocity_boat_matrix_upwind[t, u] = velocity_boat_matrix[t, u]
            angle_tw_matrix_upwind[t, u] = angle_tw_matrix[t, u]
    average_velocity_upwind = np.float(np.mean(velocity_boat_matrix_upwind))

    # Comfort
    CR = disp*density_water*2.20462/((boa*3.28084)**(4/3)*0.65*(0.7*lwl*3.28084+0.3*loa*3.28084))

    # count the number of lines to set the index number
    json.dump({'angle': angle_tw_matrix[0].tolist()}, codecs.open('assets/data/vpp_results/angles.json', 'w', encoding='utf-8'), separators=(', ',': '), sort_keys=True)
    index = sum([len(files) for r, d, files in os.walk("assets/data/vpp_results")])
   
    # Export VPP data to json file
    velocity_boat_matrix_list = velocity_boat_matrix.tolist()
    angle_tw_matrix_list = angle_tw_matrix.tolist()
    vmg_matrix_list = vmg_matrix.tolist()

    data_struct = {
        'velocity_boat_matrix_list': [NoIndent(elem) for elem in velocity_boat_matrix_list],
        'angle_tw_matrix_list': [NoIndent(elem) for elem in angle_tw_matrix_list],
        'vmg_matrix_list': [NoIndent(elem) for elem in vmg_matrix_list],
    }

    with open('assets/data/vpp_results/veloc_hull_' + str(index) + '.json', 'w') as fp:
        json.dump(data_struct, fp, cls = MyEncoder, sort_keys = True, indent = 4)

    
    return average_velocity, average_velocity_upwind, CR # velocity_boat_matrix, velocity_boat_matrix_upwind, angle_tw_matrix_upwind


# Functions to build the JSON file
class NoIndent(object):
    """ Value wrapper. """
    def __init__(self, value):
        if not isinstance(value, (list, tuple)):
            raise TypeError('Only lists and tuples can be wrapped')
        self.value = value

class MyEncoder(json.JSONEncoder):
    FORMAT_SPEC = '@@{}@@'  # Unique string pattern of NoIndent object IDs
    regex = re.compile(FORMAT_SPEC.format(r'(\d+)'))  # compile(r'@@(\d+)@@')

    def __init__(self, **kwargs):
        # Encoding keys to ignore when encoding NoIndent wrapped value
        ignore = {'cls', 'indent'}

        # Save copy of any keyword argument values needed for use here
        self._kwargs = {k: v for k, v in kwargs.items() if k not in ignore}
        super(MyEncoder, self).__init__(**kwargs)

    def default(self, obj):
        return (self.FORMAT_SPEC.format(id(obj)) if isinstance(obj, NoIndent)
                    else super(MyEncoder, self).default(obj))

    def iterencode(self, obj, **kwargs):
        format_spec = self.FORMAT_SPEC  # Local var to expedite accesss

        # Replace any marked-up NoIndent wrapped values in the JSON repr
        # with the json.dumps() of the corresponding wrapped Python object
        for encoded in super(MyEncoder, self).iterencode(obj, **kwargs):
            match = self.regex.search(encoded)
            if match:
                id = int(match.group(1))
                no_indent = PyObj_FromPtr(id)
                json_repr = json.dumps(no_indent.value, **self._kwargs)
                # Replace the matched id string with json formatted representation
                # of the corresponding Python object
                encoded = encoded.replace(
                            '"{}"'.format(format_spec.format(id)), json_repr)
            yield encoded
