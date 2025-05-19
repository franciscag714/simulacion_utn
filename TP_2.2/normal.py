import math
import matplotlib.pyplot as plt
import random


def simular_normal(n):
    def densidad_normal(x, media, desvio):
        return (1 / (desvio * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((x - media) / desvio) ** 2)

    
    def densidad_uniforme(x, a, b):
        if a <= x <= b:
            return 1 / (b - a)
        else:
            return 0

    def normal_rechazo(media, desvio): #metodo de rechazo para la normal utilizando la uniforme
        a = media - 4 * desvio  #elegimos 4 porque el 99% de los valores en una distribucion normal se encuentran en: media +- desvio * 4
        b = media + 4 * desvio

        fx_max = densidad_normal(media, media, desvio) #evaluamos la funcion densidad en x = media que es donde se produce su maximo
        gx = 1 / (b - a)
        c = fx_max / gx  #formula metodo rechazo

        while True: #corta cuando encuentra un return
            x = random.uniform(a, b)      # x ~ g(x)
            u = random.uniform(0, 1)      # u ~ U(0,1)
            fx = densidad_normal(x, media, desvio)
            gx = densidad_uniforme(x, a, b)

            if u < fx / (c * gx):
                return x

                
    
