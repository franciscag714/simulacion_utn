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
    if p <= 0 or p >= 1:
        print("ERROR: La probabilidad de exito debe estar entre 0 y 1")
        return

    # Función de masa de probabilidad de la Pascal
    def funcion_probabilidad_pascal(x, r, p):
        if x < r:
            return 0
        coef = math.comb(x - 1, r - 1)
        return coef * (p**r) * ((1 - p) ** (x - r))

    datos_directo = []
    datos_rechazo = []

    # METODO NORMAL
    for i in range(N):
        muestra = nbinom.rvs(r, p)
        datos_directo.append(muestra)

    # METODO RECHAZO DE PASCAL
    def rechazo_pascal(r, p):
        lam = r * (1 - p) / p  # media pascal
        M = 2.5  # cota para ejecutar el metodo rechazo(podemos cambiarlo)
        while True:  # hasta que encuentre un return
            y = poisson.rvs(lam)
            fx = nbinom.pmf(y, r, p)  # masa pascal
            gx = poisson.pmf(y, lam)  # masa poisson
            unif = random.uniform(0, 1)
            if gx == 0:
                continue
            if unif <= fx / (M * gx):
                return y

    for _ in range(N):
        muestra = rechazo_pascal(r, p)
        datos_rechazo.append(muestra)

    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    # ----------- FUNCIONES TEÓRICAS -----------
    x_vals = list(
        range(
            min(datos_directo + datos_rechazo), max(datos_directo + datos_rechazo) + 1
        )
    )
    y_vals = [funcion_probabilidad_pascal(x, r, p) for x in x_vals]

    # Histograma de la Simulacion Directa
    ax[0].hist(
        datos_directo,
        bins=range(min(x_vals), max(x_vals) + 1),
        density=True,
        alpha=0.6,
        edgecolor="black",
        color="skyblue",
        label="Simulación directa",
    )
    ax[0].plot(x_vals, y_vals, "r--", label="f(x) teórica")
    ax[0].set_title(f"Distribución Pascal - Método directo (r={r}, p={p})")
    ax[0].set_xlabel("Número total de ensayos (x)")
    ax[0].set_ylabel("Frecuencia relativa")
    ax[0].legend()
    ax[0].grid(True)

    # Histograma metodo de rechazo
    ax[1].hist(
        datos_rechazo,
        bins=range(min(x_vals), max(x_vals) + 1),
        density=True,
        alpha=0.6,
        edgecolor="black",
        color="lightgreen",
        label="Simulación por rechazo",
    )
    ax[1].plot(x_vals, y_vals, "r--", label="f(x) teórica")
    ax[1].set_title(f"Distribución Pascal - Método de rechazo (r={r}, p={p})")
    ax[1].set_xlabel("Número total de ensayos (x)")
    ax[1].set_ylabel("Frecuencia relativa")
    ax[1].legend()
    ax[1].grid(True)

    plt.show()
