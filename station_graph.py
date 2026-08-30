import heapq

estaciones_por_corredor = {
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

conexiones_entre_troncales = [
    ("Héroes", "Polo"),                          # B - D
    ("Calle 72", "Polo"),                        # A - D
    ("NQS Calle 75 - Zona M", "Polo"),           # E - D
    ("NQS Calle 75 - Zona M", "Escuela Militar"),  # E - D (conecta con ambas)
    ("NQS Calle 75 - Zona M", "San Martín"),     # (E) - C
    ("Calle 100", "La Castellana"),              # B - E
    ("Avenida El Dorado", "Ciudad Universitaria - Lotería de Bogotá"),  # E - K
    ("Avenida Jiménez", "Hortúa"),                # A - H
    ("Avenida Jiménez", "Museo del Oro"),         # J - H (via Av. Jiménez)
    ("Museo Nacional", "Centro Memoria"),          # M - K
    ("Calle 26", "Centro Memoria"),               # A - K
    ("Ricaurte", "Comuneros"),                     # E - G
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


PESO_ARISTA = 2


def build_graph():
    graph = Graph()

    for corredor, estaciones in estaciones_por_corredor.items():
        for i in range(len(estaciones) - 1):
            graph.add_edge(estaciones[i], estaciones[i + 1], PESO_ARISTA)

    for a, b in conexiones_entre_troncales:
        graph.add_edge(a, b, PESO_ARISTA)

    return graph


graph = build_graph()