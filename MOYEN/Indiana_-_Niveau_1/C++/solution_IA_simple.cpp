#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>

using namespace std;

enum
{
    NORTH = 0,
    EAST,
    SOUTH,
    WEST,
    //
    NO_WAY,
    LAST_DIR
} E_Dir;

const int offset_dir[LAST_DIR][2] = {
    {0, -1},
    {1, 0},
    {0, 1},
    {-1, 0},
    //
    {0, 0}
};

typedef struct
{
    int ways[4];
} typ_piece;

#define NB_TYPE_PIECE 14

const typ_piece list_pieces_IO[NB_TYPE_PIECE] = {
    {NO_WAY,  NO_WAY,   NO_WAY,   NO_WAY},  // Type0
    //
    {SOUTH,   SOUTH, NO_WAY,    SOUTH},  // Type1
    //
    {NO_WAY, WEST, NO_WAY, EAST},  // Type2
    {SOUTH,   NO_WAY,   NO_WAY,   NO_WAY},  // Type3
    //
    {WEST,    SOUTH,    NO_WAY,   NO_WAY},  // Type4
    {EAST,    NO_WAY,   NO_WAY,   SOUTH},   // Type5
    //
    {NO_WAY,  WEST,     NO_WAY,   EAST},    // Type6
    {SOUTH, SOUTH, NO_WAY, NO_WAY},  // Type7
    {NO_WAY, SOUTH, NO_WAY, SOUTH},  // Type8
    {SOUTH, NO_WAY, NO_WAY, SOUTH},  // Type9
    //
    {WEST, NO_WAY, NO_WAY, NO_WAY},  // Type10
    {EAST, NO_WAY, NO_WAY, NO_WAY},  // Type11
    {NO_WAY, SOUTH, NO_WAY, NO_WAY},  // Type12
    {NO_WAY, NO_WAY, NO_WAY, SOUTH},  // Type13
};

/**
 * url: http://www.sbin.org/doc/HOWTO/C++Programming-HOWTO-7.html
 * */
void Tokenize(const string& str,
                      vector<string>& tokens,
                      const string& delimiters = " ")
{
    // Skip delimiters at beginning.
    string::size_type lastPos = str.find_first_not_of(delimiters, 0);
    // Find first "non-delimiter".
    string::size_type pos     = str.find_first_of(delimiters, lastPos);

    while (string::npos != pos || string::npos != lastPos)
    {
        // Found a token, add it to the vector.
        tokens.push_back(str.substr(lastPos, pos - lastPos));
        // Skip delimiters.  Note the "not_of"
        lastPos = str.find_first_not_of(delimiters, pos);
        // Find next "non-delimiter"
        pos = str.find_first_of(delimiters, lastPos);
    }
}

std::map<std::string, int> map_POS = {
    {"TOP", NORTH},
    {"LEFT", WEST},
    {"RIGHT", EAST}
};

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
int main()
{
    int W; // number of columns.
    int H; // number of rows.
    cin >> W >> H; cin.ignore();
    
    std::string * LINES = new std::string[H];
    
    for (int i = 0; i < H; i++) {
        string LINE; // represents a line in the grid and contains W integers. Each integer represents one room of a given type.
        getline(cin, LINE);
        LINES[i] = LINE;
    }
    int EX; // the coordinate along the X axis of the exit (not useful for this first mission, but must be read).
    cin >> EX; cin.ignore();

    // game loop
    while (1) {
        int XI;
        int YI;
        string POS;
        cin >> XI >> YI >> POS; cin.ignore();
        
        vector<string> tokens;
        Tokenize(LINES[YI], tokens, " ");
        const int id_piece = std::stoi(tokens[XI]);
        //cerr << "Debug messages - id_piece: " << id_piece << endl;
        
        const int i_POS = map_POS[POS];
        //cerr << "Debug messages - i_POS:" << i_POS << endl;
        const int dir = list_pieces_IO[id_piece].ways[i_POS];
        //cerr << "dir: " << dir << endl;
        
        //cerr << "offset: " << offset_dir[dir][0] << endl;
        //cerr << "offset: " << offset_dir[dir][1] << endl;
        const int* offset = offset_dir[dir];
        
        const int XI_2 = XI + offset[0];
        const int YI_2 = YI + offset[1];
        
        // Write an action using cout. DON'T FORGET THE "<< endl"
        // To debug: cerr << "Debug messages..." << endl;

        //cout << "0 0" << endl; // One line containing the X Y coordinates of the room in which you believe Indy will be on the next turn.
        cout << XI_2 << " " << YI_2 << endl; // One line containing the X Y coordinates of the room in which you believe Indy will be on the next turn.
    }
}
