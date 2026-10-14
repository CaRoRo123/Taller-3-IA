"""Punto 2. Inferencia exacta por enumeración."""
from algorithms.probability import normalize

def enumerate_all(variables: list, evento_actual: dict, network) -> float:
        
        # Caso base
        if not variables:
            return 1.0

        #peserva el orden topologico
        variable_actual = variables[0]
        variables_restantes = variables[1:]

        # valor fijado
        if variable_actual in evento_actual:
            valor_fijado = evento_actual[variable_actual]
            probabilidad = network.probability(variable_actual, valor_fijado, evento_actual)
            
            # multiplicamos su probabilidad y continuamos con el resto
            return probabilidad * enumerate_all(variables_restantes, evento_actual, network)
        
        # Si la variable está oculta, sumamos sobre sus dos alternativas (0 y 1)
        else:
            suma_probabilidades = 0.0
            for valor_posible in (0, 1):
                
                nuevo_evento = evento_actual.copy()
                nuevo_evento[variable_actual] = valor_posible
                
                probabilidad = network.probability(variable_actual, valor_posible, nuevo_evento)
                suma_probabilidades = suma_probabilidades + (probabilidad * enumerate_all(variables_restantes, nuevo_evento, network))
                
            return suma_probabilidades
          
def enumeration_ask(network, query: str, evidence: dict) -> dict:
    """Calcula P(query | evidence) sobre la conjunta factorizada.

    Entradas: network es la red; query es el nombre de la
    variable consultada; evidence es {nombre de variable: 0 o 1}.
    Salida: {0: probabilidad, 1: probabilidad}.

    Tips:
    - Recorra network.variables en orden topológico.
    - Para una variable fijada multiplique su probabilidad; para una oculta
      sume las dos alternativas 0 y 1. Normalice al terminar.
    - Use copias del evento y no modifique evidence.
    - network.probability(variable, valor, evento) consulta la CPT;
      el evento debe contener los valores de todos los padres.
    - Puede usar una función auxiliar recursiva. Al terminar el recorrido,
      el producto sin factores restantes vale 1.
    - Evidencia imposible: ValueError. Consulta observada: distribución puntual
      solo si la evidencia es posible.
    """
    # Valida nombres de variables y dominio de la evidencia.
    network.validate_query(query, evidence)

    #si ya esta
    if query in evidence:
        probabilidad_evidencia = enumerate_all(network.variables, evidence, network)
        if probabilidad_evidencia == 0.0:
            raise ValueError("Evidencia imposible")
            
        # Si es posible, retornamos una distribución puntual
        valor_observado = evidence[query]
        if valor_observado == 1:
            return {0: 0.0, 1: 1.0}
        else:
            return {0: 1.0, 1: 0.0}

    
    pesos_sin_normalizar = {}
    
    for valor_consulta in (0, 1):
        
        evento_extendido = evidence.copy()
        evento_extendido[query] = valor_consulta
        
        peso = enumerate_all(network.variables, evento_extendido, network)
        pesos_sin_normalizar[valor_consulta] = peso

    # Verificamos si ambos pesos son cero (lo que significa que la evidencia dada es imposible)
    suma_pesos = pesos_sin_normalizar[0] + pesos_sin_normalizar[1]
    if suma_pesos == 0.0:
        raise ValueError("Evidencia imposible")

    
    return normalize(pesos_sin_normalizar)
    # FIN DEL BLOQUE DEL ESTUDIANTE
