import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

list_dist = []

def convert_str_to_float(str):
    return float(str.replace(',','.'))
    
def distance_AB(lonA, latA, lonB, latB):
    x = (lonA-lonB)*math.cos((latA+latB)*0.5)
    y = latA-latB
    #return math.sqrt(x**2+y**2)*6371
    return math.sqrt(x**2+y**2)     # normalisation de la distance non necessaire
    #return abs(x)+abs(y)    # fonctionne si x, y >= 1.0
    
lon = raw_input()
lat = raw_input()
#
lon = convert_str_to_float(lon)
lat = convert_str_to_float(lat)
#
n = int(raw_input())
for i in xrange(n):
    defib = raw_input()
    #
    split_defib = defib.split(';')
    #
    lon_defib, lat_defib = map(convert_str_to_float, split_defib[-2:])
    #
    list_dist.append((split_defib[1], distance_AB(lon, lat, lon_defib, lat_defib)))

print min(list_dist, key=lambda x: x[1])[0]
# Write an action using print
# To debug: print >> sys.stderr, "Debug messages..."

