import pygame as pg
import time
import os
from funciones_pygame.botones import crear_boton, dibujar_boton, dibujar_input, dibujar_lineas
from configs import SIZE_WINDOW
from archivo.funciones_archivo import sumar_lista

def actualizar_interfaz(ventana:pg.surface, diccionario_partida:dict, diccionario_ronda: dict, fuentes: dict):
    """Funcion que se encarga de actualizar la interfaz del juego

    Args:
        ventana (pg.surface): Ventana de pygame
        diccionario_partida (dict): Diccionario de la partida
        diccionario_ronda (dict): Diccionario de la ronda
        fuentes (dict): Fuentes de pygame
    """    
    tiempo_actual = time.time() - diccionario_ronda["tiempo_inicio"]
    ventana.fill((164, 187, 254))
    high_score = crear_boton(ventana,(10,ventana.get_height()-100),(70,70),"", fuentes["fuente_palabras"], "black", (164, 187, 254), imagen= os.path.join("images", "high-score.png"))
    high_score_variables = crear_boton(ventana,(70,ventana.get_height()-100),(150,50), f"{diccionario_partida['mayor_puntaje']} {diccionario_partida['mayor_nombre']}", fuentes["fuente_palabras"], "black", (164, 187, 254))
    icono_puntuacion = crear_boton(ventana, (10, 10), (50, 50), "", fuentes["fuente_palabras"], "white", (164, 187, 254), imagen=os.path.join("images", "puntuacion-mas-alta.png"))
    icono_tiempo = crear_boton(ventana, (10, 70), (50, 50), "", fuentes["fuente_palabras"], "white", "grey40", imagen=os.path.join("images", "cronometro.png"))
    tiempo_actualizado = crear_boton(ventana, (60, 70), (100, 50), f"{tiempo_actual:.2f}", fuentes["fuente_palabras"], "black", (164, 187, 254))
    puntuaje_actualizado = crear_boton(ventana, (70, 10), (50, 50), f"{sumar_lista(diccionario_partida['puntaje'])}", fuentes["fuente_palabras"], "black", (164, 187, 254))
    dibujar_boton(icono_puntuacion)
    dibujar_boton(icono_tiempo)
    dibujar_boton(puntuaje_actualizado)
    dibujar_boton(tiempo_actualizado)
    dibujar_boton(high_score)
    dibujar_boton(high_score_variables)


def mostrar_estadisticas(diccionario_partida:dict, ventana:pg.surface, carteles:dict, lista_boton_pistas:list, fuentes:dict,tiempo_total:int,puntaje_total:int):
    """Funcion que se encarga de mostrar las estadisticas del jugador

    Args:
        diccionario_partida (dict): Diccionario con los datos de la partida
        ventana (pg.surface): Ventana de pygame
        carteles (dict): Diccionario con los carteles
        lista_boton_pistas (list): Lista de botones de pistas
        fuentes (dict): Fuentes de pygame
        tiempo_total (int): Tiempo total de la partida
        puntaje_total (int): Puntaje total de la partida
    """    
    
    porcentaje = (diccionario_partida["cantidad_palabras_acertadas"][0] + diccionario_partida["cantidad_palabras_falladas"][0]) / diccionario_partida["cantidad_palabras_acertadas"][0]
    estadisticas = f"""
    Nombre: {diccionario_partida['nombre_usuario']}
    Porcentaje victorias: {porcentaje * 100:.2f}%
    Cantidad Victorias: {diccionario_partida['cantidad_palabras_acertadas'][0]}
    Cantidad Derrotas: {diccionario_partida['cantidad_palabras_falladas'][0]}
    Tiempo Total: {tiempo_total:.2f} segundos
    Puntaje Total: {puntaje_total}
    """
    if diccionario_partida["bandera_puntuo_por_tiempo"]:
        estadisticas += "\nGanaste 100 puntos por tiempo"
    boton_estadisticas = crear_boton(ventana, (0, 0), (SIZE_WINDOW[0], SIZE_WINDOW[1]), "", ("Arial", 30), "grey", "lightskyblue2")
    dibujar_boton(boton_estadisticas)
    dibujar_lineas(ventana, estadisticas, 30, 100, ("arial",30), "black")
    dibujar_boton(carteles["jugar_otra_vez"])
    carteles["jugar_otra_vez"]["Presionado"] = True

def mostrar_matriz_p(ventana: pg.Surface, matriz:list, fuente:tuple, color:str|tuple, color_fondo:str|tuple,palabra:dict):
    """Funcion que se encarga de mostrar la matriz en pantalla

    Args:
        ventana (pg.Surface): Ventana de pygame
        matriz (list): Matriz que se muestra en pantalla
        fuente (tuple): Fuente de pygame
        color (str | tuple): Color de la fuente
        color_fondo (str | tuple): Color de fondo
        palabra (dict): Palabra obtenida de la lista de palabras
    """    
    ventana_size = ventana.get_size()
    boton_ancho, boton_alto = 50, 50
    x, y = ventana_size[0] / 2 - 150, 100
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if matriz[i][j] == palabra["pais"][j]:
                boton = crear_boton(ventana, (x, y), (boton_ancho, boton_alto), matriz[i][j], fuente, color, "green", False)
            elif matriz[i][j] in palabra["pais"]:
                boton = crear_boton(ventana, (x, y), (boton_ancho, boton_alto), matriz[i][j], fuente, color, "yellow", False)
            elif matriz[i][j] == "_":
                boton = crear_boton(ventana, (x, y), (boton_ancho, boton_alto), matriz[i][j], fuente, color, color_fondo, False)
            else:
                boton = crear_boton(ventana, (x, y), (boton_ancho, boton_alto), matriz[i][j], fuente, color, (68, 65, 65), False)
            
            dibujar_boton(boton)
            x += 50  
        x = ventana_size[0] / 2 - 150
        y += 50  


def dibujar_botones_main(ventana:pg.surface, diccionario_ronda:dict,lista_boton_pistas:list, entrada:dict, boton_modos:list, fuentes:dict):
    """Funcion que se encarga de dibujar los botones de la pantalla principal

    Args:
        ventana (pg.surface): Ventana de pygame
        diccionario_ronda (dict): Diccionario de la ronda
        lista_boton_pistas (list): Lista de botones de pistas
        entrada (dict): Diccionario con la entrada del usuario
        boton_modos (list): Lista de botones de modos
        fuentes (dict): Fuentes de pygame
    """    
    for boton in boton_modos:
        dibujar_boton(boton)  
    mostrar_matriz_p(ventana, diccionario_ronda["lista_matrices"][diccionario_ronda["indice_actual"]], fuentes["fuente_matriz"], "Black", "White", diccionario_ronda["lista_palabras"][diccionario_ronda["indice_actual"]])  
    for boton in lista_boton_pistas:
        dibujar_boton(boton)
        pg.draw.rect(ventana, "navy", boton["rectangulo"], 2)  
    pg.draw.rect(ventana, "aquamarine4", boton_modos[diccionario_ronda["indice_actual"]]["rectangulo"], 2)
    dibujar_input(entrada)
