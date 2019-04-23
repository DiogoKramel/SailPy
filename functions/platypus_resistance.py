import codecs, json
import numpy as np
import csv
from platypus import NSGAII, GDE3, OMOPSO, SMPSO, SPEA2, EpsMOEA, Problem, Real, EPSILON
from functions import resistance

# more information here:
# https://platypus.readthedocs.io/en/latest/_modules/platypus/algorithms.html

def optimization_platypus_resistance():
    gaconfig_obj = codecs.open('assets/data/parametersga.json', 'r', encoding='utf-8').read()
    gaconfig = json.loads(gaconfig_obj) 
    weight1 = np.float(gaconfig["weight1"])*(-1)/10 # resistance weight
    weight2 = np.float(gaconfig["weight2"])/10 # comfort ratio weight
    bound_low1 = np.float(gaconfig["lwlmin"])
    bound_up1 = np.float(gaconfig["lwlmax"])
    bound_low2 = np.float(gaconfig["bwlmin"])
    bound_up2 = np.float(gaconfig["bwlmax"])
    bound_low3 = np.float(gaconfig["tcmin"])
    bound_up3 = np.float(gaconfig["tcmax"])
    bound_low4 = np.float(gaconfig["lcfmin"])
    bound_up4 = np.float(gaconfig["lcfmax"])
    bound_low5 = np.float(gaconfig["lcbmin"])
    bound_up5 = np.float(gaconfig["lcbmax"])
    bound_low6 = np.float(gaconfig["cbmin"])
    bound_up6 = np.float(gaconfig["cbmax"])
    bound_low7 = np.float(gaconfig["cwpmin"])
    bound_up7 = np.float(gaconfig["cwpmax"])
    bound_low8 = np.float(gaconfig["cpmin"])
    bound_up8 = np.float(gaconfig["cpmax"])
    bound_low9 = np.float(gaconfig["cmmin"])
    bound_up9 = np.float(gaconfig["cmmax"])
    
    offspringsplatypus = np.float(gaconfig["offspringsplatypus"])
    gamethod = gaconfig["gamethod"]
    dispmin = np.float(gaconfig["dispmin"])
    
    def function_platypus(vars):
        lwl = vars[0]
        bwl = vars[1]
        tcan = vars[2]
        lcf =vars[3]
        lcb = vars[4]
        cb = vars[5]
        cwp = vars[6]
        cp = vars[7]
        cm = vars[8]

        dimensions = codecs.open('assets/data/dimensions.json', 'r', encoding='utf-8').read()
        dim = json.loads(dimensions)
        alcb_coefficient = np.float(dim["alcb_coefficient"])
        velocityrange = np.array(gaconfig["velocityrange"])
        heelrange = np.array(gaconfig["heelrange"])    
        alcb = lwl*alcb_coefficient*tcan
        divcan = lwl*bwl*tcan*cb
        awp = bwl*lwl*cwp
        
        Rt = 0
        CR = 0
        Rv = 0
        Ri = 0
        Rr =0
        Rincli =0
        count = 0
        for velocity in range (velocityrange[0], velocityrange[1], 1):
            for heel in range (heelrange[0], heelrange[1], 5):
                result = resistance(lwl, bwl, tcan, alcb, cp, cm, awp, divcan, lcb, lcf, velocity, heel)
                Rt = Rt+result[0]
                Rv = Rv+result[1]
                Ri = Ri+result[2]
                Rr = Rr+result[3]
                Rincli = Rincli+result[4]
                CR = CR+result[5]
                count = count+1
        Rt = Rt/count
        CR = CR/count
        Rv = Rv/count
        Ri = Ri/count
        Rr = Rr/count

        savefile = "optimizationresistance"
        rows = []
        with open("assets/data/"+savefile+".csv", "r") as csvfile:
            csvreader = csv.reader(csvfile) 
            for row in csvreader: 
                rows.append(row)
            index = csvreader.line_num
        
        constraint1, constraint2, constraint3, constraint4, constraint5, constraint6, constraint7, valid  = False, False, False, False, False, False, False, False
        boa = bwl*1.1
        dispmass = divcan*1025
        cs = boa*3.28084/(dispmass*2.20462/64)**(1/3)

        if (lwl/bwl) > 5 or (lwl/bwl) < 2.73:
            constraint1 = True
        if (bwl/tcan) > 19.39 or (bwl/tcan) < 2.46:
            constraint2 = True
        if (lwl/divcan**(1/3)) > 8.5 or (lwl/divcan**(1/3)) < 4.34:
            constraint3 = True
        if (awp/divcan**(2/3)) > 12.67 or (awp/divcan**(2/3)) < 3.78:
            constraint4 = True
        if (divcan/(lwl*bwl*tcan)) > 0.4 or (divcan/(lwl*bwl*tcan)) < 0.3:
            constraint5 = True
        if divcan < dispmin:
            constraint6 = True
        if cs > 2:
            constraint7 = True
        if constraint1==False and constraint2 == False and constraint3 == False and constraint4 == False and constraint5 == False and constraint6 == False and constraint7 == False:
            valid = True

        exportdata = [index, format(Rt, '.4f'), format(Rv, '.4f'), format(Ri, '.4f'), format(Rr, '.4f'), format(Rincli, '.4f'), format(CR, '.4f'), format(cs, '.4f'), format(lwl, '.4f'), format(bwl, '.4f'), format(tcan, '.4f'), format(divcan, '.4f'), format(awp, '.4f'), format(lcb, '.4f'), format(lcf, '.4f'), constraint1, constraint2, constraint3, constraint4, constraint5, constraint6, constraint7, valid]
        with open("assets/data/"+savefile+".csv", "a") as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(exportdata)
        
        return [Rt, CR], [divcan-dispmin, cs-2]

    problem = Problem(9, 2, 2)
    problem.types[:] = [Real(bound_low1, bound_up1), Real(bound_low2, bound_up2), Real(bound_low3, bound_up3), Real(bound_low4, bound_up4), Real(bound_low5, bound_up5), Real(bound_low6, bound_up6), Real(bound_low7, bound_up7), Real(bound_low8, bound_up8), Real(bound_low9, bound_up9)]
    problem.directions[:] = [Problem.MINIMIZE, Problem.MAXIMIZE]
    problem.constraints[:] = "<0"
    problem.function = function_platypus

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