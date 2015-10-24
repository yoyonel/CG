# url: http://stackoverflow.com/questions/18516299/finding-a-list-of-all-largest-open-rectangles-in-a-grid-by-only-examining-a-list


class Range:
    def __init__(self, start, end=None):
        self.start = start
        self.end = end if end is not None else start

    def isEmpty(self):
        return self.start > self.end

    def isUnit(self):
        return self.start == self.end

    def intersect(self, other):
        return Range(max(self.start, other.start), min(self.end, other.end))

    def contains(self, other):
        return self.start <= other.start and self.end >= other.end

    def __repr__(self):
        return "Range(%d,%d)" % ( self.start, self.end )


class Rect:
    def __init__(self, xRange, yRange):
        self.xRange = xRange
        self.yRange = yRange

    def isEmpty(self):
        return self.xRange.isEmpty() or self.yRange.isEmpty()

    def isUnit(self):
        return self.xRange.isUnit() and self.yRange.isUnit()

    def intersect(self, other):
        return Range(max(self.start, other.start), min(self.end, other.end))

    def contains(self, other):
        return self.xRange.contains(other.xRange) and self.yRange.contains(other.yRange)

    def __repr__(self):
        return "Rect(%s,%s)" % ( self.xRange, self.yRange )


def intersect(a, b):
    r = Rect(Range(b.xRange.start, a.xRange.end), a.yRange.intersect(b.yRange))
    brokenB = not a.yRange.contains(b.yRange)
    fullyAbsorbedA = b.yRange.contains(a.yRange)
    return (r, brokenB, fullyAbsorbedA)


def findOpenRectangles(freeElements, pastRowNum):
    # From `freeElements`, compute free runs into `freeRunsPerRow`
    from collections import defaultdict

    freeRunsPerRow = defaultdict(set)
    rowNum = -1
    currRun = None
    for fe in freeElements:
        if fe[0] != rowNum:
            if currRun is not None:
                freeRunsPerRow[rowNum] |= {Rect(Range(rowNum), currRun)}
            currRun = Range(fe[1], fe[1])
            rowNum = fe[0]
        elif fe[1] == currRun.end + 1:
            currRun = Range(currRun.start, fe[1])
        else:
            freeRunsPerRow[rowNum] |= {Rect(Range(rowNum), currRun)}
            currRun = Range(fe[1], fe[1])
    if currRun is not None:
        freeRunsPerRow[rowNum] |= {Rect(Range(rowNum), currRun)}
        currRun = None
    #for freeRuns in freeRunsPerRow.items():
    #    print(freeRuns)

    # Yield open rectangles
    currRects = set()
    for currRow in range(0, pastRowNum):
        continuingRects = set()
        startingRects = set(freeRunsPerRow[currRow])
        for b in currRects:
            brokenB = True
            for a in freeRunsPerRow[currRow]:
                modifiedContinuingRect, t_brokenB, t_absorbedA = intersect(a, b)
                if not modifiedContinuingRect.isEmpty() and not [x for x in continuingRects if
                                                                 x.contains(modifiedContinuingRect)]:
                    continuingRects -= {x for x in continuingRects if modifiedContinuingRect.contains(x)}
                    continuingRects |= {modifiedContinuingRect}
                if not t_brokenB: brokenB = False
                if t_absorbedA: startingRects -= {a}
            if brokenB and not b.isUnit(): yield b
        currRects = continuingRects
        currRects |= startingRects
    for b in currRects:
        if not b.isUnit():
            yield b


input = []
input.append("   X    ")
input.append("        ")
input.append(" X      ")
input.append("     X X")
input.append("        ")
input.append("        ")
input.append("    X   ")
input.append("   X  X ")
input.append(" X     X")

# Translates input into a list of coordinates of free elements
freeElements = []
for rowNum, row in enumerate(input):
    for colNum, element in enumerate(row):
        if element == " ":
            freeElements.append((rowNum, colNum))
#for fe in freeElements:
#    print(fe)

# Find and print open rectangles
for openRect in findOpenRectangles(freeElements, len(input)):
    print(openRect)