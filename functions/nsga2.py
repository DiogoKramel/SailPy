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

#from SALib.sample import saltelli
#from SALib.analyze import sobol
#from SALib.test_functions import Ishigami

from functions import resistance

def optimize_nsgaII():
    ### PARAMATERS
    gaconfig_obj = codecs.open('data/parametersga.json', 'r', encoding='utf-8').read()
    gaconfig = json.loads(gaconfig_obj)     
    weight1 = np.float(gaconfig["weight1"])
    weight2 = np.float(gaconfig["weight2"])  # weight objectives (values) and whether minimized (negative) or maximized (positive)
    bound_low1, bound_up1 = 10, 11                                  # lwl
    bound_low2, bound_up2 = 2, 3.6                                 # bwl
    bound_low3, bound_up3 = 0.3, 0.4                               	# cb
    bound_low4, bound_up4 = 0.4, 0.8                               # tcan
    bound_low5, bound_up5 = 0.68, 0.71                                 # awp
    bound_low6, bound_up6 = 4, 5                                   # lcf
    bound_low7, bound_up7 = 4, 5                                   # lcb
    bound_low8, bound_up8 = 0.52, 0.6                                   # cp
    bound_low9, bound_up9 = 0.65, 0.78                                   # cm
    pop_size = np.int(gaconfig["popsize"])                         # number of the population
    children_size = np.int(gaconfig["childrensize"])               # number of children to produce at each generation
    max_gen = np.int(gaconfig["maxgeneration"])                    # number of times the algorithm is run
    mut_prob = np.int(gaconfig["mutprob"])/100                     # probability of mutation
    halloffame_number = np.int(gaconfig["halloffamenumber"])   # number of best individuals selected 
    indpb_value = np.int(gaconfig["indpb"])/100                    # independent probability for each attribute to be mutated
    eta_value = np.int(gaconfig["eta"])                            # crowding degree of the crossover. A high eta will produce children resembling to their parents, while a small eta will produce solutions much more different
    NDIM = 2                            # numero de dimensoes do problema (objetivos?)
    random.seed(a=42)
    
    savefile="optimizationresistance"
    ### BUILD MODEL
    def uniform(low1, up1, low2, up2, low3, up3, low4, up4, low5, up5, low6, up6, low7, up7, low8, up8, low9, up9, size=None):         # function to generate the attributes of the initial population
        return [random.uniform(low1, up1), random.uniform(low2, up2), random.uniform(low3, up3), random.uniform(low4, up4), random.uniform(low5, up5), random.uniform(low6, up6), random.uniform(low7, up7), random.uniform(low8, up8), random.uniform(low9, up9)]
    def evaluate(individual):       # calculate the evaluating functions (objetive 1 = f1 and objective = f2)  
        lwl = individual[0]
        bwl = individual[1]
        cb = individual[2]
        tcan = individual[3]
        cwp = individual[4]
        lcf = individual[5]
        lcb = individual[6]
        cp = individual[7]
        cm = individual[8]
        divcan = lwl*bwl*tcan*cb
        awp = bwl*lwl*cwp
        dimensions = codecs.open('data/dimensions.json', 'r', encoding='utf-8').read()
        dim = json.loads(dimensions)
        alcb = np.float(dim["alcb"])
        loa = np.float(dim["loa"])*0.3048
        vboat = 3
        heel = 20
        resist = resistance(lwl, bwl, tcan, alcb, cp, cm, awp, divcan, lcb, lcf, vboat, heel, savefile)
        f1 = resist[0]
        f2 = divcan/(0.65*(0.7*lwl+0.3*loa)*bwl**1.33)
        return f1, f2
    
    def feasible(individual):          # https://deap.readthedocs.io/en/master/tutorials/advanced/constraints.html
    # Feasibility function for the individual. Returns True if feasible False otherwise.
    # Adicionar todas as restricoes de parametrizacao (cb, cp, etc), Capsizing screening formula, motion comfort ratio and angle of vanishing stability
    # adicionar um counter para cada violacao
        lwl = individual[0]
        bwl = individual[1]
        cb = individual[2]
        tc = individual[3]
        cwp = individual[4]
        disp = lwl*bwl*tc*cb
        awp = bwl*lwl*cwp
        if (lwl/bwl) > 5 or (lwl/bwl) < 2.73:
           if (bwl/tc) > 19.39 or (bwl/tc) < 2.46:
                if (lwl/disp**(1/3)) > 8.5 or (lwl/disp**(1/3)) < 4.34:
                    if (awp/disp**(2/3)) > 12.67 or (awp/disp**(2/3)) < 3.78:
                        return True
                    else:
                        return False
                else:
                    return False
           else:
               return False
        else:
           return False

    creator.create("FitnessMulti", base.Fitness, weights=(weight1, weight2))              # create a function and assign the weights
    creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMulti) # define the type of each individual (array, list, ...) and inherit the Fitness attributes

    toolbox = base.Toolbox()
    toolbox.register("attr_float", uniform, bound_low1, bound_up1, bound_low2, bound_up2, bound_low3, bound_up3, bound_low4, bound_up4, bound_low5, bound_up5, bound_low6, bound_up6, bound_low7, bound_up7, bound_low8, bound_up8, bound_low9, bound_up9)               # defines how to create an individual with attributes within the bounds
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_float)       # create the individual
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)                      # create the population in a list
    toolbox.register("evaluate", evaluate)                                                          # defines what is the evaluating function
    toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=[bound_low1, bound_low2, bound_low3, bound_low4, bound_low5, bound_low6, bound_low7, bound_low8, bound_low9], up=[bound_up1, bound_up2, bound_up3, bound_up4, bound_up5, bound_up6, bound_up7, bound_up8, bound_up9], eta=eta_value)
    toolbox.register("mutate", tools.mutPolynomialBounded, low=[bound_low1, bound_low2, bound_low3, bound_low4, bound_low5, bound_low6, bound_low7, bound_low8, bound_low9], up=[bound_up1, bound_up2, bound_up3, bound_up4, bound_up5, bound_up6, bound_up7, bound_up8, bound_up9], eta=eta_value, indpb=indpb_value)
    toolbox.register("select", tools.selNSGA2)
    #toolbox.decorate("evaluate", tools.DeltaPenalty(feasible, 0))      # constraint handler, function and result that is returned

    history = History()                             # store the data to generate the genealogic diagram
    toolbox.decorate("mate", history.decorator)     # store the mate data
    toolbox.decorate("mutate", history.decorator)   # store the mutate data
    toolbox.decorate("evaluate", tools.DeltaPenalty(feasible, 99999))

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
    #best = hof[0]               # best individual  
    #bestfit = hof[0].fitness    # fitness value of the best individual
    
    ### NETWORK
    #h = history.getGenealogy(hof[0], max_depth=10)
    #graph = networkx.DiGraph(h)
    #graph = graph.reverse()     # Make the grah top-down
    #colors = [toolbox.evaluate(history.genealogy_history[i])[0] for i in graph]
    #pos = graphviz_layout(graph, prog="dot")
    #vmin = min(colors)
    #vmax = max(colors)
    #networkx.draw(graph, pos, cmap=plt.cm.get_cmap('summer'), node_color=colors, with_labels=True, vmin=vmin, vmax=vmax)
    #sm = plt.cm.ScalarMappable(cmap=plt.cm.get_cmap('summer'), norm=plt.Normalize(vmin = vmin, vmax=vmax))
    #sm._A = []
    #cb = plt.colorbar(sm)
    #cb.set_label("Fitness")
    #plt.title("Genealogy of the best individual")
    #plt.savefig("data/network.png", bbox_inches='tight',dpi=500)

    ###########cmaps names https://matplotlib.org/examples/color/colormaps_reference.html


    ### SENSITIVITY
    #problem = {
    #'num_vars': 3,
    #'names': ['x1', 'x2', 'x3'],
    #'bounds': [[bound_low1, bound_up1]]*3
    #}
    #param_values = saltelli.sample(problem, 10)    # Generate samples
    #Y = Ishigami.evaluate(param_values)                 # Run model (example)
    #Si = sobol.analyze(problem, Y, print_to_console=True)   # Perform analysis

    ### PLOTS
    par1=[]
    for i, inds in enumerate(fronts):       # two set of values, Im getting only one
        par = [toolbox.evaluate(ind) for ind in inds]
        if i == 0:
            par1 = par
    
    flength=len(history.genealogy_history)
    f1, f2, index = np.zeros(flength), np.zeros(flength), np.zeros(flength)
    for i in range (1, flength):
        f1[i]=np.float(evaluate(history.genealogy_history[i+1])[0])
        f2[i]=np.float(evaluate(history.genealogy_history[i+1])[1])
        index[i]=i
        print(i)

    return f1, f2, index