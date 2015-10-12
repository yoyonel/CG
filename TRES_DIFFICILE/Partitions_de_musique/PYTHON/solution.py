import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

w, h = [int(i) for i in raw_input().split()]
image = raw_input()

# peut etre vu comme un scan vertical de la partition image
# on compte la somme des pixels suivant un axe vertical (x=0)
# Ca nous permettra de separer les notes (sauf cas avec les 'do' et leurs
# barres qui traversent la note)counterForColumns = [0] * w
counterForColumns = [0] * w

decodeDWE = image.split(' ')
isBlackPixel = decodeDWE[0] == 'B'
cur_col = 0
for nbPixelsForThisBlock in decodeDWE[1::2]:
    nbPixelsForThisBlock = int(nbPixelsForThisBlock)
    if isBlackPixel:
        for i in range(cur_col, cur_col + nbPixelsForThisBlock):
            counterForColumns[i % w] += 1
    cur_col += nbPixelsForThisBlock
    isBlackPixel = not isBlackPixel

print >> sys.stderr, "counterForColumns: ", counterForColumns

# idees:
# (1) 'Supprimer' les barres des notes, et la barre horizontal du do
# (2) Recuperer les profils (1D) des differentes notes:
# - Noire interligne / sur la ligne
# - Blanche interligne / sur la ligne
# => (3) On peut par la suite effectuer un simple matching 1D des notes

# Write an action using print
# To debug: print >> sys.stderr, "Debug messages..."

print "AQ DH"
