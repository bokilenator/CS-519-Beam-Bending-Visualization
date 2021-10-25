import numpy as np

# Young's modulus constant in Pascal
E = {
    'aluminum': 68.0 * 10**9,
    'wood': 10.0 * 10**9,
    'titanium': 116.0 * 10**9,
    'steel': 200.0 * 10**9,}

error_msg_a = 'Is a between 0 and L?'
error_msg_support_type = 'Invalid support_type'
error_msg_xsection = 'Invalid xsection'

# F: force magnitude in newtons. this is a float.
# x: inspection location, beam deflection at this location, in meters. this is a float.
# material: will affect E (Young's modulus). expected value: 'aluminum', 'wood', 'titanium', 'steel'
# xsection: beam cross section geometry in meters. will affect I. expected value: {'type': 'rectangular', 'b': float, 'h': float}, {'type': 'circle', 'r': float}
# a: force location from left end of beam in meters. this is a float.
# L: total length of beam in meters. this is a float.
# support_type: type of beam support. expected value: 'cantilever', 'simply_supported'

def beam_deflection(F = None, x = None, material = None, xsection = None, a = None, L = None, support_type = None):
    if support_type == 'cantilever':
        if 0.0 <= x < a:
            return (-F * x ** 2 * (3 * a - x)) / (6 * E[material] * calc_I(xsection))
        elif a <= x <= L:
            return (-F * a ** 2 * (3 * x - a)) / (6 * E[material] * calc_I(xsection))
        else:
            raise Exception(error_msg_a)
    elif support_type == 'simply_supported':
        b = (L - a)
        if 0.0 <= x < a:
            return (-F * b * x * (L ** 2 - x ** 2 - (L - a) **2)) / (6 * L * E[material] * calc_I(xsection))
        elif a <= x <= L:
            return (-F * b * ( ((L / b) * (x - a) ** 3) + ((L ** 2 - b ** 2) * x) - (x**3) ) ) / (6 * L * E[material] * calc_I(xsection))
        else:
            raise Exception(error_msg_a)
    else:
        raise Exception(error_msg_support_type)
    
    
def calc_I(xsection = None):
    if xsection['type'] == 'rectangular':
        return (xsection['b'] * xsection['h'] ** 3) / 12
    elif xsection['type'] == 'circle':
        return (np.pi * xsection['r'] ** 4) / 4
    else:
        raise Exception(error_msg_xsection)
    
# print( beam_deflection(F = 113.2, x = 2.3, material = 'aluminum', xsection = {'type': 'rectangular', 'b': 3.2, 'h': 5.3}, a = 5.0, L = 10.0, support_type='cantilever') )
# print( beam_deflection(F = 113.2, x = 2.3, material = 'wood', xsection = {'type': 'circle', 'r': 3.2}, a = 5.0, L = 10.0, support_type='cantilever') )
# print( beam_deflection(F = 113.2, x = 2.3, material = 'steel', xsection = {'type': 'rectangular', 'b': 3.2, 'h': 5.3}, a = 5.0, L = 10.0, support_type='simply_supported') )

def beam_shear_force(F = None, x = None, a = None, L = None, support_type = None):
    if support_type == 'cantilever':
        if 0.0 <= x < L:
            return F
        else:
            raise Exception(error_msg_a)
    elif support_type == 'simply_supported':
        b = L - a
        if 0.0 <= x < a:
            return (F * b) / L
        elif a <= x <= L:
            return (-F * a) / L
        else:
            raise Exception(error_msg_a)
    else:
        raise Exception(error_msg_support_type)
    
# print( beam_shear_force(F = 113.2, x = 2.3, a = 3.2, L = 10.0, support_type='cantilever') )
# print( beam_shear_force(F = 113.2, x = 7.2, a = 7.1, L = 10.0, support_type='cantilever') )
# print( beam_shear_force(F = 113.2, x = 1.3, a = 7.6, L = 10.0, support_type='simply_supported') )
# print( beam_shear_force(F = 113.2, x = 8.1, a = 7.6, L = 10.0, support_type='simply_supported') )
    
def beam_bending_moment(F = None, x = None, a = None, L = None, support_type = None):
    if support_type == 'cantilever':
        return -F * (L - x)
    elif support_type == 'simply_supported':
        b = L - a
        M_max = (F * a * b) / L
        if 0.0 <= x < a:
            return (x / a) * M_max
        elif a <= x <= L:
            return M_max * ( (-(x - a) / b) + 1)
        else:
            raise Exception(error_msg_a)
    else:
        raise Exception(error_msg_support_type)

# print( beam_bending_moment(F = 113.2, x = 0.0, a = 3.2, L = 10.0, support_type='cantilever') )
# print( beam_bending_moment(F = 113.2, x = 5.0, a = 3.2, L = 10.0, support_type='cantilever') )
# print( beam_bending_moment(F = 113.2, x = 10.0, a = 3.2, L = 10.0, support_type='cantilever') )
# print( beam_bending_moment(F = 113.2, x = 0.0, a = 4.3, L = 10.0, support_type='simply_supported') )
# print( beam_bending_moment(F = 113.2, x = 2.0, a = 4.3, L = 10.0, support_type='simply_supported') )
# print( beam_bending_moment(F = 113.2, x = 4.3, a = 4.3, L = 10.0, support_type='simply_supported') )
# print( beam_bending_moment(F = 113.2, x = 5.7, a = 4.3, L = 10.0, support_type='simply_supported') )
# print( beam_bending_moment(F = 113.2, x = 10.0, a = 4.3, L = 10.0, support_type='simply_supported') )