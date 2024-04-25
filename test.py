from new import homo
from tqdm import tqdm
import sys

limit = 1

if len(sys.argv) >= 2:
    limit = int(sys.argv[1])

def testing(fileName):
    e, d = 0, 0
    for i in tqdm(range(limit)):
        temp = homo(fileName, testing=True)
        
        e += temp[0]
        d += temp[1]

    print("Encryption:", e/limit)
    print("Decryption:", d/limit)
    
print("10KB file")
testing('input_10kb.txt')
print("20KB file")
testing('input_20kb.txt')