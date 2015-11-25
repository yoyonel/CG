from itertools import permutations
from operator import itemgetter


def unflat_list_of_list(ll):
    """

    :param ll:
    :return:
    """
    return [item for sublist in ll for item in sublist]


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
                else 0
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


def longest_prefix_common_substring(s1, s2):
    """

    :param s1:
    :param s2:
    :return:
    """
    mat = compute_matrix_common_substring(s1, s2)
    l_mat = unflat_list_of_list(mat)
    return max(
        l_mat,
        key=lambda tup: is_prefix(tup, len(s2)) * tup[2]
        )


def llpcs(s1, s2):
    """
    :param s1:
    :param s2:
    :return: length of the longest prefix in common substring
    """
    return longest_prefix_common_substring(s1, s2)[2]


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
    #
    list_inclusions = [
        reduce(lambda x, y: x & y, list_bools, True)
        for list_bools in
        [
            [
                s not in list_strings[indice]
                for indice in xrange(i_s + 1, len(list_strings))
            ]
            for i_s, s in enumerate(list_strings)
        ]
    ]
    return map(
        itemgetter(0),
        filter(itemgetter(1), zip(list_strings, list_inclusions))
        )


def solver(list_strings):
    """

    :param list_strings:
    :return:

    test: AACCTT
    In [164]: list_strings = ['AAC', 'CCTT']
    In [167]: solver(list_strings)
    Out[167]: 6

    test: AGATTACAGA
    In [168]: list_strings = ['AGATTACAGA', 'GATTACA', 'TACAGA']
    In [169]: solver(list_strings)
    Out[169]: 10

    In [170]: list_strings = ['TT', 'AA', 'ACT']
    In [171]: solver(list_strings)
    Out[171]:

    """
    list_strings = filter_inclusions(list_strings)

    # somme des longueurs des strings
    # => pire des cas: aucunes strings ne peuvent se 'fusionner'
    sum_lengths_strings = sum(len(s) for s in list_strings)

    optimize_char_in_prefix_common = 0
    nb_strings_in_list = len(list_strings)
    if nb_strings_in_list > 1:
        optimize_char_in_prefix_common = max(
            [
                sum(
                    map(
                        lambda zip_result: llpcs(list_strings[zip_result[0]], list_strings[zip_result[1]]),
                        zip(list_indices[:-1], list_indices[1:])
                        )
                )
                for list_indices in permutations(xrange(nb_strings_in_list), nb_strings_in_list)
            ]
        )
    return sum_lengths_strings - optimize_char_in_prefix_common


def filter_substrings(string_list):
    """

    :param string_list:
    :return: retire les strings substrings d'une (ou plus) autre(s) string(s)
    """
    return [
        string
        for string in string_list
        if not any(string in s for s in string_list if string != s)
    ]


def longest_prefix(s1, s2):
    """

    :param s1:
    :param s2:
    :return: le plus long prefix de s1 match dans s2
    ne fonctionne pas pour tous les tests de validations ...
    pas encore trouve ce qui cloche ... bizarre ...
    """
    l_max_prefix = 0
    for i_in_s1 in xrange(0, len(s1)):
        i_in_s2 = 0
        while (i_in_s1 < len(s1)) & (i_in_s2 < len(s2)):
            if s1[i_in_s1] != s2[i_in_s2]:
                break
            i_in_s1 += 1
            i_in_s2 += 1
        l_max_prefix = max(i_in_s2, l_max_prefix)
    return l_max_prefix


def solver_simple(list_strings):
    """
        methodes utilisees:
        - filter_substrings
        - longest_prefix
    """
    list_strings = filter_substrings(list_strings)

    sum_lengths_strings = sum(len(s) for s in list_strings)

    optimize_char_in_prefix_common = 0
    if len(list_strings) > 1:
        optimize_char_in_prefix_common = max(
            [
                sum(
                    map(
                        lambda tup: longest_prefix(list_strings[tup[0]], list_strings[tup[1]]),
                        zip(list_indices[:-1], list_indices[1:]))
                )
                for list_indices in permutations(range(len(list_strings)), len(list_strings))
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
#print solver_simple(list_seqs)