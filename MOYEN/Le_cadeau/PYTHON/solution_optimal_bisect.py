import sys
import math

from bisect import * 

# url: https://docs.python.org/2/library/bisect.html
def find_le(a, x):
    'Find rightmost index of value less than or equal to x'
    i = bisect_right(a, x)
    if i:
        return i
    raise ValueError
    
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

list_contribs = []  # liste des contributions (solution)
list_budgets = []   # liste des budgets

n = int(raw_input())
c = int(raw_input())
for i in xrange(n):
    b = int(raw_input())
    # on stocke les budgets
    list_budgets.append(b)

# on verifie qu'il est possible d'acheter le cadeau
if sum(list_budgets) < c:
    print "IMPOSSIBLE"
else:
    # on trie la liste des budgets
    list_budgets.sort()
    
    # on demarre la recherche de contribution
    # avec les parametres de depart: nombre d'odds participant & somme totale (pour le cadeau) recherchee
    cur_c = c
    cur_n = n
    
    # trick pour passer au 1er tour d'iteration (sans influence)
    list_budgets_less_avg = [0]
    # on boucle tant qu'on a des participants actifs et 
    #                qu'on a des participants en dessous de la moyenne des participations
    while((len(list_budgets_less_avg)>0) & (len(list_budgets)>0)):
        # on met a jour la moyenne de participation
        avg = cur_c // cur_n
        
        # on tente de recuperer l'indice (dans la liste triee)
        # du 1er odd qui ne peut pas verser la contribution moyenne courante
        try:
            indice_for_avg = find_le(list_budgets, avg)
        except:
            indice_for_avg = 0
        
        # a partir de cet indice, on peut recupere la liste des odds qui ne peuvent pas payer cette contribution moyenne
        list_budgets_less_avg = list_budgets[:indice_for_avg]
        # et la liste des odds pouvant assumer cette contribution
        list_budgets = list_budgets[indice_for_avg:]
        
        # on met a jour la liste des contributions avec la participation maximales des odds ne possedant pas plus 
        # que la participation moyenne (courante)
        list_contribs.extend(list_budgets_less_avg)
        
        # on met a jour le nombre de participants odds et la somme totale recherchee
        cur_c -= sum(list_budgets_less_avg)
        cur_n = len(list_budgets)
            
    # a la fin: il nous reste des odds pouvant participer a la hauteur de la derniere contribution moyenne
    # on rajoute leurs contributions
    list_contribs.extend([avg]*len(list_budgets))
    
    # comme pour la moyenne on utilise des divisions entieres (pas de centimes),
    # il peut rester un complement pour arriver la somme totale
    # on propage ce complement sur les derniers odds pouvant payer au dela de la derniere contribution moyenne
    # on calcul ce complement
    diff = c - sum(list_contribs)
    # on met a jour la liste des contributions en rajoutant +1 de contributions aux derniers odds
    # ps: les derniers odds sont les plus 'riches' car on a trie (au depart) la listes des budgets
    list_contribs = list_contribs[:-diff] + map(lambda x: x+1, list_contribs[-diff:]) if diff else list_contribs
    
    # on affiche le resultat
    print "\n".join(map(str, list_contribs))
