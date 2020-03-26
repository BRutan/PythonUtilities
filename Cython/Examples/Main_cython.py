##########################################
# Main.py
##########################################
# 

from bs_options import Delta, Gamma, Rho, Theta, Vega, option_price
from math import exp, sqrt
#from options_mc import MonteCarlo
from _optionsmontecarlo_cy import MonteCarlo
from pandas import concat, DataFrame
import numpy as np
from scipy.stats import norm

def GBM_cython(args):
    """
    * Geometric Brownian Motion for Black Scholes asset price evolution 
    process.
    [0, 1, 2, 3, 4, 5, 6, 7]
    [s, rf, q, k, stepsize, t, sig, iid]
    """
    return args[0] * (1 + (args[1] - args[2]) * args[4] + args[6] * args[7] * sqrt(args[4]))

def GBM(**args):
    """
    * Geometric Brownian Motion for Black Scholes asset price evolution 
    process.
    """
    return args['s'] * (1 + (args['rf'] - args['q']) * args['step'] + args['sig'] * args['iid'] * sqrt(args['step']))


def PriceMC(finalSteps, payoff, args):
    return sum([payoff(val, args) for val in finalSteps]) / len(finalSteps)

def EuroCallPayoff(price, args):
    return max(price - args['k'], 0) * exp(-args['rf'] * args['t'])

def EuroPutPayoff(price, args):
    return max(args['k'] - price, 0) * exp(-args['rf'] * args['t'])

def PrintOptionResults(results, filepath):
    first = list(results.keys())[0]
    first = results[first]
    columns = ['Type']
    columns.extend(first.keys())
    output = DataFrame({ key : [] for key in columns })
    for key in columns:
        row = DataFrame({ key : [] for key in columns }) 
        for result in results:
            row[key] = result[key]
        output = concat(output, row)
    output.to_csv(filepath)

def Main():
    """
    * Test MonteCarlo simulation to calculate vanilla European 
    option price and greeks.
    """
    s = 100
    k = 100
    t = 1
    sig = .3
    rf = 0
    q = 0
    numpaths = 1500
    numsteps = 300
    stepsize = t / numsteps
    constArgs_dict = { 's' : s, 'k' : k, 't' : t, 'sig' : sig, 'rf' : rf, 'q' : q, 'step' : stepsize }
    constArgs = np.asarray([s, rf, q, k, stepsize, t, sig, 0], dtype=np.float64)
    test = GBM_cython(constArgs)
    # Calculate analytical results for call and put with parameters:
    trueCallResults = {}
    trueCallResults['price'] = option_price(s, q, t, sig, rf, k, True)
    trueCallResults['delta'] = Delta(s, q, t, sig, rf, k, True)
    trueCallResults['gamma'] = Gamma(s, q, t, sig, rf, k, True)
    trueCallResults['rho'] = Rho(s, q, t, sig, rf, k, True)
    trueCallResults['theta'] = Theta(s, q, t, sig, rf, k, True)
    trueCallResults['vega'] = Vega(s, q, t, sig, rf, k, True)
    truePutResults = {}
    truePutResults['price'] = option_price(s, q, t, sig, rf, k, False)
    truePutResults['delta'] = Delta(s, q, t, sig, rf, k, False)
    truePutResults['gamma'] = Gamma(s, q, t, sig, rf, k, False)
    truePutResults['rho'] = Rho(s, q, t, sig, rf, k, False)
    truePutResults['theta'] = Theta(s, q, t, sig, rf, k, False)
    truePutResults['vega']= Vega(s, q, t, sig, rf, k, False)
    # Calculate Monte Carlo versions of above:
    shiftParams = { 'delta' : 's', 'gamma' : 's', 'rho' : 'r', 'theta' : 't', 'vega' : 'sig' }
    shiftarg = { 'call' : .0001, 'put' : -.0001 }
    mcEsts = { 'call' : {}, 'put' : {} }
    calcTypes = ['price', 'delta', 'gamma', 'rho', 'theta', 'vega']
    payoff = { 'call' : EuroCallPayoff, 'put' : EuroPutPayoff }
    for optType in payoff:
        prev = 0
        denom = 1
        for calcType in calcTypes:
            args = constArgs.copy()
            if calcType == 'gamma':
                # Perform second order estimation:
                prev = mcEsts[optType]['delta']
                args[shiftParams[calcType]] -= shiftarg[optType]
                denom = shiftarg[optType] ** 2
            elif calcType in shiftParams:
                prev = mcEsts[optType]['price']
                args[shiftParams[calcType]] += shiftarg[optType]
                denom = shiftarg[optType]
            optPrice = PriceMC(MonteCarlo(GBM_cython,norm.ppf,0,args,1500,300),payoff[optType],constArgs_dict)
            mcEsts[optType][calcType] = (optPrice - prev) / denom * (-1 if calcType == 'gamma' else 1)
    
    allResults = { 'True Call' : trueCallResults, 'Monte Carlo Call' : mcCallResults, 'True Put' : truePutResults, 'Monte Carlo Put' : mcPutResults }
    PrintOptionResults(allResults, "Results.csv")

if __name__ == '__main__':
    Main()
    PriceKnockouts()