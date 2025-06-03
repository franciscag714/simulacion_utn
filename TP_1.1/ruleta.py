import random
import sys 
import statistics as stats
import matplotlib.pyplot as plt
import argparse

#--------------------------------- Definicion de variables ------------------------------------ 
ruleta = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]
promedio_esperado = stats.mean(ruleta)
varianza_esperada = stats.variance(ruleta)
desvio_esperado = stats.stdev(ruleta)
frecuencia_esperada = 1/37
valores_por_corrida = []
promedio_por_corrida = []
desvio_por_corrida = []
varianza_por_corrida = []
freq_relativa_por_corrida = []
aciertos_por_corrida = 0
MAX_TIRADAS = 10000
MAX_CORRIDAS = 20

#---------------------------------------- Definicion de funciones --------------------------------
def graficar_corrida(freq_relativa_por_corrida, promedio_por_corrida, varianza_por_corrida, desvio_por_corrida):
    fig, axs = plt.subplots(nrows=2, ncols=2)
    fig.suptitle('Datos corrida ' + str(i + 1))

    x_vals = range(1, num_tiradas + 1)  

    axs[0, 0].plot(x_vals, freq_relativa_por_corrida)
    axs[0, 0].hlines(frecuencia_esperada, 1, num_tiradas, colors='r')
    axs[0, 0].set_xlabel('Número de tirada')
    axs[0, 0].set_ylabel('Frecuencia relativa')
    axs[0, 0].legend(['Frec. relativa del número ' + str(num_elegido), 'Frecuencia esperada'])
    


    axs[0,1].plot(x_vals, promedio_por_corrida)
    axs[0,1].hlines(promedio_esperado, 1, num_tiradas, colors='r')
    axs[0,1].set_xlabel('Número de tirada')
    axs[0,1].set_ylabel('Promedio')
    axs[0, 1].legend(['Progreso de la media' , 'Promedio esperado'])

    axs[1,0].plot(x_vals[1:], varianza_por_corrida) 
    axs[1,0].hlines(varianza_esperada, 2, num_tiradas, colors='r')
    axs[1,0].set_xlabel('Número de tirada')
    axs[1,0].set_ylabel('Varianza')
    axs[1, 0].legend(['Progreso de la varianza', 'Varianza esperada'])

    axs[1,1].plot(x_vals[1:], desvio_por_corrida)  
    axs[1,1].hlines(desvio_esperado, 2, num_tiradas, colors='r')
    axs[1,1].set_xlabel('Número de tirada')
    axs[1,1].set_ylabel('Desvío')
    axs[1, 1].legend(['Progreso del desvio', 'Desvio esperado'])

    plt.tight_layout()
    plt.show()


#----------------------------------- Definicion de argumentos -----------------------------------
parser = argparse.ArgumentParser(description="Simulación de ruleta")

parser.add_argument("-c", type=int, required=True, help="Cantidad de tiradas (entero positivo)")
parser.add_argument("-n", type=int, required=True, help="Cantidad de corridas (entero positivo)")
parser.add_argument("-e", type=int, required=True, help="Número elegido (entre 0 y 36)")

# ------------------------------------------- Parseo de argumentos -----------------------------------------------------
args = parser.parse_args()

# ---------------------------------------------- Validaciones después del parseo ----------------------------------------------
if (args.c <= 0):
    print("Error: la cantidad de tiradas (-c) debe ser un entero positivo.")
    sys.exit(1)

if (args.n <= 0):
    print("Error: la cantidad de corridas (-n) debe ser un entero positivo.")
    sys.exit(1)

if args.c > MAX_TIRADAS:
    print(f"Error: la cantidad de tiradas no debe superar {MAX_TIRADAS}.")
    sys.exit(1)

if args.n > MAX_CORRIDAS:
    print(f"Error: la cantidad de corridas no debe superar {MAX_CORRIDAS}.")
    sys.exit(1)

if (args.e < 0 or args.e > 36):
    print("Error: el número elegido (-e) debe estar entre 0 y 36.")
    sys.exit(1)

print(f"Tiradas: {args.c}, Corridas: {args.n}, Número elegido: {args.e}")

num_tiradas = args.c
num_corridas = args.n
num_elegido = args.e

# --------------------------------------------------------- Inicio de la simulación -------------------------------------------------
for i in range(num_corridas):
    print("Corrida numero", i + 1)
    valores_por_corrida.clear()
    promedio_por_corrida.clear()
    desvio_por_corrida.clear()
    varianza_por_corrida.clear()
    freq_relativa_por_corrida.clear()
    aciertos_por_corrida = 0


    for j in range(num_tiradas):
        valor = random.randint(0, 36)
        valores_por_corrida.append(valor)
        promedio_por_corrida.append(stats.mean(valores_por_corrida))
        if j > 0:
            varianza_por_corrida.append(stats.variance(valores_por_corrida))
            desvio_por_corrida.append(stats.stdev(valores_por_corrida))
        if (valor == num_elegido):
            print("El numero elegido", num_elegido,  "tuvo acierto en la tirada numero", j + 1)
            aciertos_por_corrida += 1
        freq_relativa_por_corrida.append(aciertos_por_corrida/(j+1))

    print("Valores: ",valores_por_corrida)
    print("Cantidad de aciertos: ", aciertos_por_corrida)
    graficar_corrida(freq_relativa_por_corrida, promedio_por_corrida, varianza_por_corrida, desvio_por_corrida)
    print("---------------------------------------------")  

