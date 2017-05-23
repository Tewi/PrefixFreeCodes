
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
    codeTree = gdmCodeTree(weights, D)
    codeLengths = codeTree.depths()
    return codeLengths


"""
Given a list of weights, return a code tree of
minimal redundancy according to the GDM algorithm.
"""
class DaryGDMCodeTree:
    def __init__(self, weights, D):

        initialize(weights, D)
        while(len(self.externals) > 0):
            groupExternals()
            dockInternals()
            mixInternalWithExternal()
        warpUp()
        self.root(self.internals[0])

    """
    Given an array, partially sort the array and initialize the list of
    external nodes and the list of internal nodes with the
    first n0 external nodes
    """
    def initialize(self, weights, D):
        self.weights = PartiallySortedArray(weights)
        self.D = D
        self.N = len(frequencies)
        n0 = (N - 2) % (D-1) + 2 # 2 <= n0 <= D
        self.externals = [ExternalNode(self.weights,i) for i in range(n0,len(self.weights))] # N - n0 external nodes
        self.internals = [InternalNode(self.weights, [ExternalNode(self.weights,i) for i in range(0, n0)])] #internal with n0 external nodes

    """
    Given a partially sorted array of frequencies, a list of external nodes and
    a list of internal nodes, selects the external nodes of weight smaller than
    the smallest internal node, and join them by list of size D in internal nodes
    """
    def groupExternals(self):
        # EE...E
        r = self.weights.rankRight(internals[0].weight())
        nbNodes = r-len(self.weights)+len(self.externals)
        nbLists = nbNodes/self.D
        for i in range(0, nbLists):
            self.internals.append(InternalNode(self.weights, self.externals[:D])
            self.externals = self.externals[D:]
        # E..EI..I
        if numNodes % self.D > 0: #TODO fix EEIIEE
            #TODO creo que la idea es eliminar todos los EE's menores al interno
            nbExternalsLeft = numNodes % self.D
            self.internals.append(InternalNode(self.weights, self.externals[:nbExternalsLeft] + self.internals[:(D - nbExternalsLeft) ]))
            self.externals = self.externals[numNodes % D:]
            self.internals = self.internals[(D - nbExternalsLeft):]

    """
    Given a partially sorted array of frequencies and the number of frequencies
    already processed, a set of internal nodes whose weight is all within a
    factor of D, and a weight maxWeight;
    group the internal nodes by D until at least one internal node has weight
    larger than maxWeight; and return the resulting set of nodes.
    """
    #Crea nodos internos hasta el siguiente nivel IIIII...III
    def DockInternals(self):
        while len(self.externals)>0 and len(self.internals)>= self.D and self.internals[-1].weight() <= externals[0].weight():
        nbPairsToForm = len(internals) // self.D
        for i in range(nbPairsToForm):
            self.internals.append(InternalNode(self.weights,self.internals[:D]))
            self.internals = self.internals[D:]

    """ """
    def MixInternalWithExternal(self):

        if len(self.externals)==1:
            if len(self.internals)==(self.D-1):
                self.internals = [InternalNode(self.weights, self.internals + self.externals)]
                self.externals = []
            else:
                


        return 0

    def wrapUp(self):
        return 0



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
        self.CachedValueOfWeight = 0
        for child in self.children:
            if(child.CachedValueOfWeight == None):
                self.CachedValueOfWeight = None
                break
            else:
                self.CachedValueOfWeight += child.CachedValueOfWeight
        #For each consecutive pair of children check if the intervals match
        # If the node is pure
        if (False not in  [ left.interval != None \
                            and right.interval != None \
                            and left.interval.right == right.interval.left \
                            for left, right in zip(self.children, self.children[1:])]:
            self.interval = Interval(children[0].interval.left,
                                    children[-1].interval.right)
        else: # It's a mixed node
            self.interval = None
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
        depthList = []
        for child in self.children:
            depthList += child.depths(depth+1)
        return depthList

    """
    Given two code trees, compare them exactly.
    """
    def __cmp__(self,other):
        return self.partiallySortedArray == other.partiallySortedArray and\
                self.interval == other.interval and\
                self.CachedValueOfWeight == other.CachedValueOfWeight and\
                self.children == other.children
    """
    Given two code trees, compare them without restrictions on the order of the children.
    """
    def __eq__(self,other):
        return self.partiallySortedArray == other.partiallySortedArray and\
                self.CachedValueOfWeight == other.CachedValueOfWeight and\
                -1 not in [other.children.find(child) for child in self.children] ## TODO check
