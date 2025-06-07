import numpy as np
import matplotlib.pyplot as plt

# Parámetros del sistema
Q = 50          # Valor maximo de inventario
R = 20          # Punto de reorden
lead_time = 15   # Días de espera entre orden y entrega

# Costos
costo_orden = 100
costo_mantenimiento_unit = 1
costo_faltante_unit = 5

# Demanda diaria: Poisson
media_demanda = 5

# Estado del sistema
inventario = 30
dia_pedido = -1
cant_pedida = 0
costos_diarios = {
    "orden": [],
    "mantenimiento": [],
    "faltante": [],
    "total": []
}

inventario_historico = [30]

# calculo de demanda de unidades
# Primero vamos a generar 15 valores de forma aleatoria entre 1 y 8 ya que la distribucion empirica discreta se contruye a partir de un conjunto de datos observados
datos_observados = np.random.uniform(1,9,15)
# Obtener valores y frecuencias de los datos observados
valores, veces_que_salen = np.unique(datos_observados, return_counts=True)
probabilidades = veces_que_salen / sum(veces_que_salen)

#calculo arribo de personas
# Generar numeros pseudoaleatorios con distribucion de probabilidad exponencial (Usando transformada inversa)
lambd = 0.45 # Valor de LAMBDA
num_uniformes_para_exponencial = np.random.uniform(0,1,100) # num_uniformes_para_exponencial ~ U(0,1)
num_exponenciales = -np.log(1 - num_uniformes_para_exponencial) / lambd
print(num_exponenciales)

valores_t = [0]
for i in range(len(num_exponenciales)):
    valor_t = float(round(num_exponenciales[i] + valores_t[i], 4))
    valores_t.append(valor_t)

print(valores_t)

periodo = 10
periodo_actual = 0
tiempo_reposicion = -1
pedido_pendiente = 0

costo_orden_total = 0
costo_mant_total = 0
costo_falt_total = 0

for arribo in range(len(valores_t) - 1):
    valor_t = valores_t[arribo+1]
    # 1. Llegan órdenes pendientes
    if (pedido_pendiente == 1) and (valor_t >= tiempo_reposicion):
        inventario = inventario + cant_pedida
        pedido_pendiente = 0

    # 2. Demanda
    demanda_por_cliente = np.random.choice(valores, p=probabilidades)
    if demanda_por_cliente <= inventario:
        ventas = demanda_por_cliente
        producto_faltante = 0
    else:
        ventas = inventario
        producto_faltante = demanda_por_cliente - inventario
    inventario -= demanda_por_cliente

    # 3. Revisar si hay que hacer orden
    if (inventario <= R) and (pedido_pendiente == 0):
        num_reposcion_generado = np.random.uniform(1/2,1,1)
        tiempo_reposicion = valor_t + (periodo * num_reposcion_generado)
        pedido_pendiente = 1
        cant_pedida = Q - inventario
        costo_orden_total = costo_orden_total + costo_orden


    # 4. Calcular costos

    costo_mant_total = costo_mant_total + max(0, inventario * costo_mantenimiento_unit)
    costo_falt_total = costo_falt_total + (producto_faltante * costo_faltante_unit)
    costo_total = costo_orden_total + costo_mant_total + costo_falt_total

    costos_diarios["orden"].append(costo_orden_total)
    costos_diarios["mantenimiento"].append(costo_mant_total)
    costos_diarios["faltante"].append(costo_falt_total)
    costos_diarios["total"].append(costo_total)

    inventario_historico.append(inventario)


# Resultados finales
total_orden = sum(costos_diarios["orden"])
total_mant = sum(costos_diarios["mantenimiento"])
total_falt = sum(costos_diarios["faltante"])
total_total = sum(costos_diarios["total"])

print("RESULTADOS FINALES")
print(f"Costo de orden total: ${total_orden:.2f}")
print(f"Costo de mantenimiento total: ${total_mant:.2f}")
print(f"Costo de faltantes total: ${total_falt:.2f}")
print(f"Costo total: ${total_total:.2f}")

# Gráfica
plt.figure(figsize=(12,6))
plt.plot(costos_diarios["orden"], label="Costo de Orden")
plt.plot(costos_diarios["mantenimiento"], label="Costo de Mantenimiento")
plt.plot(costos_diarios["faltante"], label="Costo de Faltante")
plt.plot(costos_diarios["total"], label="Costo Total")
plt.xlabel("Indice valores T")
plt.ylabel("Costo")
plt.title("Costos del Inventario a lo Largo del Tiempo")
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(12,6))
plt.plot(valores_t, inventario_historico, label="Stock inventario")
plt.xlabel("Valor T")
plt.ylabel("Inventario")
plt.title("Stock de inventario a lo largo del tiempo")
plt.legend()
plt.grid(True)
plt.show()

