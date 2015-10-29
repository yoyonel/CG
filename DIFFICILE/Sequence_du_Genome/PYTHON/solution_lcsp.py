__author__ = 'latty'

from os.path import commonprefix
from itertools import combinations


# url: https://en.wikipedia.org/wiki/Longest_common_substring_problem
# url: https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Longest_common_substring#Python2
def longest_common_substring(s1, s2):
    m = [[0] * (1 + len(s2)) for _ in xrange(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in xrange(1, 1 + len(s1)):
        for y in xrange(1, 1 + len(s2)):
            if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    return s1[x_longest - longest: x_longest], x_longest, longest


def compute_combinaisons_for_longest_common_substrings(list_strings):
    """

    :param list_strings:
    :return:
    """
    list_results = []
    for id0, id1 in combinations(range(len(list_strings)), 2):
        substr, s1_start, longest = longest_common_substring(list_strings[id0], list_strings[id1])
        if longest:
            list_results.append((id0, id1, substr, s1_start, longest))
    return list_results


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
    :return: On utilise l'algo dynamique de 'Longest Common Substring' pour recuperer les prefixes/suffixes qui nous
    interessent
    """
    m = [[(0, 0, 0)] * (1 + len(s2)) for _ in xrange(1 + len(s1))]

    for x in xrange(1, 1 + len(s1)):
        for y in xrange(1, 1 + len(s2)):
            m[x][y] = (x, y, m[x - 1][y - 1][2] + 1 if s1[x - 1] == s2[y - 1] else 0)
    return m


def longest_prefix_suffix_common_substring(s1, s2):
    """

    :param s1:
    :param s2:
    :return: On utilise l'algo dynamique de 'Longest Common Substring' pour recuperer les prefixes/suffixes qui nous
    interessent
    """
    m = unflat_list_of_list(compute_matrix_common_substring(s1, s2))
    longest_prefix = max(m, key=lambda tup: ((tup[1] == tup[2]) & (tup[0] == len(s1))) * tup[2])
    longest_suffix = max(m, key=lambda tup: ((tup[0] == tup[2]) & (tup[1] == len(s2))) * tup[2])
    return longest_prefix, longest_suffix


def compute_combinaisons_for_longest_prefix_suffix_substrings(list_strings):
    """

    :param list_strings:
    :return:
    """
    list_results = []
    for id0, id1 in combinations(range(len(list_strings)), 2):
        longest_prefix, longest_suffix = longest_prefix_suffix_common_substring(list_strings[id0], list_strings[id1])
        list_results.append((id0, id1, longest_prefix, longest_suffix))
    return list_results


def compute_fusion_with_prefix_suffix_common(s1, s2):
    """

    :param s1:
    :param s2:
    :return:
    """
    longest_prefix, longest_suffix = longest_prefix_suffix_common_substring(s1, s2)
    #
    i1, i2, lp = longest_prefix
    fusion_prefix = s1[:i1 - lp] + s1[i1 - lp:i1] + s2[i2:] if lp else ''
    #
    i1, i2, lp = longest_suffix
    fusion_suffix = s2[:i2 - lp] + s2[i2 - lp:i2] + s1[i1:] if lp else ''
    #
    return fusion_prefix, fusion_suffix


# url: http://stackoverflow.com/questions/11263172/what-is-the-pythonic-way-to-find-the-longest-common-prefix-of-a-list-of-lists
def longest_common_prefix_suffix(s1, s2):
    """

    :param s1:
    :param s2:
    :return:
    """
    return commonprefix([s1, s2[::-1]]), commonprefix([s1[::-1], s2])


def fusion_with_prefix(s1, s2, prefix):
    """

    :param s1:
    :param s2:
    :param prefix:
    :return:
    """
    lp = len(prefix)
    return s2[:-lp] + prefix + s1[lp:]


def levenshtein(s, t):
    ''' From Wikipedia article; Iterative with two matrix rows. '''
    if s == t:
        return 0
    elif len(s) == 0:
        return len(t)
    elif len(t) == 0:
        return len(s)
    v0 = [None] * (len(t) + 1)
    v1 = [None] * (len(t) + 1)
    for i in range(len(v0)):
        v0[i] = i
    for i in range(len(s)):
        v1[0] = i + 1
        for j in range(len(t)):
            cost = 0 if s[i] == t[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
        for j in range(len(v0)):
            v0[j] = v1[j]

    return v1[len(t)]


# url: http://stackoverflow.com/questions/4664850/find-all-occurrences-of-a-substring-in-python
def find_all(a_str, sub):
    """

    :param a_str:
    :param sub:
    :return:
    """
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        # start += len(sub) # use start += 1 to find overlapping matches
        start += 1


def find_longest_suffix_prefix_common(s1, s2):
    """

    :param s1:
    :param s2:
    :return:
     exemple: s1, s2 = 'AGATTA', 'GATTACA'
     : ind_start_s2, ind_start_s1, substr = find_longest_suffix_prefix_common(s1, s2)
     : print ind_start_s2, ind_start_s1, substr
        0 1 GATT
    """
    l1 = len(s1)
    i1 = l1 - 1
    l = []
    while i1:
        l = list(find_all(s2, s1[i1:]))
        print s2, s1[i1:]
        print l
        if len(l) <= 1:
            break
        i1 -= 1
    # print l
    #print i1
    if len(l):
        i2 = l[0]
        while s2[i2] == s1[i1]:
            if i2 == 0:
                break
            i2 -= 1
            i1 -= 1
        if i2:
            return None, None, []
        else:
            return i2, i1, s1[i1:]
    else:
        return None, None, []


def fusion_strings(s1, s2):
    """

    :param s1:
    :param s2:
    :return:
    """
    ind0_start_s2, ind0_start_s1, substr0 = find_longest_suffix_prefix_common(s1, s2)
    print ind0_start_s2, ind0_start_s1, substr0
    ind1_start_s2, ind1_start_s1, substr1 = find_longest_suffix_prefix_common(s2, s1)
    print ind1_start_s2, ind1_start_s1, substr1
    if len(substr0) >= len(substr1):
        return s1[:ind0_start_s1] + substr0 + s2[ind0_start_s2 + len(substr0):]
    else:
        return s2[:ind1_start_s2] + substr1 + s1[ind1_start_s1 + len(substr1):]


def compute_combinaisons_for_common_substrings(list_strings):
    """

    :param list_strings:
    :return:
        test: AGATTACAGA
        In [357]: gens
        Out[357]: ['AGATTA', 'GATTACA', 'TACAGA']

        In [358]: compute_combinaisons_for_common_substrings(gens)
        Out[358]:
        [(0, 1, 0, 1, 'GATTA'),
         (0, 2, 0, 4, 'TA'),
         (2, 0, 0, 3, 'AGA'),
         (1, 2, 0, 3, 'TACA'),
         (2, 1, 0, 4, 'GA')]

        test: CCCTGACATGA
        In [373]: gens
        Out[373]: ['CCCTG', 'TGACA', 'CATGA'
        In [372]: compute_combinaisons_for_common_substrings(gens)
        Out[372]: [(0, 1, 0, 3, 'TG'), (1, 2, 0, 3, 'CA'), (2, 1, 0, 2, 'TGA')]
        => cas interessant car le plus rentable est de choisir (1, 2) avec 'CA' au lieu de (2, 1) avec 'TGA'
        car on peut rentabiliser 'TG' en (0, 1) par la suite.
        - dans le choix: 'TGA', on a un total de 12 caracteres au final
        - dans le choix: 'CA', on a un total de 11 caracteres au final
    """
    list_results = []
    for id0, id1 in combinations(range(len(list_strings)), 2):
        i_s2, i_s1, substr = find_longest_suffix_prefix_common(list_strings[id0], list_strings[id1])
        if i_s2 is not None:
            list_results.append((id0, id1, i_s2, i_s1, substr))
        i_s2, i_s1, substr = find_longest_suffix_prefix_common(list_strings[id1], list_strings[id0])
        if i_s2 is not None:
            list_results.append((id1, id0, i_s2, i_s1, substr))
    return list_results
