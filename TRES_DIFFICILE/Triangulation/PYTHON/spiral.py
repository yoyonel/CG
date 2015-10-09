# url: http://stackoverflow.com/a/23707273
from itertools import count
from math import ceil, floor, log10, sqrt
from collections import namedtuple


def steps_from_center():
    for n in count(start=1):
        if n % 2:
            yield RIGHT
            for _ in range(n):
                yield DOWN
            for _ in range(n):
                yield LEFT
        else:
            yield LEFT
            for _ in range(n):
                yield UP
            for _ in range(n):
                yield RIGHT


Step = namedtuple("Step", ["dx", "dy"])
RIGHT = Step(1, 0)
DOWN = Step(0, 1)
LEFT = Step(-1, 0)
UP = Step(0, -1)

max_i = int(input("What number do you want to display up to? "))

# how big does the square have to be?
max_n = int(ceil(sqrt(max_i)))

# how many digits in the largest number?
max_i_width = int(floor(log10(max_i))) + 1


# custom output formatter - make every item the same width
def output(item, format_string="{{:>{}}}".format(max_i_width)):
    return format_string.format(item)


EMPTY = output("")

# here is our initialized data structure
square = [[EMPTY] * max_n for _ in range(max_n)]

# and we start by placing a 1 in the center:
x = y = max_n // 2
square[y][x] = output(1)

for i, step in enumerate(steps_from_center(), start=2):
    if i > max_i:
        break
    else:
        x += step.dx
        y += step.dy
        square[y][x] = output(i)

print("\n".join(" ".join(row) for row in square))