from red_datos import rutas, construir_rutas_por_estacion
from station_graph import graph
import heapq

TRAVEL_TIME = 2      # minutos estimados entre estaciones consecutivas
DWELL_TIME = 2        # minutos de parada al llegar a una estación
TRANSFER_TIME = 5     # minutos de penalización por transbordo


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
    def __init__(self, station_initial, station_goal, routes, graph):
        self.station_initial = station_initial
        self.station_goal = station_goal
        self.routes = routes
        self.routes_by_station = construir_rutas_por_estacion(routes)
        self.initial_state = (station_initial, None)
        self.distances_to_goal = graph.shortest_distances_from(station_goal)

    def is_goal(self, state):
        return state[0] == self.station_goal

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
            return 0  # abordar

        if route_1 is None:
            if station == self.station_goal:
                return 0
            return TRANSFER_TIME  # bajarse/transbordar

        return TRAVEL_TIME + DWELL_TIME  # avanzar

    def heuristic(self, state):
        station = state[0]
        return self.distances_to_goal.get(station, 0)


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
        if node.parent is None:
            break
        node = node.parent

    nodes.reverse()

    actions = []
    for node in nodes:
        action = node.state
        actions.append(action)

    return actions


def mostrar_resultado(problem, solution):
    for i in range(1, len(solution)):
        prev_station, prev_route = solution[i - 1]
        station, route = solution[i]

        if prev_route is None and route is not None:
            # se acaba de abordar una ruta
            print(f"Tomar: {route}")
        elif prev_route is not None and route is None:
            # se bajó; si no es el destino final, es un transbordo
            if station != problem.station_goal:
                print(f"Transbordo en: {station}")



problem = Problem("Portal Suba", "Portal Norte", rutas, graph)

resultado = best_first_search(problem, lambda node: node.cost + problem.heuristic(node.state))

if resultado is FAIL:
    print("No se encontró una ruta.")
else:
    solution = path_actions(resultado)
    mostrar_resultado(problem, solution)
    print("Tiempo total estimado:", resultado.cost, "minutos")