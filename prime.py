def is_prime(n):
    if n <= 1 or (n % 2 == 0 and n > 2):
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


n = 88162
while not is_prime(n):
    n += 1

print(f"大於 88000 的第一個質數為：{n}")
