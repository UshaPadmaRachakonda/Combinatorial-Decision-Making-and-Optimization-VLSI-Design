import pulp as plp
import namespace
from pathlib import Path
import numpy as np

from time import time
class MIP_Solver():

    def __init__(self, config):
        self.config = config

    def solve(self, data):
        line, circuits = data

        w = int(line[0])

        model = plp.LpProblem(name='mip', sense=plp.LpMinimize)

        x,y = zip(*circuits)

        l_max = sum(y)
        max_y = np.argmax(y)
        # variables
        l = plp.LpVariable('l', lowBound=max(y), upBound=l_max, cat='Integer')

        x_h = plp.LpVariable.dict('x_h', indices=range(len(circuits)), lowBound=0, upBound=w, cat='Integer') # TODO upBound = w - x[i] ?
        y_h = plp.LpVariable.dict('y_h', indices=range(len(circuits)), lowBound=0, upBound=l_max, cat='Integer') # TODO upBound = l - y[i] ?

        rotation = plp.LpVariable.dicts('rotation', indices=range(len(circuits)), lowBound=0, upBound=1, cat='Binary')
        
        # true rotated x and y
        x_r = plp.LpVariable.dicts('x_r', indices=range(len(circuits)), lowBound=0, upBound=w, cat='Integer')
        y_r = plp.LpVariable.dicts('y_r', indices=range(len(circuits)), lowBound=0, upBound=l_max, cat='Integer')

        # objective function
        model += l

        # constraints

        # rotation
        for i in range(len(circuits)):
            # apply rotation only if the length is smaller than the width and the circuit is not a square
            if self.config.rotate and y[i] < w and x[i] != y[i]:
                model += x_r[i] == rotation[i] * y[i] + (1 - rotation[i]) * x[i]
                model += y_r[i] == rotation[i] * x[i] + (1 - rotation[i]) * y[i]
            else:
                model += x_r[i] == x[i]
                model += y_r[i] == y[i]
                model += rotation[i] == 0
            model += y_h[i] + y_r[i] <= l
            model += x_h[i] + x_r[i] <= w

        # Symmetry breaking
        # model += x_h[max_y] == 0
        # model += y_h[max_y] == 0

        # no overlap
        delta = plp.LpVariable.dicts('delta', indices=(range(len(circuits)), range(len(circuits)), range(2)), lowBound=0, upBound=1, cat='Binary')

        for i in range(len(circuits) - 1):
            for j in range(i + 1, len(circuits)):
                model+= x_h[i] + x_r[i] <= x_h[j] + delta[i][j][0] * w
                model+= x_h[j] + x_r[j] <= x_h[i] + delta[j][i][0] * w
                model+= y_h[i] + y_r[i] <= y_h[j] + delta[i][j][1] * l_max
                model+= y_h[j] + y_r[j] <= y_h[i] + delta[j][i][1] * l_max

                model+= (delta[i][j][0] + delta[i][j][1] + delta[j][i][0] + delta[j][i][1] <= 3)

        start_time = time()
        model.solve(plp.GUROBI(msg=0, timeLimit=self.config.timelimit, threads=self.config.cores)) # TODO: check solver
        duration = time() - start_time

        if model.status != 1 and model.status != 2:
            return duration, None

        solution =f"{w} {int(plp.value(l))}\n{len(circuits)}\n"
        for i in range(len(circuits)):
            solution += f"{x[i]} {y[i]} {int(x_h[i].varValue)} {int(y_h[i].varValue)} {int(rotation[i].varValue)}\n"
       
        return duration, solution