import math
import random

import bdgmath as m

# see "Maximal Poisson disk Sampling: An Improved Version of Bridson's Algorithm"
# http://extremelearning.com.au/an-improved-version-of-bridsons-algorithm-n-for-poisson-disc-sampling/
# and for the original Bridson paper: https://www.cs.ubc.ca/~rbridson/docs/bridson-siggraph07-poissondisk.pdf
    
class BlueNoiseGrid:
    def __init__(self, r, xMin, yMin, xMax, yMax, k):
        """
        r = radius
        x/y Min/Max = bounds
        k = number of points to try to place
        """
        self.radius = r
        self.xMin = xMin
        self.yMin = yMin
        self.xMax = xMax
        self.yMax = yMax
        self.k = k

        # the "grid"
        self.points = {}

        # I could conceivably extend this, but for now, always 2
        self.numDimensions = 2
        
        self.cellSize = r / math.sqrt(self.numDimensions)
        
        self.generatePoints()

    def findClosestKey(self, pt):
        closestDist = None
        closestKey = None
        
        for k in self.findGridPointsInRadius(pt, 2 * self.cellSize):
            kPt = self.points[k]
            dist = kPt.subVec2(pt).mag()
            
            if ((closestKey is None) or
                (dist < closestDist)):
                closestDist = dist
                closestKey = k
        if not (closestKey is None):
            return closestKey

        for k in self.points.keys():
            kPt = self.points[k]
            dist = kPt.subVec2(pt).mag()
            
            if ((closestKey is None) or
                (dist < closestDist)):
                closestDist = dist
                closestKey = k

        return closestKey
            

    def insertPointInGrid(self, pt):
        xi = math.floor(pt.x() / self.cellSize)
        yi = math.floor(pt.y() / self.cellSize)

        key = (xi, yi)

        assert (not (key in self.points.keys()))
        self.points[key] = pt
        return key

    def generateCandidateNeighbors(self, pt):
        epsilon = 1e-8

        rPlusE = self.radius + epsilon

        startFrac = random.uniform(0, 1)

        xP, yP = pt.components

        for j in range(0, self.k):
            theta = 2 * math.pi * (startFrac + j / self.k)

            x = xP + rPlusE * math.cos(theta)
            y = yP + rPlusE * math.sin(theta)

            if ((x >= self.xMin) and
                (y >= self.yMin) and
                (x <= self.xMax) and
                (y <= self.yMax)):
                c = m.Vector2(x,y)
                yield c

    def hasGridPointInRadius(self, pt, radius):
        # is there a more idiomatic way to do this?
        for otherPoint in self.findGridPointsInRadius(pt, radius):
            return True
        return False

    def findGridPointsInRadius(self, pt, r):
        px, py = pt.components
        #print(f"looking for grid points at radius {r} from point {px},{py}")
        
        xMinIndex = math.floor((px - r) / self.cellSize)
        yMinIndex = math.floor((py - r) / self.cellSize)
        xMaxIndex = math.ceil((px + r) / self.cellSize)
        yMaxIndex = math.ceil((py + r) / self.cellSize)

        #print(f"min {xMinIndex}, {yMinIndex} max {xMaxIndex}, {yMaxIndex}")

        rSqr = r * r

        for x in range(xMinIndex, xMaxIndex + 1):
            for y in range(yMinIndex, yMaxIndex + 1):
                probeKey = (x,y)
                #print ("looking for probeKey", probeKey)
                if probeKey in self.points.keys():
                    pV = self.points[probeKey]
                    #print(f"found probeKey vec: {pV}")
                    magSqr = pV.subVec2(pt).magsqr()
                    #print(f"magsqr: {magSqr} rSqr: {rSqr}")
                    if magSqr < rSqr:
                        #print("yielding {probeKey}")
                        yield probeKey
    
    def generatePoints(self):
        x0 = (self.xMin +self.xMax) / 2
        y0 = (self.yMin +self.yMax) / 2

        v0 = m.Vector2(x0, y0)
        key0 = self.insertPointInGrid(v0)

        activeList = [key0]
        
        while activeList:
            key = activeList.pop(random.randrange(0, len(activeList)))

            for c in self.generateCandidateNeighbors(self.points[key]):
                if not (self.hasGridPointInRadius(c, self.radius)):
                    newKey = self.insertPointInGrid(c)
                    activeList.append(newKey)
                    
            
def makeColorString(redByte, greenByte, blueByte):
    return "#%02x%02x%02x" % (redByte, greenByte, blueByte)





if __name__ == "__main__":
    import drawSvg as draw
    import drawutil

    from PIL import Image
    im = Image.open("self-portrait.png").convert("RGB").resize((1000, 1000))
    

    for frameNum in range(100):
            
        #dwg = draw.Drawing(1000, 1000, origin = 'center')
        dwg = draw.Drawing(1000, 1000)
        dwg.setRenderSize("100mm", "100mm")
    
        bng = BlueNoiseGrid(20, 0, 0, 1000, 1000, 30)
    
        for key, pt in bng.points.items():
            #print(f"key: {key} pt: {pt}")
    
            #red = random.randrange(0, 256)
            #green = random.randrange(0, 256)
            #blue = random.randrange(0, 256)
    
            xi = round(pt.x())
            yi = 1000 - round(pt.y())
    
            try:
                pixel = im.getpixel((xi, yi))
                red, green, blue = pixel
            except IndexError as ie:
                red, green, blue = 0, 0, 0
    
            fillColor = makeColorString(red, green, blue)
            
            dwg.append(draw.Circle(pt.x(),
                                   pt.y(),
                                   14,
                                   fill = fillColor,
                                   stroke_width = 1,
                                   stroke = 'none'))
    
        dwg.saveSvg("bridson.svg")
        dwg.savePng("brid_frame_%04d.png" % frameNum)


