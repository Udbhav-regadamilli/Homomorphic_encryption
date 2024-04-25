import random, time

# Key generation
def generate_key():
    p = generate_prime()
    q = generate_prime()
    
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = random.randint(3, phi_n-1)
    gcd, d, _ = extended_gcd(e, phi_n)
    
    while gcd != 1:
        e = random.randint(3, phi_n-1)
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

# Homomorphic addition
def homomorphic_mul(Messages, n):
    temp = 1
    for i in Messages:
        temp *= i
    return temp % n if temp > n else temp

# Helper functions for prime generation and extended gcd
def generate_prime():
    while True:
        number = random.randint(1000000000000, 500000000000000)
        if is_prime(number):
            return number

def normal_gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

#Extended euclidean algorithm.
def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return (gcd, y - (b // a) * x, x)

def modinv(a, m):
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError('Modular inverse does not exist')
    else:
        return x % m

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

# Homomorphic addition for each digit
def homomorphic_add(Messages, n):
    result = 1
    for i in Messages:
        result = (result * i) % n
    return result

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

def concatenate_strings(line, n, e, d, encryption, decryption):

    affine_encrypted_line = [affine_encrypt(char, e, d) for char in line]

    # Encode strings into numeric values
    encoded_str1 = [ord(char) for char in affine_encrypted_line]

    # Encrypt each character of the strings
    start = time.time()
    encrypted_str1 = [encrypt(char, n, e) for char in encoded_str1]
    end = time.time()
    encryption += end-start
    encrypted_one = encrypt(1, n, e)

    # Perform homomorphic addition
    result_encoded = [homomorphic_add([pair, encrypted_one], n) for pair in encrypted_str1]

    # Decrypt the result back into characters
    start = time.time()
    decrypted_str = [decrypt(val, n, d) for val in result_encoded]
    end = time.time()
    decryption += end-start

    # print("Decrypted Result:", decrypted_str)

    # Convert decrypted characters to string
    concatenated_str = ''.join(chr(char) for char in decrypted_str)
    concatenated_str = ''.join(affine_decrypt(char, e, d) for char in concatenated_str)
    
    encrypted_text = ''.join(str(int) for int in result_encoded)

    return [''.join(chr(char) for char in encoded_str1), concatenated_str.strip('\0'), encryption, decryption, encrypted_text.strip('\0')]

def homo():
    times = []
    messages = [10, 20]

    # for i in range(5):
    #     messages.append(random.randint(1, 10))

    start = time.time()
    
    n, e, d = generate_key()

    # Encrypt the messages
    ciphertexts = []

    for i in messages:
        ciphertexts.append(encrypt(i, n, e))

    # Perform homomorphic addition
    result_ciphertext = homomorphic_mul(ciphertexts, n)

    # Decrypt the result
    decrypted_result = decrypt(result_ciphertext, n, d)

    end = time.time()

    print("---Homomorphic with extendedGCD---")
    print("Messages:", messages)
    print("ciphertexts:",ciphertexts)
    print("Homomorphically Multiplied Ciphertext:", result_ciphertext)
    print("Decrypted Result:", decrypted_result)
    print("Time taken: ",end-start)
    times.append(end-start)

    #Without extended eculidean
    start = time.time()
    
    n, e, d = generate_key(extendedGCD=False)

    # Encrypt the messages
    ciphertexts = []

    for i in messages:
        ciphertexts.append(encrypt(i, n, e))

    # Perform homomorphic addition
    result_ciphertext = homomorphic_mul(ciphertexts, n)

    # Decrypt the result
    decrypted_result = decrypt(result_ciphertext, n, d)

    end = time.time()

    print("\n---Homomorphic without extendedGCD---")
    print("Messages:", messages)
    print("ciphertexts:",ciphertexts)
    print("Homomorphically Multiplied Ciphertext:", result_ciphertext)
    print("Decrypted Result:", decrypted_result)
    print("Time taken: ",end-start)
    times.append(end-start)


    print("\nExisting System: ", times[1])
    print("Proposed System: ", times[0])
    return times

# Main
if __name__ == '__main__':
    homo()