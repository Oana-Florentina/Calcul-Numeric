from random import random

import numpy as np
epsilon = 10**(-5)
# Muller
def choose_x1_x2_x3():
    return random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10)

def P(x):
    pass

def Horner():
    k = 3
    x = []
    x1, x2, x3 = choose_x1_x2_x3()
    x.append(x1)
    x.append(x2)
    x.append(x3)

    h0 = x[2] - x[1]
    h1 = x[3] - x[2]
    delta0 = (P(x[2])-P(x[1])) / h0
    delta1 = (P(x[3])-P(x[2])) / h1
    a = (delta1 - delta0) / h1 + h0
    b = a * h1 + delta1
    c = P(x[3])
    if b*b - 4*a*c < 0:
        return
    if max(abs(b + np.sqrt(b*b - 4*a*c)),(b - np.sqrt(b*b - 4*a*c))) < epsilon:
        return
    deltax = 2*c / max(b+np.sqrt(b*b-4*a*c),b-np.sqrt(b*b-4*a*c))
    x[3] = x[2]-deltax
    k+=1
    x[0]=x[1]
    x[1]=x[2]
    x[2]=x[3]
    while abs(deltax) > epsilon and k < 1000 and abs(deltax) < 10**8:
            h0 = x[2] - x[1]
            h1 = x[3] - x[2]
            delta0 = (P(x[2])-P(x[1])) / h0
            delta1 = (P(x[3])-P(x[2])) / h1
            a = (delta1 - delta0) / h1 + h0
            b = a * h1 + delta1
            c = P(x[3])
            if b*b - 4*a*c < 0:
                return
            if max(abs(b + np.sqrt(b*b - 4*a*c)),(b - np.sqrt(b*b - 4*a*c))) < epsilon:
                return
            deltax = 2*c / max(b+np.sqrt(b*b-4*a*c),b-np.sqrt(b*b-4*a*c))
            x[3] = x[2]-deltax
            k+=1
            x[0]=x[1]
            x[1]=x[2]
            x[2]=x[3]



