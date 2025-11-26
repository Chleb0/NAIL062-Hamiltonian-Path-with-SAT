#!/bin/python3

from pysat.solvers import Glucose42
from argparse import ArgumentParser
import sys

class HamPathSolver:
    vertices: int
    graph: list
    my_clauses: list = []
    solver: Glucose42 = Glucose42()
    input_entered: bool = False

    def translate_index(self, out: int, to: int)->int:
        """
        Translates an index of x_vi into an index of the corresponding literal
        """
        return out*self.vertices+to+1
    
    def load_solver(self):
        """
        Load the solver with the saved clauses
        """

        for clause in self.my_clauses:
            self.solver.add_clause(clause)

    def load_clauses(self):
        """
        Generates and saves the clauses for the problem.
        Needs \"load_input\" to be run prior in order to work properly.
        """
        if not self.input_entered:
            print("You can't run \"load_clauses\" because you haven't loaded the input.\nLoad the input first with \"load_input\".")
            exit(1)

        # Make sure only vertices connected by an edge can be adjacent in the path
        for row in range(self.vertices):
            for frm in range(self.vertices):
                for to in range(self.vertices):
                    if self.graph[frm][to]:
                        clause = [
                            -self.translate_index(row, frm),
                            -self.translate_index((row+1)%self.vertices, to)
                        ]
                        self.my_clauses.append(clause)

        # Make sure every step has at least one vertex
        for row in range(self.vertices):
            self.my_clauses.append([self.translate_index(row,i) for i in range(self.vertices)])

        # Make sure every vertex is present in at least one step
        for column in range(self.vertices):
            self.my_clauses.append([self.translate_index(i,column) for i in range(self.vertices)])


        # Make sure a step has at most one vertex
        for row in range(self.vertices):
            for i in range(self.vertices):
                for j in range(self.vertices):
                    if i!=j:
                        self.my_clauses.append([-self.translate_index(row, i), -self.translate_index(row,j)])

        # Make sure a vertex is present in at most one step
        for column in range(self.vertices):
            for i in range(self.vertices):
                for j in range(self.vertices):
                    if i!=j:
                        self.my_clauses.append([-self.translate_index(i, column), -self.translate_index(j,column)])

    def load_input(self):
        """
        Loads input from the input file 
        """
        self.vertices, edges = list(map(int,input().split()))

        self.graph = [[True for _ in range(self.vertices)] for _ in range(self.vertices)]
        
        # Create an inverted adjacency matrix
        for _ in range(edges):
            frm, to = list(map(int,input().split()))
            self.graph[frm][to] = False
            self.graph[to][frm] = False
        
        self.input_entered = True

    def decode_model(self)->list:
        solution = self.solver.get_model()
        path = []

        for cycle in range(self.vertices):
            for vertex in range(self.vertices):
                index = cycle*self.vertices + vertex
                if solution[index] > 0:
                    path.append(vertex)
        
        return path

    def get_answer(self):
        if (self.solver.solve()):
            for vtx in self.decode_model():
                print(vtx)
        else:
            print("There is no Hamiltionian Cycle on this graph.")

    def _print_clause_dimacs(self, clause: list):
        for literal in clause:
            print(literal,end=" ")
        print(0)

    def print_dimacs(self):
        print("p cnf",self.vertices*self.vertices, len(self.my_clauses))
        for clause in self.my_clauses:
            self._print_clause_dimacs(clause)


def parse_args()->bool:
    """
    Parses the program arguments, opens the correct file to read from and opens the correct file to write into.
    """

    parser = ArgumentParser()

    parser.add_argument(
        "-i",
        "--inputfile",
        default="usestdin",
        type=str,
        help=(
            "The instance file. If no file is entered, the program will expect an input on stdin."
        ),
    )

    parser.add_argument(
        "-o",
        "--outputfile",
        default="usestdout",
        type=str,
        help=(
            "Output file for the solution to the problem. If no file is entered, the program will print the output on stdout."
        ),
    )

    parser.add_argument(
        "-d",
        "--dimacs",
        action="store_true",
        help="If set, output will be stored in \"formula.cnf\" as a DIMACS CNF encoding of the problem.",
    )

    args = parser.parse_args()

    if args.inputfile != "usestdin":
        try:
            sys.stdin = open(args.inputfile, "r")
        except Exception as e:
            raise RuntimeError(f"Failed to open input file '{args.input}': {e}")
    
    oppen = args.outputfile
    if args.dimacs:
        oppen = "formula.cnf"

    if oppen != "usestdout":
        try:
            sys.stdout = open(oppen, "w")
        except Exception as e:
            raise RuntimeError(f"Failed to open output file '{oppen}': {e}")
    
    return args.dimacs

if __name__ == "__main__":
    dimacs = parse_args()

    solv = HamPathSolver()
    solv.load_input()
    solv.load_clauses()

    if dimacs:
        solv.print_dimacs()
    else:
        solv.load_solver()
        solv.get_answer()

