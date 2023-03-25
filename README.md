# Combinatorial Decision Making and Optimization: VLSI Design

each model can be run from the root directory of the project with the following command:
    
```bash
python <model_name>/src/main.py
```
## Models
we have implemented the following models:
- CP
- SAT
- MIP

## CP
### Requirements
To run the CP model [MiniZinc](https://www.minizinc.org/software.html) is required.
### Parameters
The CP model can be run with the following parameters:
- instance: the instance to be solved(or the path to the instances)
-  timelimit: the time limit for the solver
-  solver: the solver to be used (gecode or chuffed)
- model: the model to be used (defined inside cp/src/cp or cp/src/cp_rotate)
- cores (optional): the number of cores to be used by the solver
- rotate (optional): if the circuit can be rotated
- visualize (optional): if the solution should be visualized

## SAT
### Requirements
To run the SAT model z3 is required.
### Parameters
The SAT model can be run with the following parameters:
- instance: the instance to be solved(or the path to the instances)
- timelimit: the time limit for the solver
- rotate (optional): if the circuit can be rotated
- visualize (optional): if the solution should be visualized

## MIP
### Requirements
To run the MIP model pulp is required.
Also if we choose to use Gurobi as the solver, it is required to be installed.
### Parameters
The MIP model can be run with the following parameters:
- instance: the instance to be solved(or the path to the instances)
- timelimit: the time limit for the solver
- cores (optional): the number of cores to be used by the solver
- rotate (optional): if the circuit can be rotated
- visualize (optional): if the solution should be visualized


## Visualization
The visualization of the solution is done with the following command:
```bash 
python plot_solution.py <instance> <save_path>
```
where the instance is the instance to be visualized and save_path (optional) is the path where the image should be saved.
