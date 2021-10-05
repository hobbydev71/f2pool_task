import os
import datetime
import hashlib
def reverse(input):
    L = len(input)
    if (L % 2) != 0:
        return None
    else:
        Res = ''
        L = L // 2
        for i in range(L):
            T = input[i*2] + input[i*2+1]
            Res = T + Res
            T = ''
        return (Res)

def merkle_root(lst):
    sha256d = lambda x: hashlib.sha256(hashlib.sha256(x).digest()).digest()
    hash_pair = lambda x, y: sha256d(x[::-1] + y[::-1])[::-1]
    if len(lst) == 1: return lst[0]
    if len(lst) % 2 == 1:
        lst.append(lst[-1])
    return merkle_root([hash_pair(x,y) for x, y in zip(*[iter(lst)]*2)])

def read_varint(file):
    b = file.read(1)
    bInt = int(b.hex(),16)
    c = 0
    data = ''
    if bInt < 253:
        c = 1
        data = b.hex().upper()
    if bInt == 253: c = 3
    if bInt == 254: c = 5
    if bInt == 255: c = 9
    for j in range(1,c):
        b = file.read(1)
        b = b.hex().upper()
        data = b + data
    return data
    
def read_bytes(file,n,byte_order = 'L'):
    data = file.read(n)
    if byte_order == 'L':
        data = data[::-1]
    data = data.hex().upper()
    return data

dirInput = '/home/daniel/Desktop/Project/experiment/' 
dirOutput = '/home/daniel/Desktop/Project/experiment_out/' 
fList = os.listdir(dirInput)
fList = [x for x in fList if (x.endswith('.dat') and x.startswith('blk'))]
fList.sort()
stackHeight = 0
moreThanTwoHourCount = 0
previousHexTime = "495FAB29" 
for i in fList:
    srcLink = i
    resLink = srcLink.replace('.dat','.txt')
    resList = []
    a = 0
    t = dirInput + srcLink
    
    print ('Start ' + t + ' in ' + str(datetime.datetime.now()))
    f = open(t,'rb')
    temp = ''
    fSize = os.path.getsize(t)
    while f.tell() != fSize:
        temp = read_bytes(f,4)
        
        temp = read_bytes(f,4)
        
        tmpPos3 = f.tell()
        temp = read_bytes(f,80,'B')
        temp = bytes.fromhex(temp)
        temp = hashlib.new('sha256', temp).digest()
        temp = hashlib.new('sha256', temp).digest()
        temp = temp[::-1]        
        temp = temp.hex().upper()
        
        f.seek(tmpPos3,0)
        temp = read_bytes(f,4)
        
        temp = read_bytes(f,32)
        
        temp = read_bytes(f,32)
        
        MerkleRoot = temp
        
        temp = read_bytes(f,4)
        
        stackHeight = stackHeight + 1
        if (int(temp, 16) - int(previousHexTime, 16) > 7200):
            moreThanTwoHourCount = moreThanTwoHourCount + 1
            
            
        previousHexTime = temp
        temp = read_bytes(f,4)
        
        temp = read_bytes(f,4)
        
        temp = read_varint(f)
        txCount = int(temp,16)
        
        
        temp = ''; RawTX = ''; tx_hashes = []
        for k in range(txCount):
            temp = read_bytes(f,4)
            
            RawTX = reverse(temp)
            temp = ''
            Witness = False
            b = f.read(1)
            tmpB = b.hex().upper()
            bInt = int(b.hex(),16)
            if bInt == 0:
                tmpB = ''
                f.seek(1,1)
                c = 0
                c = f.read(1)
                bInt = int(c.hex(),16)
                tmpB = c.hex().upper()
                Witness = True
            c = 0
            if bInt < 253:
                c = 1
                temp = hex(bInt)[2:].upper().zfill(2)
                tmpB = ''
            if bInt == 253: c = 3
            if bInt == 254: c = 5
            if bInt == 255: c = 9
            for j in range(1,c):
                b = f.read(1)
                b = b.hex().upper()
                temp = b + temp
            inCount = int(temp,16)
            
            temp = temp + tmpB
            RawTX = RawTX + reverse(temp)
            for m in range(inCount):
                temp = read_bytes(f,32)
                
                RawTX = RawTX + reverse(temp)
                temp = read_bytes(f,4)                
                
                RawTX = RawTX + reverse(temp)
                temp = ''
                b = f.read(1)
                tmpB = b.hex().upper()
                bInt = int(b.hex(),16)
                c = 0
                if bInt < 253:
                    c = 1
                    temp = b.hex().upper()
                    tmpB = ''
                if bInt == 253: c = 3
                if bInt == 254: c = 5
                if bInt == 255: c = 9
                for j in range(1,c):
                    b = f.read(1)
                    b = b.hex().upper()
                    temp = b + temp
                scriptLength = int(temp,16)
                temp = temp + tmpB
                RawTX = RawTX + reverse(temp)
                temp = read_bytes(f,scriptLength,'B')
                
                RawTX = RawTX + temp
                temp = read_bytes(f,4,'B')
                
                RawTX = RawTX + temp
                temp = ''
            b = f.read(1)
            tmpB = b.hex().upper()
            bInt = int(b.hex(),16)
            c = 0
            if bInt < 253:
                c = 1
                temp = b.hex().upper()
                tmpB = ''
            if bInt == 253: c = 3
            if bInt == 254: c = 5
            if bInt == 255: c = 9
            for j in range(1,c):
                b = f.read(1)
                b = b.hex().upper()
                temp = b + temp
            outputCount = int(temp,16)
            temp = temp + tmpB
            
            RawTX = RawTX + reverse(temp)
            for m in range(outputCount):
                temp = read_bytes(f,8)
                Value = temp
                RawTX = RawTX + reverse(temp)
                temp = ''
                b = f.read(1)
                tmpB = b.hex().upper()
                bInt = int(b.hex(),16)
                c = 0
                if bInt < 253:
                    c = 1
                    temp = b.hex().upper()
                    tmpB = ''
                if bInt == 253: c = 3
                if bInt == 254: c = 5
                if bInt == 255: c = 9
                for j in range(1,c):
                    b = f.read(1)
                    b = b.hex().upper()
                    temp = b + temp
                scriptLength = int(temp,16)
                temp = temp + tmpB
                RawTX = RawTX + reverse(temp)
                temp = read_bytes(f,scriptLength,'B')
                
                
                RawTX = RawTX + temp
                temp = ''
            if Witness == True:
                for m in range(inCount):
                    temp = read_varint(f)
                    WitnessLength = int(temp,16)
                    for j in range(WitnessLength):
                        temp = read_varint(f)
                        WitnessItemLength = int(temp,16)
                        temp = read_bytes(f,WitnessItemLength)
                        
                        temp = ''
            Witness = False
            temp = read_bytes(f,4)
            
            RawTX = RawTX + reverse(temp)
            temp = RawTX
            temp = bytes.fromhex(temp)
            temp = hashlib.new('sha256', temp).digest()
            temp = hashlib.new('sha256', temp).digest()
            temp = temp[::-1]
            temp = temp.hex().upper()
            
            tx_hashes.append(temp)
            
        a += 1
        tx_hashes = [bytes.fromhex(h) for h in tx_hashes]
        temp = merkle_root(tx_hashes).hex().upper()
        if temp != MerkleRoot:
            print ('Merkle roots does not match! >',MerkleRoot,temp)
    f.close()
    f = open(dirOutput + resLink,'w')
    
    
    f.write(str(stackHeight) + ", " + str(moreThanTwoHourCount) + '\n')    
    f.close()
f = open(dirOutput + resLink, 'a')
f.write("At stack height " + str(stackHeight) + " there are ")
f.close()