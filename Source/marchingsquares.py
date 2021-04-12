import math
import drawSvg as draw

import bdgmath as m


class SampleGrid:
    def __init__(self, minX, minY, maxX, maxY, step_size, sample_func):
        self.minX = minX
        self.minY = minY
        self.maxX = maxX
        self.maxY = maxY
        self.stepSize = step_size
        self.sample_func = sample_func
        self.maxDist = 0
        self.sample()

    def samplePtToWorldPt(self, sx, sy):
        x = sx * self.stepSize + self.minX
        y = sy * self.stepSize + self.minY
        return m.Vector2(x, y)

    def sample(self):
        self.samples = {}
        sx = 0
        x = sx * self.stepSize + self.minX
        while x <= self.maxX:
            sy = 0
            y = sy * self.stepSize + self.minY
            while y <= self.maxY:
                dist = self.sample_func(m.Vector2(x,y))
                self.samples[(sx, sy)] = dist

                self.maxDist = max(self.maxDist, dist)
    
                sy += 1
                y = sy * self.stepSize + self.minY
            sx += 1
            x = sx * self.stepSize + self.minX

        #print(f"max sampled dist: {self.maxDist}")
            
    
def drawMarchingSquares(sg, ep, d):
    keys = list(sg.samples.keys())
    keys.sort()
                
    for sx, sy in keys:
        sx1 = sx + 1
        sy1 = sy + 1
        if not ((sx1, sy1) in sg.samples):
            continue

        ll = sg.samples[(sx, sy)]
        lr = sg.samples[(sx1, sy)]
        ul = sg.samples[(sx, sy1)]
        ur = sg.samples[(sx1, sy1)]

        vals = [ll, lr, ul, ur]
        if (all([v > d for v in vals]) or
            all([v < d for v in vals])):
            continue

        #print(f"found crossing {ll} {lr} {ul} {ur}")

        crossings = []

        llx, lly = sg.samplePtToWorldPt(sx, sy).components
        lrx, lry = sg.samplePtToWorldPt(sx1, sy).components
        ulx, uly = sg.samplePtToWorldPt(sx, sy1).components
        urx, ury = sg.samplePtToWorldPt(sx1, sy1).components

        if ((ll < d and lr < d) or
            (ll > d and lr > d)):
            pass
        else:
            crossX = m.mapVal(d, ll, lr, llx, lrx)
            crossY = lly
            crossings.append(m.Vector2(crossX, crossY))

        if ((ll < d and ul < d) or
            (ll > d and ul > d)):
            pass
        else:
            crossY = m.mapVal(d, ll, ul, lly, uly)
            crossX = llx
            crossings.append(m.Vector2(crossX, crossY))
        
        if ((ul < d and ur < d) or
            (ul > d and ur > d)):
            pass
        else:
            crossX = m.mapVal(d, ul, ur, ulx, urx)
            crossY = uly
            crossings.append(m.Vector2(crossX, crossY))

        if ((lr < d and ur < d) or
            (lr > d and ur > d)):
            pass
        else:
            crossY = m.mapVal(d, lr, ur, lry, ury)
            crossX = lrx
            crossings.append(m.Vector2(crossX, crossY))

        if len(crossings) == 4:
            ep.addEdge((crossings[2], crossings[3]))            
        if len(crossings) >= 2:
            ep.addEdge((crossings[0], crossings[1]))
            
        
            
