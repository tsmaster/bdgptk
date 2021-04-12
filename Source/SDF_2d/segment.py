# a Signed Distance Field (SDF) for segments

# https://www.iquilezles.org/www/articles/distfunctions2d/distfunctions2d.htm

import math
import bdgmath as m

class Segment:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def signedDistance(self, point):
        pa = point.subVec2(self.a)
        ba = self.b.subVec2(self.a)
        h = m.clamp( pa.dot2dVector2(ba) / ba.dot2dVector2(ba), 0.0, 1.0 )
        return pa.subVec2(ba.mulScalar(h)).mag()
