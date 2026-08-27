import heapq

class Node:
    def __init__(self, state, parent=None, action=None, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost

    def __str__(self):
        return f"Node(state={self.state}, action={self.action}, cost={self.cost})"

    def representation(self):
        return self.state


class Frontier:
    def __init__(self, evaluation_function):
        self.evaluation_function = evaluation_function
        self.frontierNode = []
        self.cont = 0

    def is_empty(self):
        return len(self.frontierNode) == 0

    def pop(self):
        if self.is_empty():
            raise Exception("frontera vacia")
        delete = heapq.heappop(self.frontierNode)
        return delete[2]

    def top(self):
        if self.is_empty():
            raise Exception("frontera vacia")
        return self.frontierNode[0][2]

    def add(self, node):
        valor = self.evaluation_function(node)
        heapq.heappush(self.frontierNode, (valor, self.cont, node))
        self.cont += 1


class Problem:
    def __init__(self, station_initial, station_goal, routes):
        self.station_initial = station_initial
        self.station_goal = station_goal
        self.routes = routes

    def is_goal(self, state):
        return state[0] == self.station_goal

    def result_actions(self):


    def action_cost(self):


    def heuristic(self):


FAIL = Node(None)

def expand(problem, node):
    state = node.state
    neighbors = problem.result_actions(state)
    neighbors = list(neighbors)
    expansion = []
    for neighbor in neighbors:
        cost = problem.action_cost(state, neighbor, neighbor) + node.cost
        node_1 = Node(neighbor, node, neighbor, cost)
        expansion.append(node_1)

    return expansion

def best_first_search(problem, evaluation_function):
    root_node = Node(problem.initial_state, None, None, 0)
    frontier = Frontier(evaluation_function)
    frontier.add(root_node)

    while not frontier.is_empty():
        current_node = frontier.pop()

        if problem.is_goal(current_node.state):
            return current_node

        for neighbor in expand(problem, current_node):
            frontier.add(neighbor)
    return FAIL

def path_actions(node):
    nodes = []
    while True:
        nodes.append(node)
        if node.parent == None:
            break
        node = node.parent

    nodes.reverse()

    actions = []
    for node in nodes:
        action = node.state
        actions.append(action)

    return actions


problem = Problem()

resultado = best_first_search(problem, lambda node: node.cost + problem.heuristic())

solution = path_actions(resultado)
solution_visual =
print(solution_visual)










