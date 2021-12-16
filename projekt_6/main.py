import time
from statistics import mean

def timeit(rep = 1):
    def decorator(func):
        def inner(n):
            times = []
            for i in range(rep):
                start_time = time.time()
                result = func(n)
                elapsed_time = time.time() - start_time
                times.append(int(elapsed_time * 1_000))
                print('function [{}] finished in {} ms'.format(
                    func.__name__, int(elapsed_time * 1_000)))
                print('Average time: {}'.format(mean(times)))
            return result
        return inner
    return decorator

@timeit()
def prime_factors(n):
        i = 2
        factors = []
        while i * i <= n:
            if n % i:
                i += 1
            else:
                n //= i
                factors.append(i)
        if n > 1:
            factors.append(n)
        return factors

prime_factors(31415926535897932384626)