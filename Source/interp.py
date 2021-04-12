import math

import bdgmath as m


def linearInterp(t, p0, p1):
    return m.lerp(t, p0, p1)

def cosInterp(t, p0, p1):
    # cVal ranging from 1 to -1 over 0 to 1
    cVal = math.cos(t * math.pi)

    # nCVal ranges from 0 to 1 over 0 to 1
    nCVal = 0.5 - cVal / 2

    return linearInterp(nCVal, p0, p1)
    
