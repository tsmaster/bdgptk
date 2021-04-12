# a Signed Distance Field (SDF) for circles

class Circle:
    def __init__(self, pos, r):
        self.pos = pos
        self.radius = r
        self.material = None
        self.color = None

    def signedDistance(self, point):
        d = point.subVec2(self.pos)
        return d.mag() - self.radius
