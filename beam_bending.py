# F: force magnitude in newtons. this is a float.
# x: inspection location, beam deflection at this location, in meters. this is a float.
# material: will affect E (Young's modulus). expected value: 'aluminum', 'wood', 'titanium', 'steel'
# xsection: beam cross section geometry in meters. will affect I. expected value: {type: 'rectangular', b: float, h: float}, {type: 'rectangular', r: float}
# a: force location from left end of beam in meters. this is a float.
# L: total length of beam in meters. this is a float.

def beam_deflection(F, x, material, xsection, a, L):
    pass