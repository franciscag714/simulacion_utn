import random
import matplotlib.pyplot as plt
import math
import numpy as np


def simular_gamma(N):
    print("GAMMA")
    k = float(input("Ingrese k (forma > 0): "))
    a = float(input("Ingrese a (tasa > 0): "))

    if k <= 0 or a <= 0:
        print("Error: k y a deben ser mayores que cero.")
        return

    datos = []

    # Método para k entero
    def gamma_entero(k, a):

        TR = 1.0

        for _ in range(int(k)):
            R = random.random()
            TR *= R

        X = -math.log(TR) / a

        return X

    # Método de rechazo para k no entero
    def gamma_rechazo(k, a):
        d = k - 1 / 3
        c = 1 / math.sqrt(9 * d)
        while True:
            x = random.gauss(0, 1)
            v = (1 + c * x) ** 3
            if v <= 0:
                continue
            u = random.random()
            if u < 1 - 0.0331 * x**4:
                return d * v / 4
            if math.log(u) < 0.5 * x**2 + d * (1 - v + math.log(v)):
                return d * v / a

    if k.is_integer():
        for _ in range(N):
            datos.append(gamma_entero(int(k), a))
    else:
        for _ in range(N):
            datos.append(gamma_rechazo(k, a))

    # --- Función de densidad teórica
    def densidad_gamma(x, k, a):
        if x <= 0:
            return 0
        return (a**k) / math.gamma(k) * (x ** (k - 1)) * math.exp(-a * x)

    x_vals = np.linspace(0, max(datos), 500)
    y_vals = []
    for x in x_vals:
        y_vals.append(densidad_gamma(x, k, a))

    # Histograma
    plt.hist(datos, bins=50, density=True, edgecolor="black", color="skyblue")
    plt.plot(x_vals, y_vals, "r--", label="Función de densidad teórica")
    plt.title(f"Distribucion Gamma - k={k}, a={a}")
    plt.xlabel("Valor")
    plt.ylabel("Densidad")
    plt.legend()
    plt.grid(True)
    plt.show()
