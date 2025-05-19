import random
import matplotlib.pyplot as plt

def simular_empirica_discreta(N):
    print("-----DISTRIBUCIÓN EMPÍRICA DISCRETA-----")
    cant = int(input("Ingrese la cantidad de valores posibles: "))
    if cant <= 0:
        print("Debe ingresar al menos un valor")
        return
    
    valores = []
    probabilidades = []

    for i in range(cant):
        valor = float(input(f"Ingrese el valor {i+1}: "))
        probabilidad = float(input(f"Ingrese la probabilidad de ocurrencia del valor {i+1}(Recuerde que la suma de probabilidades debe ser 1)"))
        valores.append(valor)
        probabilidades.append(probabilidad)
        
    if sum(probabilidad) != 1.0:
        print("ERROR: La suma de probabilidades debe ser 1")
        return
    
    #Muestreo directo
    def muestrear_directo(valores, probabilidades):
        u = random.random()
        acumulada = 0
        for valor, prob in zip(valores, probabilidades):
            acumulada += prob
            if u <= acumulada:
                return valor
    # ----------- SIMULACIÓN CON MÉTODO DE RECHAZO -----------
    def muestrear_por_rechazo(valores, probabilidades):
        long = len(valores)
        max_p = max(probabilidades)
        R = max_p * long  # Cota para el método de rechazo

        while True:
            # Propuesta uniforme
            i = random.randint(0, long - 1)
            x = valores[i]
            g_x = 1 / long
            f_x = probabilidades[i]

            u = random.random()
            if u <= f_x / (R * g_x):
                return x

    # ----------- GENERAR MUESTRAS -----------
    muestras_directas = [muestrear_directo(valores, probabilidades) for _ in range(N)]
    muestras_rechazo = [muestrear_por_rechazo(valores, probabilidades) for _ in range(N)]

    #GRAFICAS
    
    plt.hist(muestras_directas, bins=len(set(valores)), alpha=0.6, label="Simulación directa", density=True, edgecolor="black")
    plt.hist(muestras_rechazo, bins=len(set(valores)), alpha=0.6, label="Método de rechazo", density=True, edgecolor="black")
    plt.title("Comparación: simulación directa vs. método de rechazo")
    plt.xlabel("Valor")
    plt.ylabel("Frecuencia relativa")
    plt.legend()
    plt.grid(True)
    plt.show()
