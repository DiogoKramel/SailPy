import time, array, random, copy, math
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
#import networkx                   # genealogic tree
#from networkx.drawing.nx_agraph import graphviz_layout
from math import sqrt
from deap import algorithms, base, creator, gp, benchmarks, tools
from deap.benchmarks.tools import diversity, convergence, hypervolume
from deap.tools import History
import json, codecs
import csv

from functions import resistance

def optimize_nsgaII():
    ### PARAMATERS
    gaconfig_obj = codecs.open('assets/data/parametersga.json', 'r', encoding='utf-8').read()
    gaconfig = json.loads(gaconfig_obj)
    # weight objectives (values) and whether minimized (negative) or maximized (positive)     
    weight1 = np.float(gaconfig["weight1"])*(-1)/10 # resistance weight - multiplied by one to be minimized
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
    print(weight2)
    bound_low6, bound_up6 = 0.3, 0.4                               # cb
    bound_low7, bound_up7 = 0.68, 0.71                             # cwp
    bound_low8, bound_up8 = 0.52, 0.6                              # cp
    bound_low9, bound_up9 = 0.65, 0.78                             # cm
    velocityrange = np.array(gaconfig["velocityrange"])
    heelrange = np.array(gaconfig["heelrange"])    
    pop_size = np.int(gaconfig["popsize"])                         # number of the population
    children_size = np.int(gaconfig["childrensize"])               # number of children to produce at each generation
    max_gen = np.int(gaconfig["maxgeneration"])                    # number of times the algorithm is run
    mut_prob = np.int(gaconfig["mutprob"])/100                     # probability of mutation
    halloffame_number = np.int(gaconfig["halloffamenumber"])       # number of best individuals selected 
    indpb_value = np.int(gaconfig["indpb"])/100                    # independent probability for each attribute to be mutated
    eta_value = np.int(gaconfig["eta"])                            # crowding degree of the crossover. A high eta will produce children resembling to their parents, while a small eta will produce solutions much more different
    NDIM = 2                            # numero de dimensoes do problema (objetivos?)
    random.seed(a = 42)					# control randomnesss
    savefile="optimizationresistance"
    
    ### BUILD MODEL
    def uniform(low1, up1, low2, up2, low3, up3, low4, up4, low5, up5, low6, up6, low7, up7, low8, up8, low9, up9, size=None):         # function to generate the attributes of the initial population
        return [random.uniform(low1, up1), random.uniform(low2, up2), random.uniform(low3, up3), random.uniform(low4, up4), random.uniform(low5, up5), random.uniform(low6, up6), random.uniform(low7, up7), random.uniform(low8, up8), random.uniform(low9, up9)]
    def evaluate(individual):       # calculate the evaluating functions (objetive 1 = f1 and objective = f2)  
        lwl = individual[0]
        bwl = individual[1]
        tcan = individual[2]
        lcf = individual[3]
        lcb = individual[4]
        cb = individual[5]
        cwp = individual[6]
        cp = individual[7]
        cm = individual[8]
        divcan = lwl*bwl*tcan*cb
        awp = bwl*lwl*cwp
        dimensions = codecs.open('assets/data/dimensions.json', 'r', encoding='utf-8').read()
        dim = json.loads(dimensions)
        alcb_coefficient = np.float(dim["alcb_coefficient"])
        alcb = lwl*alcb_coefficient*tcan
        loa = lwl*1.1
        boa = bwl*1.2
        #alcb = np.float(dim["alcb"])
        #loa = np.float(dim["loa"])*0.3048
        #resistance_total = 0
        #for i in range (velocityrange[0], velocityrange[1]+1):
        #    for j in range (heelrange[0], heelrange[1]+1):
        #f1 = resistance(lwl, bwl, tcan, alcb, cp, cm, awp, divcan, lcb, lcf, np.float(velocityrange[0]), np.float(heelrange[0]), savefile)
        vboat = 3
        heel = 20
        savefile="optimizationresistance"
        resist = resistance(lwl, bwl, tcan, alcb, cp, cm, awp, divcan, lcb, lcf, vboat, heel, savefile)
        f1 = resist[0]
        f2 = divcan*1025*2.20462/((boa*3.28084)**(4/3)*0.65*(0.7*lwl*3.28084+0.3*loa*3.28084))  #motion comfort ratio
        print(f2)
        #f2 = divcan/(0.65*(0.7*lwl+0.3*loa)*bwl**1.33)
        return f1, f2
    
    def feasible(individual):  
    # https://deap.readthedocs.io/en/master/tutorials/advanced/constraints.html
    # returns true if feasible, false otherwise
    # adicionar um counter para cada violacao
        lwl = individual[0]
        bwl = individual[1]
        cb = individual[5]
        tc = individual[2]
        cwp = individual[6]
        disp = lwl*bwl*tc*cb
        awp = bwl*lwl*cwp
        br = 40		# between 28 and 56
        boa = bwl*1.2
        loa = lwl*1.05
        dispmass = disp*1025
        ssv = boa**2/(br*tc*disp**(1/3))       
        avs = 110+(400/(ssv-10)) 						# angle of vanishing stability
        cs = boa*3.28084/(dispmass*2.20462/64)**(1/3)   # capsize screening factor
        
        if (lwl/bwl) > 5 or (lwl/bwl) < 2.73:
           if (bwl/tc) > 19.39 or (bwl/tc) < 2.46:
                if (lwl/disp**(1/3)) > 8.5 or (lwl/disp**(1/3)) < 4.34:
                    if (awp/disp**(2/3)) > 12.67 or (awp/disp**(2/3)) < 3.78:
                        if avs > 110:
                            if cs < 2:
                                return True
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
           else:
               return False
        else:
           return False

    # create a function and assign the weights
    creator.create("FitnessMulti", base.Fitness, weights=(weight1, weight2))
    # define the type of each individual (array, list, ...) and inherit the Fitness attributes
    creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMulti) 

    toolbox = base.Toolbox()
    toolbox.register("attr_float", uniform, bound_low1, bound_up1, bound_low2, bound_up2, bound_low3, bound_up3, bound_low4, bound_up4, bound_low5, bound_up5, bound_low6, bound_up6, bound_low7, bound_up7, bound_low8, bound_up8, bound_low9, bound_up9)               # defines how to create an individual with attributes within the bounds
    # create the individual
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_float)       
    # create the population in a list
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)  
    # defines what is the evaluating function                    
    toolbox.register("evaluate", evaluate)                                                          
    toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=[bound_low1, bound_low2, bound_low3, bound_low4, bound_low5, bound_low6, bound_low7, bound_low8, bound_low9], up=[bound_up1, bound_up2, bound_up3, bound_up4, bound_up5, bound_up6, bound_up7, bound_up8, bound_up9], eta=eta_value)
    toolbox.register("mutate", tools.mutPolynomialBounded, low=[bound_low1, bound_low2, bound_low3, bound_low4, bound_low5, bound_low6, bound_low7, bound_low8, bound_low9], up=[bound_up1, bound_up2, bound_up3, bound_up4, bound_up5, bound_up6, bound_up7, bound_up8, bound_up9], eta=eta_value, indpb=indpb_value)
    toolbox.register("select", tools.selNSGA2)   

    history = History()                             # store the data to generate the genealogic diagram
    toolbox.decorate("mate", history.decorator)     # store the mate data
    toolbox.decorate("mutate", history.decorator)   # store the mutate data
    toolbox.decorate("evaluate", tools.DeltaPenalty(feasible, 99999)) # constraint handler, function and result that is returned

    toolbox.pop_size = pop_size                     # number of the population
    toolbox.children_size = children_size           # number of children to produce at each generation
    toolbox.max_gen = max_gen                       # number of times the algorithm is run
    toolbox.mut_prob = mut_prob                     # probability of mutation
    hof = tools.HallOfFame(halloffame_number)       # number of best individuals selected 
    
    stats_fit = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(key=len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", np.mean, axis=0)
    mstats.register("std", np.std, axis=0)
    mstats.register("min", np.min, axis=0)
    mstats.register("max", np.max, axis=0)

    logbook = tools.Logbook()
    logbook.header = "gen", "evals", "fitness", "size"
    logbook.chapters["fitness"].header = "std", "min", "avg", "max", 
    logbook.chapters["size"].header = "min", "avg", "max"

    ### RUN MODEL
    def run_ea(toolbox, stats=mstats, verbose=False):
        pop = toolbox.population(n=toolbox.pop_size)
        history.update(pop)
        pop = toolbox.select(pop, len(pop))
        return algorithms.eaMuPlusLambda(pop, toolbox, 
                                        mu=toolbox.pop_size,        # number of individuals to select for the next generation
                                        lambda_=toolbox.children_size,   # number of children to produce at each generation
                                        cxpb=1-toolbox.mut_prob,    # probability that an offspring is produced by crossover
                                        mutpb=toolbox.mut_prob,     # probability that an offspring is produced by mutation
                                        stats=mstats,
                                        halloffame=hof,             # contain the best individuals
                                        ngen=toolbox.max_gen,       # number of generation (em bom portugues: ciclos, loops, iteracoes...)
                                        verbose=False)            # print or not

    res, logbook = run_ea(toolbox, stats=mstats)					# res: ultima populacao gerada
    fronts = tools.emo.sortLogNondominated(res, len(res))           # fronts: pareto otimo desta ultima populacao
    
    ### PLOTS
    par1=[]
    for i, inds in enumerate(fronts):       # two set of values, Im getting only one
        par = [toolbox.evaluate(ind) for ind in inds]
        if i == 0:
            par1 = par
    
    flength=len(history.genealogy_history)
    f1, f2, index = np.zeros(flength), np.zeros(flength), np.zeros(flength)
    x1, x2, x3, x4, x5, x6, x7 = np.zeros(len(res)), np.zeros(len(res)), np.zeros(len(res)), np.zeros(len(res)), np.zeros(len(res)), np.zeros(len(res)), np.zeros(len(res))
    for i in range (1, flength):
        f1[i]=np.float(evaluate(history.genealogy_history[i+1])[0])
        f2[i]=np.float(evaluate(history.genealogy_history[i+1])[1])
        index[i]=i
        print(i)

    return f1, f2, index