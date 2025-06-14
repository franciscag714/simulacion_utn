import numpy as np
import matplotlib.pyplot as plt
import sys
import os

Q = int(sys.argv[2])
R = int(sys.argv[4])
costo_orden = int(sys.argv[6])
costo_mantenimiento_unit = int(sys.argv[8])
costo_faltante_unit = int(sys.argv[10])
cant_valores_t = int(sys.argv[12])

os.system('cls')
if sys.argv[1] != '-c' or sys.argv[3] != '-n' or sys.argv[5] !='-s' or sys.argv[7] !='-m' or sys.argv[9] !='-f' or sys.argv[11] !='-t':
    print("Uso: python tp2_1.py -c <Valor maximo de inventario/default 50> -n <Punto de reorden/default 20> -s <costo orden/default 100> -m <costo_mantenimiento_unit/default 1> -f <costo_faltante_unit/default 5> -t <cant_arribos/default 100>")
    sys.exit(1)

# Estado del sistema
inventario = 30
cant_pedida = 0
costos = {
    "orden": [],
    "mantenimiento": [],
    "faltante": [],
    "total": []
}

inventario_historico = [30]


#calculo arribo de personas
# Generar numeros pseudoaleatorios con distribucion de probabilidad exponencial (Usando transformada inversa)
lambd = 0.45 # Valor de LAMBDA
num_uniformes_para_exponencial = np.random.uniform(0,1,cant_valores_t) # num_uniformes_para_exponencial ~ U(0,1)
num_exponenciales = -np.log(1 - num_uniformes_para_exponencial) / lambd

valores_t = [0]
for i in range(len(num_exponenciales)):
    valor_t = float(round(num_exponenciales[i] + valores_t[i], 4))
    valores_t.append(valor_t)

print(valores_t)

periodo = 20
tiempo_reposicion = -1
pedido_pendiente = 0 ## Bandera para saber si hay un pedido de reposicion pendiente

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
    lambd = 3 # Tasa de eventos, valor de LAMBDA
    demanda_por_cliente = np.random.poisson(lam=lambd)
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

    costos["orden"].append(costo_orden_total)
    costos["mantenimiento"].append(costo_mant_total)
    costos["faltante"].append(costo_falt_total)
    costos["total"].append(costo_total)

    inventario_historico.append(inventario)


# Resultados finales
total_orden = sum(costos["orden"])
total_mant = sum(costos["mantenimiento"])
total_falt = sum(costos["faltante"])
total_total = sum(costos["total"])

print("RESULTADOS FINALES")
print(f"Costo de orden total: ${total_orden:.2f}")
print(f"Costo de mantenimiento total: ${total_mant:.2f}")
print(f"Costo de faltantes total: ${total_falt:.2f}")
print(f"Costo total: ${total_total:.2f}")

# Gráfica
plt.figure(figsize=(12,6))
plt.plot(costos["orden"], label="Costo de Orden")
plt.plot(costos["mantenimiento"], label="Costo de Mantenimiento")
plt.plot(costos["faltante"], label="Costo de Faltante")
plt.plot(costos["total"], label="Costo Total")
plt.xlabel("Arribos")
plt.ylabel("Costo")
plt.title(f"Costos del Inventario a lo Largo del Tiempo con {cant_valores_t} arribos")
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(12,6))
plt.plot(valores_t, inventario_historico, label="Stock inventario")
plt.axhline(y=0, color='red', linestyle='--')
plt.xlabel("Tiempo T")
plt.ylabel("Inventario")
plt.title(f"Stock de inventario a lo largo del tiempo con {cant_valores_t} arribos")
plt.legend()
plt.grid(True)
plt.show()

