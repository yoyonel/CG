import sys
import numpy as np
import itertools

# dictionnaires de correspondances entre les indices de lignes/interlignes issues de la detection de notes
# et les strings correspondantes aux notes
list_notes_for_lines = {
    0: 'G', 1: 'E', 2: 'C', 3: 'A', 4: 'F', 5: 'D'
}
list_notes_for_interlines = {
    0: 'F', 1: 'D', 2: 'B', 3: 'G', 4: 'E', 5: 'C'
}
# liste de correspondance entre un booleen issu d'un test sur la valeur de temps d'une note reperee
# et la string correspondantes
list_note_value = ['H', 'Q']

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

w, h = [int(i) for i in raw_input().split()]
image = raw_input()

# peut etre vu comme un scan vertical de la partition image
# on compte la somme des pixels suivant un axe vertical (x=0)
# Ca nous permettra de separer les notes (sauf cas avec les 'do' et leurs
# barres qui traversent la note)counterForColumns = [0] * w
counterForColumns = [0] * w
# Tableau de l'image, utilise par la suite pour construire un array 2D numpy
imageDecode = [0] * (w * h)
# On prepare l'encodage DWE a etre decode. On separe les valeurs : <Lettre B|W> <Nb elements>
decodeDWE = image.split(' ')
# on recupere la 'couleur' du 1er bloc declare par encodage DWE
isBlackPixel = decodeDWE[0] == 'B'
# indice de la 1ere colonne
cur_col = 0
print >> sys.stderr, "Decode and counter columns sum pixels [START]"
for nbPixelsForThisBlock in decodeDWE[1::2]:
    # on recupere la taille du bloc courant
    nbPixelsForThisBlock = int(nbPixelsForThisBlock)
    # si le pixel courant est noire
    if isBlackPixel:
        # on transfert le bloc de pixel au tableau d'image
        # on en profite pour mettre a jour un SAT sur les colonnes de l'image
        for i in range(cur_col, cur_col + nbPixelsForThisBlock):
            counterForColumns[i % w] += 1
            imageDecode[i] = 1
    # on passe au bloc suivant
    cur_col += nbPixelsForThisBlock
    # on switch la couleur pixel du prochain bloc (logique DWE)
    isBlackPixel = not isBlackPixel
print >> sys.stderr, "Decode and counter columns sum pixels [END]"
print >> sys.stderr, "counterForColumns: ", counterForColumns

# url:
# - http://stackoverflow.com/questions/8355441/fastest-way-to-populate-a-1d-numpy-array
# - http://stackoverflow.com/questions/12575421/convert-a-1d-array-to-a-2d-array-in-numpy
# - http://stackoverflow.com/questions/903853/how-to-extract-column-from-a-multi-dimentional-array
# => transfert du tableau 1D de l'image en tableau 2D numpy correspondant
np_img = np.fromiter(imageDecode, dtype=np.bool).reshape(h, w)

#
# (1) On recupere les positions des lignes (interlignes) de la portee
#
# counterForColumns est un SAT sur les colonnes de l'image
# donc contient 0 si que des pixels blancs en colonnes (en debut d'image)
# puis les premieres valeurs non nulles correspondent au debut des lignes de portees de la partition
# 1ere colonne non nulle => debut de la portee
indice_column_for_staff = counterForColumns.index(filter(lambda counter: counter, counterForColumns)[0])
# on recupere la colonne associee au debut de la portee
columns_for_staff = np_img[:, indice_column_for_staff]
# groupby sur les pixels de cette colonne (debut de la portee)
gb_columns_for_staff = itertools.groupby(columns_for_staff)
# on va traquer les debuts des blocs de pixels 'Blacks' correspondant au dessin des lignes de portees
ind_row = 0
indices_row_for_lines = []
nb_pixels_for_lines = []
# le groupby sur la colonne va nous fournir des series de blocs de pixels False/True (Blanc/Noir)
# entre deux blocs issus de groupby il y a une frontiere ou definition d'une ligne de portee
# => Chaque nouveau bloc 'True' correspond a la definition d'une nouvelle ligne de portee
for is_start_line, len_groups_pixels in [(k, len(list(g))) for k, g in gb_columns_for_staff]:
    # si c'est une ligne de portee
    if is_start_line:
        # on rajoute l'indice du debut de la ligne
        indices_row_for_lines += [ind_row]
        # on somme la hauteur des blocs de pixels definissant les lignes de portee
        # sera utile pour un SAT local sur les lignes de portees
        nb_pixels_for_lines += [len_groups_pixels]
    # on passe au bloc ligne suivant
    ind_row += len_groups_pixels
# On peut effectuer le SAT local (vertical) sur les lignes de portees
sum_column_pixels_for_lines = sum(nb_pixels_for_lines)
# on recupere la taille (en pixels) d'un bloc definissant une ligne de portee
size_in_pixels_for_line = nb_pixels_for_lines[0]
# print >> sys.stderr, "sum_column_pixels_for_lines: ", sum_column_pixels_for_lines
# print >> sys.stderr, "size_in_pixels_for_line: ", size_in_pixels_for_line

size_interlines = (indices_row_for_lines[1] - indices_row_for_lines[0])
indices_row_for_lines = [indices_row_for_lines[0] - size_interlines] + indices_row_for_lines
indices_row_for_lines += [indices_row_for_lines[-1] + size_interlines]
# indices sur les interlignes
indices_row_for_interlines = [(i0 + i1) / 2
                              for i0, i1 in zip(indices_row_for_lines[:-1], indices_row_for_lines[1:])]
indices_row_for_interlines += [indices_row_for_interlines[-1] + size_interlines]
#
print >> sys.stderr, "indices_row_for_lines: ", list(indices_row_for_lines)
print >> sys.stderr, "indices_row_for_interlines: ", list(indices_row_for_interlines)

#
indice_row_for_C = indices_row_for_lines[-1]
indice_start_for_row_for_C = indice_row_for_C * w
indice_end_for_row_for_C = (indice_row_for_C + size_in_pixels_for_line) * w
# on recalcul la somme des pixels de colonnes (en prenant en compte la modification precedente sur les lignes C)
counterForColumns = [0] * w
isBlackPixel = decodeDWE[0] == 'B'
cur_col = 0
# print >> sys.stderr, "ReDecode and Recounter columns sum pixels [START]"
for nbPixelsForThisBlock in decodeDWE[1::2]:
    nbPixelsForThisBlock = int(nbPixelsForThisBlock)
    if isBlackPixel:
        start_col = cur_col
        end_col = cur_col + nbPixelsForThisBlock
        for i in range(start_col, end_col):
            counterForColumns[i % w] += 1 * (not indice_start_for_row_for_C <= i <= indice_end_for_row_for_C)
    cur_col += nbPixelsForThisBlock
    isBlackPixel = not isBlackPixel
#print >> sys.stderr, "ReDecode and Recounter columns sum pixels [END]"
#
# fonctionne mais lent, l'operation de get sur les colonnes doit etre couteuse
#np_img[indice_row_for_C:indice_row_for_C+4] = [False] * w
#for indice_col in range(w):
#    counterForColumns[indice_col] = sum(np_img[:, indice_col])

# c
# (2) on repere les notes
#
columns_for_lines = [counter == sum_column_pixels_for_lines for counter in counterForColumns]
# print >> sys.stderr, "columns_for_lines: ", columns_for_lines
# ########################################################
# Version recherche explicite de frontieres + enumerate #
#########################################################
'''
#
# i+1 => on a l'indice de l'espace juste avant la ligne, donc on decale d'une unite de line
# tup == (True, False) =>  frontiere entre l'espace d'une interligne et une ligne de portee
start_indices_col_for_notes = [i + 1 for i, x in enumerate([tup == (True, False)
                                                            for tup in
                                                            zip(
                                                                columns_for_lines[:-1],
                                                                columns_for_lines[1:])])
                               if x][:-1]  # -1 pour la fin de la portee
print >> sys.stderr, "start_indices_col_for_notes: ", start_indices_col_for_notes
'''
'''
#
# (False, Truetup == (False, True) => frontiere
end_indices_col_for_notes = [i for i, x in enumerate([tup == (False, True)
                                                      for tup in
                                                      zip(
                                                          columns_for_lines[:-1],
                                                          columns_for_lines[1:]
                                                      )])
                             if x][1:]  # Retirer la premiere frontiere
#   end_indices_col_for_notes = end_indices_col_for_notes[1:-1]
print >> sys.stderr, "end_indices_col_for_notes: ", end_indices_col_for_notes
'''
# ##################
# Version groupby #
###################
start_indices_col_for_notes = []
end_indices_col_for_notes = []
ind_col = indice_column_for_staff
for k, len_g in [(k, len(tuple(g))) for k, g in itertools.groupby(columns_for_lines[indice_column_for_staff:])]:
    if k:  # <=> 'False' -> 'True'
        end_indices_col_for_notes += [ind_col - 1]
    else:  # <=> 'True' -> 'False'
        start_indices_col_for_notes += [ind_col]
    ind_col += len_g
start_indices_col_for_notes = start_indices_col_for_notes[:-1]
end_indices_col_for_notes = end_indices_col_for_notes[1:]
#print >> sys.stderr, "start_indices_col_for_notes: ", start_indices_col_for_notes
#print >> sys.stderr, "end_indices_col_for_notes: ", end_indices_col_for_notes

# tup indices de     depart et fin de colonnes definissant la note sur la partition
notes_on_sheet = zip(start_indices_col_for_notes, end_indices_col_for_notes)
#print >> sys.stderr, "notes_on_sheet: ", notes_on_sheet

len_cols_for_notes_on_sheet = [e - s for s, e in notes_on_sheet]
print >> sys.stderr, "len_cols_for_notes_on_sheet: ", len_cols_for_notes_on_sheet

#
# (3) on analyse les notes/groupe de notes
#
#
# il faut reperer les groupes des blanches interlignes
# elles produisent un pattern de longueur : 3 0 0 3 (parfois ...)
# present dans les tests: 4, 6, 8, 9
# mais 'etrangement' non present dans 10 11 12 (pourtant des blanches interlignes sont presentes dans la partition ...)
# pattern qu'on recherche dans a liste des longueurs de sequences
subseq = [3, 0, 0, 3]
list_gb_subseq = [
    (k, len(list_g))
    for k, list_g in [(k, list(g))
                      for k, g in itertools.groupby(len_cols_for_notes_on_sheet, lambda sublist: sublist in subseq)]
]
# on souhaite reconstruire notes_on_sheet pour remplacer les notes [3, 0, 0, 3] en une seule note [21]
new_notes_on_sheet = []
cur_indice = 0
size_in_pixels_for_note = 21
for tup_sublist in list_gb_subseq:
    is_subseq, len_sublist = tup_sublist
    if is_subseq:
        # on remplace les 4 longueurs [3, 0, 0, 3] par la longueur d'une note [21]
        # on effectue l'equivalence de transfert via nots_on_sheet
        new_notes_on_sheet += [
            (notes_on_sheet[cur_indice][0],
             notes_on_sheet[cur_indice][0] + size_in_pixels_for_note)
        ]
    else:
        # simple copie/transfert
        new_notes_on_sheet += notes_on_sheet[cur_indice:cur_indice + len_sublist]
    cur_indice += len_sublist
# on transfert le nouveau tableau dans notes_on_sheet
notes_on_sheet = new_notes_on_sheet
# on update len_cols_for_notes_on_sheet
len_cols_for_notes_on_sheet = [e - s for s, e in notes_on_sheet]
# print >> sys.stderr, "* notes_on_sheet: ", notes_on_sheet
#print >> sys.stderr, "len_cols_for_notes_on_sheet: ", len_cols_for_notes_on_sheet

results = []
offset_to_test_quarter_value = size_interlines // 4
for start_ind_col_for_note, end_ind_col_for_note in notes_on_sheet:
    len_note = end_ind_col_for_note - start_ind_col_for_note
    col_center = start_ind_col_for_note + (len_note / 2)
    col_img = list(np_img[:, col_center])
    #print >> sys.stderr, "col_img: ", col_img
    # on efface les lignes de la portee
    for indice in indices_row_for_lines:
        col_img[indice:indice + size_in_pixels_for_line] = [False] * size_in_pixels_for_line
    #print >> sys.stderr, "col_img: ", col_img
    indice_first_black_pixel_for_note = col_img.index(True)
    #
    indice_row_for_note = indice_first_black_pixel_for_note - size_in_pixels_for_line
    print >> sys.stderr, "indice_row_for_note: ", indice_row_for_note
    indice_row_for_note = min(indices_row_for_interlines + indices_row_for_lines,
                              key=lambda x: abs(x - indice_row_for_note))
    print >> sys.stderr, "*indice_row_for_note: ", indice_row_for_note
    note_is_quarter = col_img[indice_row_for_note + offset_to_test_quarter_value]
    letter_for_note_value = list_note_value[note_is_quarter]
    #
    if indice_row_for_note in indices_row_for_interlines:
        index_interlines = indices_row_for_interlines.index(indice_row_for_note)
        letter_for_note = list_notes_for_interlines[index_interlines]
        print >> sys.stderr, "index interlines: ", index_interlines
    elif indice_row_for_note in indices_row_for_lines:
        index_lines = indices_row_for_lines.index(indice_row_for_note)
        letter_for_note = list_notes_for_lines[index_lines]
        print >> sys.stderr, "index lines: ", index_lines
    #
    print >> sys.stderr, "letter_for_note: ", letter_for_note
    print >> sys.stderr, "letter_for_note_value: ", letter_for_note_value
    #
    results.append(letter_for_note + letter_for_note_value)


    #print >> sys.stderr, "indice_row_for_note: ", indice_row_for_note
    #print >> sys.stderr, "col_img[indice_row_for_note+6]: ", col_img[indice_row_for_note+6]
    #print >> sys.stderr, "indices_row_for_lines: ", list(indices_row_for_lines)
    #print >> sys.stderr, "indices_row_for_interlines: ", list(indices_row_for_interlines)

# get column
# np_img[:, indice_column] ou np_img[..., indice_column] (... : 'ellipsis')

#print "AQ DH"
print ' '.join(results)
