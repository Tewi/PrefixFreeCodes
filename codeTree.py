import unittest,doctest
from partiallySortedArrayWithPartialSumPrecomputed import PartiallySortedArray
from collections import namedtuple

Interval = namedtuple('Interval','left right')

class ExternalNode:
    """Given a partially sorted array W, and a position in it, create the corresponding External node.
The weight is computed only at request by performing a select query in the partiallySortedArray.

>>> W = PartiallySortedArray([150,140,130,120,110,32,16,10,10,10,10])
>>> x = ExternalNode(W,0)
>>> y = ExternalNode(W,0)
>>> z = ExternalNode(W,1)
>>> print(x == y)
True
>>> print(x == z)
False
>>> print(str(x))
[select(0)]
"""
    def __init__(self, partiallySortedArray, position):
        self.partiallySortedArray = partiallySortedArray
        self.position = position
        self.left = None
        self.right = None
        self.interval = Interval(position,position+1)
        self.CachedValueOfWeight = None
    def weight(self):
        if self.CachedValueOfWeight == None:
            self.CachedValueOfWeight = self.partiallySortedArray.select(self.interval[0])
        return self.CachedValueOfWeight
    def depths(self, depth=0):
        """Given a code tree, return the (unsorted) list of the depths of its leaves.
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
    """Given a partially sorted array W and two pointers, builds a node of the codeTree for the GDM algorithm.  The weight is computed only at request.

>>> W = PartiallySortedArray([100,100,50,10,10])
>>> x = ExternalNode(W,0)
>>> y = ExternalNode(W,1)
>>> z = InternalNode(W,x,y)
>>> print(W.totalNbOfQueriesPerformed())
0
>>> print(x.weight())
10
>>> print(y.weight())
10
>>> print(z.weight())
20
>>> x2 = ExternalNode(W,3)
>>> y2 = ExternalNode(W,4)
>>> z2 = InternalNode(W,x2,y2)
>>> print(z2.weight())
200
>>> z3 = InternalNode(W,z,z2)
>>> print(z3.weight())
220
>>> print(z3.depths())
[2, 2, 2, 2]

"""
    def __init__(self, partiallySortedArray, left, right):
        self.partiallySortedArray = partiallySortedArray
        self.position = None
        self.left = left
        self.right = right
        if left.CachedValueOfWeight == None or right.CachedValueOfWeight == None:
            self.CachedValueOfWeight = None
        else:
            self.CachedValueOfWeight = left.CachedValueOfWeight + right.CachedValueOfWeight
        if(left.interval != None and right.interval != None and left.interval.right == right.interval.left):
            self.interval = Interval(left.interval.left,right.interval.right)
        else:
            self.interval = None
            self.CachedValueOfWeight = left.weight() + right.weight() # Mixed nodes are systematically computed.
    def weight(self):
        if self.CachedValueOfWeight == None:
            if self.interval != None:
                self.CachedValueOfWeight = self.partiallySortedArray.rangeSum(self.interval.left,self.interval.right)
            else:
                self.CachedValueOfWeight = self.left.weight() + self.right.weight()
        return self.CachedValueOfWeight
    def depths(self, depth=0):
        """Given a code tree, return the (unsorted) list of the depths of its leaves.
"""
        depthsOnLeft =  self.left.depths(depth+1)
        depthsOnRight = self.right.depths(depth+1)
        return depthsOnLeft+depthsOnRight
    def __cmp__(self,other):
        """Given two code trees, compare them exactly.
"""
        return self.partiallySortedArray == other.partiallySortedArray and self.interval == other.interval and self.left == other.left and self.right == other.right and self.CachedValueOfWeight == other.CachedValueOfWeight
    def __eq__(self,other):
        """Given two code trees, compare them without restrictions on the order of the children.
"""
        return self.partiallySortedArray == other.partiallySortedArray and self.CachedValueOfWeight==other.CachedValueOfWeight and (
            (self.left.__eq__(other.left) and self.right.__eq__(other.right)) or 
            (self.left.__eq__(other.right) and self.right.__eq__(other.left)))
    def __str__(self):
        if self.CachedValueOfWeight == None and self.interval != None:
            string = "(rangeSum("+str(self.interval.left)+","+str(self.interval.right)+"),"+str(self.left)+","+str(self.right)+")"
        elif self.CachedValueOfWeight == None and self.interval == None:
            string = "(MixedNonComputedYet,"+str(self.left)+","+str(self.right)+")"
        else:
            string = "("+str(self.CachedValueOfWeight)+","+str(self.left)+","+str(self.right)+")"
        return string
    def toStringWithAllWeightsCalculated(self):
        """Given a node, convert the corresponding code tree to a string with all the weights calculated, children ordered so that the smallest one comes first.
        """
        string = "("+str(self.weight())+","
        if self.left.weight() <= self.right.weight():
            string += self.left.toStringWithAllWeightsCalculated()+","+self.right.toStringWithAllWeightsCalculated()+")"
        else:
            string += self.right.toStringWithAllWeightsCalculated()+","+self.left.toStringWithAllWeightsCalculated()+")"
        return string
            

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
            
        

