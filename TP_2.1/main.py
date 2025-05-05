from generadores import RandomGeneratorGLC


def main ():
  seed_input = input("Ingrese la semilla o presione ENTER para usar la hora del sistema")
  if seed_input.strip():
    try:
       seed = int(seed_input)
    except ValueError:
       print("La semilla debe ser un Numero Entero")
       return 
  else: 
     seed = None
  
  rgn = RandomGeneratorGLC(seed)

  for i in range(10):
     print(rgn.next())

main()
       