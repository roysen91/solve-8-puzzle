import driver_3 as dr
import time

def unit_test():
	start = time.time()
	puzzles = [[3,1,2,0,4,5,6,7,8],[1,2,5,3,4,0,6,7,8]]
	methods = ['bfs','dfs','ast']
	for puzzle in puzzles:
		for method in methods:
			s = dr.Solver(method,puzzle)
			s.solve()
	return time.time()-start

print(unit_test())

