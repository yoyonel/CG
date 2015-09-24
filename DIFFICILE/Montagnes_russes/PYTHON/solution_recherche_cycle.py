import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

l, c, n = [int(i) for i in raw_input().split()]

# 1er: recuperer les informations des groupes de clients pour le manege
list_groups = [0]*n
for i in xrange(n):
    pi = int(raw_input())
    #
    list_groups[i] = pi
    
# 2nd: on construit une liste de groupe de clients pour le manege
# Tips: la cle (comment souvent) est la recherche de cycle
# on peut considerer la liste des clients comme un graph
# la recherche de cycle permet de reperer la boucle d'ordonnencement
# et au final d'optimiser le calcul de gain
list_gains = []     # liste des gains
dict_gains = {}     # dictionnaire - key: indice du 1er client du groupe - value: indice du gain associe
pi = 0  # valeur/nombre du groupe de client
first_client_in_group = 0  # indice du 1er client du groupe 
available_places = l    # nombre de places restantes
nb_gain = 0     # nombre de gains calcules
i = 0   # indice du client

# init de la loop
pi = list_groups[i]     # nombre de clients dans ce groupe
b_continue = True       # condition de sortie de la boucle
on_cycle = False        # on repere si on est tombe sur un cycle
i_for_cycle = 0         # indice du cycle repere
# boucle de construction
while(b_continue):
    # si on peut rajouter ce groupe de client dans le tour de manege
    # on continue
    if pi <= available_places:
        available_places -= pi
    else:
        # sinon le groupe de client actuel fait depasser la limite des places disponible pour le tour de manege
        # on met a jour la liste des gains
        list_gains.append(l - available_places)     # on rajoute le gain pour ce tour de manege
        dict_gains[first_client_in_group] = nb_gain    # on stocke l'indice du gain pour le 1er client du groupe
        # on met a jour l'indice du 1er client pour le nouveau groupe
        first_client_in_group = i
        nb_gain += 1    # on met a jour le nombre de gains calcule
        available_places = l - pi   # on met a jour le nombre de place disponible pour le prochain tour
        
        # on recherche la presence d'un cycle
        if i in dict_gains:
            i_for_cycle = i  # on conserve l'indice du dernier/premier groupe du cycle repere
            on_cycle = True
        # conditions de sortie:
        # - on a repere un cycle
        # - early exit: on a (deja) atteint le nombre de tours de manege max
        b_continue &= not on_cycle
        b_continue &= nb_gain < c    # early exit
    # on passe au groupe suivant
    i = (i+1)%n
    pi = list_groups[i]
    # cas special: avec l'ensemble des groupes on ne remplit pas totalement le manege
    b_continue &= not( (i==0) & (nb_gain==0) )  # special case: everyone in 1 round

# special case: everyone in 1 round
if not nb_gain:
    list_gains = [l - available_places]

result = 0

if on_cycle:
    # on a repere un cycle
    # on a un premier passage des groupes (puis le cycle)
    # pour le 1er passage on calcul les gains
    result += sum(list_gains)
    # on reduit le nombre de tours (de manege)
    c -= nb_gain
    # on reconstruit la liste des gains en prenant en compte le cycle repere
    list_gains = list_gains[dict_gains[i_for_cycle]:]
    
# // : division entiere
# % : on recupere le reste d'une division entiere //
nb_cycles = c // len(list_gains)
result += nb_cycles*sum(list_gains)
rest_afer_cycle = c % len(list_gains)
result += sum(list_gains[0:rest_afer_cycle])

print result

