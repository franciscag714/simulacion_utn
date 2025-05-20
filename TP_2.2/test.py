import numpy as np
from scipy.stats import chi2

#--- TEST CHI CUADRADO  --- 
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

