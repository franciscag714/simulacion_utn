import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2



def chi_squared_uniformity_test(data, num_bins=10, show_plot=True):

    """
    OTRA FORMA DE HACER LA PRUEBA DE CHI-CUADRADO ---
    def chi_square_test(data, bins=10, alpha=0.05):
        observed, _ = np.histogram(data, bins=bins)
        expected = np.full_like(observed, len(data) / bins)
        chi_squared_stat = ((observed - expected) ** 2 / expected).sum()
        critical_value = chi2.ppf(1 - alpha, bins - 1)
        return chi_squared_stat, critical_value, chi_squared_stat < critical_value
    """
    n = len(data)
    expected_freq = n / num_bins
    observed_freq, bin_edges = np.histogram(data, bins=num_bins, range=(0, 1))

    # Estadístico Chi-Cuadrado
    chi_squared_stat = np.sum((observed_freq - expected_freq) ** 2 / expected_freq)
    df = num_bins - 1
    p_value = chi2.sf(chi_squared_stat, df)
    passes_test = p_value > 0.01

    # Gráfico (si se habilita)
    if show_plot:
        bin_labels = [f"{round(bin_edges[i],2)}–{round(bin_edges[i+1],2)}" for i in range(num_bins)]
        plt.figure(figsize=(10, 5))
        plt.bar(bin_labels, observed_freq, label='Observado', alpha=0.7)
        plt.axhline(expected_freq, color='red', linestyle='--', label='Esperado')
        plt.title('Frecuencias observadas vs. esperadas por bin')
        plt.xlabel('Intervalos (bins)')
        plt.ylabel('Frecuencia')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    return {
        "Chi-Squared Statistic": chi_squared_stat,
        "Degrees of Freedom": df,
        "p-value": p_value,
        "Passes Uniformity Test": passes_test
    }

# ------------------------------------------------ Transformada de Fourier Test ---------------------------------------------
def fourier_transform_test(sequence):

    # Convertir la secuencia a un arreglo de numpy
    seq = np.array(sequence)

    # Aplicar la Transformada Discreta de Fourier (DFT)
    dft_result = np.fft.fft(seq)

    # Obtener la magnitud de las frecuencias (valor absoluto)
    magnitudes = np.abs(dft_result)

    # Graficar el espectro de frecuencias
    plt.figure(figsize=(10, 5))
    plt.plot(magnitudes)
    plt.title("Espectro de Frecuencias de la Secuencia")
    plt.xlabel("Frecuencia")
    plt.ylabel("Magnitud")
    plt.grid(True)

    # Análisis: Ver si hay picos significativos
    threshold = 2 * np.mean(magnitudes)  # Umbral para identificar picos
    peaks = [i for i, value in enumerate(magnitudes) if value > threshold]

    # Agregar texto en el gráfico según el análisis
    if len(peaks) == 0:
        analysis_text = "El espectro de frecuencias es plano, lo que indica una secuencia aleatoria."
    else:
        analysis_text = f"Se detectaron picos en las frecuencias {peaks[0]}, {peaks[1]}, {peaks[2]} , entre otros, lo que sugiere patrones no aleatorios."

    plt.text(0.1, max(magnitudes)*0.8, analysis_text, fontsize=12, color='red', ha='left')

    # Mostrar el gráfico
    plt.show()


    result = {
        "Spectral Magnitudes": magnitudes,
        "Peaks Above Threshold": peaks,
        "Random?": len(peaks) == 0  # Si no hay picos, la secuencia es aleatoria
    }

    return result



def medium_test(valores):
    # Estudio de rachas de Wald-Wolfowitz

    cant_valores = len(valores)
    media_esperada = np.median(valores)

    secuencia = []
    for i in range(cant_valores):
        secuencia.append(1 if valores[i] > media_esperada else 0)


    rachas = 1
    for j in range(1, cant_valores):
        if(secuencia[j] != secuencia[j-1]):
            rachas += 1
      
    cant_arriba = secuencia.count(1)
    cant_abajos = secuencia.count(0)

    media_final = (2 * (cant_arriba * cant_abajos) / cant_valores ) + 1 



    plt.figure(figsize=(12, 4))


    plt.subplot(1, 2, 1)
    plt.step(range(len(secuencia)), secuencia, where='post', color='blue')
    plt.title("Secuencia de Rachas (1=Arriba de la mediana, 0=Abajo)")
    plt.xlabel("Posición")
    plt.ylabel("Valor")
    plt.yticks([0, 1])

    plt.subplot(1, 2, 2)
    plt.bar(["Observadas", "Esperadas"], [rachas, media_final], color=['blue', 'orange'])
    plt.title("Rachas Observadas vs Esperadas")
    plt.ylabel("Cantidad")
    plt.axhline(y=media_final, color='red', linestyle='--', label='Esperadas')

    plt.tight_layout()
    plt.show()



def pattern_test(valores):
    posiciones = list(range(len(valores)))

    plt.figure(figsize=(12, 6))
    plt.scatter(posiciones, valores, color="black", alpha=0.65)
    plt.xlabel("Posición en el Array")
    plt.ylabel("Valor Generado")
    plt.title("Busqueda de Patrones en la Secuencia")
    plt.grid(True)
    plt.show()
        

def sum_test(valores):
    # Test de la suma de los valores generados
    pass