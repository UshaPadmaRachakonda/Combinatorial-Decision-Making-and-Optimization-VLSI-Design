
import os
from time import time
class CP_Solver():
    def __init__(self, config):
        if config.timelimit < 1000: # require time in ms instead of s
            config.timelimit *= 1000
        self.config = config

    def solve(self, path):
        command = 'minizinc.exe --solver {self.config.solver} --time-limit {self.config.timelimit} -p {self.config.cores} "{path}" "{self.config.model}"'
        command = command.format(self=self, path=path)
        start_time = time()
        output = os.popen(command).read()
        duration = time() - start_time
        if duration > self.config.timelimit / 1000:
            return duration, None
        return duration, output
        