import collections
import re
# import sys

Token = collections.namedtuple('Token', ['typ', 'value', 'line', 'column'])

"""
        elif kind == 'MISMATCH':
            #raise RuntimeError('%r unexpected on line %d' % (value, line_num))
            pass
        """


def tokenize(code):
    """

    :param code:
    :return:
    """
    token_specification = [
        ('BLOCK_START', r'\('),  # Block start definition
        ('BLOCK_END', r'\)'),  # Block end
        ('ID', r"'[A-Za-z0-9\(\)=; \t\n]*'"),  # Identifiers
        ('BOOL', r"(false|true)"),  # Boolean
        ('NUMBER', r'\d+(\.\d*)?'),  # Integer or decimal number
        ('ASSIGN', r'='),  # Assignment operator
        ('END', r';'),  # Statement terminator
        ('NEWLINE', r'\n'),  # Line endings
        ('MISMATCH', r'.'),  # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    cur_col = 0
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group(kind)
        if kind == 'NEWLINE':
            pass
        elif kind == 'SKIP':
            pass
        elif kind == 'MISMATCH':
            pass
        else:
            # debug:
            #yield Token(kind, value, 0, 0)
            #
            if kind == 'BLOCK_START':
                cur_col += 1
                yield '\n' + '    ' * (cur_col - 1) + '(' + '\n' + '    ' * cur_col
            elif kind == 'BLOCK_END':
                cur_col -= 1
                yield '\n' + '    ' * cur_col + ')'
            elif kind == 'END':
                yield ';' + '\n' + '    ' * cur_col
            else:
                yield value


n = int(raw_input())
cgxlines = ''
for i in xrange(n):
    cgxlines += raw_input()

print re.sub(u'(?imu)^\s*\n', u'', ''.join(tokenize(cgxlines)))
# debug:
#print list(tokenize(cgxlines))
