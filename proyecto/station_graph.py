import heapq

stations_by_corridor = {
    "A": [
        "Calle 72", "Flores", "Calle 57", "Marly", "Avenida 39",
        "Calle 34", "Calle 26", "Calle 22", "Avenida Jimenez",
    ],
    "B": [
        "Terminal", "Calle 187", "Portal Norte", "Toberin", "Calle 161",
        "Mazuren", "Calle 146", "Calle 142", "Alcala", "Prado Veraniego",
        "Calle 127", "Pepe Sierra", "Calle 106", "Calle 100", "Virrey",
        "Calle 85", "Heroes",
    ],
    "C": [
        "Portal Suba", "La Campina", "Suba - Transversal 91", "21 Angeles",
        "Gratamira", "Suba - Avenida Boyaca", "Niza - Calle 127",
        "Humedal Cordoba", "Avenida Suba - Calle 116", "Puente Largo",
        "Suba - Calle 100", "Suba - Calle 95", "Rionegro", "San Martin",
    ],
    "D": [
        "Portal de la 80", "Quirigua", "Carrera 90", "Avenida Cali",
        "Granja - Carrera 77", "Minuto de Dios", "Boyaca", "Las Ferias",
        "Avenida 68", "Carrera 53", "Carrera 47", "Escuela Militar", "Polo",
    ],
    "E": [
        "La Castellana", "NQS Calle 75 - Zona M", "Av Chile", "7 de Agosto",
        "Movistar Arena", "Campin - Universidad Antonio Narino",
        "Universidad Nacional", "Avenida El Dorado", "CAD", "Paloquemao",
        "Ricaurte",
    ],
    "F": [
        "Portal Americas", "Biblioteca Tintal", "Transversal 86", "Banderas",
        "Mandalay", "Avenida Americas - Avenida Boyaca", "Marsella", "Pradera",
        "Distrito Grafiti", "Puente Aranda", "Carrera 43", "Zona Industrial",
        "CDS - Carrera 32", "Ricaurte", "San Facon - Carrera 22",
        "De La Sabana", "Avenida Jimenez",
    ],
    "G": [
        "Comuneros", "Santa Isabel", "Calle 30 Sur", "Calle 38A Sur",
        "General Santander", "Alqueria", "Venecia", "Sevillana",
        "Madelena", "Perdomo", "Portal Sur",
    ],
    "H": [
        "Hortua", "Narino", "Fucha", "Restrepo", "Olaya", "Quiroga",
        "Calle 40 Sur", "Santa Lucia", "Socorro", "Consuelo", "Molinos",
        "Danubio", "Portal Usme",
    ],
    "J": [
        "San Victorino", "Museo del Oro",
        "Las Aguas - Centro Colombo Americano", "Universidades",
    ],
    "K": [
        "Portal El Dorado", "Modelia", "Normandia", "Avenida Rojas",
        "El Tiempo", "Salitre - El Greco", "CAN", "Gobernacion",
        "Quinta Paredes", "Corferias",
        "Ciudad Universitaria - Loteria de Bogota", "Concejo de Bogota",
        "Centro Memoria", "Universidades",
    ],
    "L": [
        "San Diego", "Las Nieves", "San Victorino", "Bicentenario",
        "San Bernardo", "Policarpa",
        "Ciudad Jardin - Universidad Antonio Narino", "Avenida 1 de Mayo",
        "Country Sur", "Portal 20 de Julio",
    ],
    "M": [
        "Museo Nacional",
    ],
    "N": [
        "Tygua - San Jose", "Guatoque - Veraguas",
    ],
    "S": [
        "Bosa", "La Despensa", "Leon XIII",
        "Terreros - Hospital Cardiovascular", "San Mateo",
    ],
    "T": [
        "Biblioteca", "Parque", "Portal Tunal",
    ],
    "Z": [
        "Islandia", "Los Laureles", "Tibanica - Primavera",
    ],
}

inter_corridor_connections = [
    ("Heroes", "Polo"),
    ("Calle 72", "Polo"),
    ("NQS Calle 75 - Zona M", "Polo"),
    ("NQS Calle 75 - Zona M", "Escuela Militar"),
    ("NQS Calle 75 - Zona M", "San Martin"),
    ("Calle 100", "La Castellana"),
    ("Avenida El Dorado", "Ciudad Universitaria - Loteria de Bogota"),
    ("Avenida Jimenez", "Hortua"),
    ("Avenida Jimenez", "Museo del Oro"),
    ("Museo Nacional", "Centro Memoria"),
    ("Calle 26", "Centro Memoria"),
    ("Ricaurte", "Comuneros"),
    ("Santa Lucia", "Biblioteca"),
    ("Biblioteca Tintal", "Islandia"),
    ("Tygua - San Jose", "Hortua"),
    ("Guatoque - Veraguas", "Comuneros"),
    ("Tygua - San Jose", "Avenida Jimenez"),
    ("Tygua - San Jose", "Bicentenario"),
    ("Tygua - San Jose", "San Victorino"),
    ("Perdomo", "Bosa"),
    ("San Martin", "Polo"),
    ("Avenida Jimenez", "San Victorino")
]



class Graph:
    def __init__(self):
        self.adjacency = {}

    def add_edge(self, a, b, weight):
        self.adjacency.setdefault(a, [])
        self.adjacency.setdefault(b, [])
        self.adjacency[a].append((b, weight))
        self.adjacency[b].append((a, weight))

    def shortest_distances_from(self, source):
        distances = {source: 0}
        visited = set()
        heap = [(0, source)]

        while heap:
            dist, node = heapq.heappop(heap)

            if node in visited:
                continue

            visited.add(node)

            for neighbor, weight in self.adjacency.get(node, []):
                new_dist = dist + weight

                if neighbor not in distances or new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(heap, (new_dist, neighbor))

        return distances


EDGE_WEIGHT = 3

edge_weight_overrides = {
    frozenset({"Calle 72", "Polo"}): 6,
    frozenset({"Calle 100", "La Castellana"}): 4,
    frozenset({"Heroes", "Polo"}): 6,
    frozenset({"NQS Calle 75 - Zona M", "San Martin"}): 5,
    frozenset({"San Martin", "Polo"}): 7,
    frozenset({"Avenida El Dorado", "Ciudad Universitaria - Loteria de Bogota"}): 7,
    frozenset({"Avenida Jimenez", "San Victorino"}): 3,
    frozenset({"Tygua - San Jose", "Bicentenario"}): 7,
    frozenset({"La Castellana", "NQS Calle 75 - Zona M"}): 4,
    frozenset({"Centro Memoria", "Universidades"}): 10,
}


def edge_weight(a, b):
    return edge_weight_overrides.get(frozenset({a, b}), EDGE_WEIGHT)


def build_graph():
    graph = Graph()

    for corridor, stations in stations_by_corridor.items():
        for i in range(len(stations) - 1):
            a, b = stations[i], stations[i + 1]
            graph.add_edge(a, b, edge_weight(a, b))

    for a, b in inter_corridor_connections:
        graph.add_edge(a, b, edge_weight(a, b))

    return graph


graph = build_graph()