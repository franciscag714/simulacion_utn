from generadores import RandomGeneratorGLC, MiddleSquare, FibonacciGenerator, LehmerGenerator;
from tests import chi_squared_uniformity_test, fourier_transform_test, medium_test, pattern_test;   

def main ():
   valores = []
   seed_input = input("Ingrese la semilla o presione ENTER para usar la hora del sistema: ")
   if seed_input.strip():
      try:
         seed = int(seed_input)
      except ValueError:
         print("La semilla debe ser un Numero Entero")
         return 
   else: 
      seed = None
   rgn = RandomGeneratorGLC(seed)

   for _ in range(10000):
      rgn.next()
      valores.append(rgn.capear())

   #chi_squared_uniformity_test(valores, num_bins=10, show_plot=True)
   #medium_test(valores)
   #pattern_test(valores)
   #fourier_transform_test(valores)


main()
