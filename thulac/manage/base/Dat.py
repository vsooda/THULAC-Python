#! /usr/bin/env python2.7
#coding=utf-8
import struct
import os


class Dat:

    def __init__(self, filename):
        inputfile = open(filename, "rb")
        
        self.datSize = os.path.getsize(filename) / 8
        print self.datSize
        s = inputfile.read(8 * self.datSize)
        tmp = "<"+str(self.datSize*2)+"i"
        self.dat = struct.unpack(tmp, s)
        self.dat = tuple(self.dat)
        inputfile.close()
        self.crack_name = os.path.join("thulac/crack_models", os.path.basename(filename))
        #self.crack()
        #self.crack_with_prefix()


    def do_crack(self, depth, base, data_size, word):
        depth = depth + 1
        ind = base * 2
        if base > data_size or depth > 8:
            return word
        else:
            for j in xrange(1, data_size):
                index = self.dat[ind] + j
                if index < data_size and self.dat[2 * index + 1] == base:
                    #print index, base, unichr(j), j
                    word = word + unichr(j)
                    base = index
                    return self.do_crack(depth, base, data_size, word)
                else:
                    continue
            return word

    def crack(self):
        self.crack_fid = open(self.crack_name, 'w')
        data_size = self.datSize
        for i in xrange(1, data_size):
            if self.dat[i*2+1] == 0: #begin word
                word = unichr(i)
                base = i
                result = self.do_crack(1, base, data_size, word)
                #print result
                self.crack_fid.write(result+"\n")
        self.crack_fid.close()

    def crack_with_prefix(self):
        prefix = "旧事重".decode('utf8')
        ind = 0
        base = 0
        for i in range(len(prefix)):
            ind = self.dat[2 * ind] + ord(prefix[i])
            base = ind
            print ind
            if ind > self.datSize and self.dat[2 * ind + 1] == base:
                break
        ind = ind * 2


        result = self.do_crack(2, base, self.datSize, prefix)
        print result


    
    def printDat(self, filename):
        f = open(filename, "w")
        for i in xrange(self.datSize):
            f.write(""+self.dat[2 * i]+" "+self.dat[2 * i + 1]+"\n")
        f.close()
    
    def getIndex(self, base, character):
        ind = self.dat[2 * base] + character
        if((ind >= self.datSize) or self.dat[2 * ind + 1] != base):
            return -1
        return ind
    
    def search(self, sentence, bs, es):
        bs = []
        es = []
        empty = True
        for offset in range(len(sentence)):
            preBase = 0
            preInd = 0
            ind = 0
            for i in range(offset, len(sentence)):
                ind = preBase + sentence[i]
                if(ind < 0 or ind >= self.datSize or self.dat[2 * ind + 1] != preInd):
                    break
                preInd = ind
                preBase = self.dat[2 * ind]
                ind = preBase
                if(not (ind < 0 or ind >= self.datSize or self.dat[2 * ind + 1] != preInd)):
                    bs.append(offset)
                    es.append(i + 1)
                    if(empty):
                        empty = False
        return not empty
    
    def match(self, word):
        ind = 0
        base = 0
        for i in range(len(word)):
            ind = self.dat[2 * ind] + ord(word[i])
            if((ind > self.datSize) or (self.dat[2 * ind + 1] != base)):
                return -1
            base = ind
        ind = self.dat[2 * base]
        if((ind < self.datSize) and (self.dat[2 * ind + 1] == base)):
            return ind
        return -1

    def update(self, word, value):
        base = self.match(word)
        if(base >= 0):
            self.dat[2 * base] = value

    def getInfo(self, prefix):
        ind = 0
        base = 0
        for i in range(len(prefix)):
            data = self.dat[2*ind]
            ind = self.dat[2 * ind] + ord(prefix[i])
            print prefix[i], ord(prefix[i]), data, ind, self.dat[2*ind+1], base
            if((ind >= self.datSize) or self.dat[2 * ind + 1] != base):
                return i
            base = ind
        return -base

    def getDatSize(self):
        return self.datSize
    
    def getDat(self):
        return self.dat

if __name__ == '__main__':
    dat = Dat("thulac/models/idiom.dat")
    #dat = Dat("thulac/models/ns.dat")

        
