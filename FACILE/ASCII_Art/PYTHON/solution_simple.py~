import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

l = int(raw_input())
h = int(raw_input())
t = raw_input()

nb_letters = 27
nb_spaces = nb_letters
#
tab_ascii = [[]] * h
for i in xrange(h):
    row = raw_input()
    #
    tab_ascii[i] = row

print >> sys.stderr, "tab_ascii: ", tab_ascii

ord_A = ord('A')
ord_Z = ord('Z')

l_out_t = []
# parcourt sur la hauteur du message (lettres)
for j in range(h):
    # tableau pour la ligne horizontale courante
    cur_line = []
    # pour chaque lettre du message
    for letter in t:
        # on passe en majuscule
        letter = letter.upper()
        # on recupere son indice
        ord_letter = ord(letter)
        # si la lettre est un caractere valide (lettre de A a Z)
        # indice relatif du caractere sinon indice du caractere '?' (= 26)
        i_letter = ord_letter - ord_A if (ord_letter >= ord_A) & (ord_letter <= ord_Z) else 26
        # on calcul l'indice dans notre tableau ascii
        i_letter_in_tab = i_letter * l
        # on rajoute la ligne horizontal ASCII pour le caractere courant
        cur_line.append(tab_ascii[j][i_letter_in_tab:i_letter_in_tab + l])
    # on join les listes de caracteres
    cur_line = "".join(cur_line)
    # on rajoute la ligne horizontal au message final
    l_out_t.append(cur_line)

# on joint les listes de lignes horizontales de caracteres
out_t = '\n'.join(l_out_t) 
# on affiche le resultat
print out_t

