# A curve interface for drawing fancy stroked curves

import math

import bdgmath as m

class Curve:
    def gen_samples(self):
        pass


class CircularArc(Curve):
    """ construct with a center, a radius, and a degree range.
    0 = East
    90 = North
    """

    def __init__(self, center, radius, degree_min, degree_max):
        self.center = center
        self.radius = radius
        self.degree_range = (degree_min, degree_max)
        assert(degree_min < degree_max)

    def linear_dist_to_degrees(self, d):
        circumference = math.pi * 2 * self.radius
        return 360 * d / circumference

    def gen_samples(self, degree_increment):
        degree_min, degree_max = self.degree_range
        
        d = degree_min
        while d <= degree_max:
            r = math.radians(d)
            x = self.center.x() + math.cos(r) * self.radius
            y = self.center.y() + math.sin(r) * self.radius
            p = m.Vector2(x,y)
            outVec = p.subVec2(self.center).makeUnit()
            forwardVec = m.Vector2(-outVec.y(), outVec.x())
            yield p, forwardVec, outVec

            d += degree_increment

class CubicBezier(Curve):
    """ construct with p0, p1, p2, p3, and it will interpolate p0 and p3 with p1 and p2 as control points"""

    def __init__(self, p0, p1, p2, p3):
        self.points = [p0, p1, p2, p3]

        self.start_to_end_dist = p3.subVec2(p0).mag()

    def step_forward_by_distance(self, last_t, last_point, desired_distance):
        low_t = last_t
        high_t = 1
        low_dist = 0
        high_dist = self.points[3].subVec2(last_point).mag()

        return max(last_t + 0.01, m.mapVal(desired_distance, low_dist, high_dist, low_t, high_t))
    

    def eval(self, t):
        p0, p1, p2, p3 = self.points
        
        oneMinusT = (1 - t)
        oneMinusTSquared = oneMinusT * oneMinusT
        oneMinusTCubed = oneMinusTSquared * oneMinusT

        pt = p0.mulScalar(oneMinusTCubed).addVec2(
            p1.mulScalar(3 * t * oneMinusTSquared)).addVec2(
                p2.mulScalar(3 * t * t * oneMinusT)).addVec2(
                    p3.mulScalar(t * t * t))
        return pt

    def gen_samples(self, linear_increment=1):
        last_point = self.points[0]
        forwardVec = self.points[1].subVec2(self.points[0]).makeUnit()
        rightVec = m.Vector2(forwardVec.y(), -forwardVec.x())
        yield last_point, forwardVec, rightVec

        t = 0

        while t <= 1:
            print("t:", t)
            new_t = self.step_forward_by_distance(t, last_point, linear_increment)

            p = self.eval(new_t)
            forwardVec = self.eval(new_t + 0.1).subVec2(p).makeUnit()
            rightVec = m.Vector2(forwardVec.y(), -forwardVec.x())

            yield p, forwardVec, rightVec
            print(f"p: {p} fwd: {forwardVec} rt:{rightVec}")
            t = new_t
            last_point = p
