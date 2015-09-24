import sys, math
import itertools

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

MESSAGE = raw_input()

####################################################################################################
# Etape 1: conversion du message (string) en equivalence binaire (ASCII -> BINARY representation)
####################################################################################################
# url: http://www.tutorialspoint.com/python/string_zfill.htm
#MESSAGE_BINARY = ''.join( bin(ord(char))[2:].zfill(7) for char in MESSAGE )
# url: http://stackoverflow.com/questions/1395356/how-can-i-make-bin30-return-00011110-instead-of-0b11110
# -> string formater : https://www.python.org/dev/peps/pep-3101/
MESSAGE_BINARY = ''.join( "{0:07b}".format(ord(char)) for char in MESSAGE )

####################################################################################################
# Etape 2: Conversion du message binaire en code Chuck
####################################################################################################
# url: http://stackoverflow.com/questions/13197668/counting-consecutive-characters-in-a-string
print ' '.join( 
    ( ('0'*(2-int(binary))) + ' ' + ('0' * nb_repetition))
    for binary, nb_repetition in
    ( (k, len(list(g))) for k, g in itertools.groupby(MESSAGE_BINARY) )
   ) 


