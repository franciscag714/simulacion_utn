import random
import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as poisson


def simular_poisson(N):
    print("-------------POISSON-------------")
    p = float(input("Ingrese el valor de lambda (λ): "))
    if p <= 0:
        print("El valor de lambda debe ser mayor que 0.")
        return

    datos = []

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
             fx = (p ** x) * math.exp(-p) / math.factorial(x)
             gx = (1 / (math.sqrt(2 * math.pi * p))) * math.exp(-(x - p) ** 2 / (2 * p))
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

    for _ in range(N):
        datos.append(generar_poisson(p))


    # -------------GRÁFICAS-------------
    x_vals = np.arange(0, max(datos) + 1)
    y_vals = [densidad_poisson(x, p) for x in x_vals]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(datos, bins=max(datos) + 1, density=True, color="skyblue", edgecolor="black")
    ax.plot(x_vals, y_vals, "r--", label="f(x) teórica")
    ax.set_title("Distribución de Poisson")
    ax.set_xlabel("Valor")
    ax.set_ylabel("Densidad")
    ax.legend()
    ax.grid(True)
    plt.show()
    

