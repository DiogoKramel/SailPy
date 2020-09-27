import numpy as np
import codecs, json
import csv
from platypus import NSGAII, GDE3, OMOPSO, SMPSO, SPEA2, EpsMOEA, Problem, Real, EPSILON
from functions import resistance

# more information here: https://platypus.readthedocs.io/en/latest/_modules/platypus/algorithms.html

def optimization_platypus_resistance(lwlmin, lwlmax, bwlmin, bwlmax, tcmin, tcmax, lcfmin, lcfmax, lcbmin, lcbmax, displac, cwpmin, cwpmax, cpmin, cpmax, cmmin, cmmax, gamethod, offspringsplatypus):
    
    def function_platypus(vars):
        # each vars[i] give one random number between the minimum and maximum limit for each parameter
        lwl, bwl, tc, lcf, lcb, cwp, cp, cm = vars[0], vars[1], vars[2], vars[3], vars[4], vars[5], vars[6], vars[7]

        # import extra parameters
        dimensions = codecs.open('assets/data/dimensions.json', 'r', encoding='utf-8').read()
        dim = json.loads(dimensions)
        gaconfig_obj = codecs.open('assets/data/parametersga.json', 'r', encoding='utf-8').read()
        gaconfig = json.loads(gaconfig_obj)
        velocityrange = np.array(gaconfig["velocityrange"])
        heelrange = np.array(gaconfig["heelrange"]) 

        # calculate remaining parameters
        disp = np.float(displac)
        awp = bwl*lwl*cwp
        boa = bwl*1.1
        dispmass = disp*1025
        cs = boa*3.28084/(dispmass*2.20462/64)**(1/3)
        cb = disp/(lwl*bwl*tc)
        
        
        # calculate the resistance for a combinantion of velocities and heel angle
        Rt, CR, Rv, Ri, Rr, Rincli, count = 0, 0, 0, 0, 0, 0, 0
        for velocity in range (velocityrange[0], velocityrange[1], 1):
            for heel in range (heelrange[0], heelrange[1], 5):
                result = resistance(lwl, bwl, tc, cp, cm, cwp, disp, lcb, lcf, velocity, heel)
                Rt, Rv, Ri, Rr, Rincli, CR, count = Rt+result[0], Rv+result[1], Ri+result[2], Rr+result[3], Rincli+result[4], CR+result[5], count+1
        Rt, CR, Rv, Ri, Rr, Rincli = Rt/count, CR/count, Rv/count, Ri/count, Rr/count, Rincli/count

        # count the number of lines to set the index number
        rows = []
        with open("assets/data/optimizationresistance.csv", "r") as csvfile:
            csvreader = csv.reader(csvfile) 
            for row in csvreader: 
                rows.append(row)
            index = csvreader.line_num
        
        # calculate constraints of delft series, capsize screening factor, and displacement
        constraint1, constraint2, constraint3, constraint4, constraint5, constraint6, valid  = False, False, False, False, False, False, False
        if (lwl/bwl) > 5 or (lwl/bwl) < 2.73:
            constraint1 = True
        if (bwl/tc) > 6.5 or (bwl/tc) < 3.8: #(bwl/tcan) > 19.39 or (bwl/tcan) < 2.46 delft series seems to have unrealistic limits
            constraint2 = True
        if (lwl/disp**(1/3)) > 8.5 or (lwl/disp**(1/3)) < 4.34:
            constraint3 = True
        if (awp/disp**(2/3)) > 12.67 or (awp/disp**(2/3)) < 3.78:
            constraint4 = True
        if cs > 2:
            constraint5 = True
        if cb < 0.35:
            constraint6 = True
        if constraint1==False and constraint2 == False and constraint3 == False and constraint4 == False and constraint5 == False and constraint6 == False:
            valid = True

        # export data to csv
        exportdata = [index, format(Rt, '.4f'), format(Rv, '.4f'), format(Ri, '.4f'), format(Rr, '.4f'), format(Rincli, '.4f'), format(CR, '.4f'), format(cs, '.4f'), format(lwl, '.4f'), format(bwl, '.4f'), format(tc, '.4f'), format(disp, '.4f'), format(cwp, '.4f'), format(lcb, '.4f'), format(lcf, '.4f'), constraint1, constraint2, constraint3, constraint4, constraint5, valid]
        with open("assets/data/optimizationresistance.csv", "a", newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(exportdata)
        
        # return 2 objectives and 5 restrictions
        return [Rt, CR], [cs-2, lwl/bwl-5, 2.73-lwl/bwl, bwl/tc-6.5, 3.8-bwl/tc]

    # optimize for 9 parameters, 2 objectives and 5 restrictions
    problem = Problem(8, 2, 5)
    problem.types[:] = [Real(lwlmin, lwlmax), Real(bwlmin, bwlmax), Real(tcmin, tcmax), Real(lcfmin, lcfmax), Real(lcbmin, lcbmax), Real(cwpmin, cwpmax), Real(cpmin, cpmax), Real(cmmin, cmmax)]
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

    return offspringsplatypus