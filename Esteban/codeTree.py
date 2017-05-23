import unittest,doctest
from partiallySortedArrayWithPartialSumPrecomputed import PartiallySortedArray
from collections import namedtuple

Interval = namedtuple('Interval','left right')

class ExternalNode:
"""
Given a partially sorted array W, and a position in it, create the corresponding External node.
The weight is computed only at request by performing a select query in the partiallySortedArray.
"""
    def __init__(self, partiallySortedArray, position):
        self.partiallySortedArray = partiallySortedArray
        self.position = position
        self.children = None
        self.interval = Interval(position,position+1)
        self.CachedValueOfWeight = None
    def weight(self):
        if self.CachedValueOfWeight == None:
            self.CachedValueOfWeight = self.partiallySortedArray.select(self.position)
        return self.CachedValueOfWeight
    def depths(self, depth=0):
        """
        Given a code tree, return the (unsorted) list of the depths of its leaves.
        """
        return [depth]
    def __cmp__(self,other):
        return self.partiallySortedArray == other.partiallySortedArray and self.interval == other.interval and self.CachedValueOfWeight == other.CachedValueOfWeight
    def __eq__(self,other):
        return self.__cmp__(other)
    def __str__(self):
        if self.CachedValueOfWeight == None:
            return "[select("+str(self.position)+")]"
        else:
            return "["+str(self.CachedValueOfWeight)+"]"
    def toStringWithAllWeightsCalculated(self):
        """Given an External node, return a string with its computed weight.
        """
        return "["+str(self.weight())+"]"


class InternalNode:
"""
Given a partially sorted array W and two pointers, builds a node of the codeTree
for the GDM algorithm.  The weight is computed only at request.
"""
    def __init__(self, partiallySortedArray, children):
        self.partiallySortedArray = partiallySortedArray
        self.position = None
        self.children = children
        self.CachedValueOfWeight = 0
        if None in [child.CachedValueOfWeight for child in children]:
            self.CachedValueOfWeight = None
        else:
            self.CachedValueOfWeight = sum([child.CachedValueOfWeight for child in self.children])

        #If children are contiguos weights
        if False not in [left.interval != None and right.interval != None and left.interval.right == right.interval.left for left, right in zip(self.children, self.children[1:])]:
            self.interval = Interval(children[0].interval.left, children[-1].interval.right)
        else: # Mixed nodes are systematically computed.
            self.interval = None
            #TODO calculate weights of consecutive intervals with partialSums
            self.CachedValueOfWeight = sum([child.weight() for child in self.children])
    def weight(self):
        if self.CachedValueOfWeight == None:
            if self.interval != None:
                self.CachedValueOfWeight = self.partiallySortedArray.rangeSum(self.interval.left,self.interval.right)
            else:
                self.CachedValueOfWeight = sum([child.weight() for child in self.children])
        return self.CachedValueOfWeight

    def depths(self, depth=0):
        """
        Given a code tree, return the (unsorted) list of the depths of its leaves.
        """
        childrenDephts = []
        for child in self.children:
            childrenDephts +=child.depths(depth+1)
        return childrenDepths

    def __cmp__(self,other):
        """
        Given two code trees, compare them exactly.
        """
        return self.partiallySortedArray == other.partiallySortedArray
                and self.interval == other.interval
                and self.CachedValueOfWeight == other.CachedValueOfWeight
                and False not in [a==b for a,b in zip_longest(self.children, other.children)]

    def __eq__(self,other):
        """
        Given two code trees, compare them without restrictions on the order of the children.
        """
        return self.partiallySortedArray == other.partiallySortedArray
                and self.CachedValueOfWeight==other.CachedValueOfWeight
                and set(self.children) & set(other.children)

    def __str__(self):
        childrenString = '[' + ','.join([str(c) for c in self.children]) + ']'
        if self.CachedValueOfWeight == None and self.interval != None:
            string = "(rangeSum("+str(self.interval.left)+","+str(self.interval.right)+"),"+childrenString+")"
        elif self.CachedValueOfWeight == None and self.interval == None:
            string = "(MixedNonComputedYet,"+childrenString+")"
        else:
            string = "("+str(self.CachedValueOfWeight)+","+childrenString+")"
        return string

    def toStringWithAllWeightsCalculated(self):
        """
        Given a node, convert the corresponding code tree to a string with all the weights calculated, children ordered so that the smallest one comes first.
        """
        string = "("+str(self.weight())+","
        for child in sorted(self.children, key=lambda x : x.weight()):
            string += child.toStringWithAllWeightsCalculated() + ','        
        return string[:-1] + ')'

#TODO update to D-ary
def nodeListToString(nodes):
    """Given a list of nodes, returns a string listing the trees in the list.

>>> w = PartiallySortedArray([1,2,3,4])
>>> x = ExternalNode(w,0)
>>> y = InternalNode(w,ExternalNode(w,1),ExternalNode(w,2))
>>> z = ExternalNode(w,3)
>>> print(x.weight(),y.weight())
(1, 5)
>>> l = [x,y,z]
>>> print(nodeListToString(l))
[[1], (5,[select(1)],[select(2)]), [select(3)]]
"""
    output = "["
    for i in range(len(nodes)-1):
        output += str(nodes[i])+", "
    output += str(nodes[-1])
    output += "]"
    return output

def nodeListToStringOfWeights(nodes):
    """Given a list of nodes, returns a string listing the weights of the nodes in the list.

>>> w = PartiallySortedArray([10,20,30,40])
>>> l = [ExternalNode(w,0),InternalNode(w,ExternalNode(w,1),ExternalNode(w,2)),ExternalNode(w,3)]
>>> print(nodeListToStringOfWeights(l))
[10, 50, 40]
"""
    output = "["
    for i in range(len(nodes)-1):
        output += str(nodes[i].weight())+", "
    output += str(nodes[-1].weight())
    output += "]"
    return output

def nodeListToWeightList(nodes):
    """Given a list of nodes, returns the list of the weights of the nodes in the list.

>>> w = PartiallySortedArray([10,20,30,40])
>>> l = [ExternalNode(w,0),InternalNode(w,ExternalNode(w,1),ExternalNode(w,2)),ExternalNode(w,3)]
>>> print(nodeListToWeightList(l))
[10, 50, 40]
"""
    l = []
    for i in range(len(nodes)):
        l.append(nodes[i].weight())
    return l



def main():
    unittest.main()
if __name__ == '__main__':
    doctest.testmod()
    main()
