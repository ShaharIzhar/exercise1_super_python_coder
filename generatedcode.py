def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# Unit tests
def test_is_prime():
    assert is_prime(1) == False
    assert is_prime(2) == True
    assert is_prime(3) == True
    assert is_prime(4) == False
    assert is_prime(5) == True
    assert is_prime(9) == False
    assert is_prime(11) == True
    assert is_prime(25) == False
    assert is_prime(29) == True
    assert is_prime(-5) == False
    assert is_prime(0) == False
    assert is_prime(97) == True
    assert is_prime(100) == False
    assert is_prime(101) == True
    assert is_prime(121) == False

if __name__ == '__main__':
    test_is_prime()
    print("All tests passed.")