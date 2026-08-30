import heapq

stations_by_corridor = {
    "A": [
        "Calle 72", "Flores", "Calle 57", "Marly", "Avenida 39",
        "Calle 34", "Calle 26", "Calle 22", "Avenida Jiménez",
    ],
    "B": [
        "Terminal", "Calle 187", "Portal Norte", "Toberín", "Calle 161",
        "Mazurén", "Calle 146", "Calle 142", "Alcalá", "Prado Veraniego",
        "Calle 127", "Pepe Sierra", "Calle 106", "Calle 100", "Virrey",
        "Calle 85", "Héroes",
    ],
    "C": [
        "Portal Suba", "La Campiña", "Suba - Transversal 91", "21 Ángeles",
        "Gratamira", "Suba - Avenida Boyacá", "Niza - Calle 127",
        "Humedal Córdoba", "Avenida Suba - Calle 116", "Puente Largo",
        "Suba - Calle 100", "Suba - Calle 95", "Rionegro", "San Martín",
    ],
    "D": [
        "Portal de la 80", "Quirigua", "Carrera 90", "Avenida Cali",
        "Granja - Carrera 77", "Minuto de Dios", "Boyaca", "Las Ferias",
        "Avenida 68", "Carrera 53", "Carrera 47", "Escuela Militar", "Polo",
    ],
    "E": [
        "La Castellana", "NQS Calle 75 - Zona M", "7 de Agosto",
        "Movistar Arena", "Campín - Universidad Antonio Nariño",
        "Universidad Nacional", "Avenida El Dorado", "CAD", "Paloquemao",
        "Ricaurte",
    ],
    "F": [
        "Tibanica - Primavera", "Los Laureles", "Islandia", "Portal Américas",
        "Biblioteca Tintal", "Transversal 86", "Banderas", "Mandalay",
        "Avenida Américas - Avenida Boyacá", "Marsella", "Pradera",
        "Distrito Grafiti", "Puente Aranda", "Carrera 43", "Zona Industrial",
        "CDS - Carrera 32", "Ricaurte", "San Façon - Carrera 22",
        "De La Sabana", "Avenida Jiménez",
    ],
    "G": [
        "Comuneros", "Santa Isabel", "Calle 30 Sur", "Calle 38A Sur",
        "General Santander", "Alquería", "Venecia", "Sevillana",
        "Madelena", "Perdomo", "Portal Sur", "Bosa", "La Despensa",
        "León XIII", "Terreros - Hospital Cardiovascular", "San Mateo",
    ],
    "H": [
        "Hortúa", "Nariño", "Fucha", "Restrepo", "Olaya", "Quiroga",
        "Calle 40 Sur", "Santa Lucía", "Socorro", "Consuelo", "Molinos",
        "Danubio", "Portal Usme", "Biblioteca", "Parque", "Portal Tunal",
    ],
    "J": [
        "San Victorino", "Museo del Oro",
        "Las Aguas - Centro Colombo Americano", "Universidades",
    ],
    "K": [
        "Portal El Dorado", "Modelia", "Normandía", "Avenida Rojas",
        "El Tiempo", "Salitre - El Greco", "CAN", "Gobernación",
        "Quinta Paredes", "Corferias",
        "Ciudad Universitaria - Lotería de Bogotá", "Concejo de Bogotá",
        "Centro Memoria", "Universidades",
    ],
    "L": [
        "San Diego", "Las Nieves", "San Victorino", "Bicentenario",
        "San Bernardo", "Policarpa",
        "Ciudad Jardín - Universidad Antonio Nariño", "Avenida 1 de Mayo",
        "Country Sur", "Portal 20 de Julio",
    ],
    "M": [
        "Museo Nacional",
    ],
}

inter_corridor_connections = [
    ("Héroes", "Polo"),
    ("Calle 72", "Polo"),
    ("NQS Calle 75 - Zona M", "Polo"),
    ("NQS Calle 75 - Zona M", "Escuela Militar"),
    ("NQS Calle 75 - Zona M", "San Martín"),
    ("Calle 100", "La Castellana"),
    ("Avenida El Dorado", "Ciudad Universitaria - Lotería de Bogotá"), 
    ("Avenida Jiménez", "Hortúa"),
    ("Avenida Jiménez", "Museo del Oro"),
    ("Museo Nacional", "Centro Memoria"),
    ("Calle 26", "Centro Memoria"),
    ("Ricaurte", "Comuneros"),
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


EDGE_WEIGHT = 2


def build_graph():
    graph = Graph()

    for corridor, stations in stations_by_corridor.items():
        for i in range(len(stations) - 1):
            graph.add_edge(stations[i], stations[i + 1], EDGE_WEIGHT)

    for a, b in inter_corridor_connections:
        graph.add_edge(a, b, EDGE_WEIGHT)

    return graph


graph = build_graph()