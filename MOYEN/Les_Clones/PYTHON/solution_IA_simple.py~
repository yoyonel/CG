import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

 # nb_floors: number of floors
 # width: width of the area
 # nb_rounds: maximum number of rounds
 # exit_floor: floor on which the exit is found
 # exit_pos: position of the exit on its floor
 # nb_total_clones: number of generated clones
 # nb_additional_elevators: ignore (always zero)
 # nb_elevators: number of elevators
nb_floors, width, nb_rounds, exit_floor, exit_pos, nb_total_clones, nb_additional_elevators, nb_elevators = [int(i) for i in raw_input().split()]

dict_elevator = {}
for i in xrange(nb_elevators):
     # elevator_floor: floor on which this elevator is found
     # elevator_pos: position of the elevator on its floor
    elevator_floor, elevator_pos = [int(j) for j in raw_input().split()]
    #
    dict_elevator[elevator_floor] = elevator_pos
# on rajoute la sortie (considerer comme un elevator a prendre)
# ps: le jeu s'arretera quand un clone atteindra ce point
dict_elevator[exit_floor] = exit_pos

# indice du floor courant a resoudre (actif pour la resolution)
cur_floor_to_resolve = 0
# map pour convertir une direction en valeur numerique
dict_directions = {'LEFT': -1, 'RIGHT': 1, 'NONE': 0}
# game loop
while 1:
     # clone_floor: floor of the leading clone
     # clone_pos: position of the leading clone on its floor
     # direction: direction of the leading clone: LEFT or RIGHT
    clone_floor, clone_pos, direction = raw_input().split()
    direction = dict_directions[direction]
    clone_floor = int(clone_floor)
    clone_pos = int(clone_pos)

    # par default on attend
    cmd = 'WAIT'
    
    # si le clone de tete est sur le floor actif de resolution
    if clone_floor == cur_floor_to_resolve:
        elevator_pos = dict_elevator[clone_floor]
        # test sur la possibilite d'atteindre le prochain point d'elevation (ou sortie)
        # si atteignable par rapport a la direction courante et les positions relatives (position du drone et de l'elevateur)
        # -> on reste 'WAIT'
        # -> sinon on bloque le clone en tete et on passe au niveau/floor suivant pour la resolution
        cmd = 'BLOCK' if ((elevator_pos < clone_pos) & (direction>0)) | ((elevator_pos > clone_pos) & (direction<0)) else 'WAIT'
        # on change de floor pour la resolution
        cur_floor_to_resolve += 1
        
    # on lance la commande pour le clone de tete
    print cmd

