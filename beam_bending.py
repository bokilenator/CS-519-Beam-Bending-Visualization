import numpy as np

# Young's modulus constant in Pascal
E = {
    'aluminum': 68.0 * 10**9,
    'wood': 10.0 * 10**9,
    'titanium': 116.0 * 10**9,
    'steel': 200.0 * 10**9,}

# F: force magnitude in newtons. this is a float.
# x: inspection location, beam deflection at this location, in meters. this is a float.
# material: will affect E (Young's modulus). expected value: 'aluminum', 'wood', 'titanium', 'steel'
# xsection: beam cross section geometry in meters. will affect I. expected value: {'type': 'rectangular', 'b': float, 'h': float}, {'type': 'circle', 'r': float}
# a: force location from left end of beam in meters. this is a float.
# L: total length of beam in meters. this is a float.
# support_type: type of beam support. expected value: 'cantilever', 'simply_supported'

def beam_deflection(F = 0.0, x = 0.0, material = 'aluminum', xsection = {'type': 'rectangular', 'b': 1.0, 'h': 1.0}, a = 0.0, L = 0.0, support_type = 'cantilever'):
    if support_type == 'cantilever':
        if 0 <= x < a:
            return (-F * x ** 2 * (3 * a - x)) / (6 * E[material] * calc_I(xsection))
        elif a <= x <= L:
            return (-F * a ** 2 * (3 * x - a)) / (6 * E[material] * calc_I(xsection))
    
    
def calc_I(xsection = {'type': 'rectangular', 'b': 1.0, 'h': 1.0}):
    if xsection['type'] == 'rectangular':
        return (xsection['b'] * xsection['h'] ** 3) / 12
    elif xsection['type'] == 'circle':
        return (np.pi * xsection['r'] ** 4) / 4