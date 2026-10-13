"""Punto 1. Distribuciones discretas y decisiones de respuesta."""
import math


def normalize(weights: dict) -> dict:
    """Retorna un diccionario nuevo cuyas probabilidades suman uno.

    Entrada: weights = {resultado: peso}.
    Salida: {resultado: probabilidad}, con las mismas claves.

    Tips:
    - Conserve las claves y su orden; no modifique weights.
    - Rechace pesos negativos, no finitos, diccionarios vacíos y suma cero.
    """
    suma_total = 0.0
    for peso in weights.values():
        suma_total = suma_total + peso
    distribucion_normalizada = {}
    for resultado, peso in weights.items():
        distribucion_normalizada[resultado] = peso / suma_total
        
    return distribucion_normalizada
    
        

    # FIN DEL BLOQUE DEL ESTUDIANTE


def expected_utility(distribution: dict, utilities: dict) -> float:
    """Calcula sum_s P(s) U(s) para una acción.

    Entradas: distribution = {resultado: probabilidad} y
    utilities = {resultado: utilidad} para una sola acción.
    Salida: un número con la utilidad esperada.

    Tips:
    - distribution ya debe estar normalizada; no normalice utilidades.
    - Ambas tablas deben contener los mismos resultados posibles.
    """
    # Validación de las entradas; no modificar.
    if set(distribution) != set(utilities) or not distribution:
        raise ValueError("Probabilidades y utilidades deben tener las mismas claves")
    if any(not math.isfinite(p) or p < 0 for p in distribution.values()):
        raise ValueError("Distribución inválida")
    if not math.isclose(sum(distribution.values()), 1, abs_tol=1e-9):
        raise ValueError("La distribución debe sumar uno")
    if any(not math.isfinite(u) for u in utilities.values()):
        raise ValueError("Utilidades no finitas")
    utilidad_esperada_total = 0.0
    for resultado in distribution.keys():
        probabilidad = distribution[resultado]
        utilidad = utilities[resultado]
        
        utilidad_esperada_total = utilidad_esperada_total + (probabilidad * utilidad)
        
    return utilidad_esperada_total
    # FIN DEL BLOQUE DEL ESTUDIANTE


def best_action(distribution: dict, actions: dict) -> tuple[str, dict]:
    """Retorna (nombre de acción, utilidades esperadas por acción).

    Entradas: distribution = {resultado: probabilidad} y
    actions = {acción: {resultado: utilidad}}.
    Salida: (acción elegida, {acción: utilidad esperada}).

    Tips:
    - actions asocia cada acción con su tabla de utilidades.
    - Reutilice expected_utility y conserve la primera acción en los empates.
    """
    # Validación de las acciones; no modificar.
    if not actions:
        raise ValueError("Se requiere al menos una acción")
    utilidades_esperadas_por_accion = {}
    mejor_accion = None
    mayor_utilidad_esperada = -math.inf

    for nombre_accion, utilidades in actions.items():
        utilidad_esperada_actual = expected_utility(distribution, utilidades)
        utilidades_esperadas_por_accion[nombre_accion] = utilidad_esperada_actual
        if utilidad_esperada_actual > mayor_utilidad_esperada:
            mayor_utilidad_esperada = utilidad_esperada_actual
            mejor_accion = nombre_accion
    return mejor_accion, utilidades_esperadas_por_accion


    # FIN DEL BLOQUE DEL ESTUDIANTE
