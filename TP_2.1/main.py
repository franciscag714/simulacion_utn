from generadores import RandomGeneratorGLC, MiddleSquare, FibonacciGenerator, LehmerGenerator;
from tests import ChiSquaredUniformityTest,MediumTest, PatternTest, SumTest;
import matplotlib.pyplot as plt   
import random
import time

def graficar(valores, titulo):
   chi_test = ChiSquaredUniformityTest(valores)
   med_test = MediumTest(valores)
   pat_test = PatternTest(valores)
   sum_test = SumTest(valores)

   print("Chi-Cuadrado:", chi_test.run_test())
   print("Medium Test:", med_test.run_test())
   print("Sumatoria Test:", sum_test.run_test())

   fig, axs = plt.subplots(2, 2, figsize=(14, 8))
   fig.suptitle(titulo, fontsize=16)
   chi_test.plot(axs[0, 0])
   med_test.plot(axs[0, 1])
   pat_test.plot(axs[1, 0])
   sum_test.plot(axs[1, 1])

   plt.tight_layout()
   plt.show()


def main ():
   valores_rgn = []
   valores_ms = []
   valores_fg = []
   valores_lg = []
   valores_py = []
   seed = None

   seed_input = input("Ingrese la semilla o presione ENTER para usar la hora del sistema (Minimo de 10 caracteres): ")

   if not seed_input: 
      seed_input = None

   if seed_input is not None:
      while (int(seed_input) <= 999999999):
         seed_input = input("Ingrese la semilla o presione ENTER para usar la hora del sistema (Minimo de 10 caracteres): ")
         if seed_input.strip():
            try:
               seed = int(seed_input)
            except ValueError:
               print("La semilla debe ser un Numero Entero y tener 10 digitos o mas")
               return 
         else: 
            seed = None


   rgn = RandomGeneratorGLC(seed)
   ms = MiddleSquare(seed)
   lg = LehmerGenerator(seed)

   if seed is not None:
        fg = FibonacciGenerator(seed, (seed + 1) % 10000) 
   else:
        fg = FibonacciGenerator()  

   for _ in range(10000):
      rgn.next()
      ms.next()
      fg.next()
      lg.next()
      valores_rgn.append(rgn.capear())
      valores_ms.append(ms.capear())
      valores_fg.append(fg.capear())
      valores_lg.append(lg.capear())
      valores_py.append(random.uniform(0, 1))

   for j in range(5):
      if j == 0:
         graficar(valores_rgn, 'Random Generator')
         pass
      elif j == 1:   
         graficar(valores_ms, 'Middle Square')
         pass
      elif j == 2:
         graficar(valores_fg, 'Fibonacci Generator')
         pass
      elif j == 3:
         graficar(valores_lg, 'Lehmer Generator') 
         pass
      elif j == 4:
         graficar(valores_py, 'Python Random')


main()
