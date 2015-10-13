import sys
import numpy as np
import itertools
import re


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

w, h = [int(i) for i in raw_input().split()]
image = raw_input()

# peut etre vu comme un scan vertical de la partition image
# on compte la somme des pixels suivant un axe vertical (x=0)
# Ca nous permettra de separer les notes (sauf cas avec les 'do' et leurs
# barres qui traversent la note)counterForColumns = [0] * w
counterForColumns = [0] * w
#
imageDecode = [0] * (w * h)

decodeDWE = image.split(' ')
isBlackPixel = decodeDWE[0] == 'B'
cur_col = 0
for nbPixelsForThisBlock in decodeDWE[1::2]:
    nbPixelsForThisBlock = int(nbPixelsForThisBlock)
    if isBlackPixel:
        for i in range(cur_col, cur_col + nbPixelsForThisBlock):
            counterForColumns[i % w] += 1
            imageDecode[i] = 1
    cur_col += nbPixelsForThisBlock
    isBlackPixel = not isBlackPixel

print >> sys.stderr, "counterForColumns: ", counterForColumns

# url:
# - http://stackoverflow.com/questions/8355441/fastest-way-to-populate-a-1d-numpy-array
# - http://stackoverflow.com/questions/12575421/convert-a-1d-array-to-a-2d-array-in-numpy
# - http://stackoverflow.com/questions/903853/how-to-extract-column-from-a-multi-dimentional-array
np_img = np.fromiter(imageDecode, dtype=np.bool).reshape(h, w)

list_notes_for_lines = {
    0: 'G', 1: 'E', 2: 'C', 3: 'A', 4: 'F', 5: 'D'
}
list_notes_for_interlines = {
    0: 'F', 1: 'D', 2: 'B', 3: 'G', 4: 'E', 5: 'C'
}
list_note_value = ['H', 'Q']
#
# (1) On recupere les positions des lignes (interlignes) de la portee
#
# 1ere colonne non nulle
# => debut de la portee
indice_column_for_staff = counterForColumns.index(filter(lambda counter: counter, counterForColumns)[0])
columns_for_staff = np_img[:, indice_column_for_staff]

indices_row_for_lines = [
    i + 1  # on a l'indice de l'espace juste avant la ligne, donc on decale d'une unite de line
    for i, x in enumerate(
        [
            tup == (False, True)  # frontiere entre l'espace d'une interligne et une ligne de portee
            for tup in zip(columns_for_staff[:-1], columns_for_staff[1:])
        ]
    )
    if x
]
size_interlines = (indices_row_for_lines[1] - indices_row_for_lines[0])
indices_row_for_lines = [indices_row_for_lines[0] - size_interlines] + indices_row_for_lines
indices_row_for_lines += [indices_row_for_lines[-1] + size_interlines]
# indices sur les interlignes
indices_row_for_interlines = [(i0 + i1) / 2 for i0, i1 in zip(indices_row_for_lines[:-1], indices_row_for_lines[1:])]
# indices_row_for_interlines = [indices_row_for_interlines[0] - size_interlines] + indices_row_for_interlines
indices_row_for_interlines += [indices_row_for_interlines[-1] + size_interlines]
#
print >> sys.stderr, "indices_row_for_lines: ", list(indices_row_for_lines)
print >> sys.stderr, "indices_row_for_interlines: ", list(indices_row_for_interlines)

#
# (2) on repere les notes
#
columns_for_lines = [counter == 20 for counter in counterForColumns]
print >> sys.stderr, "columns_for_lines: ", columns_for_lines
#
start_indices_col_for_notes = [
                                  i + 1
                                  # on a l'indice de l'espace juste avant la ligne, donc on decale d'une unite de line
                                  for i, x in enumerate(
        [
            tup == (True, False)  # frontiere entre l'espace d'une interligne et une ligne de portee
            for tup in zip(columns_for_lines[:-1], columns_for_lines[1:])
        ]
    )
                                  if x
                              ][:-1]  # -1 pour la fin de la portee
#print >> sys.stderr, "start_indices_col_for_notes: ", start_indices_col_for_notes
#
end_indices_col_for_notes = [
                                i
                                for i, x in enumerate(
        [
            tup == (False, True)  # frontiere de fin de la note
            for tup in zip(columns_for_lines[:-1], columns_for_lines[1:])
        ]
    )
                                if x
                            ][1:]  # 1 pour le debut de la portee
#print >> sys.stderr, "end_indices_col_for_notes: ", end_indices_col_for_notes

# tup indices de depart et fin de colonnes definissant la note sur la partition
notes_on_sheet = zip(start_indices_col_for_notes, end_indices_col_for_notes)
print >> sys.stderr, "notes_on_sheet: ", notes_on_sheet

len_cols_for_notes_on_sheet = [e - s for s, e in notes_on_sheet]
print >> sys.stderr, "len_cols_for_notes_on_sheet: ", len_cols_for_notes_on_sheet

#
# (3) on analyse les notes/groupe de notes
#

# il faut reperer les groupes des blanches interlignes
# elles produisent un pattern de longueur : 3 0 0 3
str_len_cols_for_notes_on_sheet = ' '.join(map(str, len_cols_for_notes_on_sheet))
print >> sys.stderr, "str_len_cols_for_notes_on_sheet: ", str_len_cols_for_notes_on_sheet
# url: http://stackoverflow.com/questions/4664850/find-all-occurrences-of-a-substring-in-python
indices_start_for_half_interlines = [m.start() for m in re.finditer('3003', str_len_cols_for_notes_on_sheet)]
print >> sys.stderr, "indices_start_for_half_interlines: ", indices_start_for_half_interlines
for i, indice in enumerate(indices_start_for_half_interlines):
    indice_on_notes_sheet = indice - 4 * i
    print >> sys.stderr, "indice_on_notes_sheet: ", indice_on_notes_sheet
    notes_on_sheet[indice_on_notes_sheet:indice_on_notes_sheet + 4] = [
        (notes_on_sheet[indice_on_notes_sheet][0], notes_on_sheet[indice_on_notes_sheet + 3][1])
    ]
print >> sys.stderr, "notes_on_sheet: ", notes_on_sheet

results = []
for indice_start, indice_end in notes_on_sheet:
    len_note = indice_end - indice_start
    col_center = indice_start + len_note / 2
    col_img = list(np_img[:, col_center])
    #print >> sys.stderr, "col_img: ", col_img
    # on efface les lignes de la portee
    for indice in indices_row_for_lines:
        col_img[indice:indice + 4] = [False, False, False, False]
    #print >> sys.stderr, "col_img: ", col_img
    indice_first_black_pixel_for_note = col_img.index(True)
    #
    indice_row_for_note = indice_first_black_pixel_for_note - 4
    note_is_quarter = col_img[indice_row_for_note + 6]
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
