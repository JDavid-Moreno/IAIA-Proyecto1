# Planificador de rutas TransMilenio con A*

Sistema de planificación de rutas para TransMilenio que, dadas una estación de origen y una de destino, encuentra la ruta (o rutas) a tomar, los puntos de transbordo si aplican, y el tiempo total estimado del recorrido. Usa el algoritmo de búsqueda **A\*** (best-first search con heurística admisible) sobre un grafo construido a partir de datos reales del sistema.

## Estructura del proyecto

| Archivo                  | Contenido                                                                                                                                                                                                                                                                                                                                                                                                  |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `station_graph.py`       | Grafo de estaciones. Define los corredores/troncales (A, B, C, D, E, F, G, H, J, K, L, M, N, S, T, Z), las conexiones entre troncales (`inter_corridor_connections`), los pesos de arista distintos al default (`edge_weight_overrides`), y construye el grafo (`build_graph`). Expone `graph`, ya construido, y `Graph.shortest_distances_from(origen)` (Dijkstra), usado para precalcular la heurística. |
| `routes.py`              | Rutas reales de buses (troncales y alimentadoras/duales), cada una con su lista ordenada de estaciones. Cada ruta física tiene su sentido contrario como una entrada separada (sufijo `_R` o su propio id, ej. `B10`/`D10`). Expone `routes` y `routes_by_station` (qué rutas pasan por cada estación).                                                                                                    |
| `faster_route.py`        | Implementación de la búsqueda: clases `Node`, `Frontier`, `Problem`, funciones `expand`, `best_first_search`, `path_actions`, `show_result`. Aquí vive la lógica de A* aplicada al problema.                                                                                                                                                                                                               |
| `informe_proyecto.ipynb` | Notebook con la explicación completa del funcionamiento del proyecto (modelo, decisiones de diseño, pruebas).                                                                                                                                                                                                                                                                                              |

## Cómo funciona

### Espacio de estados
Cada estado es una tupla `(estación_actual, ruta_actual)`, donde `ruta_actual` es `None` si el pasajero está parado en una estación sin haber abordado ningún bus todavía.

### Acciones posibles (`Problem.result_actions`)
- Si no está en ninguna ruta (`ruta_actual is None`): puede **abordar** cualquiera de las rutas que pasan por esa estación (`routes_by_station`).
- Si ya está en una ruta: puede **avanzar** a la siguiente estación de esa ruta, o **bajarse** (transbordar), volviendo a `ruta_actual = None` en la misma estación.

### Costo de las acciones (`Problem.action_cost`)
- Abordar un bus: costo 0.
- Bajarse (transbordo, o llegada final): `TRANSFER_TIME` minutos, salvo que ya se llegó al destino (costo 0).
- Avanzar una estación dentro de una ruta: `TRAVEL_TIME + DWELL_TIME` (tiempo de viaje entre estaciones + tiempo de parada).

### Heurística (`Problem.heuristic`)
Distancia más corta desde la estación actual hasta el destino **siguiendo el trazado real de los corredores** (no línea recta), precalculada una sola vez con `graph.shortest_distances_from(destino)` (Dijkstra) al construir él `Problem`. Al ser una subestimación del costo real (nunca sobreestima), garantiza que A* encuentre la ruta óptima.

### Búsqueda (`best_first_search`)
Best-first search estándar con función de evaluación `f(n) = g(n) + h(n)`, usando un diccionario `reached` para no reexpandir estados ya visitados con menor o igual costo (necesario para que la búsqueda termine en tiempo razonable con la cantidad de rutas cruzadas del sistema real).

## Cómo correrlo

```
python faster_route.py
```

En el archivo, se define el problema con estación de origen y destino:

```
problem = Problem("Museo Nacional", "Portal Norte", routes, graph)

result = best_first_search(
    problem,
    lambda node: node.cost + problem.heuristic(node.state)
)
```

Y se imprime la ruta a tomar, los transbordos y la duración total en minutos.

### Ejemplo de salida
```
Tomar: <ruta>
Transbordo en: <estación>
Tomar: <otra ruta>

Duración: XX minutos
```

## Datos

Las estaciones y rutas están tomadas de datos reales de TransMilenio (buscador de rutas oficial), normalizadas para que todo nombre de estación usado en `routes.py` exista exactamente igual en `station_graph.py`.

## Estado actual / posibles mejoras
- El modelo de costo no depende de la hora ni de la frecuencia de los buses (simplificación).
- El sistema no muestra rutas alternativas cuando hay dos con tiempos muy similares (mejora pendiente).

Para el detalle completo de decisiones de diseño y pruebas, ver `informe_proyecto.ipynb`.