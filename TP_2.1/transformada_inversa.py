import random
import math
import matplotlib.pyplot as plt
import time

# Función para generar números aleatorios con distribución exponencial
def generar_exponencial(lambda_):
    # Generamos un número aleatorio uniforme entre 0 y 1
    r = random.uniform(0, 1)
    
    # Aplicamos la fórmula de la transformación inversa
    x = -math.log(1 - r) / lambda_
    
    return x

# Parámetro lambda (tasa de la distribución exponencial)
lambda_ = 1.0  # Puedes cambiar el valor de lambda según lo que necesites

# Número de muestras a generar
n_samples = 50000

# Generar n_samples números aleatorios
valores = [generar_exponencial(lambda_) for _ in range(n_samples)]

# Mostrar algunos resultados generados
print(f"Primeros 10 valores generados: {valores[:10]}")

# Graficar el histograma de los valores generados
plt.hist(valores, bins=30, density=True, alpha=0.6, color='g')

# Agregar la curva teórica de la distribución exponencial
x_vals = [i * 0.1 for i in range(0, 50)]
y_vals = [lambda_ * math.exp(-lambda_ * x) for x in x_vals]
plt.plot(x_vals, y_vals, 'r-', lw=2)

plt.title("Histograma y función de densidad exponencial")
plt.xlabel("Valor")
plt.ylabel("Frecuencia")
plt.show()


print(int(time.time()))