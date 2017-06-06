from partiallySortedArrayWithPartialSumPrecomputed import PartiallySortedArray

"""
Given a list of weights, return an array with the code lengths of
an optimal prefix free code according to the GDM algorithm.
"""
def GDM(weights, D=2):
    N = len(weights)
    # Degenerated cases
    if D < 2:
        raise Exception("Output alphabet must have at least 2 symbols")
    if N == 0:
        return []
    if N == 1:
        return [0]
    codeTree = DaryGDMCodeTree(weights, D)
    codeLengths = codeTree.root.depths()
    return codeLengths


"""
Given a list of weights, return a code tree of
minimal redundancy according to the GDM algorithm.
"""
class DaryGDMCodeTree:
    def __init__(self, weights, D):

        self.initialize(weights, D)
        while(len(self.externals) > 0):
            self.groupExternals()
            self.dockInternals()
            self.mixInternalWithExternal()
        self.wrapUp()
        self.root = self.internals[0]

    """
    Given an array, partially sort the array and initialize the list of
    external nodes and the list of internal nodes with the
    first n0 external nodes
    """
    def initialize(self, weights, D):
        self.weights = PartiallySortedArray(weights)
        self.D = D
        self.N = len(weights)
        n0 = (self.N - 2) % (self.D-1) + 2 # 2 <= n0 <= D
        self.externals = [ExternalNode(self.weights,i) for i in range(n0,len(self.weights))] # N - n0 external nodes
        self.internals = [InternalNode(self.weights, [ExternalNode(self.weights,i) for i in range(0, n0)])] #internal with n0 external nodes

    """
    Given a partially sorted array of frequencies, a list of external nodes and
    a list of internal nodes, selects the external nodes of weight smaller than
    the smallest internal node, and join them by list of size D in internal nodes
    """
    def groupExternals(self):
        # EE...E
        r = self.weights.rankRight(self.internals[0].weight())
        nbNodes = r-len(self.weights)+len(self.externals)
        nbLists = nbNodes//self.D
        for i in range(0, nbLists):
            self.internals.append(InternalNode(self.weights, self.externals[:self.D]))
            self.externals = self.externals[self.D:]
        # E..EI[EI]*
        if nbNodes % self.D > 0:
            #We pad the node with the E/I's (costly)
            nodes = self.externals[:nbNodes % self.D] + self.internals[:1]
            self.externals = self.externals[nbNodes % self.D:]
            self.internals = self.internals[1:]
            #Fill the rest of the node with the next minimun weights
            while len(nodes) < self.D:
                if self.externals and self.internals:
                    #We have to chose the lighter between E and I
                    if self.externals[0].weight() <= self.internals[0].weight():
                        #Next external is lighter
                        nodes.append(self.externals[0])
                        self.externals = self.externals[1:]
                    else:
                        #Next interal is lighter
                        nodes.append(self.internals[0])
                        self.internals = self.internals[1:]
                elif not self.internals:
                    #Only E remain
                    nodes.append(self.externals[0])
                    self.externals = self.externals[1:]
                else:
                    #Only I remain
                    nodes.append(self.internals[0])
                    self.internals = self.internals[1:]
            self.internals.append(InternalNode(self.weights, nodes))

    """
    Given a partially sorted array of frequencies and the number of frequencies
    already processed, a set of internal nodes whose weight is all within a
    factor of D, and a weight maxWeight;
    group the internal nodes by D until at least one internal node has weight
    larger than maxWeight; and return the resulting set of nodes.
    """
    #I...I
    def dockInternals(self):
        while self.externals and len(self.internals)>= self.D and self.internals[-1].weight() <= self.externals[0].weight():
            nbPairsToForm = len(self.internals) // self.D
            for i in range(nbPairsToForm):
                self.internals.append(InternalNode(self.weights,self.internals[:self.D]))
                self.internals = self.internals[self.D:]

    """ """
    def mixInternalWithExternal(self):
        if not self.externals:
            return
        # [EI]*E
        #TODO find the first r smallest intenral weights with a doubling search
        #We pad the node with the E/I's (costly)
        nodes = []
        #Fill the rest of the node with the next minimun weights
        while len(nodes) < self.D:
            if self.externals and self.internals:
                #We have to chose the lighter between E and I
                if self.externals[0].weight() <= self.internals[0].weight():
                    #Next external is lighter
                    nodes.append(self.externals[0])
                    self.externals = self.externals[1:]
                else:
                    #Next interal is lighter
                    nodes.append(self.internals[0])
                    self.internals = self.internals[1:]
            elif not self.internals:
                #Only E remain
                nodes.append(self.externals[0])
                self.externals = self.externals[1:]
            else:
                #Only I remain
                nodes.append(self.internals[0])
                self.internals = self.internals[1:]
        self.internals.append(InternalNode(self.weights, nodes))


    """
    Given a list of internal nodes (when there is no external nodes left),
    combine the nodes of the list until only one is left.
    """
    def wrapUp(self):
        #Ther should be N inner nodes left, were (N-1)/(D-1) is an integer
        while len(self.internals) > 1:
            self.internals.append(InternalNode(self.weights, self.internals[:self.D]))
            self.internals = self.internals[self.D:]
        self.internals[0].weight()



from collections import namedtuple

Interval = namedtuple('Interval','left right')

"""
Given a partially sorted array W, and a position in it, create the corresponding External node.
The weight is computed only at request by performing a select query in the partiallySortedArray.
"""
class ExternalNode:
    def __init__(self, partiallySortedArray, position):
        self.partiallySortedArray = partiallySortedArray
        self.position = position
        self.children = None
        self.interval = Interval(position,position+1)
        self.CachedValueOfWeight = None
    def weight(self):
        if self.CachedValueOfWeight == None:
            self.CachedValueOfWeight = self.partiallySortedArray.select(self.interval[0])
        return self.CachedValueOfWeight
    """
    Given a code tree, return the (unsorted) list of the depths of its leaves.
    """
    def depths(self, depth=0):
        return [depth]
    def __cmp__(self,other):
        return self.partiallySortedArray == other.partiallySortedArray and self.interval == other.interval and self.CachedValueOfWeight == other.CachedValueOfWeight
    def __eq__(self,other):
        return self.__cmp__(other)

"""
Given a partially sorted array W and an array of D pointers, builds a node of the
codeTree for the GDM algorithm.  The weight is computed only at request.
"""
class InternalNode:
    def __init__(self, partiallySortedArray, children):
        self.partiallySortedArray = partiallySortedArray
        self.position = None
        self.children = children
        #weight
        if None in [child.CachedValueOfWeight for child in children]:
            self.CachedValueOfWeight = None
        else:
            self.CachedValueOfWeight = sum([child.CachedValueOfWeight for child in self.children])
        #For each consecutive pair of children check if the intervals match
        # If the node is pure
        if False not in [left.interval != None and right.interval != None and left.interval.right == right.interval.left for left, right in zip(self.children, self.children[1:])]:
            self.interval = Interval(children[0].interval.left,
                                    children[-1].interval.right)
        else: # It's a mixed node
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

    """
    Given a code tree, return the (unsorted) list of the depths of its leaves.
    """
    def depths(self, depth=0):
        childrenDepths = []
        for child in self.children:
            childrenDepths +=child.depths(depth+1)
        return childrenDepths

    """
    Given two code trees, compare them exactly.
    """
    def __cmp__(self,other):
        return self.partiallySortedArray == other.partiallySortedArray \
                and self.interval == other.interval \
                and self.CachedValueOfWeight == other.CachedValueOfWeight \
                and False not in [a==b for a,b in zip_longest(self.children, other.children)]
    """
    Given two code trees, compare them without restrictions on the order of the children.
    """
    def __eq__(self,other):
        return self.partiallySortedArray == other.partiallySortedArray \
                and self.CachedValueOfWeight == other.CachedValueOfWeight \
                and set(self.children) & set(other.children)


if __name__ == '__main__':
    # main()
    test = [1,2,3,4,5,5,6,7]
    test2 = [1,1,2,2,2,4,5]
    print(GDM(test, 4))
