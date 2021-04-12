# a Signed Distance Field (SDF) for triangles

# https://www.iquilezles.org/www/articles/distfunctions2d/distfunctions2d.htm

import math
import bdgmath as m

class Triangle:
    def __init__(self, p0, p1, p2):
        self.points = [p0, p1, p2]
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2

    def signedDistance(self, point):
        e0 = self.p1.subVec2(self.p0)
        e1 = self.p2.subVec2(self.p1)
        e2 = self.p0.subVec2(self.p2)

        v0 = point.subVec2(self.p0)
        v1 = point.subVec2(self.p1)
        v2 = point.subVec2(self.p2)

        pq0 = v0.subVec2(e0.mulScalar(m.clamp(
            v0.dot2dVector2(e0)/e0.dot2dVector2(e0), 0, 1)))
        pq1 = v1.subVec2(e1.mulScalar(m.clamp(
            v1.dot2dVector2(e1)/e1.dot2dVector2(e1), 0, 1)))
        pq2 = v2.subVec2(e2.mulScalar(m.clamp(
            v2.dot2dVector2(e2)/e2.dot2dVector2(e2), 0, 1)))

        s = m.sign(e0.x() * e2.y() - e0.y() * e2.x())
        
        a = m.Vector2(pq0.dot2dVector2(pq0), s * (v0.x() * e0.y() - v0.y() * e0.x()))
        b = m.Vector2(pq1.dot2dVector2(pq1), s * (v1.x() * e1.y() - v1.y() * e1.x()))
        c = m.Vector2(pq2.dot2dVector2(pq2), s * (v2.x() * e2.y() - v2.y() * e2.x()))

        d = a.min(b).min(c)
        
        return -math.sqrt(d.x())*m.sign(d.y());
