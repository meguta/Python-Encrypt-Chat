class Encrypter:
    eng = [
            #Lowercase letters
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',

            #Uppercase letters
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',

            #Puncuation characters
            '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_',
            '=', '+', '[', ']', '{', '}', '\\', '|', ';', ':', '\'', '\"',
            ',', '<', '.', '>', '/', '?', ' '
    ]
    engSize = 84
    def __init__(self):
        pass
    
    def keyDecode(self, key, oldKey):
        tmp = key[0]

        i = 0
        while i != len(key):
            if key[i] == key[4]:
                key[i] = oldKey + tmp
            else:
                key[i] = oldKey[i] + oldKey[i + 1]
            i += 1
            return key


    def keyEncode(self, key):
        tmp = key[0]

        i = 0
        while i != len(key):
            if (key[i] == key[4]):
                key[i] = key[i] + tmp
            else:
                key[i] = key[i] + key[i + 1]
            i += 1
        return key

    def msgDecode(self, key, message):
        newMessage = ''
        arrCnt = 0
        
        for elem in message:
            matches = 0
            
            c = 0
            while c < self.engSize:
                if (elem == self.eng[c]):
                    letter = c - key[arrCnt]
                    if (letter >= self.engSize - 1):
                        matches += 1
                        if (arrCnt == 4):
                            newMessage += self.eng[letter]
                            arrCnt = 0
                        else:
                            newMessage += self.eng[letter]
                            arrCnt += 1
                    else:
                        letter = self.wrapping(True, self.engSize, letter)
                        matches += 1
                        if(arrCnt == 4):
                            newMessage += self.eng[letter]
                            arrCnt = 0
                        else:
                            newMessage += self.eng[letter]
                            arrCnt += 1
                c += 1
            if (matches == 0):
                if (arrCnt == 4):
                    newMessage += elem
                    arrCnt = 0
                else:
                    newMessage += elem
                    arrCnt += 1
            
        return newMessage 

    def msgEncode(self, key, message):
        newMessage = ''
        arrCnt = 0
        
        for elem in message:
            matches = 0
            
            c = 0
            while c < self.engSize:
                if (elem == self.eng[c]):
                    letter = c + key[arrCnt]
                    if (letter <= self.engSize - 1):
                        matches += 1
                        if (arrCnt == 4):
                            newMessage += self.eng[letter]
                            arrCnt = 0
                        else:
                            newMessage += self.eng[letter]
                            arrCnt += 1
                    else:
                        letter = self.wrapping(True, self.engSize, letter)
                        matches += 1
                        if(arrCnt == 4):
                            newMessage += self.eng[letter]
                            arrCnt = 0
                        else:
                            newMessage += self.eng[letter]
                            arrCnt += 1
                c += 1
            if (matches == 0):
                if (arrCnt == 4):
                    newMessage += elem
                    arrCnt = 0
                else:
                    newMessage += elem
                    arrCnt += 1
            
        return newMessage



    def wrapping(self, encrypting, size, x):
        if encrypting:
            return x % size
        else:
            if size >= 0:
                return x
            else:
                return x + size

