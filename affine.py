import random

def generate_key(extendedGCD=True):
    p = generate_prime()
    q = generate_prime()
    # print("\nP:", p)
    # print("q:", q)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = random.randint(3, phi_n-1)

    if(extendedGCD):
        gcd, d, _ = egcd(e, phi_n)
        while gcd != 1:
            e = random.randint(3, phi_n-1)
            gcd, d, _ = egcd(e, phi_n)

    if d < 0:
        d += phi_n
        
    return n, e, d

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = egcd(b % a, a)
        return g, y - (b // a) * x, x

def modinv(a, b):
    g, x, y = egcd(a, b)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % b

def affine_encrypt(plain_text, a, b):
    result = ""
    for char in plain_text:
        if char.isalnum():
            if char.isupper():
                result += chr((a * (ord(char) - ord('A')) + b) % 26 + ord('A'))
            elif char.islower():
                result += chr((a * (ord(char) - ord('a')) + b) % 26 + ord('a'))
            else:
                result += chr((a * (ord(char) - ord('0')) + b) % 10 + ord('0'))
        else:
            result += char
    return result

def affine_decrypt(cipher_text, a, b):
    result = ""
    for char in cipher_text:
        if char.isalnum():
            if char.isupper():
                a_inv = modinv(a, 26)
                result += chr((a_inv * (ord(char) - ord('A') - b)) % 26 + ord('A'))
            elif char.islower():
                a_inv = modinv(a, 26)
                result += chr((a_inv * (ord(char) - ord('a') - b)) % 26 + ord('a'))
            else:
                a_inv = modinv(a, 10)
                result += chr((a_inv * (ord(char) - ord('0') - b)) % 10 + ord('0'))
        else:
            result += char
    return result

def generate_prime():
    while True:
        number = random.randint(1000000000000, 50000000000000)
        if is_prime(number):
            return number
        
def is_prime(number):
    if number < 2:
        return False
    
    if number == 2:
        return True

    if number % 2 == 0:
        return False

    for i in range(3, int(number**0.5) + 1, 2):
        if number % i == 0:
            return False
    return True

if __name__ == '__main__':
    # Example usage:
    text = input("Enter your message: ")
    n, m, k = generate_key()

    print("m:", m)
    print("k:", k)

    encrypted_text = affine_encrypt(text, m, k)
    print("Encrypted Text:", encrypted_text)

    decrypted_text = affine_decrypt(encrypted_text, m, k)
    print("Decrypted Text:", decrypted_text)

