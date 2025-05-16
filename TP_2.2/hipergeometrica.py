import random
import math
import matplotlib.pyplot as plt

#Funcion para calcular combinaciones
def combinaciones(n, k):
    return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))

def simular_hipergeometrica(N):
    print("HIPERGEOMÉTRICA")
    N= int(input("Ingrese la cantidad de elementos de la población: "))
    K= int(input("Ingrese la cantidad de elementos de la población que son éxitos: "))
    n= int(input("Ingrese la cantidad de elementos a extraer: "))
    M= int(input("Ingrese la cantidad de simulaciones: "))
    if n > N or K > N:
        print("Error: La cantidad de éxitos o la cantidad a extraer no pueden ser mayores que la población.")
        return
    if K < 0 or N <= 0 or n <= 0 or M <= 0:
        print("Error: Los valores deben ser positivos y mayores que cero.")
        return 
    datos = []
    for _ in range(M):
        muestra = random.sample(range(N), n)
        exitos = sum(1 for i in muestra if i < K)
        datos.append(exitos)

    #FUNCIÓN DE MASA
    def hipergeometrica_masa(x, n, K, N):
        if x < max(0, n - (N - K)) or x > min(K, n):
            return 0
        return (combinaciones(K, x) * combinaciones(N - K, n - x)) / combinaciones(N, n)
    
    #METODO DE RECHAZO
    def hipergeometrica_rechazo(n, K, N):
        K_min = max(0, n - (N - K))
        K_max = min(K, n)
        rango = list(range(K_min, K_max + 1))
        y_vals = [hipergeometrica_masa(x, n, K, N) for x in rango]
        p_max = max(y_vals) 
        c = p_max * len(rango)
        while True:
            x = random.choice(rango)
            y = random.uniform(0, c * (1/len(rango)))   
            if y <= hipergeometrica_masa(x, n, K, N):
                return x
    
    #GRAFICAS
    x_vals = list(range(max(0, n - (N - K)), min(K, n) + 1))
    y_vals = [hipergeometrica_masa(x, n, K, N) for x in x_vals]
    plt.hist(
        datos,
        bins=range(max(0, n - (N - K)), min(K, n) + 2),
        align="left",
        density=True,
        edgecolor="black",
        color="skyblue",
    )
    plt.plot(x_vals, y_vals, "r--", label="Función de masa teórica")
    plt.title(f"Distribucion Hipergeometrica - n={n}, K={K}, N={N}")
    plt.xlabel("Número de éxitos")
    plt.ylabel("Probabilidad")
    plt.legend()
    plt.grid(True)
    plt.show()


