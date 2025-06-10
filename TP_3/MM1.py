import argparse
import sys 
import random 
import math 

class mm1_simulador:
    def __init__(self, num_corridas, num_usuarios, tasa_servicio, tasa_arribo_clientes):
        self.num_corridas = num_corridas
        self.num_usuarios = num_usuarios
        self.tasa_servicio = tasa_servicio
        self.tasa_arribo_clientes = tasa_arribo_clientes
        # PROCESOS FUTUROS
        self.reloj = 0.0  # Tiempo actual del reloj
        self.proximo_arribo = 0 
        self.proxima_salida = 10**30
        # ESTADO DEL SISTEMA
        self.estado_servidor = 0 # B(t)
        self.numero_clientes_en_cola = 0 #Q(t)
        self.tiempos_arribos_en_cola = []
        self.tiempo_ultimo_evento = 0
        # CONTADORES DE ESTADISTICAS
        self.contador_clientes_atendidos = 0
        self.demora_total = 0.0
        self.area_bajo_qt = 0.0 # (q(t) = Numero de clientes en cola en el tiempo t)
        self.area_bajo_bt = 0.0 # (b(t) = 1 si el servidor esta ocupado, 0 si no lo esta)
        

    def run(self):
        pass


# ---------------------------------- Declaracion de variables globales -----------------------------------

tiempos_arribos_clientes = []  # Lista para almacenar los tiempos de arribo de los clientes
tiempos_retiros_clientes = []  # Lista para almacenar los tiempos de retiro de los clientes


# ---------------------------------- Definición de funciones auxiliares -----------------------------------

def generador_numero_aleatorio():
    """Genera un número aleatorio entre 0 y 1."""
    return round(random.uniform(0, 1), 4)

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
    eventos = [] # arreglo bidimensional

    # se agregan los arribos y los retiros al arreglo eventos. +1 si es arribo, -1 si es retiro
    for a in tiempos_arribos_clientes:
        eventos.append((a, +1))
    for r in tiempos_retiros_clientes:
        eventos.append((r, -1))
        
    eventos.sort()
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
    
    print("Eventos (tiempo, tipo):", eventos)
    print("Promedio de clientes en el sistema:", promedio_clientes)


def calcular_promedio_de_clientes_en_el_cola():
    eventos = [] # arreglo bidim

    # se agregan los arribos y los retiros al arreglo eventos. 
    for a in tiempos_arribos_clientes:
        eventos.append((a, +1))
    for r in tiempos_retiros_clientes:
        eventos.append((r, -1))
        
    eventos.sort()
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

    print("Promedio de clientes en la cola:", promedio_clientes_en_cola)


def calcular_tiempo_promedio_en_el_sistema():
    tiempo_total = 0.0

    for i in range(len(tiempos_retiros_clientes)):
        tiempo_total += tiempos_retiros_clientes[i] - tiempos_arribos_clientes[i]
    
    cantidad_clientes = len(tiempos_retiros_clientes) # se podria utilizar el parametro de entrada -n, ya que este es la cantidad de usuarios
    
    promedio_tiempo = tiempo_total / cantidad_clientes      
    
    print("Tiempo promedio en el sistema:", promedio_tiempo)

def calcular_tiempo_promedio_en_la_cola():
    eventos = [] # arreglo bidim

    # se agregan los arribos y los retiros al arreglo eventos. 
    for a in tiempos_arribos_clientes:
        eventos.append((a, +1))
    for r in tiempos_retiros_clientes:
        eventos.append((r, -1))
        
    eventos.sort()
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

    print("Promedio de tiempo en la cola:", promedio_tiempo_en_cola)

def calcular_utilizacion_servidor():
    eventos = [] # arreglo bidim

    # se agregan los arribos y los retiros al arreglo eventos. 
    for a in tiempos_arribos_clientes:
        eventos.append((a, +1))
    for r in tiempos_retiros_clientes:
        eventos.append((r, -1))
        
    eventos.sort()
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

    print("-----------------------------------------------------------------------")
    print("La utilizacion del servicio del peluquero fue de un ", utilizacion_del_servicio*100, "%")
    print("El tiempo total del servicio", tiempo_total)
    

def calcular_probabilidad_de_encontrar_n_clientes_en_cola():
    eventos = []
    tiempo_n_cliente_en_cola = []
    probabilidad_de_n_clientes_en_cola = []
   

    for a in tiempos_arribos_clientes:
        eventos.append((a, +1))
    for r in tiempos_retiros_clientes:
        eventos.append((r, -1))
        
    eventos.sort()
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
        print("La probabilidad de encontrar ",i, "clientes en cola es", probabilidad_de_n_clientes_en_cola[i])
    
    print(sum(probabilidad_de_n_clientes_en_cola))

    
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

if (args.n <= 0):
    print("Error: la cantidad de usuarios a simular (-n) debe ser un entero positivo.")
    sys.exit(1)

if (args.mu <= 0):
    print("Error: la tasa de servicio (-mu) debe ser un real positivo.")
    sys.exit(1)

if (args.l <= 0):
    print("Error: la tasa de arribo de clientes (-l) debe ser un real positivo.")
    sys.exit(1)

if (args.l > args.mu):
    print("Error: la tasa de arribo de clientes (-l) debe ser menor o igual a la tasa de servicio (-mu).")
    sys.exit(1)


num_corridas = args.c
num_usuarios = args.n
tasa_servicio = args.mu
tasa_arribo = args.l

# Rutina de inicializacion 


def simular():

    # Calcular tiempos de arribo y retiro de clientes
    calcular_tiempo_arribo_salida(tasa_arribo, tasa_servicio, num_usuarios)

    calcular_promedios_clientes_en_el_sistema()

    calcular_promedio_de_clientes_en_el_cola()

    calcular_tiempo_promedio_en_el_sistema()

    calcular_tiempo_promedio_en_la_cola()
    calcular_utilizacion_servidor()
    calcular_probabilidad_de_encontrar_n_clientes_en_cola()
simular()