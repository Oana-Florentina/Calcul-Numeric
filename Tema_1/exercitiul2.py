

def find_u():
    m = 0
    u = 0
    while True:
        if 1+ 10 ** (-m) == 1:
            print("Valoarea lui u cu zecimale:", '{0:.1000f}'.format(u))
            print("Valoarea lui u:", u)
            print("Valoarea lui u urmator:", 10**(-m)+1)
            print("Valaorea lui m:", m-1)
            return u
        else:
            u = 10 ** (-m)
        m += 1

def verify_operation_plus():

    x = 1.0
    u = find_u()
    y = u / 10
    z = u / 10
    result1 = (x + y) + z
    result2 = x + (y + z)
    print("Rezultatul 1:", result1)
    print("Rezultatul 2:", result2)

    return x, y, z, result1 != result2



print(verify_operation_plus())


def verify_operation_multiply(x, y, z):

    return (x * y) * z != x * (y * z)

print(verify_operation_multiply(0.4, 0.2, 0.3))
