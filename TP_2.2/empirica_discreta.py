import random
import matplotlib.pyplot as plt
from test import ChiSquaredDiscreteTest


def simular_empirica_discreta(N):
    print("-------------EMPÍRICA DISCRETA-------------")
    cant = int(input("Ingrese la cantidad de valores posibles: "))
    if cant <= 0:
        print("Debe ingresar al menos un valor")
        return

    valores = []
    probabilidades = []

    for i in range(cant):
        valor = float(input(f"Ingrese el valor {i+1}: "))
        probabilidad = float(
            input(
                f"Ingrese la probabilidad de ocurrencia del valor {i+1}(Recuerde que la suma de probabilidades debe ser 1)"
            )
        )
        valores.append(valor)
        probabilidades.append(probabilidad)

        
    if sum(probabilidades) != 1:
        print("ERROR: La suma de probabilidades debe ser 1")
        return

    densidad = {val: prob for val, prob in zip(valores, probabilidades)}

    # -------------MÉTODO DE MUESTREO DIRECTO-------------
    def muestrear_directo(valores, probabilidades):
        u = random.random()
        acumulada = 0
        for valor, prob in zip(valores, probabilidades):
            acumulada += prob
            if u <= acumulada:
                return valor

    # -----------MÉTODO DE RECHAZO-----------
    def muestrear_por_rechazo(valores, probabilidades):
        long = len(valores)
        max_p = max(probabilidades)
        R = max(probabilidades) / (1 / long)

        while True:
            # Propuesta uniforme
            i = random.randint(0, long - 1)
            x = valores[i]
            g_x = 1 / long
            f_x = probabilidades[i]

            u = random.random()
            if u <= f_x / (R * g_x):
                return x

    # -----------GENERAR MUESTRAS-----------
    muestras_directas = [muestrear_directo(valores, probabilidades) for _ in range(N)]
    muestras_rechazo = [
        muestrear_por_rechazo(valores, probabilidades) for _ in range(N)
    ]

    # -------------TESTEO-------------
    print("\n--- Test Chi Cuadrado sobre Simulación Directa ---")
    test1 = ChiSquaredDiscreteTest(muestras_directas, densidad)
    print(test1.run_test())

    print("\n--- Test Chi Cuadradl sobre Método de Rechazo ---")
    test2 = ChiSquaredDiscreteTest(muestras_rechazo, densidad)
    print(test2.run_test())

    # -------------GRAFICAS-------------
    fig, ax = plt.subplots(2, 2, figsize=(12, 5))

    # Histograma muestreo directo
    ax[0, 0].hist(
        muestras_directas,
        bins=len(set(valores)),
        density=True,
        alpha=0.6,
        label="Simulación directa",
        edgecolor="black",
    )
    ax[0, 0].plot(valores, probabilidades, "ro--", label="Probabilidades teóricas")
    ax[0, 0].set_title("Distribución empírica - Simulación Directa")
    ax[0, 0].set_xlabel("Valor")
    ax[0, 0].set_ylabel("Frecuencia relativa")
    ax[0, 0].legend()
    ax[0, 0].grid(True)

    # Histograma método de rechazo
    ax[0, 1].hist(
        muestras_rechazo,
        bins=len(set(valores)),
        density=True,
        alpha=0.6,
        label="Rechazo",
        edgecolor="black",
    )
    ax[0, 1].plot(valores, probabilidades, "ro--", label="Probabilidades teóricas")
    ax[0, 1].set_title("Distribución empírica - Método de Rechazo")
    ax[0, 1].set_xlabel("Valor")
    ax[0, 1].set_ylabel("Frecuencia relativa")
    ax[0, 1].legend()
    ax[0, 1].grid(True)

    test1.plot(ax[1, 0], "Muestreo Directo")
    test2.plot(ax[1, 1], "Rechazo")

    plt.show()
