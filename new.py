import random
import time
from affine import affine_decrypt, affine_encrypt

# Key generation
def generate_key(bit_length):
    p = generate_prime(bit_length)
    q = generate_prime(bit_length)
    
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = random.randint(2**(bit_length-1), phi_n - 1)
    gcd, d, _ = extended_gcd(e, phi_n)
    
    while gcd != 1:
        e = random.randint(2**(bit_length-1), phi_n - 1)
        gcd, d, _ = extended_gcd(e, phi_n)

    if d < 0:
        d += phi_n
    
    return n, e, d

# Encryption
def encrypt(plaintext, n, e):
    return pow(plaintext, e, n)

# Decryption
def decrypt(ciphertext, n, d):
    return pow(ciphertext, d, n)

# Homomorphic addition for each digit
def homomorphic_add(Messages, n):
    result = 1
    for i in Messages:
        result = (result * i) % n
    return result

# Helper functions for prime generation and extended gcd
def generate_prime(bit_length):
    while True:
        number = random.randint(2**(bit_length-1), 2**bit_length - 1)
        if is_prime(number):
            return number

def normal_gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Extended euclidean algorithm.
def extended_gcd(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1

    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1

    return a, x0, y0

# Optimized is_prime function
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


def concatenate_strings(line, n, e, d, encryption, decryption):

    affine_encrypt_line = [affine_encrypt(char, e, d) for char in line]
    print("a: ","".join(affine_encrypt_line))

    # Encode strings into numeric values
    encoded_str1 = [ord(char) for char in affine_encrypt_line]

    # Encrypt each character of the strings
    start = time.time()
    encrypted_str1 = [encrypt(char, n, e) for char in encoded_str1]
    end = time.time()
    print("e: ","".join(map(str, encoded_str1)))
    encryption += end-start
    encrypted_one = encrypt(1, n, e)

    # Perform homomorphic addition
    result_encoded = [homomorphic_add([pair, encrypted_one], n) for pair in encrypted_str1]
    print("H: ", "".join(map(str, result_encoded)))

    # Decrypt the result back into characters
    start = time.time()
    decrypted_str = [decrypt(val, n, d) for val in result_encoded]
    end = time.time()
    print("D: ", "".join(map(str, decrypted_str)))
    decryption += end-start

    # print("Decrypted Result:", decrypted_str)

    # Convert decrypted characters to string
    concatenated_str = ''.join(chr(char) for char in decrypted_str)
    concatenated_str = ''.join(affine_decrypt(char, e, d) for char in concatenated_str)

    return [concatenated_str.strip('\0'), encryption, decryption]


def homo(fileName, testing=False):
    
    start = time.time()
    
    # Generate RSA keys with 80-bit length
    n, e, d = generate_key(10)

    if(not testing):
        print("---Homomorphic String Concatenation---")
        print("n:", n)
        print("e:", e)
        print("d:", d)

        print("\nProcessing started")

    encryption = 0
    decryption = 0
    result_str = ""
    count = 0

    with open(fileName, 'r') as file:
        for line in file:
            count += 1
            concatenated_str, encryption, decryption = concatenate_strings(line, n, e, d, encryption, decryption)
            result_str += concatenated_str
            print(f"line {count}: done") if (not testing) else None
    
    end = time.time()

    if(not testing):
        print("Result_str:", result_str)
        print("\nEncryption time:", encryption)
        print("Decryption time:", decryption)
        print("Time taken: ", end - start)
    return [encryption, decryption]

# Main
if __name__ == '__main__':
    homo('text.txt')
