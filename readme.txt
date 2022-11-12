#Requirement:
>= Python 3.5
simplejson==3.13.2
pygame==1.9.3
PyOpenGL==3.1.0
numpy==1.14.0

#Solver
Command: python solver.py "level" "Algorithm"
         level: 01->15
         Algorithm:
            - DFS: Depth First Search
            - BFS: Breadth First Search
            - GA: Genetic algorithm
        Ex: python solver.py 01 DFS

#Visual
Command: python visual.py ./level/"x".json 
         x: 1->15
         Enter the solution: String of path
          - U: Up
          - D: Down
          - R: Right
          - L: Left
        Ex: python visual.py ./level/1.json 
        -> Enter the solution: RRDRRRD