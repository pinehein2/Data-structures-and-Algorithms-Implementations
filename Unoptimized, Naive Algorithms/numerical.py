import random

def karatsuba(x , y):
    if x < 10 or y < 10:
        return x * y
    else:
        n = max(len(str(x)), len(str(y)))
        half = n//2
        a = x // (10 ** (half))
        b = x % (10 ** (half))
        c = y // (10 ** (half))
        d = y % (10 ** (half))
        ac = karatsuba(a, c)
        bd = karatsuba(b, d)
        adbc = karatsuba(a+b, c+d) - ac - bd
        return ac * (10 ** (2 * half)) + (adbc * (10 ** half)) + bd


def miller_rabin(num):
    """
    Determines if a number is possibly a prime
    """
    def randomized_primality(num):
        """
        Determines if a number is possibly a prime for odd numbers greater than 3
        """
        k = 64 #Number of tests
        s = 0
        t = num - 1
        while t % 2 == 0:
            s = s + 1
            t = t//2
        for _ in range(k):
            a = random.randint(2,num-2)
            x = pow(a, t, num)
            if x == 1: #Case 4
                continue
            for _ in range(1, s):
                prev = x
                x = pow(x, x, num)
                if x == 1:
                    if prev != num-1: #Case 3
                        return True
                    else: #Case 2
                        x = 1
                        break
            if x != 1 % num: #Case 1
                return True #Definitely a prime
        return False #Needs more testing to be 100% sure
    
    if num % 2 == 1 and num > 3: #Input must be an odd number greater than 3
        return randomized_primality(num)
    if num == 2 or num == 3: #2 and 3 are prime
        return True
    return False #Incase of 1 and lower


print(karatsuba(13445,3245))