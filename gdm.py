import unittest,doctest
# from functionsToTestPrefixFreeCodes import testPFCAlgorithm, compressByRunLengths
from partiallySortedArrayWithPartialSumPrecomputed import PartiallySortedArray
from codeTree import Interval, ExternalNode, InternalNode, nodeListToStringOfWeights, nodeListToString, nodeListToWeightList

def INITIALIZE(frequencies):
    """Given a partially sorted array, initialize the list of internal nodes with the two first external nodes:

>>> frequencies = PartiallySortedArray([90,80,70,60,50,40,30,20,10])
>>> frequencies,nodes,nbFrequenciesProcessed = INITIALIZE(frequencies)
>>> print(len(nodes))
2
>>> print(nodeListToString(nodes))
[[select(0)], [select(1)]]

Note that the weight of those external nodes is not computed yet, for a reason:
the function GROUP will join those two nodes, and compute the weight of the resulting node, *without* ordering those nodes between themselves. It saves only one comparison but it's the spirit that counts. So the cached value of those two nodes is still None:

>>> print(nodes[0].CachedValueOfWeight,nodes[1].CachedValueOfWeight)
(None, None)

Beware: don't base yourself on the content of the list when printed (print(nodeListToStringOfWeights(nodes))): this depends of the implementation of PartiallySortedArray!

"""
    assert(len(frequencies)>1)
    nodes = []
    nodes.append(ExternalNode(frequencies,0))
    nodes.append(ExternalNode(frequencies,1))
    nbFrequenciesProcessed = 2
    return frequencies,nodes,nbFrequenciesProcessed


def GROUP(frequencies,nodes,nbFrequenciesProcessed):
    """Given an partially sorted array of frequencies, a vector of nodes, and the number of frequencies already transformed into nodes, combines the two nodes of least weights into a new node, and all the frequencies of  weight smaller than or equal to the later into External Nodes.

>>> frequencies = PartiallySortedArray([10,10,11,13,14,15,20,30])
>>> nodes = [ExternalNode(frequencies,0),ExternalNode(frequencies,1)]
>>> nbFrequenciesProcessed = 2
>>> frequencies,nodes,nbFrequenciesProcessed = GROUP(frequencies,nodes,nbFrequenciesProcessed)
>>> print(nodeListToString(nodes))
[[select(2)], [select(3)], [select(4)], [select(5)], [select(6)], (20,[select(0)],[select(1)])]

At the end of the process (as before it), all the nodes are within a factor of two of each other:

>>> nodeListToWeightList(nodes)
[11, 13, 14, 15, 20, 20]
"""
    if len(nodes)==1:
        externalNode = ExternalNode(frequencies,nbFrequenciesProcessed)
        externalNode.weight() # Insure the external node is the smallest available.
        nodes = [InternalNode(frequencies,nodes[0],externalNode)]
        nbFrequenciesProcessed += 1
    elif len(nodes)>=2:
        internalNode = InternalNode(frequencies,nodes[0],nodes[1])
        nodes = nodes[2:]+[internalNode]
        r = frequencies.rankRight(internalNode.weight())
        newNodes = [] 
        for i in range(nbFrequenciesProcessed,r):
            newNodes.append(ExternalNode(frequencies,i))
        nodes = newNodes + nodes
    return frequencies,nodes,nbFrequenciesProcessed

# def oldGROUP(frequencies,nodes,nbFrequenciesProcessed):
#     """Computes the weight of the smallest (first) node in nodes, 
# ranks it among the frequencies, and creates the corresponding external nodes.         

# """
#     r = frequencies.rankRight(nodes[0].weight())        
#     if len(nodes)==1 and r == nbFrequenciesProcessed: # if there is only one internal node and it is smaller than any external node
#         nodes[0].weight()
#         nodes = [InternalNode(frequencies,nodes[0],ExternalNode(frequencies,r))]
#         nbFrequenciesProcessed += 1
#     else:
#         if (r-nbFrequenciesProcessed) % 2 == 1: # if there is an odd number of external nodes smaller than the smallest internal node,
#             nodes = [ExternalNode(frequencies,r-1)]+nodes # promote the last external node by adding it directly to the list of nodes.
#         for i in range((r-nbFrequenciesProcessed)//2): # pair the even number of nodes preceding it, andd add them to the list of nodes.
#             left = ExternalNode(frequencies,nbFrequenciesProcessed+2*i)
#             right = ExternalNode(frequencies,nbFrequenciesProcessed+2*i+1)        
#             nodes.append(InternalNode(frequencies,left,right))
#         nbFrequenciesProcessed = r
#     return frequencies,nodes,nbFrequenciesProcessed



# def DOCK(frequencies,nodes,nbFrequenciesProcessed):
#     """Given a set of internal nodes whose weight is all within a factor of two, group them two by two until at least one internal node has weight larger than the weight of the next External node (but smaller than twice this weight).

# >>> frequencies = PartiallySortedArray([8]*4+[32])
# >>> frequencies,nodes,nbFrequenciesProcessed = INITIALIZE(frequencies)
# >>> print(len(nodes))
# 2
# """
#     while len(nodes)>1 and nodes[-1].weight() <= frequencies.select(nbFrequenciesProcessed):
#         nbPairsToForm = len(nodes) // 2
#         for i in range(nbPairsToForm):
#             nodes.append(InternalNode(frequencies,nodes[0],nodes[1]))
#             nodes = nodes[2:]
#     return frequencies,nodes,nbFrequenciesProcessed


# def MERGE(frequencies,nodes,nbFrequenciesProcessed):
#     """Merge the list of Internal nodes with the external nodes of weights within a factor of two of it.

# """
#     r = frequencies.rank( 2 * nodes[0].weight() )
#     internalNodesToMerge = nodes
#     externalNodesToMerge = []
#     for p in range(nbFrequenciesProcessed,r):
#         externalNodesToMerge.append(ExternalNode(frequencies,p))
#     nbFrequenciesProcessed = r
#     nodes = []
#     while( len(internalNodesToMerge)>0 and len(externalNodesToMerge)>0 ):
#         children = []
#         for i in range(2):
#             if len(externalNodesToMerge)==0 or ( len(internalNodesToMerge)>0  and internalNodesToMerge[0].weight() < externalNodesToMerge[0].weight() ) :
#                 children.append(internalNodesToMerge[0])
#                 internalNodesToMerge = internalNodesToMerge[1:]
#             else:
#                 children.append(externalNodesToMerge[0])
#                 externalNodesToMerge = internalNodesToMerge[1:]
#         nodes.append(InternalNode(frequencies,children[0],children[1]))
#     nodes = internalNodesToMerge + externalNodesToMerge + nodes
#     return frequencies,nodes,nbFrequenciesProcessed


# def WRAPUP(frequencies,nodes):
#     """Combine the internal nodes of a list until only one is left.

# """
#     while len(nodes) > 1:
#         if len(nodes) % 2 == 1:
#             nodes[-1].weight()
#         for i in range( len(nodes) // 2):
#             nodes.append(InternalNode(frequencies,nodes[0],nodes[1]))
#             nodes = nodes[2:]
#     nodes[0].weight()
#     return frequencies,nodes

# def gdmCodeTree(frequencies):
#     """Given a partially sorted list of weights, return a code tree of minimal
# redundancy according to the GDM algorithm.

# >>> print(gdmCodeTree(PartiallySortedArray([1,1,1,1])))
# (4,(2,[select(0)],[select(1)]),(rangeSum(2,4),[select(2)],[select(3)]))
# """
#     if len(frequencies) == 0 :
#         return None
#     elif len(frequencies)==1:
#         return ExternalNode(frequencies,0)
#     frequencies,nodes,nbFrequenciesProcessed = INITIALIZE(frequencies)
#     while nbFrequenciesProcessed < len(frequencies):
#         frequencies,nodes,nbFrequenciesProcessed = GROUP(frequencies,nodes,nbFrequenciesProcessed)
#         frequencies,nodes,nbFrequenciesProcessed = DOCK(frequencies,nodes,nbFrequenciesProcessed)
#         frequencies,nodes,nbFrequenciesProcessed = MERGE(frequencies,nodes,nbFrequenciesProcessed)
#     frequencies,nodes = WRAPUP(frequencies,nodes)
#     return nodes[0]

# def gdm(frequencies):
#     """Given a sorted list of weights, return an array with the code lengths of an optimal prefix free code according to the GDM algorithm.

# >>> print(gdm([1,1,1,1]))
# [2, 2, 2, 2]
# >>> print(gdm([1,2,4,8,16,32,64,128,256]))
# [8, 8, 7, 6, 5, 4, 3, 2, 1]

# """
#     # Degenerated cases
#     if len(frequencies) == 0 :
#         return []
#     elif len(frequencies)==1:
#         return [0]
#     elif len(frequencies)==2:
#         return [1,1]
#     codeTree = gdmCodeTree(PartiallySortedArray(frequencies))
#     codeLengths = codeTree.depths()
#     return codeLengths

        
def main():
    unittest.main()
if __name__ == '__main__':
    doctest.testmod()
    main()
            
        

