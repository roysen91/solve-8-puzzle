import sys
import time
import copy
import resource

class Queue:
	def __init__(self):
		self.items = []
		self.set = set()
	def isEmpty(self):
		return self.items == []
	def enqueue(self, item):
		self.items.insert(0,item)
		self.set.add(item)
	def dequeue(self):
		item = self.items.pop()
		self.set.discard(item)
		return item
	def peek(self):
		return self.items[-1]
	def size(self):
		return len(self.items)

class Stack:
	def __init__(self):
		self.items = []
		self.set = set()
	def isEmpty(self):
		return self.items == []
	def push(self,item):
		self.items.append(item)
		self.set.add(item)
	def pop(self):
		item = self.items.pop()
		self.set.discard(item)
		return item
	def peek(self):
		return self.items[-1]
	def size(self):
		return len(self.items)

class MinHeap:
	def __init__(self):
		self.items = []
		self.set = set()
	def insert(self,item):
		item.manhattan = manhattan(item.config)
		self.items.append(item)
		self.set.add(item)
		self.sort()
	def minimum(self):
		return self.items[-1]
	def extractMin(self):
		item = self.items.pop()
		self.set.discard(item)
		return item
	def decreaseKey(self,other,key):
		for item in self.items:
			if item.config == other.config:
				if item.manhattan > key:
					item.manhattan = key
					self.sort()
					break
	def isEmpty(self):
		return self.items==[]
	def sort(self):
		self.items = sorted(self.items, key= lambda item: item.manhattan, reverse=True)


def memo(f):
	"Memoize function f, whose args must all be hashable."
	cache = {}
	def fmemo(*args):
		if args not in cache:
			cache[args] = f(*args)
		return cache[args]
	fmemo.cache = cache
	return fmemo
@memo
def manhattan(config):
	cum = 0
	goal_index = {'1':(0,1),'2':(0,2),'3':(1,0),'4':(1,1),'5':(1,2),'6':(2,0),'7':(2,1),'8':(2,2)}
	config = list(config)
	for i,item in enumerate(config):
		if item != '0':
			row = int(i/3)
			col = i%3
			cum += abs(goal_index[item][0]-row)+abs(goal_index[item][1]-col)
	return cum


def bfs(initial_state):
	max_depth = 0
	expanded = 0
	Q = Queue()
	Q.enqueue(initial_state)
	explored = set()

	while not Q.isEmpty():
		state = Q.dequeue()
		explored.add(state)
		if state.goal_state():
			return expanded,max_depth,state
		expanded += 1
		for neighbor in state.neighbors():
			if neighbor not in Q.set and neighbor not in explored:
				Q.enqueue(neighbor)
				if neighbor.depth > max_depth:
					max_depth = neighbor.depth
	return expanded,max_depth,False

def dfs(initial_state):
	max_depth = 0
	expanded = 0
	S = Stack()
	S.push(initial_state)
	explored = set()

	while not S.isEmpty():
		state = S.pop()
		explored.add(state)
		if state.goal_state():
			return expanded,max_depth,state
		expanded += 1
		# push to stack in reverse UDLR order
		for neighbor in reversed(state.neighbors()):
			if neighbor not in S.set and neighbor not in explored:
				S.push(neighbor)
				if neighbor.depth > max_depth:
					max_depth = neighbor.depth
	return expanded,max_depth,False

def ast(initial_state):
	max_depth = 0
	expanded = 0
	H = MinHeap()
	H.insert(initial_state)
	explored = set()

	while not H.isEmpty():
		state = H.extractMin()
		explored.add(state)
		if state.goal_state():
			return expanded,max_depth,state
		expanded += 1
		for neighbor in state.neighbors():
			if neighbor not in H.set and neighbor not in explored:
				H.insert(neighbor)
				if neighbor.depth > max_depth:
					max_depth = neighbor.depth
				#else if neighbor in H.set:
			#		H.decreaseKey(neighbor)
	return expanded,max_depth,False

class State():
	def __init__(self,conf):
		# init 8-puzzle-board
		self.depth = 0
		self.parent = None
		self.mv = None
		self.zero_index = conf.index('0')
		self.config = conf
		self.manhattan = 0
	def goal_state(self):
		# check if final state is reached
		if self.config == '012345678':
			return True
		else:
			return False
	def __eq__(self,other):
		return self.config == other.config
	def __hash__(self):
		return hash(self.config)
	def neighbors(self):
		states = [self.move('Up'),self.move('Down'),self.move('Left'),self.move('Right')]
		neighbors = [state for state in states if state]
		return neighbors
	def swap(self,conf,i,j):
		conf = list(conf)
		conf[i],conf[j] = conf[j],conf[i]
		return ''.join(str(e) for e in conf)
	def move(self,direction):
		child = State(self.config)
		child.parent = self
		child.depth = self.depth+1
		child.mv = direction

		if direction == 'Up':
			if child.zero_index-3 > -1:
				child.config = self.swap(child.config,child.zero_index,child.zero_index-3)
				child.zero_index -= 3
				return child
			else:
				return False
		if direction == 'Down':
			if child.zero_index+3 < 9:
				child.config = self.swap(child.config,child.zero_index,child.zero_index+3)
				child.zero_index += 3
				return child
			else:
				return False
		if direction == 'Left':
			if child.zero_index-1 not in (-1,2,5):
				child.config = self.swap(child.config,child.zero_index,child.zero_index-1)
				child.zero_index -= 1
				return child
			else:
				return False
		if direction == 'Right':
			if child.zero_index+1 not in (3,6,9):
				child.config = self.swap(child.config,child.zero_index,child.zero_index+1)
				child.zero_index += 1
				return child
			else:
				return False


class Solver():
	def __init__(self,method,conf):
		self.method = method
		# init puzzle 
		self.start_state = State(''.join(str(e) for e in conf))
		self.end_state = None
		# path to goal
		self.path  = []
		# cost of path
		self.cost = len(self.path)
		# nodes expanded 
		self.nodes = 0
		# search depth
		self.depth = 0
		# max search depth 
		self.max_depth = 0
		self.time = 0
	def solve(self):
		start = time.time()
		if self.method == 'bfs':
			self.nodes,self.max_depth,state = bfs(self.start_state)
			self.depth = state.depth
			self.get_path(state)
		if self.method == 'dfs':
			self.nodes,self.max_depth,state = dfs(self.start_state)
			self.depth = state.depth
			self.get_path(state)
		if self.method == 'ast':
			self.nodes,self.max_depth,state = ast(self.start_state)
			self.depth = state.depth
			self.get_path(state)
		self.time = time.time()-start
		self.finish()
	def get_path(self,state):
		while state.parent is not None:
			self.path.insert(0,state.mv)
			self.cost += 1
			state = state.parent


	def finish(self):
		with open('output.txt','w') as f:
			f.write((	'path_to_goal: {}\n'
						'cost_of_path: {}\n'
						'nodes_expanded: {}\n'
						'search_depth: {}\n'
						'max_search_depth: {}\n'
						'running_time: {:.8f}\n'
						'max_ram_usage: {:.8f}\n'.format(self.path,self.cost,self.nodes,self.depth,self.max_depth,
							self.time,resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*10**-6)))



if __name__ == '__main__':
	method, config = sys.argv[1],list(map(int,sys.argv[2].split(',')))
	s = Solver(method,config)
	s.solve()
	sys.exit()
