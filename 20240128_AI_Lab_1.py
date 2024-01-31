"""
Option 3: N-Puzzle (for GWIDs ending with 1,2,4)
- Description: 
  Write a program that solves the N-puzzle on an n*n grid. The goal is to rearrange the square blocks
  of the puzzle to be in order with the fewest possible moves. The puzzle includes numbers from 1 to N,
  with one blank space. Squares can be moved horizontally and vertically into the blank space.

- Examples:
  8-Puzzle: A 3*3 grid labeled 1 through 8 and one blank square.
  15-Puzzle: A 4*4 grid labeled 1 through 15 and one blank square.

- Algorithm: 
  Use the A* search algorithm for the implementation.

- Constraints: 
  The size of the grid, n, must be between 3 and 25 (3 <= n <= 25).

- Input Format:
  A file with n lines, each containing n numbers separated by tabs, representing the puzzle configuration.
  The number 0 represents the blank space. The program should be able to handle any data size within the
  specified constraints. A sample file 'n-puzzle.txt' is provided.

- Note:
  A graphical user interface is not required for this implementation.
"""
# shi qiu 20240128 6511 Ai class Lab 1
import heapq
import copy
import time
import random


class Node:
    def __init__(self, matrix, g, h):
        self.matrix = matrix

        self.g = g  # Steps taken
        self.h = h  # dist to ideal
        self.f = g + h  # Total cost

    def __lt__(self, other):
        # priority queue f compare
        return self.f < other.f


class N_Puzzle:
    def ideal_matrix(length):
        complete_matrix = [[-1] * length for _ in range(length)]
        # print(complete_matrix)
        num = 1
        for row in range(length):
            for col in range(length):
                if num == length**2:
                    num = 0
                complete_matrix[row][col] = num
                num += 1
        # print(complete_matrix)
        return complete_matrix

    # --------------------------- create correct matrix
    def manhattan_dist(current, ideal):
        dist = 0
        current_dict = {}
        ideal_dict = {}

        for row in range(len(current)):
            for col in range(len(current[0])):
                current_dict[current[row][col]] = (row, col)
                ideal_dict[ideal[row][col]] = (row, col)
        for key in current_dict:
            if key != 0:
                dist += abs(current_dict[key][0] - ideal_dict[key][0]) + abs(
                    current_dict[key][1] - ideal_dict[key][1]
                )
        return dist

    # --------------------------------- calculate distance between current and correct matrix

    def hashable(matrix):
        return tuple(tuple(row) for row in matrix)

    # ----------------- turn matrix addable to close set

    def get_next(matrix):
        # give current matrix, return next possiable matrixs
        next_matrix = []
        n = len(matrix)
        r, c = 0, 0
        for row in range(n):
            for col in range(n):
                if matrix[row][col] == 0:
                    r = row
                    c = col
                    break
        dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for d in dir:
            if 0 <= r + d[0] < n and 0 <= c + d[1] < n:
                matrix[r][c], matrix[r + d[0]][c + d[1]] = (
                    matrix[r + d[0]][c + d[1]],
                    matrix[r][c],
                )
                next_matrix.append([row[:] for row in matrix])
                matrix[r][c], matrix[r + d[0]][c + d[1]] = (
                    matrix[r + d[0]][c + d[1]],
                    matrix[r][c],
                )
        return next_matrix

    # ------------- Generate next possible matrix list

    def A_Star(self, given_matrix):  # return min possible steps
        open_set = []
        closed_set = set()
        ideal_positions = N_Puzzle.ideal_matrix(len(given_matrix))

        start_node = Node(
            given_matrix,
            0,
            N_Puzzle.manhattan_dist(given_matrix, ideal_positions),
        )
        heapq.heappush(open_set, start_node)

        node_count = 0

        while open_set:
            current = heapq.heappop(open_set)
            if current.h == 0:
                return current.g  # Return number of steps to solution
            node_count += 1
            if node_count > 1000:  # about 10s
                return -2  # too big to search, posibily no solution

            closed_set.add(N_Puzzle.hashable(current.matrix))

            for next_matrix in N_Puzzle.get_next(current.matrix):
                if N_Puzzle.hashable(next_matrix) in closed_set:
                    continue

                g = current.g + 1  # steps+1
                h = N_Puzzle.manhattan_dist(next_matrix, ideal_positions)
                next_node = Node(next_matrix, g, h)

                found = False
                for node in open_set:
                    if N_Puzzle.hashable(node.matrix) == N_Puzzle.hashable(next_matrix):
                        found = True  # in open_set
                        break

                if not found:
                    heapq.heappush(open_set, next_node)

        return -1

    def main():
        print("Program Start\n")
        matrix = []
        with open("n-puzzle.txt", "r") as file:
            for line in file:
                print(line)
                row = [int(num) for num in line.split()]
                matrix.append(row)
        # print(matrix)
        complete_matrix = N_Puzzle.ideal_matrix(3)

        # -------------------get_next test
        # print(N_Puzzle.get_next(matrix))
        # print(N_Puzzle.get_next(complete_matrix))
        # -------------------

        print(N_Puzzle.manhattan_dist(matrix, complete_matrix))

        puzzle_solver = N_Puzzle()
        start_time = time.time()

        steps = puzzle_solver.A_Star(matrix)
        print(format(time.time() - start_time))
        print("Minimum steps to solve the puzzle:", steps)
        # random generate test:

        # ------------------------------file read


# N_Puzzle.main()


def random_solve(n):
    def generate_matrix(n):
        numbers = list(range(n * n))
        random.shuffle(numbers)
        return [numbers[i * n : (i + 1) * n] for i in range(n)]

    def print_matrix(matrix):
        for row in matrix:
            print(" ".join(str(num).ljust(2) for num in row))

    random_matrix = generate_matrix(n)
    print("Randomly Generated N-Puzzle:")
    print_matrix(random_matrix)

    puzzle_solver = N_Puzzle()
    start_time = time.time()
    steps = puzzle_solver.A_Star(random_matrix)
    end_time = time.time()

    print("\nTime Taken: {:.2f} seconds".format(end_time - start_time))
    if steps == -2:
        print("Search interrupted after 1000 nodes.")
    elif steps == -1:
        print("No solution found.")
    else:
        print("Minimum steps to solve the puzzle:", steps)


random_solve(3)
