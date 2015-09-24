#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <iterator>

using namespace std;

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

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
int main()
{
    int N; // the number of temperatures to analyse
    cin >> N; cin.ignore();
    string TEMPS; // the N temperatures expressed as integers ranging from -273 to 5526
    getline(cin, TEMPS);

    //cerr << "TEMPS: " << TEMPS << endl;
    
    vector<string> tokens;
    Tokenize(TEMPS, tokens, " ");
    std::string min_temp = "0";
    
    if (tokens.size() > 0)
    {
        /** urls: 
         * http://www.cplusplus.com/reference/algorithm/min_element/
         * http://en.cppreference.com/w/cpp/language/lambda
         * http://www.cplusplus.com/reference/string/stoi/
         * */
        min_temp = *std::min_element(
            tokens.begin(), 
            tokens.end(), 
            [] (string s_n1, string s_n2) { 
                const int n1 = std::stoi(s_n1);
                const int n2 = std::stoi(s_n2);
                const int abs_n1 = abs(n1);
                const int abs_n2 = abs(n2);
                if ((abs_n1 == abs_n2) && n2 < 0)
                    return true;
                else
                    return abs_n1 < abs_n2;
            }
            );
        
        // Write an action using cout. DON'T FORGET THE "<< endl"
        // To debug: cerr << "Debug messages..." << endl;
    }

    cout << min_temp << endl;
}
