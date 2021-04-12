import math
import bdgmath as m

def axialFromPixel(pt, size):
    q = (math.sqrt(3) * pt.x() / 3 - pt.y() /3) / size
    r = (2 * pt.y() / 3) / size
    ax = AxialCoord(q, r)
    return ax.axRound()

def cubeFromPixel(pt, size):
    q = (math.sqrt(3) * pt.x() / 3 - pt.y() /3) / size
    r = (2 * pt.y() / 3) / size
    ax = AxialCoord(q, r)
    cube = ax.toCube()
    return cube.cubeRound()

class AxialCoord:
    def __init__(self, q, r):
        self.coordinates = (q,r)

    def q(self):
        return self.coordinates[0]

    def r(self):
        return self.coordinates[1]

    def toCube(self):
        x = self.q()
        z = self.r()
        y = -x-z
        return CubeCoord(x,y,z)

    def toPixel(self, size):
        x = size * (math.sqrt(3) * self.q() + math.sqrt(3) * self.r() / 2)
        y = size * (3 * self.r() / 2)
        return m.Vector2(x, y)

    def axRound(self):
        cube = self.toCube()
        roundedCube = cube.cubeRound()
        return roundedCube.toAxial()


class CubeCoord:
    def __init__(self, x, y, z):
        self.coordinates = (x,y,z)
        s = sum(self.coordinates)
        if not (s == 0):
            print("making cubeCoordinate with x {x} y {y} z {z}")
            assert(s == 0)

    def x(self):
        return self.coordinates[0]

    def y(self):
        return self.coordinates[1]

    def z(self):
        return self.coordinates[2]

    def equal(self, other):
        return ((self.x() == other.x()) and
                (self.y() == other.y()) and
                (self.z() == other.z()))

    def toAxial(self):
        q = self.x()
        r = self.z()

        return AxialCoord(q, r)

    def toPixel(self, size):
        ax = self.toAxial()
        return ax.toPixel(size)

    def cubeRound(self):
        rx = round(self.x())
        ry = round(self.y())
        rz = round(self.z())

        x_diff = abs(rx - self.x())
        y_diff = abs(ry - self.y())
        z_diff = abs(rz - self.z())

        if x_diff > y_diff and x_diff > z_diff:
            rx = -ry - rz
        elif y_diff > z_diff:
            ry = -rx - rz
        else:
            rz = -rx - ry

        return CubeCoord(rx, ry, rz)

    def add(self, other):
        return CubeCoord(self.x() + other.x(),
                         self.y() + other.y(),
                         self.z() + other.z())

    def scale(self, scalar):
        return CubeCoord(self.x() * scalar,
                         self.y() * scalar,
                         self.z() * scalar)

    def neighbor(self, d):
        return self.add(cubeDirection(d))

    def __str__(self):
        return "C<%d, %d, %d>"%self.coordinates

def cubeDirection(d):
    units = [CubeCoord(1, -1, 0), # east
             CubeCoord(1, 0, -1), # ne
             CubeCoord(0, 1, -1), # nw
             CubeCoord(-1, 1, 0), # west
             CubeCoord(-1, 0, 1), # sw
             CubeCoord(0, -1, 1)] # se

    return units[d]

def genCubeRingPoints(center, radius):
    if radius == 0:
        yield center
        return

    curCube = center.add(cubeDirection(4).scale(radius))

    for side in range(6):
        for step in range(radius):
            yield curCube
            curCube = curCube.neighbor(side)

def genCubeSpiralPoints(center, radius):
    for i in range(radius + 1):
        yield from genCubeRingPoints(center, i)

def cubeDistance(a, b):
    return (abs(a.x() - b.x()) +
            abs(a.y() - b.y()) +
            abs(a.z() - b.z())) // 2
