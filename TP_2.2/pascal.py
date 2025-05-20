import random
import matplotlib.pyplot as plt
import math


def simular_pascal(N):
    print("----------------DISTRIBUCION PASCAL--------------")
    e = int(input("Ingrese la cantidad de exitos deseados: "))
    if e <= 0:
        print("ERROR: La cantidad de exitos deseados debe ser minimo 1")
        return
    p = float(input("Ingrese la probabilidad de exito: "))
    if p <= 0 or p >= 1:
        print("ERROR: La probabilidad debe estar entre 0 y 1")
        return
    n = int(input("Ingrese la cantidad de muestras a generar (n > 0): "))
    if n <= 0:
        print("Error: la cantidad de muestras debe ser mayor que cero.")
        return

    # Función de masa de probabilidad de la Pascal
    def funcion_probabilidad_pascal(x, r, p):
        if x < r:
            return 0
        coef = math.comb(x - 1, r - 1)
        return coef * (p**r) * ((1 - p) ** (x - r))
