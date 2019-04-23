import numpy as np
import codecs, json
import csv
from platypus import NSGAII, GDE3, OMOPSO, SMPSO, SPEA2, EpsMOEA, Problem, Real, EPSILON
from functions import resistance

# more information here: https://platypus.readthedocs.io/en/latest/_modules/platypus/algorithms.html

def optimization_platypus_resistance(lwlmin, lwlmax, bwlmin, bwlmax, tcmin, tcmax, lcfmin, lcfmax, lcbmin, lcbmax, cbmin, cbmax, cwpmin, cwpmax, cpmin, cpmax, cmmin, cmmax, gamethod, offspringsplatypus, dispmin):
    
    def function_platypus(vars):
        # each vars[i] give one random number between the minimum and maximum limit for each parameter
        lwl, bwl, tcan, lcf, lcb, cb, cwp, cp, cm = vars[0], vars[1], vars[2], vars[3], vars[4], vars[5], vars[6], vars[7], vars[8]

        # import extra parameters
        dimensions = codecs.open('assets/data/dimensions.json', 'r', encoding='utf-8').read()
        dim = json.loads(dimensions)
        gaconfig_obj = codecs.open('assets/data/parametersga.json', 'r', encoding='utf-8').read()
        gaconfig = json.loads(gaconfig_obj)
        alcb_coefficient = np.float(dim["alcb_coefficient"]) 
        velocityrange = np.array(gaconfig["velocityrange"])
        heelrange = np.array(gaconfig["heelrange"]) 

        # calculate remaining parameters   
        alcb = lwl*alcb_coefficient*tcan
        divcan = lwl*bwl*tcan*cb
        awp = bwl*lwl*cwp
        boa = bwl*1.1
        dispmass = divcan*1025
        cs = boa*3.28084/(dispmass*2.20462/64)**(1/3)
        
        # calculate the resistance for a combinantion of velocities and heel angle
        Rt, CR, Rv, Ri, Rr, Rincli, count = 0, 0, 0, 0, 0, 0, 0
        for velocity in range (velocityrange[0], velocityrange[1], 1):
            for heel in range (heelrange[0], heelrange[1], 5):
                result = resistance(lwl, bwl, tcan, alcb, cp, cm, awp, divcan, lcb, lcf, velocity, heel)
                Rt, Rv, Ri, Rr, Rincli, CR, count = Rt+result[0], Rv+result[1], Ri+result[2], Rr+result[3], Rincli+result[4], CR+result[5], count+1
        Rt, CR, Rv, Ri, Rr = Rt/count, CR/count, Rv/count, Ri/count, Rr/count

        # count the number of lines to set the index number
        rows = []
        with open("assets/data/optimizationresistance.csv", "r") as csvfile:
            csvreader = csv.reader(csvfile) 
            for row in csvreader: 
                rows.append(row)
            index = csvreader.line_num
        
        # calculate constraints of delft series, capsize screening factor, and displacement
        constraint1, constraint2, constraint3, constraint4, constraint5, constraint6, constraint7, valid  = False, False, False, False, False, False, False, False
        if (lwl/bwl) > 5 or (lwl/bwl) < 2.73:
            constraint1 = True
        if (bwl/tcan) > 19.39 or (bwl/tcan) < 2.46:
            constraint2 = True
        if (lwl/divcan**(1/3)) > 8.5 or (lwl/divcan**(1/3)) < 4.34:
            constraint3 = True
        if (awp/divcan**(2/3)) > 12.67 or (awp/divcan**(2/3)) < 3.78:
            constraint4 = True
        if divcan < dispmin:
            constraint5 = True
        if cs > 2:
            constraint6 = True
        if constraint1==False and constraint2 == False and constraint3 == False and constraint4 == False and constraint5 == False and constraint6 == False:
            valid = True

        # export data to csv
        exportdata = [index, format(Rt, '.4f'), format(Rv, '.4f'), format(Ri, '.4f'), format(Rr, '.4f'), format(Rincli, '.4f'), format(CR, '.4f'), format(cs, '.4f'), format(lwl, '.4f'), format(bwl, '.4f'), format(tcan, '.4f'), format(divcan, '.4f'), format(awp, '.4f'), format(lcb, '.4f'), format(lcf, '.4f'), constraint1, constraint2, constraint3, constraint4, constraint5, constraint6, valid]
        with open("assets/data/optimizationresistance.csv", "a") as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(exportdata)
        
        # return 2 objectives and 2 restrictions
        return [Rt, CR], [divcan-dispmin, cs-2]

    # optimize for 9 parameters, 2 objectives and 2 restrictions
    problem = Problem(9, 2, 2)
    problem.types[:] = [Real(lwlmin, lwlmax), Real(bwlmin, bwlmax), Real(tcmin, tcmax), Real(lcfmin, lcfmax), Real(lcbmin, lcbmax), Real(cbmin, cbmax), Real(cwpmin, cwpmax), Real(cpmin, cpmax), Real(cmmin, cmmax)]
    problem.directions[:] = [Problem.MINIMIZE, Problem.MAXIMIZE]
    problem.constraints[:] = "<0"
    problem.function = function_platypus

    # six methods applied (there is four more still not applied)
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