import random
import math
import matplotlib.pyplot as plt
import numpy as np
from test import ChiSquaredDiscreteTest

# -------------MÉTODO DEL LIBRO-------------
def poisson_libro(p):
    b = math.exp(-p)
    tr = 1.0
    x = 0
    while tr > b:
        r = random.random()
        tr = tr * r
        if tr > b:
            x += 1
    return x

# -------------MÉTODO DE RECHAZO-------------
def poisson_rechazo(p):
    c = math.sqrt(2 * math.pi * p)
    while True:
        x = int(random.gauss(mu=p, sigma=math.sqrt(p) + 0.5))
        if x < 0:
            continue
        fx = (p**x) * math.exp(-p) / math.factorial(x)
        gx = (1 / (math.sqrt(2 * math.pi * p))) * math.exp(
            -((x - p) ** 2) / (2 * p)
        )
        u = random.random()
        if u < fx / (gx * c):
            return x

def generar_poisson(p):
    if p < 10:
        return poisson_libro(p)
    else:
        return poisson_rechazo(p)

# -------------FUNCIÓN DE DENSIDAD-------------
def densidad_poisson(x, lamb):
    return (lamb**x) * math.exp(-lamb) / math.factorial(x)


def simular_poisson(N):
    print("-------------POISSON-------------")
    p = float(input("Ingrese el valor de lambda (λ): "))
    if p <= 0:
        print("El valor de lambda debe ser mayor que 0.")
        return

    datos = []

    for _ in range(N):
        datos.append(generar_poisson(p))

    # -------------GRÁFICAS-------------
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    x_vals = np.arange(0, max(datos) + 1)
    y_vals = [densidad_poisson(x, p) for x in x_vals]

    funcion_densidad = {x: densidad_poisson(x, p) for x in x_vals}
    # -------------TESTEO-------------
    print("\n---Test de Chi Cuadrado sobre Método de Rechazo ---")
    test = ChiSquaredDiscreteTest(datos, funcion_densidad)
    print(test.run_test())

    ax[0].hist(
        datos, bins=max(datos) + 1, density=True, color="skyblue", edgecolor="black"
    )
    ax[0].plot(x_vals, y_vals, "r--", label="f(x) teórica")
    ax[0].set_title("Distribución de Poisson")
    ax[0].set_xlabel("Valor")
    ax[0].set_ylabel("Densidad")
    ax[0].legend()
    ax[0].grid(True)

    test.plot(ax[1], "Rechazo")
    plt.show()
