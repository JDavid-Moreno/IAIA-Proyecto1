from routes import routes, build_routes_by_station
from station_graph import graph
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
        self.frontier_node = []
        self.count = 0

    def is_empty(self):
        return len(self.frontier_node) == 0

    def pop(self):
        if self.is_empty():
            raise Exception("empty frontier")
        delete = heapq.heappop(self.frontier_node)
        return delete[2]

    def top(self):
        if self.is_empty():
            raise Exception("empty frontier")
        return self.frontier_node[0][2]

    def add(self, node):
        value = self.evaluation_function(node)
        heapq.heappush(self.frontier_node, (value, self.count, node))
        self.count += 1


class Problem:
    def __init__(self, initial_station, goal_station, routes, graph):
        self.initial_station = initial_station
        self.goal_station = goal_station
        self.routes = routes
        self.routes_by_station = build_routes_by_station(routes)
        self.initial_state = (initial_station, None)
        self.distances_to_goal = graph.shortest_distances_from(goal_station)

    def is_goal(self, state):
        return state[0] == self.goal_station

    def result_actions(self, state):
        station, current_route = state
        new_states = []

        if current_route is None:
            for route_id in self.routes_by_station[station]:
                new_state = (station, route_id)
                new_states.append(new_state)
        else:
            route_stations = self.routes[current_route]["stations"]
            index = route_stations.index(station)

            if index + 1 < len(route_stations):
                next_station = route_stations[index + 1]
                new_state = (next_station, current_route)
                new_states.append(new_state)

            new_state = (station, None)
            new_states.append(new_state)

        return new_states

    def action_cost(self, state, action, state_1):
        station, route = state
        station_1, route_1 = state_1

        if route is None:
            return 0

        if route_1 is None:
            if station == self.goal_station:
                return 0
            return TRANSFER_TIME

        return TRAVEL_TIME + DWELL_TIME

    def heuristic(self, state):
        station = state[0]
        return self.distances_to_goal.get(station, 0)


FAIL = Node(None)
TRAVEL_TIME = 3
DWELL_TIME = 4
TRANSFER_TIME = 5

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
    reached = {}

    while not frontier.is_empty():
        current_node = frontier.pop()

        if current_node.state in reached and reached[current_node.state] <= current_node.cost:
            continue

        reached[current_node.state] = current_node.cost

        if problem.is_goal(current_node.state):
            return current_node

        for neighbor in expand(problem, current_node):
            frontier.add(neighbor)

    return FAIL


def path_actions(node):
    nodes = []
    while True:
        nodes.append(node)
        if node.parent is None:
            break
        node = node.parent
    nodes.reverse()
    actions = []

    for node in nodes:
        action = node.state
        actions.append(action)
    return actions


def show_result(problem, solution):
    for i in range(1, len(solution)):
        previous_station, previous_route = solution[i - 1]
        station, route = solution[i]

        if previous_route is None and route is not None:
            print(f"Tomar: {route}")

        elif previous_route is not None and route is None:
            if station != problem.goal_station:
                print(f"Transbordo en: {station}")


problem = Problem("Portal Norte", "Banderas", routes, graph)

result = best_first_search(
    problem,
    lambda node: node.cost + problem.heuristic(node.state)
)

if result is FAIL:
    print("No se encontro ruta.")
else:
    solution = path_actions(result)
    show_result(problem, solution)
    print()
    print("Duración:", result.cost, "minutos")