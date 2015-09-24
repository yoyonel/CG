import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

dict_cards_values = { str(value): value for value in range(2, 11) }
dict_cards_values.update( { 'J': 11, 'Q': 12, 'K': 13, 'A': 14 } )

n = int(raw_input()) # the number of cards for player 1
cardsp_1 = [0]*n
for i in xrange(n):
    cardp_1 = raw_input() # the n cards of player 1
    # url: http://stackoverflow.com/questions/14215338/python-remove-multiple-character-in-list-of-string
    cardsp_1[i] = dict_cards_values[cardp_1.strip('DHCS')]

m = int(raw_input()) # the number of cards for player 2
cardsp_2 = [0]*m
for i in xrange(m):
    cardp_2 = raw_input() # the m cards of player 2
    cardsp_2[i] = dict_cards_values[cardp_2.strip('DHCS')]
    

# Write an action using print
# To debug: print >> sys.stderr, "Debug messages..."
#print >> sys.stderr, "cardsp_1: ", cardsp_1
#print >> sys.stderr, "cardsp_2: ", cardsp_2

nb_manche = 0

b_continue = True

# boucle infinie de jeu
while(b_continue):

    if len(cardsp_1) == 0:
        print "2 %d" % (nb_manche)
        b_continue = False
    elif len(cardsp_2) == 0:
        print "1 %d" % (nb_manche)
        b_continue = False
    else:
        cardp_1 = cardsp_1.pop(0)
        cardp_2 = cardsp_2.pop(0)
        #
        if cardp_1 > cardp_2:
            cardsp_1.append(cardp_1)
            cardsp_1.append(cardp_2)
        elif cardp_1 < cardp_2:
            cardsp_2.append(cardp_1)
            cardsp_2.append(cardp_2)
        else:
            '''
            print >> sys.stderr, '##########"BATAILLE ##########'
            print >> sys.stderr, "cardsp_1: ", cardsp_1 
            print >> sys.stderr, "-> len(cardsp_1): ", len(cardsp_1)
            print >> sys.stderr, "cardsp_2: ", cardsp_2
            print >> sys.stderr, "-> len(cardsp_2): ", len(cardsp_2)
            '''
            stack_cardsp_1 = []
            stack_cardsp_2 = []
            # bataille
            while( b_continue & (cardp_1 == cardp_2) ):
                # si un des joueurs n'a pas assez de cartes pour la bataille
                if (len(cardsp_1) < 4) | (len(cardsp_2) < 4):
                    print "PAT"
                    b_continue = False
                else:
                    #
                    stack_cardsp_1.append(cardp_1)
                    stack_cardsp_2.append(cardp_2)
                    #
                    for _ in range(3): stack_cardsp_1.append(cardsp_1.pop(0))
                    for _ in range(3): stack_cardsp_2.append(cardsp_2.pop(0))
                    #
                    cardp_1 = cardsp_1.pop(0)
                    cardp_2 = cardsp_2.pop(0)
            #
            if b_continue:  
                if cardp_1 > cardp_2:
                    cardsp_1.append(cardp_1)
                    cardsp_1.extend(stack_cardsp_1)
                    cardsp_1.extend(stack_cardsp_2)
                    cardsp_1.append(cardp_2)
                else:
                    cardsp_2.append(cardp_1)
                    cardsp_2.extend(stack_cardsp_1)
                    cardsp_2.extend(stack_cardsp_2)
                    cardsp_2.append(cardp_2)
    #
    nb_manche += 1

