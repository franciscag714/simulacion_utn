
import random
import math
import matplotlib.pyplot as plt


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
    x_vals = list(range(0, n + 1))
    y_vals = []
    for x in x_vals:
        y_vals.append(densidad_binomial(x, n, p))

    # Histograma método de rechazo
    plt.hist(
        datos,
        bins=range(n + 2),
        align="left",
        density=True,
        edgecolor="black",
        color="skyblue",
    )
    plt.plot(x_vals, y_vals, "r--", label="Función de densidad teórica")
    plt.title(f"Distribucion Binomial - n={n}, p={p}")
    plt.xlabel("Número de éxitos")
    plt.ylabel("Probabilidad")
    plt.legend()
    plt.grid(True)
    plt.show()
