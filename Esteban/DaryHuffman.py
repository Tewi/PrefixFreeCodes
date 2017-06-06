from heapq import *
import math



"""
Implementation of the Huffman algorithm as described by Huffman in his 1952.

This is an heap-based implementation of the method originally described by
Huffman in 1952.

It receives as input an array of integer frequencies of symbols and size of the
output alphabet.

Given a list of weights, return a representation of an optimal prefix free code,
as a list of codelengths.
"""
def huffman(weights, D=2):
    N = len(weights)
    # Degenerated cases
    if D < 2:
        raise Exception("Output alphabet must have at least 2 symbols")
    if N == 0:
        return []
    if N == 1:
        return [0]
    tree = DaryHuffmanCodeTree(weights, D)
    codeLengths = depths(tree.root)
    return codeLengths



"""
Given a code tree, return the (unsorted) list of the depths of its leaves.
"""
def depths(tree, depth=0):
    if tree == []:
        return []
    if len(tree) == 1: # Leaf
        return [depth]
    else: # Inner node
        childrenDepths = []
        for child in tree[1]:
            childrenDepths += depths(child, depth+1)
        return childrenDepths

"""
Given an unsorted list of of at least two weights, return a D-ary code tree
of minimal redundancy according to Huffman's's algorithm.
"""
class DaryHuffmanCodeTree:
    def __init__(self, frequencies, D):
        self.frequencies = frequencies
        self.D = D
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
            heappush(heap, [w, children]) # reinsert
        # D least probable symbols are taken together
        while len(heap) > 1:
            children = []
            w = 0
            for x in range(D): # D elements
                freq = heappop(heap)
                children.insert(0, freq)
                w += freq[0]
            heappush(heap, [w, children])
        #Root has probability 1 (sum of all the frequencies)
        self.root = heappop(heap)
