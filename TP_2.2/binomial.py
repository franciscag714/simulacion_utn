import random
import math
import matplotlib.pyplot as plt
from test import ChiSquaredDiscreteTest


def simular_binomial(N):
    print("-------------BINOMIAL-------------")
    p = float(input("Ingrese la probabilidad de exito (0 < p < 1): "))
    if not (0 < p < 1):
        print("Error: la probabilidad debe estar entre 0 y 1.")
        return
    n = int(input("Ingrese la cantidad de ensayos de Bernoulli: "))
    if n <= 0:
        print("Error: la cantidad de ensayos debe ser mayor que cero.")
        return
    datos = []

    # -------------MÉTODO DE RECHAZO (libro)-------------
    def binomial_rechazo(n, p):
        x = 0.0
        for _ in range(n):
            r = random.random()
            if r < p:
                x = x + 1
        return x

    # -------------FUNCIÓN DE DENSIDAD-------------
    def densidad_binomial(x, n, p):
        comb = math.comb(n, x)
        return comb * (p**x) * ((1 - p) ** (n - x))

    for _ in range(N):
        datos.append(binomial_rechazo(n, p))

    # -------------GRÁFICA-------------
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    x_vals = list(range(0, n + 1))
    y_vals = []
    for x in x_vals:
        y_vals.append(densidad_binomial(x, n, p))

    funcion_densidad = {x: densidad_binomial(x, n, p) for x in x_vals}
    # -------------TESTEO-------------
    print("\n---Test de Chi Cuadrado sobre Método de Rechazo ---")
    test = ChiSquaredDiscreteTest(datos, funcion_densidad)
    print(test.run_test())

    # Histograma método de rechazo
    ax[0].hist(
        datos,
        bins=range(n + 2),
        align="left",
        density=True,
        edgecolor="black",
        color="skyblue",
    )
    ax[0].plot(x_vals, y_vals, "r--", label="Función de densidad teórica")
    ax[0].set_title(f"Distribucion Binomial - n={n}, p={p}")
    ax[0].set_xlabel("Número de éxitos")
    ax[0].set_ylabel("Probabilidad")
    ax[0].legend()
    ax[0].grid(True)

    test.plot(ax[1], "Rechazo")

    plt.show()
