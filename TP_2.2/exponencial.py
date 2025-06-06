import random
import numpy as np
import matplotlib.pyplot as plt
from test import KolmogorovSmirnovTest


# -------------MÉTODO DE LA TRANSFORMACIÓN INVERSA-------------
def exponencial_inversa(lambd, r):
    return -(1 / lambd) * np.log(r)

# -------------MÉTODO DE VON NEUMANN (rechazo)-------------
def exponencial_von_neumann(lambd, N):
    datos_von_neumann = []
    while len(datos_von_neumann) < N:
        u1 = np.random.uniform(0, 1)
        u2 = np.random.uniform(0, 1)
        if u2 <= np.exp(-u1):
            x = u1 / lambd
            datos_von_neumann.append(x)
    return datos_von_neumann


# -------------FUNCIÓN DE DENSIDAD-------------
def densidad_exponencial(x, lambd):
    return lambd * np.exp(-lambd * x)


def simular_exponencial(N):
    print("-------------EXPONENCIAL-------------")
    lambd = float(input("Ingrese el valor de lambda: "))
    if lambd <= 0:
        raise ValueError("Lambda debe ser mayor que 0")

    datos_inversa = []
    for i in range(N):
        x = exponencial_inversa(lambd, random.random())
        datos_inversa.append(x)

    datos_rechazo = exponencial_von_neumann(lambd, N)


    # -------------TESTEO-------------
    print(
        "\n---Test de Kolmogorov - Smirnov sobre Método de Transformación Inversa ---"
    )
    test = KolmogorovSmirnovTest(
        datos_inversa, tipo="exponencial", parametros={"lambd": lambd}
    )
    print(test.run_test())

    print("\n---Test de Kolmogorov - Smirnov sobre Método de Rechazo ---")
    test2 = KolmogorovSmirnovTest(
        datos_rechazo, tipo="exponencial", parametros={"lambd": lambd}
    )
    print(test2.run_test())

    # -------------GRÁFICAS-------------
    x_vals = np.linspace(0, 5, 100)
    y_vals = densidad_exponencial(x_vals, lambd)

    fig, ax = plt.subplots(2, 2, figsize=(12, 5))
    # Histograma método transformación inversa
    ax[0, 0].hist(
        datos_inversa, bins=50, density=True, color="skyblue", edgecolor="black"
    )
    ax[0, 0].plot(x_vals, y_vals, "r--", label="f(x) teórica")
    ax[0, 0].set_title("Distribución Exponencial - Método de la Transformación Inversa")
    ax[0, 0].set_xlabel("Valor")
    ax[0, 0].set_ylabel("Densidad")
    ax[0, 0].legend()
    ax[0, 0].grid(True)

    # Histograma método de rechazo
    ax[0, 1].hist(
        datos_rechazo, bins=50, density=True, color="skyblue", edgecolor="black"
    )
    ax[0, 1].plot(x_vals, y_vals, "r--", label="f(x) teórica")
    ax[0, 1].set_title("Distribución Exponencial - Método de Rechazo")
    ax[0, 1].set_xlabel("Valor")
    ax[0, 1].set_ylabel("Densidad")
    ax[0, 1].legend()
    ax[0, 1].grid(True)

    test.plot(ax[1, 0], "Transformación Inversa")
    test2.plot(ax[1, 1], "Rechazo")

    plt.tight_layout()
    plt.show()
