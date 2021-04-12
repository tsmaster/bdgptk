import math
import random
import drawSvg as draw

import bdgmath as m
import drawutil


def getSkinToneRGBBytes():
    # from https://colorswall.com/palette/2513/
    colors = [(197, 140, 133),
              (236, 188, 180),
              (209, 163, 164),
              (161, 102, 94),
              (80, 51, 53),
              (89, 47, 42)]

    t = random.uniform(0, len(colors)-1)
    c0 = math.floor(t)
    c1 = c0 + 1
    frac = t - c0

    #print(f"c0 {c0} c1 {c1} t {t} frac {frac}")
    skinCol = [m.clamp(round(m.lerp(t, colors[c0][idx], colors[c1][idx])), 0, 255) for idx in range(3)]

    return tuple(skinCol)


class Person():
    def __init__(self, pos, median_height = 110, height_radius = 10):
        self.pos = pos

        self.height = median_height + random.uniform(-height_radius, height_radius)
        self.headDiameter = self.height / random.uniform(2.8, 3.2)
        self.headRadius = self.headDiameter / 2
        self.headCenterY = pos.y() + self.height - self.headRadius

        headRed, headGreen, headBlue = getSkinToneRGBBytes()
        self.headColorString = "#%02X%02X%02X" % (headRed, headGreen, headBlue)
        self.bodyLength = self.height / random.uniform(2.8, 3.2)
        self.neckY = self.headCenterY - self.headRadius
        self.pelvisY = self.neckY - self.bodyLength

        self.halfLegWidth = self.headRadius * random.uniform(0.9, 1.1)
        
        self.armSpread = self.headRadius * random.uniform(1.4, 1.6)
        self.leftHandLift = self.armSpread * random.uniform(-0.3, 0.2)
        self.rightHandLift = self.armSpread * random.uniform(-0.3, 0.2)
        self.shoulderY = self.neckY - self.bodyLength / random.uniform(1.9, 2.1)
        

    def draw(self, dwg):
        x,y = self.pos.components
        
        dwg.append(draw.Circle(x,
                               self.headCenterY,
                               self.headRadius,
                               fill = self.headColorString,
                               stroke_width=4, stroke='black'))
        
        p = draw.Path(stroke_width = 4, stroke='black')
        p.M(x, self.neckY)
        p.L(x, self.pelvisY)
        dwg.append(p)

        p = draw.Path(stroke_width = 4, stroke = 'black', fill='none')
        p.M(x - self.halfLegWidth, y)
        p.L(x, self.pelvisY)
        p.L(x + self.halfLegWidth, y)
        dwg.append(p)

        p = draw.Path(stroke_width = 4, stroke = 'black', fill='none')
        p.M(x - self.armSpread, self.shoulderY + self.leftHandLift)
        p.L(x, self.shoulderY)
        p.L(x + self.armSpread, self.shoulderY + self.rightHandLift)
        dwg.append(p)

        #self.drawBB(dwg)

    def drawBB(self, dwg):
        pos1, pos2 = self.getBB()
        dx = pos2.x() - pos1.x()
        dy = pos2.y() - pos1.y()

        dwg.append(draw.Rectangle(pos1.x(), pos1.y(),
                                  dx, dy,
                                  fill = 'none',
                                  stroke = 'red',
                                  stroke_width = 2))

        dwg.append(draw.Circle(self.pos.x(),
                               self.pos.y(),
                               4,
                               fill='blue',
                               stroke = 'none'))

    def getBB(self):

        px, py = self.pos.components
        
        minPos = m.Vector2(px - self.armSpread, py)
        maxPos = m.Vector2(px + self.armSpread, py + self.height)

        return (minPos, maxPos)

    
        
