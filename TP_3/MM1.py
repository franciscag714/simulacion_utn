import argparse
import sys 
import random 
import math 
## Ver diagrama de flujo de mecanismo del proximo evento

## ------------------------------- Medidas de desempeño -----------------------------------------------
# demora promedio: promedio_demora = sum(d(n))/n
# numero promedio de clientes en cola: promedio_clientes_en_cola = integral() de 0 a T(n) de Q(t)dt / T(n)
# B(t) = 1 , si el servidor esta ocupado en el tiempo t
# B(t) = 0, si el servidor esta desocupado en el tiempo t
# medida de cuan ocupado está el servidor: u(n): ocupacion_servidor = integral de 0 a T(n) de B(t)dt / T(n)

"""
----Metricas a obtener por simulacion----


Promedio de clientes en el sistema (𝐿)

Promedio de clientes en la cola (𝐿𝑞)

Tiempo promedio en el sistema (𝑊)

Tiempo promedio en la cola (𝑊𝑞)

Utilización del servidor (𝜌=𝜆/𝜇)

Probabilidad de encontrar n clientes en cola

Probabilidad de denegacion de servicio con colas finitas (tamaño máximo: 0, 2, 5, 10, 50)

------- Parametros a variar --------
Tasa de servicio (𝜇): fija (por ejemplo: 1 cliente por minuto)

Tasa de arribo (𝜆): multiplos de la tasa de servicio:

25% (0.25𝜇)

50% (0.50𝜇)

75% (0.75𝜇)

100% (1.00𝜇)

125% (1.25𝜇) ← sistema se satura

----------------------------- modelo MM1) --------------------------------
Generar llegadas con distribucion exponencial (parametro 𝜆)

Generar servicios con distribucion exponencial (parametro 𝜇)

Simular la cola FIFO (primero en llegar, primero en ser atendido)

Medir:

Cuántos clientes hay en el sistema en cada instante

Cuánto tiempo esperan

Si fueron rechazados (si la cola tiene tamaño máximo)

Cuánto tiempo estuvo el servidor ocupado

----------------------------------- PROBABILIDADES -----------------------------------------------------------
Probabilidad de encontrar n clientes en cola: contar cuántas veces hay exactamente n clientes esperando

Probabilidad de denegación de servicio: proporción de clientes que no entraron por cola llena

----------------------------- PARAMETROS DE ENTRADA ----------------------------------

lambda --> Tasa de arribo de clientes al sistema (clientes/tiempo) | siempre es menor que mu

mu --> Tasa de servicio del servidor (clientes/tiempo) | siempre es mayor que lambda, si no se cumpliese seria un sistema inestable debido a que llegan mas de lo que se atiende lambda

N --> Cantidad de usuarios a simular 

C --> Corridas del sistema (cantidad de veces que se simula el sistema con los mismos parametros)


"""

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


simular()