import random
import matplotlib.pyplot as plt
import math

from scipy.stats import nbinom, poisson

def simular_pascal(N):
    print("-------------------PASCAL----------------")
    r = int(input("Ingrese el numero de exitos(r > 0): "))
    if r <= 0:
        print("ERROR: El numero de exitos deseado debe ser mayor a 0 ")

        return
    p = float(input("Ingrese la probabilidad de exito(0 < p < 1): "))
    if p <= 0 or p >=1:
        print("ERROR: La probabilidad de exito debe estar entre 0 y 1")
        return
    n = int(input("Ingrese la cantidad de muestras a generar (n > 0): "))
    if n <= 0:
        print("Error: la cantidad de muestras debe ser mayor que cero.")
        return

    # Función de masa de probabilidad de la Pascal
    def funcion_probabilidad_pascal(x, r, p):
        if x < r:
            return 0
        coef = math.comb(x - 1, r - 1)
        return coef * (p**r) * ((1 - p) ** (x - r))

    datos_directo = []
    datos_rechazo = []

    #METODO NORMAL
    for i in range(N):
        muestra = nbinom.rvs(r,p)
        datos_directo.append(muestra)

    #METODO RECHAZO DE PASCAL
    def rechazo_pascal(r,p):
        lam = r * (1-p)/p #media pascal
        M = 2.5 #cota para ejecutar el metodo rechazo(podemos cambiarlo)
        while True: #hasta que encuentre un return
            y = poisson.rvs(lam)
            fx = nbinom.pmf(y,r,p) #masa pascal
            gx = poisson.pmf(y, lam) #masa poisson
            unif = random.uniform(0,1)
            if gx == 0:
                continue
            if unif <= fx / (M * gx):
                return y
    for _ in range(N):
        muestra = rechazo_pascal(r,p)
        datos_rechazo.append(muestra)


    plt.hist(datos_directo, bins=range(min(datos_directo), max(datos_directo)+1), alpha=0.5, label="Normal", density=True, edgecolor="black")
    plt.hist(datos_rechazo, bins=range(min(datos_rechazo), max(datos_rechazo)+1), alpha=0.5, label="Rechazo", density=True, edgecolor="black")
    plt.title("Simulación Distribución Pascal")
    plt.xlabel("Número de Fracasos")
    plt.ylabel("Frecuencia Relativa")
    plt.legend()
    plt.grid(True)
    plt.show()