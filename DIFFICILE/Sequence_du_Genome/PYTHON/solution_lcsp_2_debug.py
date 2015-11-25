from itertools import permutations
from operator import itemgetter
import sys


def unflat_list_of_list(ll):
    """

    :param ll:
    :return:
    """
    return [item for sublist in ll for item in sublist]


# url: https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Longest_common_substring#Python2
def compute_matrix_common_substring(s1, s2):
    """

    :param s1:
    :param s2:
    :return: On utilise l'algo dynamique de 'Longest Common Substring'
             pour recuperer les prefixes/suffixes qui nous interessent
    """
    m = [[(0, 0, 0)] * (1 + len(s2)) for _ in xrange(1 + len(s1))]

    for x in xrange(1, 1 + len(s1)):
        for y in xrange(1, 1 + len(s2)):
            m[x][y] = (
                x, y, m[x - 1][y - 1][2] + 1
                if s1[x - 1] == s2[y - 1]
                else 0, 0, 0
                )
    return m


def is_prefix(tup, l_s2):
    """
    """
    return (tup[0] == tup[2]) & (tup[1] == l_s2)


def is_suffix(tup, l_s1):
    """
    """
    return (tup[1] == tup[2]) & (tup[0] == l_s1)


def lpcs(s1, s2):
    """

    :param s1:
    :param s2:
    :return: longest prefix common substring
    """
    # sys.stderr.write("lpcs de : %s et %s\n" % (s1, s2))
    mat = compute_matrix_common_substring(s1, s2)
    l_mat = unflat_list_of_list(mat)
    tup_max = max(
        l_mat,
        key=lambda tup: is_suffix(tup, len(s1)) * tup[2]
        )
    indentation_s2 = len(s1) - tup_max[2]
    return tup_max[2], indentation_s2


def print_string_with_indentations(tup, pprefix=True, psuffix=True):
    """
    """
    if pprefix:
        sys.stderr.write('-'*(tup[0]-1) + '>')

    sys.stderr.write(tup[1])

    if psuffix:
        sys.stderr.write('\n' + '-'*tup[0])


# def print_string_with_indentation(tup):
#     """
#     tup: indentation, string
#     """
#     sys.stderr.write(
#         '-'*(tup[0]-1) + '>' +
#         tup[1]
#         )


# def print_string_with_indentations(tup):
#     """
#     tup: indentation, string
#     """
#     print_string_with_indentation(tup)
#     sys.stderr.write('\n' + '-'*tup[0])


def sum_of_concat_prefix(l_str, li):
    """
    """
    list_indices = zip(li[:-1], li[1:])
    l_lpcs = map(
        lambda l_2i: lpcs(l_str[l_2i[0]], l_str[l_2i[1]]),
        list_indices
        )
    l2_str = map(lambda i: l_str[i], li)
    # on recupere la 1ere colonne: max length concat prefix
    lm_lpcs = zip(*l_lpcs)[0]
    sum_cp = sum(lm_lpcs)

    # 2nd colonne: indentation pour l'affichage des s2
    l_ind = list(zip(*l_lpcs)[1])
    #
    print_string_with_indentations((0, l2_str[0]), False, True)
    #
    map(
        print_string_with_indentations,
        zip(l_ind, l2_str[1:-1])
        )
    #
    print_string_with_indentations((l_ind[-1], l2_str[-1]), True, False)
    sys.stderr.write('\n')

    sys.stderr.write('=> ' + str(sum_cp))
    sys.stderr.write('\n')

    return sum_cp


def filter_inclusions(list_strings):
    """

    :param list_strings:
    :return:

    In [157]: list_strings = ['GAT', 'AGATTA']
    In [158]: filter_inclusions(list_strings)
    Out[158]: ['AGATTA']

    In [159]: list_strings = ['AGATTA', 'GAT']
    In [160]: filter_inclusions(list_strings)
    Out[160]: ['AGATTA']
    """
    #
    list_strings = sorted(list_strings, key=lambda x: len(x))
    len_list_strings = len(list_strings)
    #
    list_inclusions = [
        reduce(lambda x, y: x & y, list_bools, True)
        for list_bools in
        [
            [
                string not in list_strings[indice]
                for indice in xrange(ind + 1, len_list_strings)
            ]
            for ind, string in enumerate(list_strings)
        ]
    ]
    return map(
        itemgetter(0),
        filter(itemgetter(1), zip(list_strings, list_inclusions))
        )


def solver(l_str):
    """

    :param l_str:
    :return:

    test: AACCTT
    In [164]: l_str = ['AAC', 'CCTT']
    In [167]: solver(l_str)
    Out[167]: 6

    test: AGATTACAGA
    In [168]: l_str = ['AGATTACAGA', 'GATTACA', 'TACAGA']
    In [169]: solver(l_str)
    Out[169]: 10

    In [170]: l_str = ['TT', 'AA', 'ACT']
    In [171]: solver(l_str)
    Out[171]:

    """
    l_str = filter_inclusions(l_str)

    # somme des longueurs des strings
    # => pire des cas: aucunes strings ne peuvent se 'fusionner'
    sum_lengths_strings = sum(len(s) for s in l_str)

    optimize_char_in_prefix_common = 0
    # lls: length list string <=> number strings in list
    lls = len(l_str)
    if lls > 1:
        optimize_char_in_prefix_common = max(
            [
                sum_of_concat_prefix(l_str, li)
                for li in permutations(xrange(lls), lls)
            ]
        )
    return sum_lengths_strings - optimize_char_in_prefix_common


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

list_seqs = []
n = int(raw_input())
for i in xrange(n):
    subseq = raw_input()
    #
    list_seqs.append(subseq)

print solver(list_seqs)
