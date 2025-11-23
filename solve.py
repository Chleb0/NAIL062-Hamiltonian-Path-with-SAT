from pysat.solvers import Glucose42
import subprocess
from argparse import ArgumentParser

class HamPathSolver:
    vertices: int
    graph: list
    solver: Glucose42

    def translate_index(self, out: int, to: int)->int:
        return out*self.vertices+to+1
    
    def translate_inv_index(self, out: int, to: int)->int:
        return out*self.vertices+to+1 + self.vertices*self.vertices

    def load_solver(self):

        for _ in range(self.vertices):
            clause = []

            for frm in range(self.vertices):
                for to in self.graph[self.vertices]:
                    clause.append(self.translate_index(frm,to))
            
            solver.add_clause(clause)

        for row in range(self.vertices):
            clause = [-(self.translate_index(row, i)) for i in range(self.vertices)]
            for out in range(self.vertices):
                clause[out] = self.translate_inv_index(row, out)
                solver.add_clause(clause)
                clause[out] = -(self.translate_index(row, out))
            
            real_clause = [self.translate_inv_index(row, i) for i in range(self.vertices)]
            solver.add_clause(real_clause)


        for row in range(self.vertices):
            clause = [-(self.translate_index(row, i)) for i in range(self.vertices)]
            for out in range(self.vertices):
                clause[out] = self.translate_inv_index(row, out)
                solver.add_clause(clause)
                clause[out] = -(self.translate_index(row, out))
            
            real_clause = [self.translate_inv_index(row, i) for i in range(self.vertices)]
            solver.add_clause(real_clause)

    def load_input(self):
        self.vertices, edges = list(map(int,input().split()))

        graph = [[] for _ in range(self.vertices)]
        
        for _ in range(edges):
            frm, to = list(map(int,input().split()))
            graph[frm].append(to)
            graph[to].append(frm)


if __name__ == "__main__":
    solver = Glucose42()

