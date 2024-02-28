def find_u():
    m = 0
    u = 0
    while True:
        if 10 ** (-m) <= 0:
            print("Valoarea lui u:", '{0:.1000f}'.format(u))
            print("Valoarea lui u urmator:", 10**(-m)+1)
            print("Valaorea lui m:", m)
            break
        else:
            u = 10 ** (-m)
        m += 1

find_u()