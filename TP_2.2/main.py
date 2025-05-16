from uniforme import simular_uniforme
from exponencial import simular_exponencial
from gamma import simular_gamma


def main():

    N = int(input("Ingrese la cantidad de numeros a generar: "))
    if N <= 0:
        print("Error: la cantidad de números debe ser mayor a cero.")
        return

    simular_uniforme(N)
    simular_exponencial(N)
    simular_gamma(N)


if __name__ == "__main__":  # para que se ejecute main solo
    main()
