"""
red_datos.py
============

Rutas reales de TransMilenio con sus paradas (orden real, origen ->
destino). Usado por Problem para result_actions / action_cost.

NOTA: esto es DISTINTO del grafo de grafo_estaciones.py — ese es solo
para la heurística y usa TODAS las troncales; este archivo es solo
las rutas específicas que tu sistema puede realmente ofrecer al
usuario (con transbordo incluido).

Nivel de confianza de cada ruta:
- B12: verificado en fuente oficial de TransMilenio (transmilenio.gov.co)
- Resto (B10, B26, B28, F28, E32): con paradas específicas de una
  fuente no primaria, sin verificación independiente.
"""

_b12_stations = [
    "Portal Sur", "Perdomo", "General Santander", "Comuneros",
    "Ricaurte", "Avenida El Dorado", "Universidad Nacional",
    "7 de Agosto", "NQS Calle 75 - Zona M", "La Castellana",
    "Calle 100", "Calle 127", "Prado Veraniego", "Calle 142",
    "Toberín", "Portal Norte",
]

rutas = {
    "B12": {"nombre": "B12", "stations": _b12_stations},
    "G12": {"nombre": "G12", "stations": list(reversed(_b12_stations))},
    "B10": {
        "nombre": "B10",
        "stations": [
            "Portal de la 80", "Carrera 90", "Avenida Cali",
            "Granja - Carrera 77", "Boyaca", "Avenida 68", "Carrera 53",
            "Carrera 47", "Calle 85", "Calle 100", "Alcalá", "Calle 146",
            "Mazurén", "Toberín", "Portal Norte",
        ],
    },
    "B26": {
        "nombre": "B26",
        "stations": [
            "Portal Américas", "Biblioteca Tintal", "Transversal 86",
            "Banderas", "Mandalay", "Avenida Américas - Avenida Boyacá",
            "Héroes", "Calle 85", "Virrey", "Calle 100", "Calle 127",
            "Alcalá",
        ],
    },
    "B28": {
        "nombre": "B28",
        "stations": [
            "Portal Américas", "Biblioteca Tintal", "Banderas", "Marsella",
            "Zona Industrial", "CDS - Carrera 32", "La Castellana",
            "Calle 106", "Pepe Sierra", "Prado Veraniego", "Calle 146",
            "Calle 161", "Portal Norte",
        ],
    },
    "F28": {
        "nombre": "F28",
        "stations": [
            "Portal Norte", "Calle 161", "Calle 146", "Prado Veraniego",
            "Pepe Sierra", "Calle 106", "La Castellana", "CDS - Carrera 32",
            "Zona Industrial", "Marsella", "Banderas", "Biblioteca Tintal",
            "Portal Américas",
        ],
    },
    "E32": {
        "nombre": "E32",
        "stations": [
            "Portal Américas", "Banderas", "CAD", "7 de Agosto",
            "NQS Calle 75 - Zona M",
        ],
    },
    "C19": {
        "nombre": "C19",
        "stations": [
            "Portal Américas", "Biblioteca Tintal", "Banderas", "Mandalay", "7 de Agosto",
            "NQS Calle 75 - Zona M",
        ],
    },
}


def construir_rutas_por_estacion(rutas: dict) -> dict:
    rutas_por_estacion: dict[str, list[str]] = {}
    for ruta_id, datos in rutas.items():
        for estacion in datos["stations"]:
            rutas_por_estacion.setdefault(estacion, [])
            if ruta_id not in rutas_por_estacion[estacion]:
                rutas_por_estacion[estacion].append(ruta_id)
    return rutas_por_estacion


rutas_por_estacion = construir_rutas_por_estacion(rutas)