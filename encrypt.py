def Encryption(s):
    enclist=[48,99,55,54,91,79,122,109,78,68,44,77,120,34,70,53,73,40,72,41,123,61,51,64,87,81,126,117,96,80,39,66,60,76,88,98,52,86,124,42,105,65,121,58,38,95,69,63,59,92,119,43,125,89,67,50,46,83,113,45,107,85,104,74,114,62,84,118,100,97,112,93,35,71,103,36,106,57,115,90,110,108,75,47,49,82,116,37,94,111,101,33,102,56]
    encstr=""
    for i in s:
        encstr=encstr+chr(enclist[ord(i)-33])
    return encstr


def Decryption(p):
    declist=[124,46,105,108,120,77,63,50,52,72,84,43,92,89,116,33,117,88,55,69,48,36,35,126,110,76,81,65,54,98,80,56,74,64,87,42,79,47,106,51,49,96,115,66,44,41,38,62,58,118,90,99,94,70,57,67,86,112,37,82,104,121,78,61,102,68,34,101,123,125,107,95,73,109,93,114,40,113,122,103,91,97,111,119,60,100,83,45,75,39,53,71,85,59]
    decstr=""
    for i in p:
        decstr=decstr+chr(declist[ord(i)-33])
    return decstr


print("Enter the string to Encrypt and decrypt : ")
s=input()
print("Encrypted String : ",Encryption(s))
p = Encryption(s)
print("Decrypted String : ",Decryption(p))
