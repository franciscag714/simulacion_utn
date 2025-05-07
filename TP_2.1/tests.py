import numpy as np
from scipy.stats import chi2


class ChiSquaredUniformityTest:
    def __init__(self, data, num_bins=10):
        self.data = data
        self.num_bins = num_bins
        self.n = len(data)
        self.expected_freq = self.n / self.num_bins
        self.observed_freq, self.bin_edges = np.histogram(data, bins=self.num_bins, range=(0, 1))

    def run_test(self):
        chi_squared_stat = np.sum((self.observed_freq - self.expected_freq) ** 2 / self.expected_freq)
        df = self.num_bins - 1
        p_value = chi2.sf(chi_squared_stat, df)
        passes_test = p_value > 0.01

        return {
            "Estadístico Chi-Cuadrado": chi_squared_stat,
            "Grados de libertad": df,
            "Valor p": p_value,
            "Prueba de uniformidad": passes_test
        }

    def plot(self, ax):
        bin_labels = [f"{round(self.bin_edges[i], 2)}–{round(self.bin_edges[i+1], 2)}" for i in range(self.num_bins)]
        ax.bar(bin_labels, self.observed_freq, label='Observado', alpha=0.7)
        ax.axhline(self.expected_freq, color='red', linestyle='--', label='Esperado')
        ax.set_title('Chi Cuadrado')
        ax.set_xlabel('Bins')
        ax.set_ylabel('Frecuencia')
        ax.legend()
        ax.tick_params(axis='x', rotation=45)


class MediumTest:
    def __init__(self, valores):
        self.valores = valores
        self.median = np.median(valores)
        self.sequence = [1 if x > self.median else 0 for x in valores]
        self.rachas = 1 + sum(1 for i in range(1, len(self.sequence)) if self.sequence[i] != self.sequence[i - 1])
        self.cant_arriba = self.sequence.count(1)
        self.cant_abajo = self.sequence.count(0)
        self.mediana_esperada = (2 * self.cant_arriba * self.cant_abajo) / len(valores) + 1

    def run_test(self):
        return {
            "Rachas Observadas": self.rachas,
            "Rachas Esperadas": self.mediana_esperada
        }

    def plot(self, ax):
        ax.bar(["Obs.", "Esp."], [self.rachas, self.mediana_esperada], color=['blue', 'orange'])
        ax.axhline(y=self.mediana_esperada, color='red', linestyle='--')
        ax.set_title("Test de Rachas")
        ax.set_ylabel("Cantidad")


class PatternTest:
    def __init__(self, valores):
        self.valores = valores

    def plot(self, ax):
        ax.scatter(range(len(self.valores)), self.valores, color="black", alpha=0.65)
        ax.set_title("Patrones")
        ax.set_xlabel("Posición")
        ax.set_ylabel("Valor")
        ax.grid(True)


class SumTest:
    def __init__(self, valores):
        self.valores = valores
        self.n = len(valores)
        self.sum_observed = np.sum(valores)
        self.sum_expected = self.n * 0.5
        self.variance = self.n * (1 / 12)
        self.std_dev = np.sqrt(self.variance)

    def run_test(self):
        z = (self.sum_observed - self.sum_expected) / self.std_dev
        return {
            "Suma Observada": self.sum_observed,
            "Suma Esperada": self.sum_expected,
            "Z-Score": z
        }

    def plot(self, ax):
        ax.bar(['Obs.', 'Esp.'], [self.sum_observed, self.sum_expected], alpha=0.7)
        ax.errorbar(['Esp.'], [self.sum_expected], yerr=[self.std_dev], fmt='none', capsize=5, color='red')
        ax.set_title('Test de Suma')
        ax.set_ylabel('Suma Total')