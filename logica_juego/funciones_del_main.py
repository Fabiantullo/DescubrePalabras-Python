import time
import os
import pygame as pg
from funciones_pygame.botones import crear_boton, dibujar_boton, dibujar_lineas, dibujar_input
from funciones_pygame.funciones_logica import verificar_perdio_gano, reiniciar_variables
from funciones_pygame.interfaz import actualizar_interfaz, dibujar_botones_main, mostrar_estadisticas, mostrar_matriz_p
from logica_juego.funciones import generar_palabras, generar_lista_matrices
from archivo.funciones_archivo import guardar_puntuacion, sumar_lista
from configs import SIZE_WINDOW

    
def comprobar_estado_juego(diccionario_partida:dict, diccionario_ronda:dict, ventana:pg.surface, entrada:dict, palabras:dict, DIFICUTYS:list, carteles:dict, lista_boton_pistas:list, fuentes:dict, lista_botones_modos:list):
    """Funcion que se encarga de comprobar el estado del juego

    Args:
        diccionario_partida (dict): Diccionario con los datos de la partida
        diccionario_ronda (dict): Diccionario con los datos de la ronda
        ventana (pg.surface): Ventana de pygame
        entrada (dict): Diccionario con la entrada del usuario
        palabras (dict): Diccionario con las palabras
        DIFICUTYS (list): Lista de dificultades
        carteles (dict): Diccionario con los carteles
        lista_boton_pistas (list): Lista de botones de pistas
        fuentes (dict): Fuentes de pygame
        lista_botones_modos (list): Lista de botones de modos
    """    
    if diccionario_partida["cantidad_palabras_acertadas"][0] == 5 or diccionario_partida["cantidad_palabras_falladas"][0] == 3:
        if not diccionario_partida["nombre_usuario"]:
            reiniciar_variables(diccionario_ronda, palabras, DIFICUTYS)
            dibujar_boton(carteles["cartel_usuario"])
            dibujar_input(entrada)
            diccionario_partida["bandera_pantalla_final"] = True
        else:
            if not diccionario_partida["bandera_archivo_guardado"]:
                
                diccionario_partida["tiempo_total"], diccionario_partida["puntaje_total"] = guardar_puntuacion(lista_boton_pistas, diccionario_partida)

                diccionario_partida["bandera_archivo_guardado"] = True
            elif diccionario_partida["bandera_archivo_guardado"]:
                mostrar_estadisticas(diccionario_partida, ventana, carteles, lista_boton_pistas, fuentes, diccionario_partida["tiempo_total"], diccionario_partida["puntaje_total"])
    else:
        dibujar_botones_main(ventana, diccionario_ronda, lista_boton_pistas, entrada, lista_botones_modos, fuentes)

    
def crear_diccionario_partida(ventana:pg.surface):
    """Funcion que se encarga de crear el diccionario de la partida

    Args:
        ventana (pg.surface): Ventana de pygame

    Returns:
        dict: Devuelve un diccionario con los datos de la partida
    """    
    diccionario_partida = {}
    diccionario_partida["puntaje"] = [0]
    diccionario_partida["cantidad_palabras_acertadas"] = [0]
    diccionario_partida["cantidad_palabras_falladas"] = [0]
    diccionario_partida["cantidad_intentos_actuales"] = 0
    diccionario_partida["tiempo_rondas"] = [0]
    diccionario_partida["bandera_pantalla_final"] = False
    diccionario_partida["nombre_usuario"] = None
    diccionario_partida["bandera_archivo_guardado"] = False
    diccionario_partida["bandera_puntuo_por_tiempo"] = False
    diccionario_partida["ventana"] = ventana
    diccionario_partida["estado_juego"] = "pantalla_inicio"
    diccionario_partida["sonido"] = False
    diccionario_partida["tiempo_total"] = 0
    diccionario_partida["puntaje_total"] = 0
    return diccionario_partida

def crear_diccionario_ronda(DIFICULTYS:list, palabras:dict, TRYS:int) -> dict:
    """Funcion que se encarga de crear el diccionario de la ronda

    Args:
        DIFICULTYS (list): Lista de dificultades
        palabras (dict): Diccionario con las palabras
        TRYS (int): Cantidad de intentos

    Returns:
        dict: Devuelve un diccionario con los datos de la ronda
    """    
    diccionario_ronda = {}
    diccionario_ronda["lista_palabras"] = generar_palabras(DIFICULTYS , palabras)
    diccionario_ronda["lista_matrices"] = generar_lista_matrices(DIFICULTYS, diccionario_ronda["lista_palabras"],TRYS)
    diccionario_ronda["dificultad_actual"] = DIFICULTYS[0]
    diccionario_ronda["indice_actual"] = 0
    diccionario_ronda["lista_intentos"] = [0] * len(DIFICULTYS)
    diccionario_ronda["sets_acertados"] = set()
    return diccionario_ronda

def manejar_inicio (diccionario_partida:dict,ventana:pg.surface,carteles:dict,fuentes:dict):
    """Funcion que se encarga de manejar la pantalla de inicio

    Args:
        diccionario_partida (dict): Diccionario con los datos de la partida
        ventana (pg.surface): Ventana de pygame
        carteles (dict): Diccionario con los carteles
        fuentes (dict): Fuentes de pygame
    """    
    if diccionario_partida["estado_juego"] == "pantalla_inicio":
        dibujar_boton(carteles["pantalla_inicio"])
        carteles["boton_jugar"] = crear_boton(ventana,(SIZE_WINDOW[0]/2 -150,SIZE_WINDOW[1]/2 -100),(150, 50), "Jugar", fuentes["fuente_palabras"], "black", "salmon")
        carteles["boton_ayuda"] = crear_boton(ventana,(SIZE_WINDOW[0]/2 + 50,SIZE_WINDOW[1]/2 -100),(150, 50), "Ayuda", fuentes["fuente_palabras"], "black", "salmon")
        dibujar_boton(carteles["boton_jugar"]) 
        dibujar_boton(carteles["boton_ayuda"])
        if carteles["Activar_Sonido"]["Presionado"]:
            dibujar_boton(carteles["Activar_Sonido"])
        else:
            dibujar_boton(carteles["Desactivar_Sonido"])
    manejar_ayuda(diccionario_partida,ventana,carteles,fuentes)
    
            
def manejar_ayuda(diccionario_partida:dict,ventana:pg.surface,carteles:dict,fuentes:dict):
    """Funcion que se encarga de manejar la pantalla de ayuda

    Args:
        diccionario_partida (dict): Diccionario con los datos de la partida
        ventana (pg.surface): Ventana de pygame
        carteles (dict): Diccionario con los carteles
        fuentes (dict): Fuentes de pygame
    """    
    SIZE_WINDOW = ventana.get_size()
    if diccionario_partida["estado_juego"] == "pantalla_ayuda":
        carteles["explicacion"] = crear_boton(ventana,(0,0),(SIZE_WINDOW[0],SIZE_WINDOW[1]),"", fuentes["fuente_palabras"], "black", (164, 187, 254))
        dibujar_boton(carteles["explicacion"])
        explicacion = """
        Bienvenido a Palabrini, el juego donde debes adivinar las palabras de los paises.
        Para jugar debes seleccionar una dificultad y adivinar las palabras.
        Tenes 6 intentos para adivinar la palabra, si fallas pierdes un intento.
        Si adivinas la palabra ganas puntos.
        Tenes 3 comodines que te ayudaran a adivinar la palabra.
        Descubrir continente, te dice el continente al que pertenece la palabra.
        Descubrir letras, te muestra una letra de la palabra en la posicion correcta.
        Descubrir comida, te muestra una comida tipica del pais.
        El juego termina si adivinas 5 o fallas 3 palabras.
        Si lo haces antes de 15 minutos ganas 100 puntos extras."""
        dibujar_lineas(ventana, explicacion, 25, SIZE_WINDOW[1] / 2 - 200, fuentes["fuente_palabras"], "black")
        dibujar_boton(carteles["boton_volver"])
        
def manejar_juego(diccionario_partida:dict,ventana:pg.surface,diccionario_ronda:dict,fuentes:dict,entrada:dict,palabras:dict,DIFICUTYS:list,carteles:dict, lista_boton_pistas:list, boton_modos:list):
    """Funcion que se encarga de manejar el juego

    Args:
        diccionario_partida (dict): Diccionario con los datos de la partida
        ventana (pg.surface): Ventana de pygame
        diccionario_ronda (dict): Diccionario de la ronda
        fuentes (dict): Fuentes de pygame
        entrada (dict): Diccionario con la entrada del usuario
        palabras (dict): Diccionario con las palabras
        DIFICUTYS (list): Lista de dificultades
        carteles (dict): Diccionario con los carteles
        lista_boton_pistas (list): Lista de botones de pistas
        boton_modos (list): Lista de botones de modos
    """    
    if diccionario_partida["estado_juego"] == "pantalla_juego":
        actualizar_interfaz(ventana, diccionario_partida, diccionario_ronda, fuentes)
        comprobar_estado_juego(diccionario_partida, diccionario_ronda, ventana, entrada, palabras, DIFICUTYS, carteles, lista_boton_pistas, fuentes, boton_modos)
        
def crear_fuentes()->dict:
    """Funcion que se encarga de crear las fuentes

    Returns:
        dict: Devuelve un diccionario con las fuentes
    """    
    fuentes = {}
    fuentes["fuente_palabras"] = ("Arial", 20)
    fuentes["fuente_matriz"] = ("Arial", 30)
    fuentes["fuente_pistas"] = ("Arial", 15)
    return fuentes