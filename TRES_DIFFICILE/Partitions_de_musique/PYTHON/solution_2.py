import sys
import numpy as np
import itertools

list_notes_for_lines = {
    0: 'G', 1: 'E', 2: 'C', 3: 'A', 4: 'F', 5: 'D'
}
list_notes_for_interlines = {
    0: 'F', 1: 'D', 2: 'B', 3: 'G', 4: 'E', 5: 'C'
}
list_note_value = ['H', 'Q']


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

w, h = [int(i) for i in raw_input().split()]
image = raw_input()

#
# imageDecode = [False] * (w * h)
imageDecode = []

decodeDWE = image.split(' ')
isBlackPixel = decodeDWE[0] == 'B'
cur_col = 0
for nbPixelsForThisBlock in decodeDWE[1::2]:
    imageDecode += [isBlackPixel] * int(nbPixelsForThisBlock)
    isBlackPixel = not isBlackPixel

# url:
# - http://stackoverflow.com/questions/8355441/fastest-way-to-populate-a-1d-numpy-array
# - http://stackoverflow.com/questions/12575421/convert-a-1d-array-to-a-2d-array-in-numpy
# - http://stackoverflow.com/questions/903853/how-to-extract-column-from-a-multi-dimentional-array
np_img = np.fromiter(imageDecode, dtype=np.bool).reshape(h, w)
# get column
# np_img[:, indice_column] ou np_img[..., indice_column] (... : 'ellipsis')

counterForColumns = [0] * w
#
column = np_img[:, 0]
counterForColumns[0] = sum(np_img[:, 0])
indice_col = 0
while not counterForColumns[indice_col]:
    indice_col += 1
    column = np_img[:, indice_col]
    counterForColumns[indice_col] = sum(column)
#print >> sys.stderr, "counterForColumns: ", counterForColumns

#
# (1) On recupere les positions des lignes (interlignes) de la portee
#
# 1ere colonne non nulle
# => debut de la portee
#indice_column_for_staff = counterForColumns.index(filter(lambda counter: counter, counterForColumns)[0])
#columns_for_staff = np_img[:, indice_column_for_staff]
indice_column_for_staff = indice_col
column_for_staff = column

indices_row_for_lines = [
    i + 1  # on a l'indice de l'espace juste avant la ligne, donc on decale d'une unite de line
    for i, x in enumerate(
        [
            tup == (False, True)  # frontiere entre l'espace d'une interligne et une ligne de portee
            for tup in zip(column_for_staff[:-1], column_for_staff[1:])
        ]
    )
    if x
]

gb_columns_for_staff = itertools.groupby(column_for_staff)
#print >> sys.stderr, "taille des lignes de la portee: ", [len(list(g)) for k, g in gb_columns_for_staff if k]
nb_pixels_for_lines = [len(list(g)) for k, g in gb_columns_for_staff if k]
size_in_pixels_for_line = nb_pixels_for_lines[0]
print >> sys.stderr, "size_in_pixels_for_line: ", size_in_pixels_for_line
#sum_column_pixels_for_lines = sum(nb_pixels_for_lines)
#print >> sys.stderr, "sum_column_pixels_for_lines: ", sum_column_pixels_for_lines

'''
size_interlines = (indices_row_for_lines[1] - indices_row_for_lines[0])
indices_row_for_lines = [indices_row_for_lines[0] - size_interlines] + indices_row_for_lines
indices_row_for_lines += [indices_row_for_lines[-1] + size_interlines]
# indices sur les interlignes
indices_row_for_interlines = [(i0 + i1) / 2 for i0, i1 in zip(indices_row_for_lines[:-1], indices_row_for_lines[1:])]
indices_row_for_interlines += [indices_row_for_interlines[-1] + size_interlines]
#
print >> sys.stderr, "indices_row_for_lines: ", list(indices_row_for_lines)
print >> sys.stderr, "indices_row_for_interlines: ", list(indices_row_for_interlines)

#
# (2) on repere les notes
#
#sum_column_pixels_for_lines = 20
columns_for_lines = [counter == sum_column_pixels_for_lines for counter in counterForColumns]
print >> sys.stderr, "columns_for_lines: ", columns_for_lines
#
# i+1 => on a l'indice de l'espace juste avant la ligne, donc on decale d'une unite de line
# tup == (True, False) =>  frontiere entre l'espace d'une interligne et une ligne de portee
start_indices_col_for_notes = [i + 1 for i, x in enumerate([tup == (True, False)
                                                            for tup in
                                                            zip(
                                                                columns_for_lines[:-1],
                                                                columns_for_lines[1:])])
                               if x][:-1]  # -1 pour la fin de la portee
# print >> sys.stderr, "start_indices_col_for_notes: ", start_indices_col_for_notes
#
# (False, Truetup == (False, True) => frontiere
end_indices_col_for_notes = [i for i, x in enumerate([tup == (False, True)
                                                      for tup in
                                                      zip(
                                                          columns_for_lines[:-1],
                                                          columns_for_lines[1:]
                                                      )])
                             if x][1:]  # Retirer la premiere frontiere

# print >> sys.stderr, "end_indices_col_for_notes: ", end_indices_col_for_notes

# tup indices de depart et fin de colonnes definissant la note sur la partition
notes_on_sheet = zip(start_indices_col_for_notes, end_indices_col_for_notes)
print >> sys.stderr, "notes_on_sheet: ", notes_on_sheet

len_cols_for_notes_on_sheet = [e - s for s, e in notes_on_sheet]
print >> sys.stderr, "len_cols_for_notes_on_sheet: ", len_cols_for_notes_on_sheet

#
# (3) on analyse les notes/groupe de notes
#

#
# il faut reperer les groupes des blanches interlignes
# elles produisent un pattern de longueur : 3 0 0 3 (parfois ...)
#
subseq = [3, 0, 0, 3]
list_gb_subseq = [
    (k, len(list_g))
    for k, list_g in [(k, list(g))
                      for k, g in itertools.groupby(len_cols_for_notes_on_sheet, lambda sublist: sublist in subseq)]
]
new_notes_on_sheet = []
cur_indice = 0
for tup_sublist in list_gb_subseq:
    is_subseq, len_sublist = tup_sublist
    if is_subseq:
        new_notes_on_sheet += [(notes_on_sheet[cur_indice][0], notes_on_sheet[cur_indice][0]+21)]
    else:
        new_notes_on_sheet += notes_on_sheet[cur_indice:cur_indice+len_sublist]
    cur_indice += len_sublist
#
notes_on_sheet = new_notes_on_sheet
print >> sys.stderr, "* notes_on_sheet: ", notes_on_sheet
len_cols_for_notes_on_sheet = [e - s for s, e in notes_on_sheet]
print >> sys.stderr, "len_cols_for_notes_on_sheet: ", len_cols_for_notes_on_sheet


results = []
for indice_start, indice_end in notes_on_sheet:
    len_note = indice_end - indice_start
    col_center = indice_start + (len_note/2)
    col_img = list(np_img[:, col_center])
    #print >> sys.stderr, "col_img: ", col_img
    # on efface les lignes de la portee
    for indice in indices_row_for_lines:
        col_img[indice:indice + size_in_pixels_for_line] = [False] * size_in_pixels_for_line
    #print >> sys.stderr, "col_img: ", col_img
    indice_first_black_pixel_for_note = col_img.index(True)
    #
    indice_row_for_note = indice_first_black_pixel_for_note - size_in_pixels_for_line
    note_is_quarter = col_img[indice_row_for_note + (size_interlines//4)]
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
'''
#print "AQ DH"
#print ' '.join(results)
