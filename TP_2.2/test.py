import numpy as np
from scipy.stats import chi2, kstest, norm, expon


# --- TEST CHI CUADRADO PARA DISTRIBUCIÓN UNIFORME CONTINUA ---
class ChiSquaredUniformityTest:
    def __init__(self, data, a=0, b=1, num_bins=10):
        self.data = data
        self.a = a
        self.b = b
        self.num_bins = num_bins
        self.n = len(data)
        self.freq_esperada = self.n / self.num_bins
        self.freq_observada, self.bin_edges = np.histogram(
            data, bins=self.num_bins, range=(a, b)
        )

    def run_test(self):
        chi_squared_stat = np.sum(
            (self.freq_observada - self.freq_esperada) ** 2 / self.freq_esperada
        )
        df = self.num_bins - 1
        p_value = chi2.sf(chi_squared_stat, df)

        return {
            "Estadístico Chi-Cuadrado": chi_squared_stat,
            "Grados de libertad": df,
            "Valor p": p_value,
            "¿Pasa el test?": p_value > 0.01,
        }

    def plot(self, ax, metodo):
        bin_labels = [
            f"{round(self.bin_edges[i], 2)}–{round(self.bin_edges[i+1], 2)}"
            for i in range(self.num_bins)
        ]
        ax.bar(bin_labels, self.freq_observada, label="Observado", alpha=0.7)
        ax.axhline(self.freq_esperada, color="red", linestyle="--", label="Esperado")
        ax.set_title("Chi Cuadrado - " + metodo)
        ax.set_xlabel("Intervalos")
        ax.set_ylabel("Frecuencia")
        ax.legend()
        ax.tick_params(axis="x", rotation=45)
        ax.grid(True)


# --- TEST CHI CUADRADO PARA DISTRIBUCIONES DISCRETAS (BINOMIAL, POISSON, EMPÍRICA) ---
class ChiSquaredDiscreteTest:
    def __init__(self, data, funcion_densidad_esperada: dict):
        self.data = data
        self.funcion_densidad_esperada = funcion_densidad_esperada
        self.n = len(data)

        self.freq_observada = {x: 0 for x in funcion_densidad_esperada}
        for val in data:
            if val in self.freq_observada:
                self.freq_observada[val] += 1

        self.freq_esperada = {
            x: self.n * p for x, p in funcion_densidad_esperada.items()
        }

    def run_test(self):
        chi2_stat = 0
        df = 0
        for x in self.funcion_densidad_esperada:
            O = self.freq_observada[x]
            E = self.freq_esperada[x]
            if E > 0:
                chi2_stat += (O - E) ** 2 / E
                df += 1
        df -= 1
        p_value = chi2.sf(chi2_stat, df)

        return {
            "Estadístico Chi²": chi2_stat,
            "Grados de libertad": df,
            "Valor p": p_value,
            "¿Pasa el test?": p_value > 0.01,
        }

    def plot(self, ax, metodo):
        valores = sorted(self.freq_esperada.keys())
        obs = [self.freq_observada.get(x, 0) for x in valores]
        esp = [self.freq_esperada.get(x, 0) for x in valores]

        x = range(len(valores))
        width = 0.4

        ax.bar(
            [v - width / 2 for v in x],
            obs,
            width=width,
            label="Observado",
            color="skyblue",
            edgecolor="black",
        )
        ax.bar(
            [v + width / 2 for v in x],
            esp,
            width=width,
            label="Esperado",
            color="salmon",
            edgecolor="black",
        )

        ax.set_xticks(x)
        ax.set_xticklabels(valores)
        ax.set_xlabel("Valor")
        ax.set_ylabel("Frecuencia")
        ax.set_title("Chi Cuadrado - " + metodo)
        ax.legend()
        ax.grid(True)


# --- TEST KS PARA DISTRIBUCIONES CONTINUAS (NORMAL, EXPONENCIAL) ---
class KolmogorovSmirnovTest:
    def __init__(self, data, tipo, parametros=None):
        self.data = np.array(data)
        self.tipo = tipo
        self.parametros = parametros or {}

    def run_test(self):
        if self.tipo == "normal":
            mu = self.parametros.get("mu", 0)
            sigma = self.parametros.get("sigma", 1)
            stat, p_value = kstest(self.data, "norm", args=(mu, sigma))

        elif self.tipo == "exponencial":
            lambd = self.parametros.get("lambd", 1)
            stat, p_value = kstest(self.data, "expon", args=(0, 1 / lambd))

        else:
            raise ValueError("Distribución no soportada")

        return {
            "Estadístico KS": stat,
            "Valor p": p_value,
            "¿Pasa el test?": p_value > 0.01,
        }

    def plot(self, ax, metodo):
        data = np.sort(self.data)
        n = len(data)
        ecdf = np.arange(1, n + 1) / n

        if self.tipo == "normal":
            mu = self.parametros.get("mu", 0)
            sigma = self.parametros.get("sigma", 1)
            cdf = norm.cdf(data, loc=mu, scale=sigma)
        elif self.tipo == "exponencial":
            lambd = self.parametros.get("lambd", 1)
            cdf = expon.cdf(data, scale=1 / lambd)
        else:
            raise ValueError("Distribución no soportada")

        ks_stat = np.max(np.abs(cdf - ecdf))
        idx_max = np.argmax(np.abs(cdf - ecdf))

        ax.plot(data, ecdf, label="ECDF (empírica)", drawstyle="steps-post")
        ax.plot(data, cdf, label="CDF teórica", linestyle="--", color="red")
        ax.axvline(
            data[idx_max], color="black", linestyle="--", label=f"D = {ks_stat:.4f}"
        )
        ax.fill_between(data, ecdf, cdf, color="gray", alpha=0.3)

        ax.set_title(f"KS - " + metodo)
        ax.set_xlabel("x")
        ax.set_ylabel("Probabilidad acumulada")
        ax.legend()
        ax.grid(True)
