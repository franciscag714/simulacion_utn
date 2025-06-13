import argparse
import sys 
import random 
import math 
import matplotlib.pyplot as plt

# ---------------------------------- Declaracion de variables globales -----------------------------------

# Lista para almacenar los tiempos de retiro de los clientes
tiempos_arribos_clientes = []  # Lista para almacenar los tiempos de arribo de los clientes
tiempos_retiros_clientes = []  

# ---------------------------------- Definición de funciones auxiliares -----------------------------------
def generador_arreglo_eventos():
    eventos = [] # arreglo bidimensional

    # se agregan los arribos y los retiros al arreglo eventos. +1 si es arribo, -1 si es retiro
    for a in tiempos_arribos_clientes:
        eventos.append((a, +1))
    for r in tiempos_retiros_clientes:
        eventos.append((r, -1))

    eventos.sort()    
    return eventos

def generador_numero_aleatorio():
    """Genera un número aleatorio entre 0 y 1."""
    return random.uniform(0, 1)

def calcular_demora(tiempos_arribos_clientes, tiempos_retiros_clientes):
    """demora = tiempo de todos los clientes que estan esperando en la cola. + la diferencia entre el cliente que esta en servicio con el tiempo de mi llegada"""
    demora =  max(tiempos_retiros_clientes) - max(tiempos_arribos_clientes) 
    return demora if demora > 0 else 0

def calcular_tiempo_arribo_salida(tasa_arribo, tasa_servicio, cantidad_usuarios): 
    for i in range(0, cantidad_usuarios):
        if i == 0:
            # Arribo del primer cliente
            numero_aleatorio_arribo = generador_numero_aleatorio()
            nro_arribo_cliente = round(((-1/tasa_arribo)*math.log(numero_aleatorio_arribo)), 4)
            tiempos_arribos_clientes.append(nro_arribo_cliente)
            # Retiro del primer cliente
            numero_aleatorio_retiro = generador_numero_aleatorio()
            tiempo_retiro_cliente = round(((-1/tasa_servicio)*math.log(numero_aleatorio_retiro) + tiempos_arribos_clientes[i]), 4)
            tiempos_retiros_clientes.append(tiempo_retiro_cliente)
        else:
            #Arribo de los proximos clientes
            numero_aleatorio_arribo = generador_numero_aleatorio()
            tiempo_ultimo_arribo = round(((-1/tasa_arribo)*math.log(numero_aleatorio_arribo)) + tiempos_arribos_clientes[i-1], 4)
            tiempos_arribos_clientes.append(tiempo_ultimo_arribo)
            # Retiro de los proximos clientes
            numero_aleatorio_retiro = generador_numero_aleatorio()
            demora = calcular_demora(tiempos_arribos_clientes, tiempos_retiros_clientes)
            tiempo_total_cliente = round(((-1/tasa_servicio)*math.log(numero_aleatorio_retiro) + tiempos_arribos_clientes[i] + demora), 4)
            tiempos_retiros_clientes.append(tiempo_total_cliente)
    
    print("Tiempos de arribo de clientes:", tiempos_arribos_clientes)
    print("Tiempos de retiro de clientes:", tiempos_retiros_clientes)


def calcular_promedios_clientes_en_el_sistema():
    print("\n--CALCULO PROMEDIO CLIENTES EN EL SISTEMA--\n")
    eventos = generador_arreglo_eventos()
    area = 0.0
    tiempo_anterior = eventos[0][0]
    cantidad_clientes_actuales = 1

    for e in eventos[1:]:
        tiempo_evento, tipo_evento = e
        duracion_evento = tiempo_evento - tiempo_anterior
        tiempo_anterior = tiempo_evento
        if tipo_evento == +1:
            area += duracion_evento * cantidad_clientes_actuales
            cantidad_clientes_actuales += 1
        elif tipo_evento == -1:
            area += duracion_evento * cantidad_clientes_actuales
            cantidad_clientes_actuales -= 1

    promedio_clientes = area / max(tiempos_retiros_clientes)
    
    return promedio_clientes    


def calcular_promedio_de_clientes_en_el_cola():
    print("\n--CALCULO PROMEDIO CLIENTES EN COLA--\n")
    eventos = generador_arreglo_eventos()
    area = 0.0
    tiempo_anterior = eventos[0][0]
    cantidad_clientes_actuales = 1

    for e in eventos[1:]:
        tiempo_evento, tipo_evento = e
        duracion_evento = tiempo_evento - tiempo_anterior
        tiempo_anterior = tiempo_evento
        if tipo_evento == +1: # Es decir, si el evento es un arribo
            if cantidad_clientes_actuales > 1:
                area += duracion_evento * (cantidad_clientes_actuales - 1)
            cantidad_clientes_actuales += 1
        elif tipo_evento == -1: # Es decir, si el evento es un retiro
            if cantidad_clientes_actuales > 1:
                area += duracion_evento * (cantidad_clientes_actuales - 1)
            cantidad_clientes_actuales -= 1

    promedio_clientes_en_cola = area / max(tiempos_retiros_clientes)
    
    return promedio_clientes_en_cola


def calcular_tiempo_promedio_en_el_sistema():
    print("\n--CALCULO TIEMPO PROMEDIO EN EL SISTEMA--\n")
    tiempo_total = 0.0

    for i in range(len(tiempos_retiros_clientes)):
        tiempo_total += tiempos_retiros_clientes[i] - tiempos_arribos_clientes[i]
    
    cantidad_clientes = len(tiempos_retiros_clientes) # se podria utilizar el parametro de entrada -n, ya que este es la cantidad de usuarios
    
    promedio_tiempo = tiempo_total / cantidad_clientes      
    
    return promedio_tiempo

def calcular_tiempo_promedio_en_la_cola():
    print("\n--CALCULO TIEMPO PROMEDIO EN COLA--\n")
    eventos = generador_arreglo_eventos()
    tiempo_total = 0.0
    tiempo_anterior = eventos[0][0]
    cantidad_clientes_actuales = 1

    for e in eventos[1:]:
        tiempo_evento, tipo_evento = e
        duracion_evento = tiempo_evento - tiempo_anterior
        tiempo_anterior = tiempo_evento
        if tipo_evento == +1: # Es decir, si el evento es un arribo
            if cantidad_clientes_actuales > 1:
                tiempo_total += duracion_evento 
            cantidad_clientes_actuales += 1
        elif tipo_evento == -1: # Es decir, si el evento es un retiro
            if cantidad_clientes_actuales > 1:
                tiempo_total += duracion_evento
            cantidad_clientes_actuales -= 1

    cantidad_clientes = len(tiempos_retiros_clientes)  # se podria utilizar el parametro de entrada -n, ya que este es la cantidad de usuarios
    
    promedio_tiempo_en_cola = tiempo_total / cantidad_clientes
    
    return promedio_tiempo_en_cola

def calcular_utilizacion_servidor():
    print("\n--CALCULO UTILIZACION SERVIDOR--\n")
    eventos = generador_arreglo_eventos()
    tiempo_total_en_servicio = 0.0 # tiempo en que el peluquero esta activo
    tiempo_anterior = eventos[0][0]
    cantidad_clientes_actuales = 1

    for e in eventos[1:]:
        tiempo_evento, tipo_evento = e
        duracion_evento = tiempo_evento - tiempo_anterior
        tiempo_anterior = tiempo_evento
        if cantidad_clientes_actuales > 0:
            tiempo_total_en_servicio += duracion_evento
        if tipo_evento == +1: # Es decir, si el evento es un arribo
            cantidad_clientes_actuales += 1
        elif tipo_evento == -1: # Es decir, si el evento es un retiro
            cantidad_clientes_actuales -= 1
        

    tiempo_total = max(tiempos_retiros_clientes)  # se podria utilizar el parametro de entrada -n, ya que este es la cantidad de usuarios
    
    utilizacion_del_servicio = tiempo_total_en_servicio / tiempo_total
    
    return utilizacion_del_servicio
    

def calcular_probabilidad_de_encontrar_n_clientes_en_cola():
    print("\n--CALCULO PROBABILIDAD DE ENCONTRAR N CLIENTES EN COLA--\n")
    eventos = generador_arreglo_eventos()
    tiempo_n_cliente_en_cola = []
    probabilidad_de_n_clientes_en_cola = []

    tiempo_total = 0.0
    tiempo_anterior = 0
    cantidad_clientes_actuales = 0

    for e in eventos:
        tiempo_evento, tipo_evento = e
        duracion_evento = tiempo_evento - tiempo_anterior
        tiempo_anterior = tiempo_evento

        if cantidad_clientes_actuales >= len(tiempo_n_cliente_en_cola):
            tiempo_n_cliente_en_cola.append(0.0)

        if tipo_evento == +1: 
            tiempo_n_cliente_en_cola[cantidad_clientes_actuales] += duracion_evento 
            cantidad_clientes_actuales += 1
        elif tipo_evento == -1: 
            tiempo_n_cliente_en_cola[cantidad_clientes_actuales] += duracion_evento 
            cantidad_clientes_actuales -= 1

    tiempo_total = max(tiempos_retiros_clientes) 
    
  
    for i in range(len(tiempo_n_cliente_en_cola)):
        probabilidad_de_n_clientes_en_cola.append(0.0) # Inicializar la lista de probabilidades con ceros
        probabilidad_de_n_clientes_en_cola[i] = tiempo_n_cliente_en_cola[i]/tiempo_total
        
    return probabilidad_de_n_clientes_en_cola

def probabilidad_de_denegacion_de_servicio():
    print("\n--CALCULO PROBABILIDAD DE DENEGACION DE SERVICIO--\n")
    k = [[0,0.0], [2,0.0], [5,0.0], [10,0.0], [50,0.0]]
    eventos = generador_arreglo_eventos()
    
    for max_cola in k:
        contador_clientes_denegados = 0  
        contador_clientes_actuales = 0
        for e in eventos:

            tiempo_evento, tipo_evento = e
            
            if tipo_evento == +1: 
                if contador_clientes_actuales > max_cola[0]:
                    contador_clientes_denegados += 1
                else:
                    contador_clientes_actuales += 1
            elif tipo_evento == -1:
                contador_clientes_actuales -= 1
                
        probabilidad_denegacion = contador_clientes_denegados / len(tiempos_arribos_clientes)    

        max_cola[1] = probabilidad_denegacion
    
    return k
    

def calcular_valores_estadisticos_teoricos(tasa_servicio, tasa_arribo, cant_clientes):
    print("\n--CALCULO VALORES ESTADISTICOS TEORICOS--\n")
    utilizacion_servidor, numero_promedio_de_clientes_en_el_sistema, numero_promedio_clientes_en_cola, tiempo_promedio_en_el_sistema, tiempo_promedio_en_cola = calculos_estadisticos_generales(tasa_servicio, tasa_arribo)
    probabilidad_n_clientes_en_cola = calcular_probabilidades_n_clientes_en_cola_teorica(utilizacion_servidor, cant_clientes)
    probabilidades_denegacion_servicio = calcular_probabilidad_denegacion_servicio_teorica(utilizacion_servidor)

    return utilizacion_servidor, numero_promedio_de_clientes_en_el_sistema, numero_promedio_clientes_en_cola, tiempo_promedio_en_el_sistema, tiempo_promedio_en_cola, probabilidad_n_clientes_en_cola, probabilidades_denegacion_servicio

def calculos_estadisticos_generales(tasa_servicio, tasa_arribo):
    utilizacion_servidor = tasa_arribo / tasa_servicio
    numero_promedio_de_clientes_en_el_sistema = utilizacion_servidor / (1 - utilizacion_servidor)
    numero_promedio_clientes_en_cola = (utilizacion_servidor ** 2) / (1 - utilizacion_servidor)
    tiempo_promedio_en_el_sistema = 1 / (tasa_servicio - tasa_arribo)
    tiempo_promedio_en_cola = tasa_arribo / (tasa_servicio * (tasa_servicio - tasa_arribo))
    
    return utilizacion_servidor, numero_promedio_de_clientes_en_el_sistema, numero_promedio_clientes_en_cola, tiempo_promedio_en_el_sistema, tiempo_promedio_en_cola

def calcular_probabilidades_n_clientes_en_cola_teorica(utilizacion_servidor, cant_clientes):
    probabilidad_n_clientes_en_cola_por_corrida = []
    for n in range(0, cant_clientes + 1):  
        if n == 0:
            probabilidad_n_clientes = 1 - utilizacion_servidor
        else:
            probabilidad_n_clientes = (utilizacion_servidor ** (n+1)) * ((1 - utilizacion_servidor))
        probabilidad_n_clientes_en_cola_por_corrida.append(probabilidad_n_clientes)
    
    return probabilidad_n_clientes_en_cola_por_corrida

def calcular_probabilidad_denegacion_servicio_teorica(utilizacion_servidor):
    ks = [0, 2, 5, 10, 50]
    probabilidades_denegacion_servicio_por_corrida = [] 
    if utilizacion_servidor != 1:
        for k in ks: 
            probabilidad_denegacion = ((1 - utilizacion_servidor) * (utilizacion_servidor ** k)) / (1 - utilizacion_servidor ** (k + 1))
            probabilidades_denegacion_servicio_por_corrida.append(probabilidad_denegacion)
    else:
        for k in ks:
            probabilidad_denegacion = 1 / (k + 1)
            probabilidades_denegacion_servicio_por_corrida.append(probabilidad_denegacion)
    return probabilidades_denegacion_servicio_por_corrida

def resumen_simulacion(
    tasas_arribo,
    promedio_de_los_clientes_en_el_sistema_por_tasa,
    promedio_de_los_clientes_en_cola_por_tasa,
    tiempo_promedio_en_el_sistema_por_tasa,
    tiempo_promedio_en_cola_por_tasa,
    promedio_de_utilizacion_del_servidor_tasa,
    probabilidad_de_encontrar_n_clientes_en_cola_por_tasa_y_n_final,
    probabilidad_de_denegacion_de_servicio_por_tasa_y_denegacion_n_final
):


    # 1) Tabla de métricas numéricas
    data = [
        promedio_de_los_clientes_en_el_sistema_por_tasa,
        promedio_de_los_clientes_en_cola_por_tasa,
        tiempo_promedio_en_el_sistema_por_tasa,
        tiempo_promedio_en_cola_por_tasa,
        promedio_de_utilizacion_del_servidor_tasa
    ]
    col_labels = [f"{t:.2f}" for t in tasas_arribo]

    fig, ax = plt.subplots(figsize=(len(tasas_arribo)*1.2, 3))
    ax.axis('off')
    tabla = ax.table(
        cellText=data,
        colLabels=col_labels,
        rowLabels=[
            "Clientes en sistema",
            "Clientes en cola",
            "Tiempo en sistema",
            "Tiempo en cola",
            "Utilización servidor"
        ],
        loc='center'
    )
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.scale(1, 2)
    ax.set_title("Métricas por tasa de arribo")
    plt.show()

    # 2) Evolución: clientes en cola
    plt.figure()
    for tasa, dist in zip(tasas_arribo, probabilidad_de_encontrar_n_clientes_en_cola_por_tasa_y_n_final):
        xs = [n for (n, _) in dist]
        ys = [p for (_, p) in dist]
        plt.plot(xs, ys, label=f"Tasa {tasa:.2f}")
    plt.xlabel("Número de clientes en cola")
    plt.ylabel("Probabilidad")
    plt.title("Evolución: Distribución de clientes en cola")
    plt.legend()
    plt.show()

    # 3) Evolución: probabilidad de denegación
    plt.figure()
    for tasa, dist in zip(tasas_arribo, probabilidad_de_denegacion_de_servicio_por_tasa_y_denegacion_n_final):
        xs = [n for (n, _) in dist]
        ys = [p for (_, p) in dist]
        plt.plot(xs, ys, label=f"Tasa {tasa:.2f}")
    plt.xlabel("Número de clientes denegados")
    plt.ylabel("Probabilidad de denegación")
    plt.title("Evolución: Probabilidad de denegación de servicio")
    plt.legend()
    plt.show()


#----------------------------------- Definicion de argumentos -----------------------------------

parser = argparse.ArgumentParser(description="Simulación de un modelo MM1")

parser.add_argument("-c", type=int, required=True, help="Cantidad de corridas del sistema")
parser.add_argument("-n", type=int, required=True, help="Cantidad de usuarios a simular")
parser.add_argument("-mu", type=float, required=True, help="Tasa de servicio del servidor (clientes/tiempo) | siempre es mayor que lambda, si no se cumpliese seria un sistema inestable debido a que llegan mas de lo que se atiende lambda")
parser.add_argument("-l", type=float, required=True, help="Tasa de arribo de clientes al sistema (clientes/tiempo) | siempre es menor que mu")


# ------------------------------------------- Parseo de argumentos -----------------------------------------------------
args = parser.parse_args()

# ---------------------------------------------- Validaciones después del parseo ----------------------------------------------
if (args.c <= 0):
    print("Error: la cantidad de corridas (-c) debe ser un entero positivo.")
    sys.exit(1)

if (args.c < 10):
    print("Error: la cantidad de corridas (-c) debe ser MAYOR o igual a 10.")
    sys.exit(1)

if (args.n <= 0):
    print("Error: la cantidad de usuarios a simular (-n) debe ser un entero positivo.")
    sys.exit(1)

if (args.mu <= 0):
    print("Error: la tasa de servicio (-mu) debe ser un real positivo.")
    sys.exit(1)

if (args.l <= 0):
    print("Error: la tasa de arribo de clientes (-l) debe ser un real positivo.")
    sys.exit(1)

num_corridas = args.c
num_usuarios = args.n
tasa_servicio = args.mu
tasa_arribo = args.l


def simular():
    tasas_arribo = [
        tasa_arribo,
        0.25 * tasa_servicio,
        0.5  * tasa_servicio,
        0.75 * tasa_servicio,
        0.99 * tasa_servicio,
        1.25 * tasa_servicio
    ]
    denegaciones = [0, 2, 5, 10, 50]

    promedio_de_los_clientes_en_el_sistema_por_tasa = []
    promedio_de_los_clientes_en_cola_por_tasa    = []
    tiempo_promedio_en_el_sistema_por_tasa       = []
    tiempo_promedio_en_cola_por_tasa             = []
    promedio_de_utilizacion_del_servidor_tasa    = []

    probabilidad_de_encontrar_n_clientes_en_cola_por_tasa_y_n_final = []
    probabilidad_de_denegacion_de_servicio_por_tasa_y_denegacion_n_final = []

    for tasa in tasas_arribo:
        # inicializo acumuladores escalares
        promedio_de_los_clientes_en_el_sistema_por_tasa.append(0.0)
        promedio_de_los_clientes_en_cola_por_tasa.append(0.0)
        tiempo_promedio_en_el_sistema_por_tasa.append(0.0)
        tiempo_promedio_en_cola_por_tasa.append(0.0)
        promedio_de_utilizacion_del_servidor_tasa.append(0.0)

        # *** aquí creo listas NUEVAS para esta tasa ***
        probabilidad_de_encontrar_n_clientes_en_cola_por_tasa_y_n = [
            [usuario, 0.0] for usuario in range(num_usuarios + 1)
        ]
        probabilidad_de_denegacion_de_servicio_por_tasa_y_denegacion_n = [
            [d, 0.0] for d in denegaciones
        ]

        # simulo num_corridas veces
        for _ in range(num_corridas):
            tiempos_arribos_clientes.clear()
            tiempos_retiros_clientes.clear()

            print("---------------------------------------------------------------------------------------------")
            print("Los cálculos para una tasa de", tasa, "son:")

            calcular_tiempo_arribo_salida(tasa, tasa_servicio, num_usuarios)

            promedio_clientes_en_sistema = calcular_promedios_clientes_en_el_sistema()
            promedio_clientes_en_cola    = calcular_promedio_de_clientes_en_el_cola()
            tiempo_promedio_en_el_sistema = calcular_tiempo_promedio_en_el_sistema()
            tiempo_promedio_en_cola      = calcular_tiempo_promedio_en_la_cola()
            promedio_utilizacion_servidor= calcular_utilizacion_servidor()

            # acumulo en las listas locales
            probs_cola = calcular_probabilidad_de_encontrar_n_clientes_en_cola()
            for idx, p in enumerate(probs_cola):
                probabilidad_de_encontrar_n_clientes_en_cola_por_tasa_y_n[idx][1] += p

            probs_deneg = probabilidad_de_denegacion_de_servicio()
            for idx, pair in enumerate(probs_deneg):
                probabilidad_de_denegacion_de_servicio_por_tasa_y_denegacion_n[idx][1] += pair[1]

            """calcular_valores_estadisticos_teoricos(tasa_servicio, tasa, num_usuarios)"""

            # acumulo escalars
            promedio_de_los_clientes_en_el_sistema_por_tasa[-1] += promedio_clientes_en_sistema
            promedio_de_los_clientes_en_cola_por_tasa[-1]    += promedio_clientes_en_cola
            tiempo_promedio_en_el_sistema_por_tasa[-1]       += tiempo_promedio_en_el_sistema
            tiempo_promedio_en_cola_por_tasa[-1]             += tiempo_promedio_en_cola
            promedio_de_utilizacion_del_servidor_tasa[-1]    += promedio_utilizacion_servidor

        # promediar escalars
        promedio_de_los_clientes_en_el_sistema_por_tasa[-1] /= num_corridas
        promedio_de_los_clientes_en_cola_por_tasa[-1]    /= num_corridas
        tiempo_promedio_en_el_sistema_por_tasa[-1]       /= num_corridas
        tiempo_promedio_en_cola_por_tasa[-1]             /= num_corridas
        promedio_de_utilizacion_del_servidor_tasa[-1]    /= num_corridas

        # promediar distribuciones
        for i in range(len(probabilidad_de_encontrar_n_clientes_en_cola_por_tasa_y_n)):
            probabilidad_de_encontrar_n_clientes_en_cola_por_tasa_y_n[i][1] /= num_corridas
        for i in range(len(probabilidad_de_denegacion_de_servicio_por_tasa_y_denegacion_n)):
            probabilidad_de_denegacion_de_servicio_por_tasa_y_denegacion_n[i][1] /= num_corridas

        # guardo las listas NUEVAS en las finales
        probabilidad_de_encontrar_n_clientes_en_cola_por_tasa_y_n_final.append(
            probabilidad_de_encontrar_n_clientes_en_cola_por_tasa_y_n
        )
        probabilidad_de_denegacion_de_servicio_por_tasa_y_denegacion_n_final.append(
            probabilidad_de_denegacion_de_servicio_por_tasa_y_denegacion_n
        )


    print("---------------------------------")
    print("Promedio de clientes en el sistema por tasa: ", promedio_de_los_clientes_en_el_sistema_por_tasa)
    print("Promedio de clientes en cola por tasa:       ", promedio_de_los_clientes_en_cola_por_tasa)
    print("Tiempo promedio en el sistema por tasa:      ", tiempo_promedio_en_el_sistema_por_tasa)
    print("Tiempo promedio en cola por tasa:            ", tiempo_promedio_en_cola_por_tasa)
    print("Promedio de utilización del servidor por tasa:", promedio_de_utilizacion_del_servidor_tasa)

    # print("Probabilidad de denegación de servicio por tasa y n: ", probabilidad_de_denegacion_de_servicio_por_tasa_y_denegacion_n_final)
    # print("Probabilidad de encontrar n clientes en cola por tasa y n: ", probabilidad_de_encontrar_n_clientes_en_cola_por_tasa_y_n_final)

    resumen_simulacion(
    tasas_arribo,
    promedio_de_los_clientes_en_el_sistema_por_tasa,
    promedio_de_los_clientes_en_cola_por_tasa,
    tiempo_promedio_en_el_sistema_por_tasa,
    tiempo_promedio_en_cola_por_tasa,
    promedio_de_utilizacion_del_servidor_tasa,
    probabilidad_de_encontrar_n_clientes_en_cola_por_tasa_y_n_final,
    probabilidad_de_denegacion_de_servicio_por_tasa_y_denegacion_n_final
    )

simular()

"""         
                ------------------------ Calculo POR CORRIDA Y POR TASA ----------------------------------
            promedio_clientes_en_sistema = calcular_promedios_clientes_en_el_sistema()
            promedio_de_los_clientes_en_el_sistema_por_corrida_y_tasa.append([i , tasa, round(promedio_clientes_en_sistema, 4)])

            promedio_clientes_en_cola = calcular_promedio_de_clientes_en_el_cola()
            promedio_de_los_clientes_en_cola_por_corrida_y_tasa.append([i ,tasa, round(promedio_clientes_en_cola, 4)])
            
            tiempo_promedio_en_el_sistema =  calcular_tiempo_promedio_en_el_sistema()
            tiempo_promedio_en_el_sistema_por_corrida_y_tasa.append([i ,tasa, round(tiempo_promedio_en_el_sistema, 4)])

            tiempo_promedio_en_cola = calcular_tiempo_promedio_en_la_cola()
            tiempo_promedio_en_cola_por_corrida_y_tasa.append([i ,tasa, round(tiempo_promedio_en_cola, 4)])
            
            promedio_utilizacion_del_servidor = calcular_utilizacion_servidor()
            promededio_de_utilizacion_del_servidor_por_corrida_y_tasa.append([i ,tasa, round(promedio_utilizacion_del_servidor, 4)])

            probabilidad_de_encontrar_n_clientes_en_cola = calcular_probabilidad_de_encontrar_n_clientes_en_cola()

            probabilidad_de_encontrar_n_clientes_en_cola =  calcular_probabilidad_de_encontrar_n_clientes_en_cola()
            probabilidad_de_encontrar_n_clientes_en_cola_por_corrida_y_tasa.append([i ,tasa, probabilidad_de_encontrar_n_clientes_en_cola])

            graficar_metricas(promedio_de_los_clientes_en_el_sistema_por_corrida_y_tasa,
            promedio_de_los_clientes_en_cola_por_corrida_y_tasa,
            tiempo_promedio_en_el_sistema_por_corrida_y_tasa,
            tiempo_promedio_en_cola_por_corrida_y_tasa,
            promededio_de_utilizacion_del_servidor_por_corrida_y_tasa, probabilidad_de_encontrar_n_clientes_en_cola_por_corrida_y_tasa)

            graficar_probabilidad_denegacion(probabilidad_de_denegacion_de_servicio_por_corrida_tasa_y_denegacion_n)
            graficar_probabilidad_encontrar_n_clientes(probabilidad_de_encontrar_n_clientes_en_cola_por_corrida_tasa_y_n)
"""
