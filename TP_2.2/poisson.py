import random
import math
import matplotlib.pyplot as plt


def simular_poisson(N):
    print("-------------POISSON-------------")
    p = float(input("Ingrese el valor de lambda (λ): "))

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

    # Método de rechazo()
    # def poisson_rechazo(N, lamb):
    # return

    def generar_poisson(p):
        if p < 10:
            return poisson_libro(p)
        # else:
        # return poisson_rechazo(p)

    # -------------FUNCIÓN DE DENSIDAD
    def densidad_poisson(x, lamb):
        return (lamb**x) * math.exp(-lamb) / math.factorial(x)

    for _ in range(N):
        datos.append(generar_poisson(p))
