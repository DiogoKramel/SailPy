import numpy as np
import codecs, json
import csv
import os, glob                             # Delete results files before running
from platypus import NSGAII, GDE3, OMOPSO, SMPSO, SPEA2, EpsMOEA, Problem, Real, EPSILON
from functions import vpp_solve
# more information here: https://platypus.readthedocs.io/en/latest/_modules/platypus/algorithms.html


def optimization_platypus_vpp(offspringsplatypus, gamethod, windspeedrange, windanglerange):
    
    # Clean the folder with previous results
    #folder = "assets/data/vpp_results/*"
    #files = glob.glob(folder)
    #for f in files:
    #    os.remove(f)

    # Adjust input data
    minimum_tw_knots = np.float(windspeedrange[0])
    maximum_tw_knots = np.float(windspeedrange[1])+1
    minimum_tw_angle = np.float(windanglerange[0])*10
    maximum_tw_angle = np.float(windanglerange[1])*10+1
    print(minimum_tw_knots, maximum_tw_knots, minimum_tw_angle, maximum_tw_angle)

    # Import dimensions
    dim_obj = codecs.open('assets/data/dimensions_hull_limits.json', 'r', encoding='utf-8').read()
    dim = json.loads(dim_obj) 
    lwlmin = np.float(dim["lwlmin"])
    lwlmax = np.float(dim["lwlmax"])
    bwlmin = np.float(dim["bwlmin"])
    bwlmax = np.float(dim["bwlmax"])
    tcmin = np.float(dim["tcmin"])
    tcmax = np.float(dim["tcmax"])
    lwl_avg = (lwlmax+lwlmin)/2
    lcbmin = np.float(dim["lcbmin"]) - lwl_avg/2
    lcbmax = np.float(dim["lcbmax"]) - lwl_avg/2
    lcfmin = np.float(dim["lcfmin"]) - lwl_avg/2
    lcfmax = np.float(dim["lcfmax"]) - lwl_avg/2
    cbmin = np.float(dim["cbmin"])
    cbmax = np.float(dim["cbmax"])
    cmmin = np.float(dim["cmmin"])
    cmmax = np.float(dim["cmmax"])
    cpmin = np.float(dim["cpmin"])
    cpmax = np.float(dim["cpmax"])
    cwpmin = np.float(dim["cwpmin"])
    cwpmax = np.float(dim["cwpmax"])


    dim_obj = codecs.open('assets/data/dimensions-appendages-limits.json', 'r', encoding='utf-8').read()
    dim = json.loads(dim_obj)
    fbmin = np.float(dim["fbmin"])
    fbmax = np.float(dim["fbmax"])
    boamin = np.float(dim["boamin"])
    boamax = np.float(dim["boamax"])
    mass_crew = 280
    pmin = np.float(dim["pmin"])
    pmax = np.float(dim["pmax"])
    emin = np.float(dim["emin"])
    emax = np.float(dim["emax"])
    imin = np.float(dim["imin"])
    imax = np.float(dim["imax"])
    jmin = np.float(dim["jmin"])
    jmax = np.float(dim["jmax"])
    spanRmin = np.float(dim["spanRmin"])
    spanRmax = np.float(dim["spanRmax"])
    tipcRmin = np.float(dim["tipcRmin"])
    tipcRmax = np.float(dim["tipcRmax"])
    rootcRmin = np.float(dim["rootcRmin"])
    rootcRmax = np.float(dim["rootcRmax"])
    tiptcksRmin = np.float(dim["tiptcksRmin"])
    tiptcksRmax = np.float(dim["tiptcksRmax"])
    roottcksRmin = np.float(dim["roottcksRmin"])
    roottcksRmax = np.float(dim["roottcksRmax"])
    sweepRdegmin = np.float(dim["sweepRdegmin"])
    sweepRdegmax = np.float(dim["sweepRdegmax"])
    spanKmin = np.float(dim["spanKmin"])
    spanKmax = np.float(dim["spanKmax"])
    tipcKmin = np.float(dim["tipcKmin"])
    tipcKmax = np.float(dim["tipcKmax"])
    rootcKmin = np.float(dim["rootcKmin"])
    rootcKmax = np.float(dim["rootcKmax"])
    tiptcksKmin = np.float(dim["tiptcksKmin"])
    tiptcksKmax = np.float(dim["tiptcksKmax"])
    roottcksKmin = np.float(dim["roottcksKmin"])
    roottcksKmax = np.float(dim["roottcksKmax"])
    sweepKdegmin = np.float(dim["sweepKdegmin"])
    sweepKdegmax = np.float(dim["sweepKdegmax"])
    badmin = np.float(dim["badmin"])
    badmax = np.float(dim["badmax"])
    splmin = np.float(dim["splmin"])
    splmax = np.float(dim["splmax"])
    lpgmin = np.float(dim["lpgmin"])
    lpgmax = np.float(dim["lpgmax"])
    ehmmin = np.float(dim["ehmmin"])
    ehmmax = np.float(dim["ehmmax"])
    emdcmin = np.float(dim["emdcmin"])
    emdcmax = np.float(dim["emdcmax"])
    hsrmin = np.float(dim["hsrmin"])
    hsrmax = np.float(dim["hsrmax"])
    pmzmin = np.float(dim["pmzmin"])
    pmzmax = np.float(dim["pmzmax"])
    emzmin = np.float(dim["emzmin"])
    emzmax = np.float(dim["emzmax"])
    badmzmin = np.float(dim["badmzmin"])
    badmzmax = np.float(dim["badmzmax"])
    xceamin = np.float(dim["xceamin"])
    xceamax = np.float(dim["xceamax"])

            
    def function_platypus_vpp(vars):
        
        
        # each vars[i] give one random number between the minimum and maximum limit for each parameter
        loa, lwl, boa, bwl, tc, lcb, lcf = vars[0], vars[1], vars[2], vars[3], vars[4], vars[5], vars[6]
        cb, cm, cp, cwp, free_board = vars[7], vars[8], vars[9], vars[10], vars[11]
        height_mainsail, base_mainsail, height_foretriangle, base_foretriangle = vars[12], vars[13], vars[14], vars[15]
        span_rudder, tip_chord_rudder, root_chord_rudder, tip_thickness_rudder, root_thickness_rudder, sweep_rudder_deg = vars[16], vars[17], vars[18], vars[19], vars[20], vars[21]
        span_keel, tip_chord_keel, root_chord_keel, tip_thickness_keel, root_thickness_keel, sweep_keel_deg = vars[22], vars[23], vars[24], vars[25], vars[26], vars[27]
        boom_heigth_deck, length_spinnaker, perpendicular_jib = vars[28], vars[29], vars[30]
        height_mast, diameter_mast, height_surface_rudder, height_mizzen, base_mizzen, boom_height_mizzen = vars[31], vars[32], vars[33], vars[34], vars[35], vars[36]
        lead_sail = vars[37]
        
        resultados = vpp_solve('main+genoa', loa, lwl, boa, bwl, tc, lcb, lcf, cb, cm, cp, cwp, 4.5, 0.8, free_board, 5.674, lead_sail, \
            mass_crew, height_mainsail, base_mainsail, height_foretriangle, base_foretriangle, boom_heigth_deck, length_spinnaker, \
            perpendicular_jib, span_rudder, tip_chord_rudder, root_chord_rudder, tip_thickness_rudder, root_thickness_rudder, \
            sweep_rudder_deg, span_keel, tip_chord_keel, root_chord_keel, tip_thickness_keel, root_thickness_keel, sweep_keel_deg, \
            '6digit', '6digit', height_mast, diameter_mast, height_surface_rudder, height_mizzen, base_mizzen, boom_height_mizzen, 0, 0, 0, \
            minimum_tw_knots, maximum_tw_knots, minimum_tw_angle, maximum_tw_angle)

            #lat_surface_cb, KG,lead_rudder
            #naca_keel, naca_rudder, chord_bulb_keel, diameter_bulb, surface_area_bulb
        
        # Count the number of lines to set the index number
        index = sum([len(files) for r, d, files in os.walk("assets/data/vpp_results")])
        if index > 1:
            index = index-1
        
        # Export data to csv
        exportdata = [index, format(resultados[0], '.4f'), format(resultados[1], '.4f'), format(resultados[2], '.4f'), 'true']
        with open("assets/data/optimizationvpp.csv", "a") as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(exportdata)
        print(index)

        return resultados[0], resultados[2]


    # Optimize for 9 parameters, 2 objectives and 2 restrictions
    problem = Problem(38, 2)
    problem.types[:] = [Real(lwlmin, lwlmax), Real(lwlmin, lwlmax), Real(boamin, boamax), Real(bwlmin, bwlmax), \
        Real(tcmin, tcmax), Real(lcbmin, lcbmax), Real(lcfmin, lcfmax), Real(cbmin, cbmax), Real(cmmin, cmmax), \
        Real(cpmin, cpmax), Real(cwpmin, cwpmax), Real(fbmin, fbmax), Real(pmin, pmax), Real(emin, emax), \
        Real(imin, imax), Real(jmin, jmax), Real(spanRmin, spanRmax), Real(tipcRmin, tipcRmax), Real(rootcRmin, rootcRmax), \
        Real(tiptcksRmin, tiptcksRmax), Real(roottcksRmin, roottcksRmax), Real(sweepRdegmin, sweepRdegmax), \
        Real(spanKmin, spanKmax), Real(tipcKmin, tipcKmax), Real(rootcKmin, rootcKmax), Real(tiptcksKmin, tiptcksKmax), \
        Real(roottcksKmin, roottcksKmax), Real(sweepKdegmin, sweepKdegmax), \
        Real(badmin, badmax), Real(splmin, splmax), Real(lpgmin, lpgmax), \
        Real(ehmmin, ehmmax), Real(emdcmin, emdcmax), Real(hsrmin, hsrmax), Real(pmzmin, pmzmax), Real(emzmin, emzmax), \
        Real(badmzmin, badmzmax), Real(xceamin, xceamax)]

    problem.directions[:] = [Problem.MAXIMIZE, Problem.MAXIMIZE]
    problem.function = function_platypus_vpp

    # Six methods applied (there is four more still not applied)
    if gamethod == 'NSGAII':
        algorithm = NSGAII(problem)
    elif gamethod == 'GDE3':
        algorithm = GDE3(problem)
    elif gamethod == 'OMOPSO':
        algorithm = OMOPSO(problem, epsilons = 0.05)
    elif gamethod == 'SMPSO':
        algorithm = SMPSO(problem)
    elif gamethod == 'SPEA2':
        algorithm = SPEA2(problem)
    elif gamethod == 'EpsMOEA':
        algorithm = EpsMOEA(problem, epsilons = 0.05)

    algorithm.run(np.int(offspringsplatypus))

    return "ok"