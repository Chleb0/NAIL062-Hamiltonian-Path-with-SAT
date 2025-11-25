# Finding a Hamiltionian cycle with SAT-Solver

This repository contains a solver to the Hamiltionian cycle problem using SAT-solver tools, more specifically, Glucose 4.2.

## Problem description

The Hamiltonian Path problem is a decision problem asking whether a given graph contains a path that visits each vertex exactly once. 
An example of a valid input format would be a first line with positive integers $n$ (number of vertices) and $m$ (number of edges), followed by $m$ lines.
On the $i$-th line, there are positive integers $ 0 <= x,y < n$, denoting that an edge exists between $x$ and $y$.

**Example**:
```
5 5
0 1
1 2
4 0
2 3
3 4
```

## SAT Encoding

The problem is encoded with exactly $n^2$ variables.

## Usage

You'll need to complete a few steps in order to use the solver.

1. Install dependencies
2. Make the program executable
3. Prepare the input
4. Run the solver

### Installing dependencies

The solver uses a python library Python-SAT, you will need to install it before moving on.

You can install it by running:
```
pip install python-sat
```

### Making the program executable

Next, you will need to make the program executable.

To do this, run:
`chmod +x solve.py`

Alternatively, you can run the program directly with python, like so:
`python3 solve.py`

### Prepare the input

Prepare the problem you want the program to sovle