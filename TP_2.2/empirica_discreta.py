import random
import matplotlib.pyplot as plt
from test import ChiSquaredDiscreteTest


# -----------MÉTODO DE RECHAZO-----------
def muestrear_por_rechazo(valores, probabilidades):
    long = len(valores)
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

    # -----------GENERAR MUESTRAS-----------

    muestras_rechazo = [
        muestrear_por_rechazo(valores, probabilidades) for _ in range(N)
    ]

    # -------------TESTEO-------------

    print("\n--- Test Chi Cuadradl sobre Método de Rechazo ---")
    test2 = ChiSquaredDiscreteTest(muestras_rechazo, densidad)
    print(test2.run_test())

    # -------------GRAFICAS-------------
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))


    # Histograma método de rechazo
    ax[0].hist(
        muestras_rechazo,
        bins=len(set(valores)),
        density=True,
        alpha=0.6,
        label="Rechazo",
        edgecolor="black",
    )
    ax[0].plot(valores, probabilidades, "ro--", label="Probabilidades teóricas")
    ax[0].set_title("Distribución empírica - Método de Rechazo")
    ax[0].set_xlabel("Valor")
    ax[0].set_ylabel("Frecuencia relativa")
    ax[0].legend()
    ax[0].grid(True)

    test2.plot(ax[1], "Rechazo")

    plt.show()
