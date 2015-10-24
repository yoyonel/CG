#include<iostream>

using namespace std;

int i_nb_indents = 0;
bool b_new_line = true;

#define TOKEN_SPACE             ' '
#define TOKEN_QUOTE             '\''
#define TOKEN_NEWLINE           '\n'
#define TOKEN_TAB               '\t'
#define TOKEN_BLOCK_START       '('
#define TOKEN_BLOCK_END         ')'
#define TOKEN_BLOCK_SEPERATOR   ';'

#define PRINT_SPACES    cout << "    ";
#define PRINT_INDENTS                   \
    if(b_new_line)                      \
    for(int i=0;i<i_nb_indents;++i)     \
      PRINT_SPACES                      \
  b_new_line = false;

// url: http://stackoverflow.com/a/6936114
#define VA_NARGS_IMPL(_1, _2, _3, _4, _5, N, ...) N
#define VA_NARGS(...) VA_NARGS_IMPL(X,##__VA_ARGS__, 4, 3, 2, 1, 0)
#define VARARG_IMPL2(base, count, ...) base##count(__VA_ARGS__)
#define VARARG_IMPL(base, count, ...) VARARG_IMPL2(base, count, __VA_ARGS__)
#define VARARG(base, ...) VARARG_IMPL(base, VA_NARGS(__VA_ARGS__), __VA_ARGS__)

#define PRINT_TOKENS3(x, y, z) cout << x << y << z;
#define PRINT_TOKENS2(x, y) cout << x << y;
#define PRINT_TOKENS1(x) cout << x;
#define PRINT_TOKENS(...) VARARG(PRINT_TOKENS, __VA_ARGS__)

int main() {
    int n;
    cin >> n;
    bool b_begin_quote_sequence = false;
    char c;
    cin >> noskipws;
    while (cin >> c) {
        // on est dans une sequence de quote
        // on ne touche pas a la chaine de caractere a l'interieur de la sequence
        if (b_begin_quote_sequence) {
            // on verifie qu'on ne sort pas de la sequence de quote
            b_begin_quote_sequence = c != TOKEN_QUOTE;
            cout << c;
        }
        else {
            switch (c) {
                // on supprime les caracteres speciaux d'espaces/formatages
                case TOKEN_SPACE:
                case TOKEN_TAB:
                case TOKEN_NEWLINE:
                    break;
                    // on est tombe sur un ';' -> on commence une nouvelle ligne
                case TOKEN_BLOCK_SEPERATOR:
                    PRINT_TOKENS(TOKEN_BLOCK_SEPERATOR, TOKEN_NEWLINE)
                    b_new_line = true;
                    break;
                    // on demarre un nouveau bloc '('
                case TOKEN_BLOCK_START:
                    if (!b_new_line) {
                        PRINT_TOKENS(TOKEN_NEWLINE)
                        b_new_line = true;
                    }
                    PRINT_INDENTS
                    ++i_nb_indents;
                    PRINT_TOKENS(TOKEN_BLOCK_START, TOKEN_NEWLINE)
                    b_new_line = true;
                    break;
                    // on termine un bloc ')'
                case TOKEN_BLOCK_END:
                    if (!b_new_line) {
                        PRINT_TOKENS(TOKEN_NEWLINE)
                        b_new_line = true;
                    }
                    --i_nb_indents;
                    PRINT_INDENTS
                    PRINT_TOKENS(TOKEN_BLOCK_END)
                    break;
                    // on demarre une sequence quote '('
                case TOKEN_QUOTE:
                    b_begin_quote_sequence = true;
                    PRINT_INDENTS
                    PRINT_TOKENS(TOKEN_QUOTE)
                    break;
                    // sinon -> on affiche le caractere
                default:
                PRINT_INDENTS
                    cout << c;
            }
        }
    }
}