import time, array, random, copy, math
import pandas as pd
import numpy as np
#import networkx                   # genealogic tree
#from networkx.drawing.nx_agraph import graphviz_layout
from math import sqrt
from deap import algorithms, base, creator, gp, benchmarks, tools
from deap.benchmarks.tools import diversity, convergence, hypervolume
from deap.tools import History
import json, codecs
import csv

from functions import vpp_solve

def optimization_deap_appendages():
    ### PARAMATERS
    gaconfig_obj = codecs.open('assets/data/parametersga-appendages.json', 'r', encoding='utf-8').read()
    gaconfig = json.loads(gaconfig_obj)
    weight1 = np.float(gaconfig["weight1"])/10 # velocity
    weight2 = np.float(gaconfig["weight2"])/10 # comfort ratio weight
    windspeedrange = np.array(gaconfig["windspeedrange"])
    windanglerange = np.array(gaconfig["windanglerange"])    
    pop_size = np.int(gaconfig["popsize"])
    children_size = np.int(gaconfig["childrensize"])
    max_gen = np.int(gaconfig["maxgeneration"])
    mut_prob = np.int(gaconfig["mutprob"])/100
    halloffame_number = np.int(gaconfig["halloffamenumber"])
    indpb_value = np.int(gaconfig["indpb"])/100
    eta_value = np.int(gaconfig["eta"])
    gamethod = np.int(gaconfig["gamethod"])      

    limits_obj = codecs.open('assets/data/dimensions-appendages-limits.json', 'r', encoding='utf-8').read()
    limits = json.loads(limits_obj) 
    for item in limits:
        item = str(item)
        if item != "category":
            globals()[item] = np.float(limits[item])
    bound_low1, bound_up1 = badmin, badmax
    bound_low2, bound_up2 = emin, emax
    bound_low3, bound_up3 = ehmmin, ehmmax
    bound_low4, bound_up4 = emdcmin, emdcmax
    bound_low5, bound_up5 = hsrmin, hsrmax
    bound_low6, bound_up6 = imin, imax
    bound_low7, bound_up7 = jmin, jmax
    bound_low8, bound_up8 = lpgmin, lpgmax
    bound_low9, bound_up9 = pmin, pmax
    bound_low10, bound_up10 = rootcKmin, rootcKmax
    bound_low11, bound_up11 = rootcRmin, rootcRmax
    bound_low12, bound_up12 = roottcksKmin, roottcksKmax
    bound_low13, bound_up13 = roottcksRmin, roottcksRmax
    bound_low14, bound_up14 = spanKmin, spanKmax
    bound_low15, bound_up15 = spanRmin, spanRmin
    bound_low16, bound_up16 = splmin, splmax
    bound_low17, bound_up17 = sweepKdegmin, sweepKdegmax
    bound_low18, bound_up18 = sweepRdegmin, sweepRdegmax
    bound_low19, bound_up19 = tipcKmin, tipcKmax
    bound_low20, bound_up20 = tipcRmin, tipcRmax
    bound_low21, bound_up21 = tiptcksKmin, tiptcksKmax
    bound_low22, bound_up22 = tiptcksRmin, tiptcksRmax
    bound_low23, bound_up23 = xceamin, xceamax
      
    NDIM = 2
    random.seed(a = 42)
    savefile="optimizationresistance"
    
    ### BUILD MODEL
    def uniform(low1, up1, low2, up2, low3, up3, low4, up4, low5, up5, low6, up6, low7, up7, low8, up8, low9, up9, low10, up10, low11, up11, low12, up12, low13, up13, low14, up14, low15, up15, low16, up16, low17, up17, low18, up18, low19, up19, low20, up20, low21, up21, low22, up22, low23, up23, size=None):
        return [random.uniform(low1, up1), random.uniform(low2, up2), random.uniform(low3, up3), random.uniform(low4, up4), random.uniform(low5, up5), random.uniform(low6, up6), random.uniform(low7, up7), random.uniform(low8, up8), random.uniform(low9, up9), random.uniform(low10, up10), random.uniform(low11, up11), random.uniform(low12, up12), random.uniform(low13, up13), random.uniform(low14, up14), random.uniform(low15, up15), random.uniform(low16, up16), random.uniform(low17, up17), random.uniform(low18, up18), random.uniform(low19, up19), random.uniform(low20, up20), random.uniform(low21, up21), random.uniform(low22, up22), random.uniform(low23, up23)]
    def evaluate(individual): 
        bad = individual[0]
        esail = individual[1]
        ehm = individual[2]
        emdc = individual[3]
        hsr = individual[4]
        isail = individual[5]
        jsail = individual[6]
        lpg = individual[7]
        psail = individual[8]
        rootcK = individual[9]
        rootcR = individual[10]
        roottcksK = individual[11]
        roottcksR = individual[12]
        spanK = individual[13]
        spanR = individual[14]
        spl = individual[15]
        sweepKdeg = individual[16]
        sweepRdeg = individual[17]
        tipcK = individual[18]
        tipcR = individual[19]
        tiptcksK = individual[20]
        tiptcksR = individual[21]
        xcea = individual[22]
        
        dim_obj = codecs.open('assets/data/dimensions-new.json', 'r', encoding='utf-8').read()
        dim = json.loads(dim_obj) 
        # bwl, disp, lcb, lcf, lwl, tc, sailset
        for item in dim:
            item = str(item)
            if item != "category":
                globals()[item] = np.float(dim[item])
        
        dimapp_obj = codecs.open('assets/data/dimensions-appendages.json', 'r', encoding='utf-8').read()
        dimapp = json.loads(dimapp_obj)
        boa = np.float(dimapp["boa"])
        fb = np.float(dimapp["fb"])
        lr = np.float(dimapp["lr"])
        boa = np.float(dimapp["xcea"])
        fb = np.float(dimapp["mcrew"])
        marcaK = np.float(dimapp["marcaK"])
        marcaR = np.float(dimapp["marcaR"])
        mcrew = np.float(dimapp["mcrew"])

        dimensions = codecs.open('assets/data/dimensions.json', 'r', encoding='utf-8').read()
        dim = json.loads(dimensions)
        cb = np.float(dim["cb"])
        cm = np.float(dim["cm"])
        cp = np.float(dim["cp"])
        cwp = np.float(dim["cwp"])
        scb = np.float(dim["scb"])
        kb = np.float(dim["kb"])
        kg = np.float(dim["kg"])
        itwp = np.float(dim["itwp"])
        GMtrans = np.float(dim["gmt"])
        bmt = np.float(dim["bmt"])
        alcb_coefficient = np.float(dim["alcb_coefficient"])
        awp = bwl*lwl*cwp
        alcb = lwl*alcb_coefficient*tc
        am = cm*bwl*tc
        loa = lwl*1.1
        boa = bwl*1.2
        #vboat = 3
        #heel = 20
        savefile="optimizationvpp"
        results = vpp_solve(sailset, lwl, loa, bwl, tc, disp, lcb, lcf, cb, cm, cp, cwp, awp, alcb, am, boa, scb, kb, kg, itwp, GMtrans, bmt, fb, lr, xcea, mcrew, psail, esail, isail, jsail, bad, spl, lpg, spanR, tipcR, rootcR, tiptcksR, roottcksR, sweepRdeg, spanK, tipcK, rootcK, tiptcksK, roottcksK, sweepKdeg, marcaK, marcaR, ehm, emdc, hsr, savefile)
        f1 = results[0]
        f2 = results[1]

        return f1, f2
    '''
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
                        if avs > 50:	#UPDATE
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
    '''
    creator.create("FitnessMulti", base.Fitness, weights=(weight1, weight2))
    creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMulti) 

    toolbox = base.Toolbox()
    toolbox.register("attr_float", uniform, bound_low1, bound_up1, bound_low2, bound_up2, bound_low3, bound_up3, bound_low4, bound_up4, bound_low5, bound_up5, bound_low6, bound_up6, bound_low7, bound_up7, bound_low8, bound_up8, bound_low9, bound_up9, bound_low10, bound_up10, bound_low11, bound_up11, bound_low12, bound_up12, bound_low13, bound_up13, bound_low14, bound_up14, bound_low15, bound_up15, bound_low16, bound_up16, bound_low17, bound_up17, bound_low18, bound_up18, bound_low19, bound_up19, bound_low20, bound_up20, bound_low21, bound_up21, bound_low22, bound_up22, bound_low23, bound_up23)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_float)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)      
    toolbox.register("evaluate", evaluate)                                                          
    toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=[bound_low1, bound_low2, bound_low3, bound_low4, bound_low5, bound_low6, bound_low7, bound_low8, bound_low9, bound_low10, bound_low11, bound_low12, bound_low13, bound_low14, bound_low15, bound_low16, bound_low17, bound_low18, bound_low19, bound_low20, bound_low21, bound_low22, bound_low23], up=[bound_up1, bound_up2, bound_up3, bound_up4, bound_up5, bound_up6, bound_up7, bound_up8, bound_up9, bound_up10, bound_up11, bound_up12, bound_up13, bound_up14, bound_up15, bound_up16, bound_up17, bound_up18, bound_up19, bound_up20, bound_up21, bound_up22, bound_up23], eta=eta_value)
    toolbox.register("mutate", tools.mutPolynomialBounded, low=[bound_low1, bound_low2, bound_low3, bound_low4, bound_low5, bound_low6, bound_low7, bound_low8, bound_low9, bound_low10, bound_low11, bound_low12, bound_low13, bound_low14, bound_low15, bound_low16, bound_low17, bound_low18, bound_low19, bound_low20, bound_low21, bound_low22, bound_low23], up=[bound_up1, bound_up2, bound_up3, bound_up4, bound_up5, bound_up6, bound_up7, bound_up8, bound_up9, bound_up10, bound_up11, bound_up12, bound_up13, bound_up14, bound_up15, bound_up16, bound_up17, bound_up18, bound_up19, bound_up20, bound_up21, bound_up22, bound_up23], eta=eta_value, indpb=indpb_value)
    if gamethod == 1:
        toolbox.register("select", tools.selNSGA2)
    elif gamethod == 2:
        toolbox.register("select", tools.selSPEA2)

    history = History()
    toolbox.decorate("mate", history.decorator)
    toolbox.decorate("mutate", history.decorator)
    #toolbox.decorate("evaluate", tools.DeltaPenalty(feasible, 99999)

    toolbox.pop_size = pop_size
    toolbox.children_size = children_size
    toolbox.max_gen = max_gen
    toolbox.mut_prob = mut_prob
    hof = tools.HallOfFame(halloffame_number)
    
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
                                        mu=toolbox.pop_size,
                                        lambda_=toolbox.children_size,
                                        cxpb=1-toolbox.mut_prob,
                                        mutpb=toolbox.mut_prob,
                                        stats=mstats,
                                        halloffame=hof,
                                        ngen=toolbox.max_gen,
                                        verbose=False)

    res, logbook = run_ea(toolbox, stats=mstats)
    fronts = tools.emo.sortLogNondominated(res, len(res))

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