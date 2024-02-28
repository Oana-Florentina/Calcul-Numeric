def find_u():
    m = 0
    u = 0
    while True:
        if 10 ** (-m) == 0:
            print("Valoarea lui u cu zecimale:", '{0:.1000f}'.format(u))
            print("Valoarea lui u:", u)
            print("Valoarea lui u urmator:", 10**(-m)+1)
            print("Valaorea lui m:", m)
            return u
        else:
            u = 10 ** (-m)
        m += 1

find_u()



