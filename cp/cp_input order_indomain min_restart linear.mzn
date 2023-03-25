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
array[CIRCUITS] of var 0..w: x_h;
array[CIRCUITS] of var 0..l_max: y_h;


% Global constraints

constraint cumulative(x_h, x, y, l);
constraint cumulative(y_h, y, x, w);



% do not overlap
constraint diffn(x_h, y_h, x, y);

% Implied constraints
constraint max([x_h[i] + x[i] | i in CIRCUITS]) <= w;

% Symmetries breaking constraints
constraint (y_h[max_y] = 0 /\ x_h[max_y] = 0);




% objective
var int: l = max([y_h[i] + y[i] | i in CIRCUITS]);

% Search
ann: search_ann_x;
search_ann_x = int_search(x_h, input_order, indomain_min);
ann: search_ann_y = int_search(y_h, input_order, indomain_min);
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
  ["\n\(x[i]) \(y[i]) \(x_h[i]) \(y_h[i]) 0" | i in CIRCUITS];
  