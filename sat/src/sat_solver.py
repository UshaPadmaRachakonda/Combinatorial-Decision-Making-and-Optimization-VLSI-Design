from itertools import combinations
import z3
import numpy as np
from time import time

class SAT_Solver:
    def __init__(self, config):
        self.config = config

    def at_least_one_np(self, bool_vars):
        return z3.Or(bool_vars)

    def at_most_one_np(self, bool_vars, name = ""):
        return [z3.Not(z3.And(pair[0], pair[1])) for pair in combinations(bool_vars, 2)]

    def at_least_one_he(self, bool_vars):
        return self.at_least_one_np(bool_vars)

    def at_most_one_he(self, bool_vars, name):
        if len(bool_vars) <= 4:
            return z3.And(self.at_most_one_np(bool_vars))
        y = z3.Bool(f"y_{name}")
        return z3.And(z3.And(self.at_most_one_np(bool_vars[:3] + [y])), z3.And(self.at_most_one_he(bool_vars[3:] + [z3.Not(y)], name+"_")))

    def exactly_one_he(self, bool_vars, name):
        return z3.And(self.at_most_one_he(bool_vars, name), self.at_least_one_he(bool_vars))

    def check_solution(self, data, l):
        line, circuits = data

        y_max = np.argmax([y for _, y in circuits])
    
        w = int(line[0])
        # x,y = zip(*circuits)
    
    
        board = [[[z3.Bool(f"board_y{i}_x{j}_c{k}") for k in range (len(circuits))] for j in range (w)] for i in range (l)]
    
        s = z3.Solver()
    
        # no overlapping
        for j in range(w):
            for i in range(l):
                s.add(self.at_most_one_he(board[i][j], f"board_y{i}_x{j}"))
    
        # position
        position_constraints = []
        for i, circuit in enumerate(circuits):
            x, y = circuit
            all_positions = []

            for k in range(l - y + 1): # y
                for j in range(w - x + 1): # x
                    circuit_position = []
                    for y_h in range(l):
                        for x_h in range(w):
                            if y_h >= k and y_h < k + y and x_h >= j and x_h < j + x:
                                circuit_position.append(board[y_h][x_h][i])
                            else:
                                circuit_position.append(z3.Not(board[y_h][x_h][i]))
                    # for y_h in range(k, k + y):    
                    #     for x_h in range(j, j + x):
                    #             circuit_position.append(board[y_h][x_h][i])
                    all_positions.append(z3.And(circuit_position))

            
            if x!= y and self.config.rotate and x < l and y < w:
                
                for j in range(l - x + 1):
                    for k in range(w - y + 1):
                        rotated_circuit_position = []
                        for y_h in range(l):
                            for x_h in range(w):
                                if y_h >= j and y_h < j + x and x_h >= k and x_h < k + y:
                                    rotated_circuit_position.append(board[y_h][x_h][i])
                                else:
                                    rotated_circuit_position.append(z3.Not(board[y_h][x_h][i]))
                        # for y_h in range(j, j + x):
                        #     for x_h in range(k, k + y):
                        #             rotated_circuit_position.append(board[y_h][x_h][i])
                all_positions.append(z3.And(rotated_circuit_position))
            
            position_constraints.append(self.exactly_one_he(all_positions, f"all_positions_{i}"))
        
        s.add(position_constraints)
        x, y = circuits[y_max]

        # symmetry breaking
        s.add([board[y_h][x_h][y_max]  for x_h in range(x) for y_h in range(y)])
        
        if s.check() == z3.sat:
            return np.array([[[z3.is_true(s.model()[board[i][j][k]]) for k in range (len(circuits))] for j in range (w)] for i in range (l)])
        else:
            return None
    def get_solution(self, board, circuits):
        solution = f"{len(board[0])} {len(board)}\n{len(circuits)}\n"
        for i, circuit in enumerate(circuits):
            x, y = circuit
            # get bottom left corner
            y1, x1 = list(zip(*np.where(board[:, :, i])))[0]

            x_r = board[y1, :, i].sum()
            y_r = board[:, x1, i].sum()

            rotated = x_r != x or y_r != y

            solution+= f"{x} {y} {x1} {y1} {int(rotated)}\n"
        return solution
    def solve(self, data):
        w, circuits = data
        w = int(w[0])
        _, y = zip(*circuits)

        l_max = sum(y)
        l_min = max(y)
        start_time = time()
        for l in range(l_min, l_max + 1):
            print("\t \t trying", l)
            board = self.check_solution(data, l)
            duration = time() - start_time
            if duration > self.config.timelimit:
                return duration, None
            if board is not None:
                duration = time() - start_time
                return duration, self.get_solution(board, circuits)
        duration = time() - start_time
        return duration, None


   