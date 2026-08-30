import heapq
from datos_operativos import rutas, tiempos, PENALIZACION_TRANSBORDO


class Nodo:
    def __init__(self, estado, padre=None, accion=None, costo=0):
        self.estado = estado
        self.padre = padre
        self.accion = accion
        self.costo = costo

    def __str__(self):
        return f"Nodo(estado={self.estado}, accion={self.accion}, costo={self.costo})"

    def representation(self):
        return self.estado


FALLO = Nodo(None)


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
        return heapq.heappop(self.frontierNode)[2]

    def top(self):
        if self.is_empty():
            raise Exception("frontera vacia")
        return self.frontierNode[0][2]

    def add(self, node):
        valor = self.evaluation_function(node)
        heapq.heappush(self.frontierNode, (valor, self.cont, node))
        self.cont += 1


def dijkstra_desde(tiempos, origen):
    dist = {origen: 0}
    heap = [(0, origen)]
    visitados = set()
    while heap:
        d, u = heapq.heappop(heap)
        if u in visitados:
            continue
        visitados.add(u)
        for v, costo in tiempos.get(u, {}).items():
            nuevo = d + costo
            if nuevo < dist.get(v, float("inf")):
                dist[v] = nuevo
                heapq.heappush(heap, (nuevo, v))
    return dist


class Problema:
    def __init__(self, estado_inicial, estacion_objetivo, rutas, tiempos,
                 penalizacion_transbordo=PENALIZACION_TRANSBORDO):
        self.estado_inicial = estado_inicial
        self.estacion_objetivo = estacion_objetivo
        self.rutas = rutas
        self.tiempos = tiempos
        self.penalizacion_transbordo = penalizacion_transbordo
        self.heuristicas = dijkstra_desde(tiempos, estacion_objetivo)

    def is_goal(self, estado):
        estacion, _ = estado
        return estacion == self.estacion_objetivo

    def _rutas_en(self, estacion):
        return [r for r, paradas in self.rutas.items() if estacion in paradas]

    def result_actions(self, estado):
        estacion, ruta_actual = estado
        acciones = []
        for ruta in self._rutas_en(estacion):
            if ruta != ruta_actual:
                acciones.append((estacion, ruta))
        if ruta_actual != "Ninguna":
            paradas = self.rutas[ruta_actual]
            idx = paradas.index(estacion)
            if idx < len(paradas) - 1:
                acciones.append((paradas[idx + 1], ruta_actual))
        return acciones

    def action_cost(self, estado, estado_siguiente):
        estacion, ruta_actual = estado
        estacion_sig, _ = estado_siguiente
        if estacion == estacion_sig:
            return 0 if ruta_actual == "Ninguna" else self.penalizacion_transbordo
        return self.tiempos[estacion][estacion_sig]

    def heuristic(self, estado):
        estacion, _ = estado
        return self.heuristicas.get(estacion, float("inf"))


def expand(problema, nodo):
    expansion = []
    for estado_siguiente in problema.result_actions(nodo.estado):
        costo = nodo.costo + problema.action_cost(nodo.estado, estado_siguiente)
        expansion.append(Nodo(estado_siguiente, nodo, estado_siguiente, costo))
    return expansion


def best_first_search(problema, evaluation_function):
    nodo_raiz = Nodo(problema.estado_inicial, None, None, 0)
    frontera = Frontier(evaluation_function)
    frontera.add(nodo_raiz)
    visitados = []

    while not frontera.is_empty():
        nodo_actual = frontera.pop()
        if problema.is_goal(nodo_actual.estado):
            return nodo_actual
        if nodo_actual.estado in visitados:
            continue
        visitados.append(nodo_actual.estado)
        for hijo in expand(problema, nodo_actual):
            if hijo.estado not in visitados:
                frontera.add(hijo)
    return FALLO


def construir_itinerario(nodo_meta):
    nodos = []
    n = nodo_meta
    while n is not None:
        nodos.append(n)
        n = n.padre
    nodos.reverse()

    pasos = []
    ruta_actual = None
    for n in nodos:
        estacion, ruta = n.estado
        if ruta != "Ninguna" and ruta != ruta_actual:
            if ruta_actual is None:
                pasos.append(f"Tomar: {ruta}")
            else:
                pasos.append(f"Transbordo en: {estacion}")
                pasos.append(f"Tomar: {ruta}")
            ruta_actual = ruta
    return pasos, nodo_meta.costo


if __name__ == "__main__":
    estacion_origen = "Portal Américas"
    estacion_destino = "7 de Agosto"

    problema = Problema((estacion_origen, "Ninguna"), estacion_destino, rutas, tiempos)
    resultado = best_first_search(problema, lambda n: n.costo + problema.heuristic(n.estado))

    print(f"Origen: {estacion_origen}")
    print(f"Destino: {estacion_destino}\n")

    if resultado is FALLO:
        print("No se encontró una ruta.")
    else:
        pasos, tiempo_total = construir_itinerario(resultado)
        for paso in pasos:
            print(paso)
        print(f"\nTiempo estimado: {tiempo_total} minutos")