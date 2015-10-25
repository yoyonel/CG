package main

import (
	"fmt"
	"math/rand"
)

// A Vec2 represents a vector with coordinates X and Y in 2-dimensional
// euclidian space.
type Vec2 struct {
	X, Y int
}

// A Size represents the dimensions of a rectangle.
type Size struct {
	// Width and height
	W, H int
}

var (
// V2Zero is the zero vector (0,0).
	V2Zero = Vec2{0, 0}
// V2Unit is the unit vector (1,1).
	V2Unit = Vec2{1, 1}
// V2UnitX is the x-axis unit vector (1,0).
	V2UnitX = Vec2{1, 0}
// V2UnitY is the y-axis unit vector (0,1).
	V2UnitY = Vec2{0, 1}
)

// V2 is shorthand for Vec2{X: x, Y: y}.
func V2(x, y int) Vec2 {
	return Vec2{x, y}
}

// Add returns the vector v+w.
func (v Vec2) Add(w Vec2) Vec2 {
	return Vec2{v.X + w.X, v.Y + w.Y}
}

// Neg returns the negated vector of v.
func (v Vec2) Neg() Vec2 {
	return v.Mul(-1)
}

// Mul returns the vector v*s.
func (v Vec2) Mul(s int) Vec2 {
	return Vec2{v.X * s, v.Y * s}
}

func (v Vec2) IsEqual(other Vec2) bool {
	return v.X == other.X && v.Y == other.Y
}

var (
	directions = []Vec2{
        V2UnitY.Neg(),
        V2UnitX.Neg(),
        V2UnitY,
        V2UnitX}
	i_dir = 0
	dir = directions[i_dir]
	center_board = Vec2{35/2,20/2}
	destination = center_board
)

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/

func position_on_board(pos Vec2) bool {
	return (pos.X >= 0) && (pos.X < 35) && (pos.Y >= 0) && (pos.Y < 20)
}

func cell_is_free(pos Vec2, board []string) bool {
	return board[pos.Y][pos.X] == '.'
}

func position_is_valid(pos Vec2, board []string) bool {
    return position_on_board(pos) && cell_is_free(pos, board)
}

func compute_next_position(pos Vec2, dir Vec2) Vec2 {
	return pos.Add(dir)
}

func main() {
	// opponentCount: Opponent count
	var opponentCount int
	fmt.Scan(&opponentCount)

	for {
		var gameRound int
		fmt.Scan(&gameRound)

		// x: Your x position
		// y: Your y position
		// backInTimeLeft: Remaining back in time
		var x, y, backInTimeLeft int
		fmt.Scan(&x, &y, &backInTimeLeft)
		pos := Vec2{x, y}

		for i := 0; i < opponentCount; i++ {
			// opponentX: X position of the opponent
			// opponentY: Y position of the opponent
			// opponentBackInTimeLeft: Remaining back in time of the opponent
			var opponentX, opponentY, opponentBackInTimeLeft int
			fmt.Scan(&opponentX, &opponentY, &opponentBackInTimeLeft)
		}

		board := make([]string, 0, 20)
		for i := 0; i < 20; i++ {
			// line: One line of the map ('.' = free, '0' = you, otherwise the id of the opponent)
			var line string
			fmt.Scan(&line)
			//
			board = append(board, line)
		}
		
		next_pos := compute_next_position(pos, dir)
		if position_is_valid(next_pos, board) {
			destination = next_pos
		    pos = next_pos
		} else {
			// Compute a new direction
			b_continue := true
			for i:=1; b_continue; i++ {
				i_dir = (i_dir+1)%4
				dir = directions[i_dir]
				next_pos = compute_next_position(pos, dir)
				b_continue = (i<3) && !position_is_valid(next_pos, board)
			}
			// is a valid direction/new position ?
			if position_is_valid(next_pos, board) {
				destination = next_pos
				pos = next_pos
			} else {
				if (pos.IsEqual(destination)) {
					if destination.IsEqual(center_board) {
						destination = Vec2{rand.Intn(35), rand.Intn(20)}
					} else {
						// if no new direction available go back to the center
						destination = center_board
					}
				} 
				pos = destination
			}
		}
		
		// fmt.Fprintln(os.Stderr, "Debug messages...")

		fmt.Printf("%v %v\n", int(pos.X), int(pos.Y)) // action: "x y" to move or "BACK rounds" to go back in time
	}
}