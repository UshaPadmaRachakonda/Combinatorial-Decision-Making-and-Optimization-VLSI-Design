include "diffn.mzn";
include "cumulative.mzn";

int: w; % width
int: n;

set of int: CIRCUITS = 1..n;

array[CIRCUITS] of int : x;
array[CIRCUITS] of int : y;

int: l_max = sum(y);
int: max_y = arg_max(y);

% decision variable
array[CIRCUITS] of var 0..w: p_x;
array[CIRCUITS] of var 0..l_max: p_y;
array[CIRCUITS] of var bool: orientation;

array[CIRCUITS] of var 0..l_max: y_r = [if orientation[i] then x[i] else y[i] endif | i in CIRCUITS];
array[CIRCUITS] of var 0..w: x_r = [if orientation[i] then y[i] else x[i] endif | i in CIRCUITS];


%  Global constraints

constraint cumulative(p_x, x_r, y_r, l);
constraint cumulative(p_y, y_r, x_r, w);

% do not overlap
constraint diffn(p_x, p_y, x_r, y_r);

constraint forall (i in CIRCUITS) ( if(y[i] > w) then orientation[i] == false else true endif); 

constraint max([p_x[i] + x[i] | i in CIRCUITS]) <= w;

% Implied constraints

constraint max([p_y[i] + y[i] | i in CIRCUITS]) <= l_max;
constraint forall (i in CIRCUITS) (x[i] == y[i] -> orientation[i] == false);

% Symmetries breaking constraints
constraint (p_y[max_y] = 0 /\ p_x[max_y] = 0);

% objective
var int: l = max([p_y[i] + y_r[i] | i in CIRCUITS]);

% Search
ann: search_ann_x;
search_ann_x = int_search(p_x, input_order, indomain_min);
ann: search_ann_y = int_search(p_y, input_order, indomain_min);
ann: restart_ann = restart_linear(100);
solve 
  :: search_ann_x
  :: search_ann_y
  :: restart_ann
  minimize l;

output [
  "\(w) \(l)\n",
  "\(n)",
  ] ++ 
  ["\n\(x[i]) \(y[i]) \(p_x[i]) \(p_y[i]) \(if orientation[i] then 1 else 0 endif)" | i in CIRCUITS];
  