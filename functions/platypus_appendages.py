import numpy as np
import codecs, json
import csv
from platypus import NSGAII, GDE3, OMOPSO, SMPSO, SPEA2, EpsMOEA, Problem, Real, EPSILON
from functions import vpp_solve
import os

# more information here: https://platypus.readthedocs.io/en/latest/_modules/platypus/algorithms.html

def optimization_platypus_vpp():
    
    def function_platypus_vpp(vars):
        # each vars[i] give one random number between the minimum and maximum limit for each parameter
        bwl = np.float(vars[0])
        resultados = vpp_solve('main+genoa', 12.041, 10.012, 3.71, bwl, 0.567, -0.346, -0.6, 0.43, 0.77, 0.558, 0.715, 4.5, 0.8, 1.3, 5.674, 0.7, \
        280, 15.1, 4.7, 16.9, 4.3, 1.11, 16.6, 6.45, 1.47, 0.32, 0.688, 0.119, 0.123, \
        14, 1.5, 1.05, 1.85, 0.175, 0.105, 21,\
        '6digit', '6digit', 16.5, 0.185, 0, 0, 0, 0, 0, 0, 0, \
        6, 21)
        
        # count the number of lines to set the index number
        index = sum([len(files) for r, d, files in os.walk("assets/data/vpp_results")])
        if index > 1:
            index = index-1
        
        # export data to csv
        exportdata = [index, format(resultados[0], '.4f'), format(resultados[1], '.4f'), format(resultados[2], '.4f'), 'true']
        with open("assets/data/optimizationvpp.csv", "a") as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(exportdata)
        print(index)
        return resultados[0]

    # optimize for 9 parameters, 2 objectives and 2 restrictions
    problem = Problem(1, 1)
    problem.types[:] = Real(2.5, 3.5)
    problem.function = function_platypus_vpp

    algorithm = NSGAII(problem)
    algorithm.run(15)

    return "ok"