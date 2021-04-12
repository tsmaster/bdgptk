import math
import bdgmath as m
import drawSvg as draw

###
# TODO
# add a vertex dictionary, with a "toKey" method
# def toKey(Vector2) -> hashableTuple
# this should speed up insertVert
#
# when picking a path to add a segment to, collect many (all?) legal previous paths,
# and prefer the one that is currently longest
#
# when yielding the paths, do so in sorted (x-start?) order, potentially flipping paths
# end-to-end so that the end that's lower in x is the preferred start point

EPSILON = 10e-2

class EdgePool:
    def __init__(self):
        # list of world vertices
        self.vertices = []

        # list of lists of vertex indices
        self.paths = []

        self.connectedVerts = []
        

    def getPath(self, vertIndex, atEnd):
        for pi, p in enumerate(self.paths):
            #print(f"checking path {pi} {p}")
            if p[0] == vertIndex:
                self.paths.pop(pi)
                if atEnd:
                    p.reverse()
                return p
            if p[-1] == vertIndex:
                self.paths.pop(pi)
                if not atEnd:
                    p.reverse()
                return p
        return None

    def insertVert(self, v):
        for oi, other in enumerate(self.vertices):
            d = v.subVec2(other).mag()

            if d < EPSILON:
                return oi
        self.vertices.append(v)
        return len(self.vertices) - 1

    def addEdge(self, seg):
        v0, v1 = seg
        v0i = self.insertVert(v0)
        v1i = self.insertVert(v1)

        indexTuple = (min(v0i, v1i), max(v0i, v1i))
        if indexTuple in self.connectedVerts:
            return
        self.connectedVerts.append(indexTuple)

        #print(f"adding edge {v0i} {v1i}")

        prePath = self.getPath(v0i, True)
        postPath = self.getPath(v1i, False)

        if prePath is None:
            p = [v0i, v1i]
        else:
            p = prePath + [v1i]

        if not (postPath is None):
            p = p + postPath[1:]

        #print(f"adding {p} to paths")

        self.paths.append(p)

    def addEdgeList(self, edge_list):
        for i in range(1, len(edge_list)):
            j = i - 1
            self.addEdge((edge_list[j], edge_list[i]))

    def getPaths(self):
        for p in self.paths:
            yield [self.vertices[i] for i in p]

    def getSortedPaths(self):
        outPaths = []

        for p in self.paths:
            xB = self.vertices[p[0]].x()
            xE = self.vertices[p[-1]].x()

            if xE < xB:
                p = p[:]
                p.reverse()

                outPaths.append((xE, p))
            else:
                outPaths.append((xB, p))
        outPaths.sort()

        for x, p in outPaths:
            yield [self.vertices[i] for i in p]

    def getGreedySortedPaths(self, startpoint = None):
        if startpoint is None:
            startpoint = m.Vector2(0, 0)

        outPaths = []

        unusedPaths = self.paths[:]

        while unusedPaths:
            closestDist = None
            closestPath = None
            closestIndex = None

            for pi, p in enumerate(unusedPaths):
                d = startpoint.subVec2(self.vertices[p[0]]).mag()
                if closestPath is None or d < closestDist:
                    closestPath = p
                    closestIndex = pi
                    closestDist = d
                d = startpoint.subVec2(self.vertices[p[-1]]).mag()
                if d < closestDist:
                    closestPath = list(reversed(p))
                    closestIndex = pi
                    closestDist = d
            del(unusedPaths[closestIndex])
            outPaths.append([self.vertices[x] for x in closestPath])
            startpoint = self.vertices[closestPath[-1]]
        return outPaths

    def drawPaths(self, dwg, width = 2, color = 'black', startpoint = None):
        paths = self.getGreedySortedPaths(startpoint)

        for edge_path in paths:
            p = draw.Path(stroke_width = width, stroke = color, fill='none')
            p.M(*edge_path[0].components)
            for v in edge_path[1:]:
                p.L(*v.components)
            dwg.append(p)

        

            
            
                
            


        
