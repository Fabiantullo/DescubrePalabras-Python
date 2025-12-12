import random
import pygame as pg

def obtener_palabra(lista_palabras:list, dificultad:int) -> dict:
    """Obtiene una palabra de la lista de palabras que coincida con la dificultad

    Args:
        lista_palabras (dict): Lista de palabras
        dificultad (int): Dificultad de la palabra

    Returns:
        dict: Palabra obtenida
    """    
    candidatas = [p for p in lista_palabras if p["caracteres"] == dificultad]
    if candidatas:
        return random.choice(candidatas)
    
    print(f"No se encontraron palabras con dificultad {dificultad}")
    return None            

def generar_palabras(dificultad:list, diccionario_palabras: dict) -> list:
    """Funcion que se encarga de generar una lista de palabras

    Args:
        dificultad (list): Lista de dificultades
        diccionario_palabras (dict): Diccionario con las palabras

    Returns:
        list: Lista de palabras
    """    
    lista_palabras = []
    for i in range(len(dificultad)):
        palabra_generada = obtener_palabra(diccionario_palabras,dificultad[i])
        lista_palabras.append(palabra_generada)
        
    return lista_palabras

def generar_lista_matrices (dificultad:list ,lista_palabras: list,intentos:int) -> list:
    """Funcion que se encarga de generar una lista de matrices

    Args:
        dificultad (list): Lista de dificultades
        lista_palabras (list): Lista de palabras
        intentos (int): Cantidad de intentos

    Returns:
        list: Lista de matrices
    """    
    lista_matrices = []
    for i in range(len(dificultad)):
        matriz = generar_matriz(lista_palabras[i],intentos)
        lista_matrices.append(matriz)
    return lista_matrices

def generar_matriz(palabra_obtenida: dict, intentos:int) -> list:
    """Genera una matriz de la palabra obtenida
    
    Args:
        palabra_obtenida (dict): Palabra obtenida de la lista de palabras
        intentos (int): Cantidad de intentos

    Returns:
        list: Matriz generada
    """    
    matriz = []
    for i in range(intentos):
        matriz_temporal = ["_"] * palabra_obtenida["caracteres"]
        matriz.append(matriz_temporal)
    return matriz

def modificar_puntuacion_nuevo(diccionario_ronda: dict,
                               lista_puntuacion: list) -> int:
    """Modifica la puntuacion del jugador en la ronda actual

    Args:
        diccionario_ronda (dict): Diccionario con los datos de la ronda
        lista_puntuacion (list): Lista con los datos de la puntuacion

    Returns:
        int: Puntuacion obtenida
    """    

    puntuacion = 0
    if len(diccionario_ronda["sets_acertados"]) == len(diccionario_ronda["lista_palabras"][diccionario_ronda["indice_actual"]]["pais"]):
        intentos = diccionario_ronda["lista_intentos"][diccionario_ronda["indice_actual"]] - 1
        for i in range(len(lista_puntuacion)):
            if diccionario_ronda["lista_palabras"][diccionario_ronda["indice_actual"]]["caracteres"] == lista_puntuacion[i][0]:
                puntuacion += lista_puntuacion[i][1]
                if intentos > 1:
                    puntuacion -= lista_puntuacion[i][2] * intentos
    return puntuacion

def generar_letra_random(ventana:pg.Surface, diccionario_rondas:dict, fuente:tuple) -> None:  
    """Genera una letra random en la matriz

    Args:
        ventana (pg.Surface): Ventana de pygame
        diccionario_rondas (dict): Diccionario con los datos de la ronda
        fuente (tuple): Fuente de pygame
    """    
    validacion = True
    letras_sin_acertar = recuperar_letras_no_acertadas(diccionario_rondas["lista_palabras"][diccionario_rondas["indice_actual"]],  diccionario_rondas["sets_acertados"])
    while validacion:
        letra_random = random.choice(letras_sin_acertar)
        if verificar_que_la_letra_no_se_haya_adivinado(letra_random, diccionario_rondas["lista_matrices"][diccionario_rondas["indice_actual"]],diccionario_rondas["sets_acertados"]):
            diccionario_rondas["lista_matrices"][diccionario_rondas["indice_actual"]][diccionario_rondas["lista_intentos"][diccionario_rondas["indice_actual"]]][letra_random] = diccionario_rondas["lista_palabras"][diccionario_rondas["indice_actual"]]["pais"][letra_random] 
            diccionario_rondas["lista_intentos"][diccionario_rondas["indice_actual"]], diccionario_rondas["sets_acertados"].add(letra_random)
            validacion = False


def recuperar_letras_no_acertadas(palabra: dict, indices_acertados: set) -> list:
    """Recupera las letras no acertadas de la palabra

    Args:
        palabra (dict): Palabra obtenida de la lista de palabras
        indices_acertados (set): Indices correctos de la palabra

    Returns:
        list: Letras no acertadas de la palabra
    """
    letras_no_acertadas = []
    for i in range(len(palabra["pais"])):
        if i not in indices_acertados:
            letras_no_acertadas.append(i)
            print(letras_no_acertadas)
    return letras_no_acertadas


def verificar_que_la_letra_no_se_haya_adivinado(letra: str, matriz: list, indices_acertados: set) -> bool:
    """Verifica que la letra no se haya adivinado anteriormente

    Args:
        letra (str): Letra a verificar
        matriz (list): Matriz que se muestra en pantalla
        indices_acertados (set): Indices correctos de la palabra

    Returns:
        bool: True si la letra no se ha adivinado, False si se ha adivinado
    """
    validacion = True
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if letra == matriz[i][j] and j in indices_acertados:
                validacion = False
    return validacion




def toggle_sonido(diccionario_partida:dict, carteles:dict, activar:bool):
    """Activa o desactiva el sonido

    Args:
        diccionario_partida (dict): Diccionario con los datos de la partida
        carteles (dict): Diccionario con los carteles
        activar (bool): True para activar, False para desactivar
    """    
    diccionario_partida["sonido"] = activar
    carteles["Activar_Sonido"]["Presionado"] = activar
    carteles["Desactivar_Sonido"]["Presionado"] = not activar

def activar_sonido(diccionario_partida:dict, carteles:dict):
    """Activa el sonido

    Args:
        diccionario_partida (dict): Diccioanrio con los datos de la partida
        carteles (dict): Diccionario con los carteles
    """    
    toggle_sonido(diccionario_partida, carteles, True)

def desactivar_sonido(diccionario_partida:dict, carteles:dict):
    """Desactiva el sonido

    Args:
        diccionario_partida (dict): Diccionario con los datos de la partida
        carteles (dict): Diccionario con los carteles
    """    
    toggle_sonido(diccionario_partida, carteles, False)
