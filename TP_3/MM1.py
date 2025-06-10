import argparse
import sys 
import random 
import math 
import matplotlib.pyplot as plt

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


probabilidades_n_clientes_en_cola_por_tasa_de_arribo = []
probabilidades_denegacion_servicio_por_tasa_de_arribo = [] 

def calcular_valores_estadisticos(tasa_servicio, tasa_arribo):
    utilizacion_servidor = tasa_arribo / tasa_servicio
    numero_promedio_en_el_sistema = utilizacion_servidor / (1 - utilizacion_servidor)
    numero_promedio_clientes_en_cola = (utilizacion_servidor ** 2) / (1 - utilizacion_servidor)
    tiempo_promedio_en_el_sistema = 1 / (tasa_servicio - tasa_arribo)
    tiempo_promedio_en_cola = tasa_arribo / (tasa_servicio * (tasa_servicio - tasa_arribo))

    print(f"Utilización del servidor (ρ): {utilizacion_servidor:.4f}")
    print(f"Número promedio de clientes en el sistema (L): {numero_promedio_en_el_sistema:.4f}")
    print(f"Número promedio de clientes en la cola (Lq): {numero_promedio_clientes_en_cola:.4f}")
    print(f"Tiempo promedio en el sistema (W): {tiempo_promedio_en_el_sistema:.4f}")
    print(f"Tiempo promedio en la cola (Wq): {tiempo_promedio_en_cola:.4f}")

    return utilizacion_servidor


def calcular_probabilidades_n_clientes_en_cola(utilizacion_servidor):
    probabilidad_n_clientes_en_cola_por_corrida = []
    for n in range(0, 20):  
        if n == 0:
            probabilidad_n_clientes = 1 - utilizacion_servidor
        else:
            probabilidad_n_clientes = (utilizacion_servidor ** (n+1)) * ((1 - utilizacion_servidor))
        probabilidad_n_clientes_en_cola_por_corrida.append(probabilidad_n_clientes)
    
    return probabilidad_n_clientes_en_cola_por_corrida

def calcular_probabilidad_denegacion_servicio(utilizacion_servidor):
    ks = [0, 2, 5, 10, 50]
    probabilidades_denegacion_servicio_por_corrida = [] 
    if utilizacion_servidor < 1:
        for k in ks: 
            probabilidad_denegacion = ((utilizacion_servidor ** k) * (1 - utilizacion_servidor)) / (1 - (utilizacion_servidor ** (k + 1)))
            probabilidades_denegacion_servicio_por_corrida.append(probabilidad_denegacion)
    else:
        for k in ks:
            probabilidad_denegacion = 1 / (k + 1)
            probabilidades_denegacion_servicio_por_corrida.append(probabilidad_denegacion)
    return probabilidades_denegacion_servicio_por_corrida


def graficar(probabilidades_n_clientes_en_cola_por_tasa_de_arribo, probabilidades_denegacion_servicio_por_tasa_de_arribo, tasas_arribo_real, tasa_servicio):
    # Graficar probabilidades de n clientes en cola
    plt.figure(figsize=(12, 6))
    for i, prob_n_clientes in enumerate(probabilidades_n_clientes_en_cola_por_tasa_de_arribo):
        plt.plot(range(len(prob_n_clientes[0])), prob_n_clientes[0], label=f'Tasa de arribo: {tasas_arribo_real[i]:.2f} clientes/tiempo')
    
    plt.title('Probabilidad de n clientes en cola')
    plt.xlabel('Número de clientes en cola (n)')
    plt.ylabel('Probabilidad P(n)')
    plt.legend()
    plt.grid()
    plt.show()

    # Graficar probabilidades de denegación de servicio
    plt.figure(figsize=(12, 6))
    for i, prob_denegacion in enumerate(probabilidades_denegacion_servicio_por_tasa_de_arribo):
        plt.plot([0, 2, 5, 10, 50], prob_denegacion[0], label=f'Tasa de arribo: {tasas_arribo_real[i]:.2f} clientes/tiempo')
    
    plt.title('Probabilidad de denegación de servicio')
    plt.xlabel('Número máximo de clientes en el sistema (k)')
    plt.ylabel('Probabilidad P(Denegación)')
    plt.legend()
    plt.grid()
    plt.show()

def simular():

    porcentaje_tasas_de_arribo = [0.25, 0.50, 0.75, 0.99, 1.25] 
    tasas_arribo_real = []
    for i in porcentaje_tasas_de_arribo:
        tasa_arribo = i * tasa_servicio
        tasas_arribo_real.append(tasa_arribo)
        prob_n_clientes = []
        prob_denegacion = []
        for j in range(num_corridas):
            
            utilizacion_servidor = calcular_valores_estadisticos(tasa_servicio, tasa_arribo)

            prob_n_clientes.append(calcular_probabilidades_n_clientes_en_cola(utilizacion_servidor))

            prob_denegacion.append(calcular_probabilidad_denegacion_servicio(utilizacion_servidor))
    
        probabilidades_n_clientes_en_cola_por_tasa_de_arribo.append(prob_n_clientes)
        probabilidades_denegacion_servicio_por_tasa_de_arribo.append(prob_denegacion)


        # Llamás a graficar UNA VEZ al final, con todas las tasas
        graficar(probabilidades_n_clientes_en_cola_por_tasa_de_arribo,
                    probabilidades_denegacion_servicio_por_tasa_de_arribo,
                    tasas_arribo_real,
                    tasa_servicio)
                
simular()

