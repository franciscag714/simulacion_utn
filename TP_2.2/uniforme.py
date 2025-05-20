import random
import matplotlib.pyplot as plt
import numpy as np
from test import ChiSquaredUniformityTest

# -------------MÉTODO DE LA TRANSFORMACIÓN INVERSA-------------
def uniforme_inversa(a, b, r):
    return a + (b - a) * r


def simular_uniforme(N):
    print("-------------UNIFORME-------------")
    a = float(input("Ingrese el limite inferior a: "))
    b = float(input("Ingrese el limite superior b: "))
    if a >= b:
        print("Error: el límite inferior debe ser menor que el superior.")
        return

    datos_inversa = []
    for i in range(N):
        x = uniforme_inversa(a, b, random.random())
        datos_inversa.append(x)

    # -------------MÉTODO DE RECHAZO-------------
    f_max = 1 / (b - a)
    datos_rechazo = []

    while len(datos_rechazo) < N:
        x = random.uniform(a, b)
        y = random.uniform(0, f_max)

        if y <= f_max:
            datos_rechazo.append(x)

    # -------------FUNCIÓN DE DENSIDAD-------------
    x_vals = np.linspace(a, b, 500)
    y_vals = [1 / (b - a) if a <= x <= b else 0 for x in x_vals]

    # -------------TESTEO-------------
    print("\n---Test de Chi Cuadrado sobre Método de Transformación Inversa ---")
    test = ChiSquaredUniformityTest(datos_inversa, a=a, b=b)
    print(test.run_test())

    print("\n--- Test de Chi² sobre Método de Rechazo ---")
    test2 = ChiSquaredUniformityTest(datos_rechazo, a=a, b=b)
    print(test2.run_test())

    # -------------GRÁFICAS-------------
    fig, ax = plt.subplots(2, 2, figsize=(12, 5))

    # Histograma método de la transformación inversa
    ax[0, 0].hist(
        datos_inversa, bins=50, density=True, color="skyblue", edgecolor="black"
    )
    ax[0, 0].plot(x_vals, y_vals, "r--", label="f(x) teórica")
    ax[0, 0].set_title("Distribución Uniforme - Método de la Transformación Inversa")
    ax[0, 0].set_xlabel("Valor")
    ax[0, 0].set_ylabel("Densidad")
    ax[0, 0].legend()
    ax[0, 0].grid(True)

    # Histograma método de rechazo
    ax[0, 1].hist(
        datos_rechazo, bins=50, density=True, color="skyblue", edgecolor="black"
    )
    ax[0, 1].plot(x_vals, y_vals, "r--", label="f(x) teórica")
    ax[0, 1].set_title("Distribución Uniforme - Método de Rechazo")
    ax[0, 1].set_xlabel("Valor")
    ax[0, 1].set_ylabel("Densidad")
    ax[0, 1].legend()
    ax[0, 1].grid(True)

    test.plot(ax[1, 0], "Transformación Inversa")
    test2.plot(ax[1, 1], "Rechazo")

    plt.tight_layout()
    plt.show()
