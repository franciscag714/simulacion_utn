from uniforme import simular_uniforme
from exponencial import simular_exponencial
from gamma import simular_gamma
from poisson import simular_poisson
from binomial import simular_binomial
from hipergeometrica import simular_hipergeometrica
from normal import simular_normal
from empirica_discreta import simular_empirica_discreta
from pascal import simular_pascal


def main():

    N = int(input("Ingrese la cantidad de numeros a generar: "))
    if N <= 0:
        print("Error: la cantidad de números debe ser mayor a cero.")
        return

    simular_uniforme(N)
    simular_exponencial(N)
    simular_gamma(N)
    simular_normal(N)
    simular_pascal(N)
    simular_binomial(N)
    simular_hipergeometrica(N)
    simular_poisson(N)
    simular_empirica_discreta(N)


if __name__ == "__main__":  # para que se ejecute main solo
    main()
