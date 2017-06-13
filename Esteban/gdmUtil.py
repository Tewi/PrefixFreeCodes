from heapq import *
import math
import re


def getAlpha(weights, D=2):
    signature = getEISignature(weights, D)
    return len(re.findall(r'E+', signature)) #number of E..E blocks in the signature

def getEISignature(weights, D=2):
    N = len(weights)
    # Degenerated cases
    if D < 2:
        raise Exception("Output alphabet must have at least 2 symbols")
    if N == 0:
        return ""
    if N == 1:
        return "E"
    return DaryHuffmanCodeTree(weights, D).EI



"""
Given an unsorted list of of at least two weights, return a D-ary code tree
of minimal redundancy according to Huffman's's algorithm.
"""
class DaryHuffmanCodeTree:
    def __init__(self, frequencies, D):
        self.frequencies = frequencies
        self.D = D

        #EI signature
        self.EI = ""
        # Number of messages
        N = len(frequencies)
        # First we insert the frequencies in the priority queue
        heap = []
        for f in frequencies:
            heappush(heap, [f])
        # The first auxiliary ensemble has n0 least probable messages
        n0 = (N - 2) % (D-1) + 2 # 2 <= n0 <= D
        if n0 > 0:
            children = []
            w = 0
            for x in range(n0):
                freq = heappop(heap)
                children.insert(0, freq) #
                w += freq[0]
                self.EI += 'E'
            heappush(heap, [w, children]) # reinsert
        # D least probable symbols are taken together
        while len(heap) > 1:
            children = []
            w = 0
            for x in range(D): # D elements
                freq = heappop(heap)
                children.insert(0, freq)
                w += freq[0]
                #Check if the child is external or internal
                if len(freq) == 2: #Internal
                    self.EI += 'I'
                else:
                    self.EI += 'E'


            heappush(heap, [w, children])
        #Root has probability 1 (sum of all the frequencies)
        self.EI += 'I'
        self.root = heappop(heap)


if __name__ == '__main__':
    f = \
    [ \
        [1, 2, 3, 4, 5, 5, 6, 7], \
        [4, 4, 4, 4], \
        [8, 1, 2, 4], \
        [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368]
    ]

    w = f[3]
    D = 10
    for w in f:
        print(w)
        print(getEISignature(w, D))
        print(getAlpha(w, D))
