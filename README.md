# solve-8-puzzle

The goal is to solve the 8-puzzle using tree search algorithms. 

This is the first project of the Artificial Intelligence Course of ColumbiaX on edx: https://www.edx.org/course/artificial-intelligence-ai-columbiax-csmm-101x-4

The game can be manually played here: http://mypuzzle.org/sliding (have a go it is not that easy :)

Command line execution: 

`python3 driver_3.py <method> <board>`

The following algorithms (methods) are used:
  * breadth-first search (`bfs`)
  * depth-first search (`dfs`)
  * A-star search (`ast`)


When executed, the program will create / write to a file called output.txt, containing the following statistics:

`path_to_goal`: the sequence of moves taken to reach the goal

`cost_of_path`: the number of moves taken to reach the goal

`nodes_expanded`: the number of nodes that have been expanded

`search_depth`: the depth within the search tree when the goal node is found

`max_search_depth`:  the maximum depth of the search tree in the lifetime of the algorithm

`running_time`: the total running time of the search instance, reported in seconds

`max_ram_usage`: the maximum RAM usage in the lifetime of the process as measured by the ru_maxrss attribute in the resource module, reported in megabytes

Note: running time and max_ram_usage will vary depending on the system.

#### Example 1:

`$ python3 driver_3.py bfs 1,2,5,3,4,0,6,7,8`

`path_to_goal: ['Up', 'Left', 'Left']`

`cost_of_path: 3`

`nodes_expanded: 10`

`search_depth: 3`

`max_search_depth: 4`

`running_time: 0.00188088`

`max_ram_usage: 0.07812500`

#### Example 2:

`$ python3 driver_3.py dfs 1,2,5,3,4,0,6,7,8`

`path_to_goal: ['Up', 'Left', 'Left']`

`cost_of_path: 3`

`nodes_expanded: 181437`

`search_depth: 3`

`max_search_depth: 66125`

`running_time: 5.01608433`

`max_ram_usage: 4.23940217`


## Test Cases
All these cases should work.

#### Test Case #1

`python3 driver_3.py bfs 3,1,2,0,4,5,6,7,8`

`python3 driver_3.py dfs 3,1,2,0,4,5,6,7,8`

`python3 driver_3.py ast 3,1,2,0,4,5,6,7,8`

#### Test Case #2

`python3 driver_3.py bfs 1,2,5,3,4,0,6,7,8`

`python3 driver_3.py dfs 1,2,5,3,4,0,6,7,8`

`python3 driver_3:.py ast 1,2,5,3,4,0,6,7,8`
