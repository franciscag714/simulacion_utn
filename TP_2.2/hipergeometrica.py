import random
import math
import matplotlib.pyplot as plt


# Funcion para calcular combinaciones
def combinaciones(n, k):
    return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))


def simular_hipergeometrica(N):
    print("-------------HIPERGEOMÉTRICA-------------")
    poblacion_N = int(input("Ingrese la cantidad de elementos de la población: "))
    K = int(input("Ingrese la cantidad de elementos de la población que son éxitos: "))
    n = int(input("Ingrese la cantidad de elementos a extraer: "))

    if n > poblacion_N or K > poblacion_N:
        print(
            "Error: La cantidad de éxitos o la cantidad a extraer no pueden ser mayores que la población."
        )
        return
    if K < 0 or poblacion_N <= 0 or n <= 0:
        print("Error: Los valores deben ser positivos y mayores que cero.")
        return

    datos = []
    for _ in range(N):
        muestra = random.sample(range(poblacion_N), n)
        exitos = sum(1 for i in muestra if i < K)
        datos.append(exitos)

    # -------------FUNCIÓN DE MASA-------------
    def hipergeometrica_masa(x, n, K, Np):
        if x < max(0, n - (Np - K)) or x > min(K, n):
            return 0
        return (combinaciones(K, x) * combinaciones(Np - K, n - x)) / combinaciones(
            Np, n
        )

    # -------------METODO DE RECHAZO-------------
    def hipergeometrica_rechazo(n, K, Np):
        K_min = max(0, n - (Np - K))
        K_max = min(K, n)
        rango = list(range(K_min, K_max + 1))
        y_vals = [hipergeometrica_masa(x, n, K, Np) for x in rango]
        p_max = max(y_vals)
        c = p_max * len(rango)
        while True:
            x = random.choice(rango)
            y = random.uniform(0, c * (1 / len(rango)))
            if y <= hipergeometrica_masa(x, n, K, Np):
                return x

    datos_rechazo = [hipergeometrica_rechazo(n, K, poblacion_N) for _ in range(N)]

    # -------------GRAFICAS-------------
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    x_vals = list(range(max(0, n - (N - K)), min(K, n) + 1))
    y_vals = [hipergeometrica_masa(x, n, K, N) for x in x_vals]

    ax[0].hist(
        datos,
        bins=range(min(x_vals), max(x_vals) + 2),
        align="left",
        density=True,
        edgecolor="black",
        color="skyblue",
        label="Simulación directa",
    )
    ax[0].plot(x_vals, y_vals, "r--", label="f(x) teórica")
    ax[0].set_title(
        f"Hipergeométrica - n={n}, K={K}, N={poblacion_N} - Muestreo directo"
    )
    ax[0].set_xlabel("Número de éxitos")
    ax[0].set_ylabel("Frecuencia relativa")
    ax[0].legend()
    ax[1].grid(True)

    ax[1].hist(
        datos_rechazo,
        bins=range(min(x_vals), max(x_vals) + 2),
        align="left",
        density=True,
        edgecolor="black",
        color="lightgreen",
        label="Simulación por rechazo",
    )
    ax[1].plot(x_vals, y_vals, "r--", label="Función de masa teórica")
    ax[1].set_title(
        f"Hipergeométrica - n={n}, K={K}, N={poblacion_N} - Método de rechazo"
    )
    ax[1].set_xlabel("Número de éxitos")
    ax[1].set_ylabel("Frecuencia relativa")
    ax[1].legend()
    ax[1].grid(True)

    plt.tight_layout()
    plt.show()
