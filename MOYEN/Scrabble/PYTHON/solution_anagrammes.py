import sys
import math
from bisect import bisect_left
from itertools import combinations

scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2, 
         "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3, 
         "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1, 
         "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4, 
         "x": 8, "z": 10}

# url: http://stackoverflow.com/questions/5485654/how-can-this-python-scrabble-word-finder-be-made-faster
def build_anadict(list_words):
    d = {}
    lets = set('abcdefghijklmnopqrstuvwxyz\n')
    
    for word in list_words:
        # on suppoe tous les mots (du dictionnaire) valides
        #if len(set(word) - lets) == 0 and len(word) > 2 and len(word) < 9:
        #word = word.strip()
        key = ''.join(sorted(word))
        d.setdefault(key, [word]).append(word)
      
    anadict = [' '.join([key]+value) for key, value in d.iteritems()]
    anadict.sort()
    
    return anadict

def build_dict_index(list_words):
    dict_index = {}
    for index, word in enumerate(list_words):
        dict_index[word] = index
    return dict_index
    
def score_word(word):
  return sum([scores[c] for c in word])

def findwords(rack, anadict, nb_min_letters=1):
    rack = ''.join(sorted(rack))
    foundwords = []
    for i in xrange(nb_min_letters,len(rack)+1):
        # url: https://docs.python.org/2/library/itertools.html#itertools.combinations
        for comb in combinations(rack,i):
            ana = ''.join(comb)
            # url: https://docs.python.org/2/library/bisect.html
            j = bisect_left(anadict, ana)
            if j == len(anadict):
                continue
            words = anadict[j].split()
            if words[0] == ana:
                foundwords.extend(words[1:])
    return foundwords
  
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

list_words = []

n = int(raw_input())
for i in xrange(n):
    w = raw_input()
    #
    list_words.append(w)

letters = raw_input()

# construction du dictionnaire d'anagrammes
anadict = build_anadict(list_words)
dict_index = build_dict_index(list_words)

# cherche l'ensemble des mots dans le dictionnaire
# qu'on puisse ecrire avec les lettres/tiles scrabble du joueur
foundwords = set(findwords(letters, anadict))
# on calcul les scores pour chacun des mots trouves
scored = [(score_word(word), word) for word in foundwords]
# on recupere le score max
max_score = max(scored, key=lambda x: x[0])[0]
#  on recupere les mots associes au score max et on associe l'indice d'insertion dans le dictionnaire
list_words_with_max_scored = [(dict_index[word], word) for score, word in scored if score == max_score]
# on recupere le mot (de score max) insere le 1er dans le dictionnaire
print min(list_words_with_max_scored)[1]
