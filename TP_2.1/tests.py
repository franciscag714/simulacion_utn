from scipy.stats import chisquare
import numpy as np
import time
def chi_square_test(generator, n=1000, bins=10):
    data = [generator.next() / generator.m for _ in range(n)]
    frequencies, _ = np.histogram(data, bins=bins, range=(0, 1))
    expected = [n / bins] * bins
    chi2, p = chisquare(frequencies, expected)
    print(f"Chi-Square Test: chi2={chi2}, p-value={p}")


def test_independencia(generator, n=1000, lag=1):
    resultados = [generator.next() for _ in range(n)]
    correlacion = sum(resultados[i] * resultados[i + lag] for i in range(n - lag))
    print(f"Autocorrelación con lag {lag}: {correlacion}")
    return correlacion



def test_secuencias(generator, n=1000):
    resultados = [generator.next() % 2 for _ in range(n)]  # 0 o 1 para simplificar
    cambios = sum(1 for i in range(1, n) if resultados)

def test_secuencias(generator, n=1000):
    resultados = [generator.next() % 2 for _ in range(n)]  # 0 o 1 para simplificar
    cambios = sum(1 for i in range(1, n) if resultados)


print(int(time.time()) % 10000)