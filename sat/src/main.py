import argparse
from pathlib import Path
import os
from sat_solver import SAT_Solver
from utils import read_file, plot
import pandas as pd

def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--instance', type=str, default='./instances')
    parser.add_argument('--timelimit', type=int, default=300)
    parser.add_argument('--rotate', type=bool, default=False)
    parser.add_argument('--visualize', type=bool, default=True)
    args = parser.parse_args()

    return args



def write_output(output, path, name):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + name, 'w') as f:
        f.write(output)
    
def execute_solver(args):


    data = read_file(args.instance)
    solver = SAT_Solver(args)

    duration, output =  solver.solve(data)
    
    if output:
        output+=f"{duration}"
        if args.rotate:
            path = f'./sat/out/sat_rotate/sat_sb/'
        else:
            path = f'./sat/out/sat/sat_sb/'
        name = Path(args.instance).stem + '.txt'
        write_output(output, path, name)
        if args.visualize:
            plot(read_file(path + name))
    
    return duration, output
        

def main(args):
    # is a folder

    if Path(args.instance).is_dir():
        instances = sorted(list(Path(args.instance).glob('*.txt')), key=lambda x: int(x.stem.split('-')[1].split('.')[0])) 
    else:
        instances = [Path(args.instance)]
    for entry in instances:
        print(f"Processing {entry.stem}")
        args.instance = str(entry)
        _, output = execute_solver(args)
        if output:
            print(f"- success")
        else:
            print(f"- failed")
        

if __name__ == '__main__':
    args = read_args()
    main(args)

 