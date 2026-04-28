import math

def sieve(n):
    if n < 2:
        return [], []

    # --- Sieve of Eratosthenes ---
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(math.sqrt(n)) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False

    primes = [i for i in range(2, n + 1) if is_prime[i]]

    # --- Integers relatively prime to n ---
    # Find prime factors of n
    temp = n
    prime_factors_of_n = set()
    for p in primes:
        if p * p > temp:
            break
        if temp % p == 0:
            prime_factors_of_n.add(p)
            while temp % p == 0:
                temp //= p
    if temp > 1:
        prime_factors_of_n.add(temp)

    # Eliminate multiples of those prime factors
    relatively_prime = [
        i for i in range(1, n)
        if not any(i % p == 0 for p in prime_factors_of_n)
    ]

    return primes, relatively_prime


if __name__ == "__main__":
    n = 30
    primes, rel_prime = sieve(n)
    print(f"Primes up to {n}: {primes}")
    print(f"Integers relatively prime to {n}: {rel_prime}")