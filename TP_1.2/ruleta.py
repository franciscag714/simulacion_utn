import random
import sys
import matplotlib.pyplot as plt
import argparse

# --------------------------------- Definicion de variables ------------------------------------
ruleta = [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    33,
    34,
    35,
    36,
]
frecuencia_esperada = 1 / 37
valores_por_corrida = []
freq_relativa_por_corrida = []
flujo_de_caja = []
aciertos_por_corrida = 0
color = str
fila = 0
zona = 0
resultado = ""
MAX_TIRADAS = 10000
MAX_CORRIDAS = 20
capital_inicial = 10000
apuesta_inicial = 100


# ---------------------------------------- Definicion de funciones --------------------------------
def graficar_corrida(freq_relativa_por_corrida, flujo_de_caja):
    fig, axs = plt.subplots(nrows=1, ncols=2)
    fig.suptitle("Datos corrida " + str(i + 1))

    x_vals_freq = range(1, len(freq_relativa_por_corrida) + 1)
    flujo_de_caja_sin_inicial = flujo_de_caja[1:]
    x_vals_flujo = range(1, len(flujo_de_caja_sin_inicial) + 1)

    # Gráfico de frecuencia relativa
    axs[0].bar(x_vals_freq, freq_relativa_por_corrida, color="red", edgecolor="black")
    axs[0].hlines(frecuencia_esperada, 1, len(freq_relativa_por_corrida), colors="blue")
    axs[0].set_xlabel("n (número de tiradas)")
    axs[0].set_ylabel("fr (frecuencia relativa)")
    axs[0].legend(
        [
            "Frecuencia esperada 1/37",
            "frsa (Frecuencia relativa de\nobtener la apuesta favorable segun n)",
        ],
        loc="best",
    )

    # Gráfico de flujo de caja
    axs[1].plot(x_vals_flujo, flujo_de_caja_sin_inicial, color="red")
    axs[1].hlines(10000, 1, len(flujo_de_caja_sin_inicial), colors="blue")
    axs[1].set_xlabel("n (número de tiradas)")
    axs[1].set_ylabel("cc (cantidad de capital)")
    axs[1].legend(["Flujo de caja", "Capital inicial)"], loc="best")

    plt.tight_layout()
    plt.show()


def color_num(num):
    if num in {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}:
        color = "rojo"
    elif num in {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}:
        color = "negro"
    elif num == 0:
        color = "verde"
    return color


def columna_num(num):
    if num in {1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34}:
        columna = 1
    elif num in {2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35}:
        columna = 2
    elif num in {3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36}:
        columna = 3
    else:
        columna = 0
    return columna


def zona_num(num):
    if num in range(1, 13):
        zona = 1
    elif num in range(13, 25):
        zona = 2
    elif num in range(25, 37):
        zona = 3
    else:
        zona = 0
    return zona


def paridad_num(num):
    if num % 2 == 0:
        resultado = "par"
    else:
        resultado = "impar"
    return resultado


def martingala(apuesta_inicial, num_elegido, num, cap, elec):
    if num != num_elegido:
        cap = cap - apuesta_inicial
        apuesta = apuesta_inicial * 2
    else:
        if elec == 1:
            cap = cap + apuesta_inicial * 36
            apuesta = 100
        elif elec == 2:
            cap = cap + apuesta_inicial * 2
            apuesta = 100
        elif elec == 3:
            cap = cap + apuesta_inicial * 2
            apuesta = 100
        elif elec == 4 or elec == 5:
            cap = cap + apuesta_inicial * 3
            apuesta = 100
    return apuesta, cap


def dalembert(apuesta_inicial, mundo, mundo_a_comparar, cap, elec):
    if mundo != mundo_a_comparar:
        cap = cap - apuesta_inicial
        apuesta = apuesta_inicial + 1
    else:
        if elec == 1:
            cap = cap + apuesta_inicial * 36
            apuesta = max(1, apuesta_inicial - 1)
        elif elec == 2:
            cap = cap + apuesta_inicial * 2
            apuesta = max(1, apuesta_inicial - 1)
        elif elec == 3:
            cap = cap + apuesta_inicial * 2
            apuesta = max(1, apuesta_inicial - 1)
        elif elec == 4 or elec == 5:
            cap = cap + apuesta_inicial * 3
            apuesta = max(1, apuesta_inicial - 1)
    return apuesta, cap


def fibonacci(apuesta_inicial, mundo, mundo_a_comparar, cap, secuencia, indice, elec):
    if mundo != mundo_a_comparar:
        cap = cap - apuesta_inicial
        indice += 1
        if indice >= len(secuencia):
            secuencia.append(secuencia[-1] + secuencia[-2])
    else:
        if elec == 1:
            cap = cap + apuesta_inicial * 36
            indice = max(0, indice - 2)
        elif elec == 2:
            cap = cap + apuesta_inicial * 2
            indice = max(0, indice - 2)
        elif elec == 3:
            cap = cap + apuesta_inicial * 2
            indice = max(0, indice - 2)
        elif elec == 4 or elec == 5:
            cap = cap + apuesta_inicial * 3
            indice = max(0, indice - 2)
    apuesta = secuencia[indice]
    return apuesta, cap, secuencia, indice


def paroli(apuesta_inicial, num_elegido, num, cap, elec):
    if num != num_elegido:
        cap = cap - apuesta_inicial
        apuesta = apuesta_inicial
    else:
        if elec == 1:
            cap = cap + apuesta_inicial * 36
            apuesta = apuesta_inicial * 2
        elif elec == 2:
            cap = cap + apuesta_inicial * 2
            apuesta = apuesta_inicial * 2
        elif elec == 3:
            cap = cap + apuesta_inicial * 2
            apuesta = apuesta_inicial * 2
        elif elec == 4 or elec == 5:
            cap = cap + apuesta_inicial * 3
            apuesta = apuesta_inicial * 2
    return apuesta, cap


# ----------------------------------- Definicion de argumentos -----------------------------------
parser = argparse.ArgumentParser(description="Simulación de ruleta")
opciones = parser.add_mutually_exclusive_group(required=True)
parser.add_argument(
    "-c", type=int, required=True, help="Cantidad de tiradas (entero positivo)"
)
parser.add_argument(
    "-n", type=int, required=True, help="Cantidad de corridas (entero positivo)"
)
opciones.add_argument("-e", type=int, help="Número elegido (entre 0 y 36)")
parser.add_argument(
    "-s", type=str, required=True, help="Estrategia elegida (m, f, d, o)"
)
parser.add_argument("-a", type=str, required=True, help="Cantidad de capital (i, f)")
opciones.add_argument("-b", type=str, help="Color rojo o negro")
opciones.add_argument("-p", type=str, help="par o impar")
opciones.add_argument(
    "-z", type=int, help="1 (primera docena), 2 (segunda docena) o 3 (tercera docena)"
)
opciones.add_argument(
    "-d",
    type=int,
    help="1 (primera columna), 2 (segunda columna) o 3 (tercera columna)",
)

# ------------------------------------------- Parseo de argumentos -----------------------------------------------------
args = parser.parse_args()

# ---------------------------------------------- Validaciones después del parseo ----------------------------------------------
if args.c <= 0:
    print("Error: la cantidad de tiradas (-c) debe ser un entero positivo.")
    sys.exit(1)

if args.n <= 0:
    print("Error: la cantidad de corridas (-n) debe ser un entero positivo.")
    sys.exit(1)

if args.c > MAX_TIRADAS:
    print(f"Error: la cantidad de tiradas no debe superar {MAX_TIRADAS}.")
    sys.exit(1)

if args.n > MAX_CORRIDAS:
    print(f"Error: la cantidad de corridas no debe superar {MAX_CORRIDAS}.")
    sys.exit(1)

if args.e is not None:
    if args.e < 0 or args.e > 36:
        print("Error: el número elegido (-e) debe estar entre 0 y 36.")
        sys.exit(1)
    mundo = args.e
    eleccion = 1

if args.s != "m" and args.s != "f" and args.s != "d" and args.s != "o":
    print("Error: la estrategia elegida (-s) debe ser 'f', 'm', 'd' u 'o'")
    sys.exit(1)

if args.a != "f" and args.a != "i":
    print("Error: el capital elegido (-a) debe ser finito (f) o infinito (i)")
    sys.exit(1)

if args.b is not None:
    if args.b != "rojo" and args.b != "negro":
        print("Error: el color elegido (-b) debe ser 'rojo' o 'negro'.")
        sys.exit(1)
    mundo = args.b
    eleccion = 2

if args.p is not None:
    if args.p != "par" and args.p != "impar":
        print("Error: la paridad elegida (-p) debe ser 'par' o 'impar'.")
        sys.exit(1)
    mundo = args.p
    eleccion = 3

if args.z is not None:
    if args.z != 1 and args.z != 2 and args.z != 3:
        print(
            "Error: la zona elegida (-z) debe ser 1 (primera docena), 2 (segunda docena) o 3 (tercera docena)."
        )
        sys.exit(1)
    mundo = args.z
    eleccion = 4

if args.d is not None:
    if args.d != 1 and args.d != 2 and args.d != 3:
        print(
            "Error: la columna elegida (-d) debe ser 1 (primera columna), 2 (segunda columna) o 3 (tercera columna)."
        )
        sys.exit(1)
    mundo = args.d
    eleccion = 5

print(
    f"Tiradas: {args.c}, Corridas: {args.n}, Número elegido: {args.e}, Estrategia elegida: {args.s}, Capital elegido: {args.a}, Color elegido: {args.b}, Paridad elegida: {args.p}, Zona elegida: {args.z}, Columna elegida: {args.d} "
)

num_tiradas = args.c
num_corridas = args.n
num_elegido = args.e
est_elegida = args.s
cap_elegido = args.a
color_elegido = args.b
paridad_elegida = args.p
zona_elegida = args.z
columna_elegida = args.d

# --------------------------------------------------------- Inicio de la simulación -------------------------------------------------
for i in range(num_corridas):
    print("Corrida numero", i + 1)
    valores_por_corrida.clear()
    freq_relativa_por_corrida.clear()
    flujo_de_caja = [10000]
    aciertos_por_corrida = 0
    perdidas_por_corrida = 0
    capital_inicial = 10000
    apuesta_inicial = 100
    secuencia = [1, 1, 2, 3, 5, 8, 13, 21]
    indice = 0

    for j in range(num_tiradas):
        valor = random.randint(0, 36)
        if args.e is not None:
            mundo_a_comparar = valor
        if args.b is not None:
            mundo_a_comparar = color_num(valor)
        if args.p is not None:
            mundo_a_comparar = paridad_num(valor)
        if args.z is not None:
            mundo_a_comparar = zona_num(valor)
        if args.d is not None:
            mundo_a_comparar = columna_num(valor)
        valores_por_corrida.append(valor)

        if valor != 0:
            color_aleatorio = color_num(valor)
            columna_aleatorio = columna_num(valor)
            zona_aleatorio = zona_num(valor)
            par_aleatorio = paridad_num(valor)

        if est_elegida == "m":
            ap, capital = martingala(
                apuesta_inicial, mundo, mundo_a_comparar, capital_inicial, eleccion
            )
        elif est_elegida == "f":
            ap, capital, secuencia, indice = fibonacci(
                apuesta_inicial,
                mundo,
                mundo_a_comparar,
                capital_inicial,
                secuencia,
                indice,
                eleccion,
            )
        elif est_elegida == "d":
            ap, capital = dalembert(
                apuesta_inicial, mundo, mundo_a_comparar, capital_inicial, eleccion
            )
        elif est_elegida == "o":
            ap, capital = paroli(
                apuesta_inicial, mundo, mundo_a_comparar, capital_inicial, eleccion
            )

        flujo_de_caja.append(capital_inicial)

        if mundo_a_comparar == mundo:
            print(
                "El mundo elegido:",
                mundo,
                ", tuvo acierto en la tirada numero",
                j + 1,
            )
            aciertos_por_corrida += 1
        else:
            perdidas_por_corrida += 1
        freq_relativa_por_corrida.append(aciertos_por_corrida / (j + 1))

        print("Capital: ", capital)
        apuesta_inicial = ap
        capital_inicial = capital

        if cap_elegido == "f":
            if capital_inicial <= 0 or capital_inicial < apuesta_inicial:
                print("Banca rota")
                break

    print("Valores: ", valores_por_corrida)
    print("Cantidad de aciertos: ", aciertos_por_corrida)
    print("Cantidad de perdidas: ", perdidas_por_corrida)
    graficar_corrida(freq_relativa_por_corrida, flujo_de_caja)

    print("---------------------------------------------")
