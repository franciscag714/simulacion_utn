import math
import matplotlib.pyplot as plt
import random
<<<<<<< Updated upstream
from test import KolmogorovSmirnovTest


def simular_normal(n):
    def densidad_normal(x, media, desvio):
        return (1 / (desvio * math.sqrt(2 * math.pi))) * math.exp(
            -0.5 * ((x - media) / desvio) ** 2
        )
=======
import numpy as np


def simular_normal(n):
    media = float(input("Ingrese la media requerida: "))
    desvio = float(input("Ingrese el desvio estandar: "))
    if desvio < 0:
        print("ERROR: El desvio debe ser mayor o igual a 0")
        return
    def densidad_normal(x, media = 0, desvio = 1):
        return (1 / (desvio * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((x - media) / desvio) ** 2)
>>>>>>> Stashed changes

    def densidad_uniforme(x, a, b):
        if a <= x <= b:
            return 1 / (b - a)
        else:
            return 0

    def normal_rechazo(
        media, desvio
    ):  # metodo de rechazo para la normal utilizando la uniforme
        a = (
            media - 4 * desvio
        )  # elegimos 4 porque el 99% de los valores en una distribucion normal se encuentran en: media +- desvio * 4
        b = media + 4 * desvio

        fx_max = densidad_normal(
            media, media, desvio
        )  # evaluamos la funcion densidad en x = media que es donde se produce su maximo
        gx = 1 / (b - a)
        c = fx_max / gx  # formula metodo rechazo

        while True:  # corta cuando encuentra un return
            x = random.uniform(a, b)  # x ~ g(x)
            u = random.uniform(0, 1)  # u ~ U(0,1)
            fx = densidad_normal(x, media, desvio)
            gx = densidad_uniforme(x, a, b)

            if u < fx / (c * gx):
                return x
    muestras_rechazo = []
    muestras_normal = []
    for i in range(n):
        valor_rechazo = normal_rechazo(media,desvio)
        muestras_rechazo.append(valor_rechazo)
        valor_normal = random.gauss(media, desvio)
        muestras_normal.append(valor_normal)

<<<<<<< Updated upstream
    # -------------FUNCIÓN DE DENSIDAD-------------
    # -------------TESTEO-------------
    print("\n---Test de Kolmogorov - Smirnov sobre Método de Rechazo ---")
    test = KolmogorovSmirnovTest()  # completar
    print(test.run_test())
    # -------------GRÁFICAS-------------
=======
                
    plt.subplot(1, 2, 1)
    plt.hist(muestras_rechazo, bins=30, density=True, alpha=0.7, color='skyblue', label='Muestras (rechazo)')
    x_vals = np.linspace(media - 5 * desvio, media + 5 * desvio, 500)
    y_vals = [(1 / (desvio * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - media) / desvio) ** 2) for x in x_vals]
    plt.plot(x_vals, y_vals, 'r-', label='Densidad teórica')
    plt.axvline(media, color='black', linestyle='--', label='Media')
    plt.title("Método de rechazo")
    plt.xlabel("Valor")
    plt.ylabel("Densidad")
    plt.legend()
    plt.grid(True)

    # Segundo gráfico: Distribución normal simulada directamente
    plt.subplot(1, 2, 2)
    plt.hist(muestras_normal, bins=30, density=True, alpha=0.7, color='lightgreen', label='Muestras (normal)')
    plt.plot(x_vals, y_vals, 'r-', label='Densidad teórica')
    plt.axvline(media, color='black', linestyle='--', label='Media')
    plt.title("Simulación directa (gauss)")
    plt.xlabel("Valor")
    plt.ylabel("Densidad")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()
>>>>>>> Stashed changes
