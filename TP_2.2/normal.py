import math
import matplotlib.pyplot as plt
import random
from test import KolmogorovSmirnovTest


def simular_normal(n):
    def densidad_normal(x, media, desvio):
        return (1 / (desvio * math.sqrt(2 * math.pi))) * math.exp(
            -0.5 * ((x - media) / desvio) ** 2
        )
import numpy as np


def simular_normal(n):
    media = float(input("Ingrese la media requerida: "))
    desvio = float(input("Ingrese el desvio estandar: "))
    if desvio < 0:
        print("ERROR: El desvio debe ser mayor o igual a 0")
        return
    def densidad_normal(x, media = 0, desvio = 1):
        return (1 / (desvio * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((x - media) / desvio) ** 2)

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

    
    # -------------TESTEO-------------
    print("\n---Test de Kolmogorov - Smirnov sobre Método de Rechazo ---")
    test = KolmogorovSmirnovTest(muestras_normal, "normal", {"mu": media , "sigma": desvio})  # completar
    print(test.run_test())
    print("\n---Test de Kolmogorov - Smirnov sobre Método de Rechazo ---")
    test2 = KolmogorovSmirnovTest(muestras_rechazo, "normal", {"mu": media , "sigma": desvio})  # completar
    print(test2.run_test())
    # -------------GRÁFICAS-------------
                
    fig, ax = plt.subplots(2, 2, figsize=(12, 5))
    ax[0,0].hist(muestras_rechazo, bins=30, density=True, alpha=0.7, color='skyblue', label='Muestras (rechazo)')
    x_vals = np.linspace(media - 5 * desvio, media + 5 * desvio, 500)
    y_vals = [(1 / (desvio * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - media) / desvio) ** 2) for x in x_vals]
    ax[0,0].plot(x_vals, y_vals, 'r-', label='Densidad teórica')
    ax[0,0].axvline(media, color='black', linestyle='--', label='Media')
    ax[0,0].set_title("Método de rechazo")
    ax[0,0].set_xlabel("Valor")
    ax[0,0].set_ylabel("Densidad")
    ax[0,0].legend()
    ax[0,0].grid(True)

    # Segundo gráfico: Distribución normal simulada directamente
    
    ax[0,1].hist(muestras_normal, bins=30, density=True, alpha=0.7, color='lightgreen', label='Muestras (normal)')
    ax[0,1].plot(x_vals, y_vals, 'r-', label='Densidad teórica')
    ax[0,1].axvline(media, color='black', linestyle='--', label='Media')
    ax[0,1].set_title("Simulación directa (gauss)")
    ax[0,1].set_xlabel("Valor")
    ax[0,1].set_ylabel("Densidad")
    ax[0,1].legend()
    ax[0,1].grid(True)

    test.plot(ax[1,1],"Simulacion Directa")
    test2.plot(ax[1,0], "Rechazo")
    plt.tight_layout()
    plt.show()