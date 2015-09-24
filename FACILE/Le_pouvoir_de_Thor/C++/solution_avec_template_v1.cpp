#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <algorithm>

using namespace std;

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 * ---
 * Hint: You can use the debug stream to print initialTX and initialTY, if Thor does not follow your orders.
 **/
 

// url: http://stackoverflow.com/questions/15724738/template-operator-overloading-implementation-outside-class-header
 // forward declarations
template<typename T> class TVec2;
template<typename T> TVec2<T> operator-(const TVec2<T> &a, const TVec2<T> &b);
template<typename T> TVec2<T> operator+(const TVec2<T> &a, const TVec2<T> &b);

 /**
  * Class for Vector2
  * */
  template <typename T>
 class TVec2 {
     
     public:
     TVec2<T>(T _x, T _y) : x(_x), y(_y) {}
     
     T norm2()      const { return x*x + y*y; }
     
     friend TVec2<T> operator-<>(const TVec2<T> &a, const TVec2<T> &b);
     friend TVec2<T> operator+<>(const TVec2<T> &a, const TVec2<T> &b);
     
     static T dist2(TVec2<T> v1, TVec2<T> v2) { return (v2 - v1).norm2(); }
     
     /**
      * convert Vec2 into std::string
      * url: http://stackoverflow.com/questions/5076472/how-can-i-format-a-stdstring-using-a-collection-of-arguments
      * */
     operator std::string () 
     { 
         std::stringstream s;
         s << "(" << x << ", " << y << ")";
         return s.str();
     }
     
     private:
     union {
         struct { T x, y; };
         T v[2];
     };
 };
 
template<class T>
TVec2<T> operator-(const TVec2<T> &a, const TVec2<T> &b) { return TVec2<T>(a.x - b.x, a.y - b.y); }
template<class T>
TVec2<T> operator+(const TVec2<T> &a, const TVec2<T> &b) { return TVec2<T>(a.x + b.x, a.y + b.y); }

 /**
  * Class for Direction
  * */
 template<typename T>
 class TDir {
     
     public:
     TDir<T>(TVec2<T> _offset, std::string _str_command) : v2_offset(_offset), str_command(_str_command), m_distance(T(0)) {}
     
     inline TVec2<T> move(const TVec2<T>& position) const { return position + v2_offset; }
     
     inline TVec2<T> offset() const { return v2_offset; }
     inline std::string command() const { return str_command; }
     inline T distance() const { return m_distance; } 
     
     inline T set_distance(const T &_distance) { m_distance = _distance; } ;
     
     private:
     TVec2<T> v2_offset;
     std::string str_command;
     T m_distance;
 };


// SPECIALIZATION DES TEMPLATES
typedef unsigned short ushort;
//
typedef TVec2<ushort> Vec2;
typedef TDir<ushort> Dir;
 
 /**
  * List of directions
  * */
 const std::vector<Dir> list_dir = {
     Dir(Vec2(0, -1), "N"),
     Dir(Vec2(+1, -1), "NE"),
     Dir(Vec2(+1, 0), "E"),
     Dir(Vec2(+1, +1),"SE"),
     Dir(Vec2(0, +1), "S"),
     Dir(Vec2(-1, +1),"SW"),
     Dir(Vec2(-1, 0), "W"),
     Dir(Vec2(-1, -1), "NW")
     };
 
 /**
  * Compute the index of the minimum element (using iterator)
  * url: http://stackoverflow.com/questions/9687957/index-of-minimum-element-in-a-stdlist
  * */
template <class ForwardIterator>
  std::size_t min_element_index ( ForwardIterator first, ForwardIterator last )
{
  ForwardIterator lowest = first;
  std::size_t index = 0;
  std::size_t i = 0;
  if (first==last) return index;
  while (++first!=last) {
    ++i;
    if (*first<*lowest) {
      lowest=first;
      index = i;
    }
  }
  return index;
}

/**
 * Tool class for distances computation (here the algorithm for choosing the direction)
 * */
class Tools_Distance 
{
    public:
    static float compute_distance_to(
        const Vec2& origin,
        const Vec2& destination,
        const Dir& direction
        )
        {
            // 'discrete' euclidian distance (distance in a grid, using a sqrt for calculation)
            //return Vec2::dist(direction.move(origin), destination);
            // square of 'discrete' euclidian (just dot product, no sqrt) [OPTIMISATION]
            return Vec2::dist2(direction.move(origin), destination);
        }
        
    static std::vector<float> compute_distance_to(
        const Vec2& origin,
        const Vec2& destination,
        const std::vector<Dir> list_dir
        )
        {
            std::vector<float> list_distances;
            
            for(const auto dir : list_dir)
            {
                const float& dist = compute_distance_to(origin, destination, dir);
                list_distances.push_back(dist);
            }
            return list_distances;
        }
    
    static Dir choose_direction(
        const Vec2& origin,
        const Vec2& destination,
        const std::vector<Dir> list_dir
        )
    {
        const std::vector<float>& list_distances = compute_distance_to(origin, destination, list_dir);
        const std::size_t& index = min_element_index(list_distances.begin(), list_distances.end());
        return list_dir[index];
    }
        
};

int main()
{
    const Tools_Distance td;
    
    int LX; // the X position of the light of power
    int LY; // the Y position of the light of power
    int initialTX; // Thor's starting X position
    int initialTY; // Thor's starting Y position
    cin >> LX >> LY >> initialTX >> initialTY; cin.ignore();
    
    Vec2 thor_pos(initialTX, initialTY);
    const Vec2 light_pos(LX, LY);
    
    // game loop
    while (1) {
        int E; // The level of Thor's remaining energy, representing the number of moves he can still make.
        cin >> E; cin.ignore();

        const Dir& cur_dir = td.choose_direction(thor_pos, light_pos, list_dir);
        thor_pos = cur_dir.move(thor_pos);
        const std::string& command = cur_dir.command();

        cout << command << endl;
    }
}
