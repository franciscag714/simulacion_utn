import random
import sys 

# Creacion de variables aleatorias
valores = []
ganadas = [],[]
frec_relativa_num_elegido = 0

# Verificar si se proporciona el número de valores como argumento
if len(sys.argv) != 7 or sys.argv[1] != "-c" or sys.argv[3] != "-n" or sys.argv[5] != "-e" or int(sys.argv[6]) > 36 or int(sys.argv[6]) < 0:
    print("Uso: python ruleta.py -c <num_tiradas> -n <num_corridas> -e <num_elegido>")
    sys.exit(1)

# Obtener el número de valores de los argumentos de la línea de comandos
num_tiradas = int(sys.argv[2])
num_corridas = int(sys.argv[4])
num_elegido = int(sys.argv[6])
print(num_tiradas, num_corridas, num_elegido)

# Generar los valores aleatorios entre 0 y 36 y almacenarlos en una lista
for i in range(num_corridas):

  print("Corrida numero", i + 1)
  for j in range(num_tiradas):
      valor = random.randint(0, 36)
      if (valor == num_elegido):
          print("El numero elegido", num_elegido,  "tuvo acierto en la tirada numero", j + 1)
          ganadas[0].append(j+1)
          ganadas[1].append(i+1)
          
    
      valores.append(valor)
      print("Numero de tirada numero", j + 1, ":", valor)
  print("---------------------------------------------")  

print(ganadas)
print(len(ganadas[0]))
print("El numero elegido", num_elegido, "fue acertado", len(ganadas[1]), "veces en", num_corridas, "corridas")
print("Cantidad de tiradas:", num_tiradas * num_corridas)
print("La frecuencia relativa del numero elegido es", (len(ganadas[1])/(num_corridas*num_tiradas)))

