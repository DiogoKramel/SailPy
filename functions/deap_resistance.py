import time, array, random, copy, math
import pandas as pd
import numpy as np
from math import sqrt
from deap import algorithms, base, creator, gp, benchmarks, tools
from deap.benchmarks.tools import diversity, convergence, hypervolume
from deap.tools import History
import json, codecs
import csv

from functions import resistance

def optimization_deap_resistance(lwlmin, lwlmax, bwlmin, bwlmax, tcmin, tcmax, lcfmin, lcfmax, lcbmin, lcbmax, cbmin, cbmax, cwpmin, cwpmax, cpmin, cpmax, cmmin, cmmax, dispmin):
    ### PARAMATERS
    gaconfig_obj = codecs.open('assets/data/parametersga.json', 'r', encoding='utf-8').read()
    gaconfig = json.loads(gaconfig_obj)
    # weight objectives (values) and whether minimized (negative) or maximized (positive)     
    weight1 = np.float(gaconfig["weight1"])*(-1)/10 # resistance weight - multiplied by one to be minimized
    weight2 = np.float(gaconfig["weight2"])/10 # comfort ratio weight
    velocityrange = np.array(gaconfig["velocityrange"])
    heelrange = np.array(gaconfig["heelrange"])

    bound_low1, bound_up1 = lwlmin, lwlmax
    bound_low2, bound_up2 = bwlmin, bwlmax
    bound_low3, bound_up3 = tcmin, tcmax
    bound_low4, bound_up4 = lcfmin, lcfmax
    bound_low5, bound_up5 = lcbmin, lcbmax
    bound_low6, bound_up6 = cbmin, cbmax
    bound_low7, bound_up7 = cwpmin, cwpmax
    bound_low8, bound_up8 = cpmin, cpmax
    bound_low9, bound_up9 = cmmin, cmmax
    
    pop_size = np.int(gaconfig["popsize"])                         # number of the population
    children_size = np.int(gaconfig["childrensize"])               # number of children to produce at each generation
    max_gen = np.int(gaconfig["maxgeneration"])                    # number of times the algorithm is run
    mut_prob = np.int(gaconfig["mutprob"])/100                     # probability of mutation
    halloffame_number = np.int(gaconfig["halloffamenumber"])       # number of best individuals selected 
    indpb_value = np.int(gaconfig["indpb"])/100                    # independent probability for each attribute to be mutated
    eta_value = np.int(gaconfig["eta"])                            # crowding degree of the crossover. A high eta will produce children resembling to their parents, while a small eta will produce solutions much more different
    selectionmethod = np.int(gaconfig["selectionmethod"])
    mutationmethod = np.int(gaconfig["mutationmethod"])
    crossovermethod = np.int(gaconfig["crossovermethod"])
    NDIM = 2                            # numero de dimensoes do problema (objetivos?)
    random.seed(a = 42)					# control randomnesss
    savefile = "optimizationresistance"
    
    ### BUILD MODEL
    def uniform(low1, up1, low2, up2, low3, up3, low4, up4, low5, up5, low6, up6, low7, up7, low8, up8, low9, up9, size=None):         # function to generate the attributes of the initial population
        return [random.uniform(low1, up1), random.uniform(low2, up2), random.uniform(low3, up3), random.uniform(low4, up4), random.uniform(low5, up5), random.uniform(low6, up6), random.uniform(low7, up7), random.uniform(low8, up8), random.uniform(low9, up9)]
    def evaluate(individual):       # calculate the evaluating functions (objetive 1 = f1 and objective = f2)  
        lwl, bwl, tcan, lcf, lcb, cb, cwp, cp, cm = individual[0], individual[1], individual[2], individual[3], individual[4], individual[5], individual[6], individual[7], individual[8]
        divcan = lwl*bwl*tcan*cb
        awp = bwl*lwl*cwp
        
        dimensions = codecs.open('assets/data/dimensions.json', 'r', encoding='utf-8').read()
        dim = json.loads(dimensions)
        alcb_coefficient = np.float(dim["alcb_coefficient"])
        alcb = lwl*alcb_coefficient*tcan
        loa = lwl*1.05
        boa = bwl*1.1
        savefile="optimizationresistance"

        Rt, CR, Rv, Ri, Rr, Rincli, count = 0, 0, 0, 0, 0, 0, 0
        for vboat in range (velocityrange[0], velocityrange[1], 1):
            for heel in range (heelrange[0], heelrange[1], 5):
                result = resistance(lwl, bwl, tcan, alcb, cp, cm, awp, divcan, lcb, lcf, vboat, heel)
                Rt, Rv, Ri, Rr, Rincli, CR, count = Rt+result[0], Rv+result[1], Ri+result[2], Rr+result[3], Rincli+result[4], CR+result[5], count+1
        Rt, CR, Rv, Ri, Rr, Rincli = Rt/count, CR/count, Rv/count, Ri/count, Rr/count, Rincli/count

        f1 = Rt
        f2 = CR

        exportresults(savefile, boa, tcan, divcan, lwl, bwl, awp, lcb, lcf, Rt, Rv, Ri, Rr, Rincli, CR, dispmin)
            
        return f1, f2
    
    def feasible(individual):  
    # https://deap.readthedocs.io/en/master/tutorials/advanced/constraints.html
    # returns true if feasible, false otherwise
    # adicionar um counter para cada violacao
        lwl, bwl, tc, lcf, lcb, cb, cwp, cp, cm = individual[0], individual[1], individual[2], individual[3], individual[4], individual[5], individual[6], individual[7], individual[8]
        
        disp = lwl*bwl*tc*cb
        awp = bwl*lwl*cwp
        boa = bwl*1.2
        loa = lwl*1.05
        dispmass = disp*1025
        cs = boa*3.28084/(dispmass*2.20462/64)**(1/3)   # capsize screening factor
        csmax = 2
        
        if (lwl/bwl) > 5 or (lwl/bwl) < 2.73:
           if (bwl/tc) > 6.5 or (bwl/tc) < 3.8: #(bwl/tcan) > 19.39 or (bwl/tcan) < 2.46 delft series seems to have unrealistic limits
                if (lwl/disp**(1/3)) > 8.5 or (lwl/disp**(1/3)) < 4.34:
                    if (awp/disp**(2/3)) > 12.67 or (awp/disp**(2/3)) < 3.78:
                        if cs > csmax:
                            if disp < dispmin:
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
    
    if crossovermethod == 1:
        toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=[bound_low1, bound_low2, bound_low3, bound_low4, bound_low5, bound_low6, bound_low7, bound_low8, bound_low9], up=[bound_up1, bound_up2, bound_up3, bound_up4, bound_up5, bound_up6, bound_up7, bound_up8, bound_up9], eta=eta_value)
    if crossovermethod == 2:
        toolbox.register("mate", tools.cxOnePoint)
    if crossovermethod == 3:
        toolbox.register("mate", tools.cxTwoPoints)
    if crossovermethod == 4:
        toolbox.register("mate", tools.cxUniform, indpb=indpb_value)
    
    if mutationmethod == 1:
        toolbox.register("mutate", tools.mutPolynomialBounded, low=[bound_low1, bound_low2, bound_low3, bound_low4, bound_low5, bound_low6, bound_low7, bound_low8, bound_low9], up=[bound_up1, bound_up2, bound_up3, bound_up4, bound_up5, bound_up6, bound_up7, bound_up8, bound_up9], eta=eta_value, indpb=indpb_value)
    if mutationmethod == 2:
        toolbox.register("mutate", tools.mutGaussian, mu=[lwl, bwl, tcan, lcf, lcb, cb, cwp, cp, cm], sigma=0.5, indpb=indpb_value)
    
    if selectionmethod == 1:
        toolbox.register("select", tools.selNSGA2)
    elif selectionmethod == 2:
        toolbox.register("select", tools.selSPEA2)

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

    return f1, f2, index

def exportresults(savefile, boa, tcan, divcan, lwl, bwl, awp, lcb, lcf, Rt, Rv, Ri, Rr, Rincli, CR, dispmin):
    rows = []
    with open("assets/data/optimizationresistance.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile) 
        for row in csvreader: 
            rows.append(row)
        index = csvreader.line_num
    print(index)
    
    constraint1, constraint2, constraint3, constraint4, constraint5, constraint6, valid  = False, False, False, False, False, False, False, False
    dispmass = divcan*1025
    cs = boa*3.28084/(dispmass*2.20462/64)**(1/3)

    if (lwl/bwl) > 5 or (lwl/bwl) < 2.73:
        constraint1 = True
    if (bwl/tcan) > 6.5 or (bwl/tcan) < 3.8:
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

    exportdata = [index, format(Rt, '.4f'), format(Rv, '.4f'), format(Ri, '.4f'), format(Rr, '.4f'), format(Rincli, '.4f'), format(CR, '.4f'), format(cs, '.4f'), format(lwl, '.4f'), format(bwl, '.4f'), format(tcan, '.4f'), format(divcan, '.4f'), format(awp, '.4f'), format(lcb, '.4f'), format(lcf, '.4f'), constraint1, constraint2, constraint3, constraint4, constraint5, constraint6, valid]

    with open("assets/data/optimizationresistance.csv", "a") as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(exportdata)
    
    return cs