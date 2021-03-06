import unittest,doctest




def EISignatureAndAlternation(W):
    """Given a list of weights, return the EI signature and the Alternation of the instance recording the result of each comparison performed by Huffman's algorithm or van Leeuwen's algorithm.
 
    >>> EISignatureAndAlternation([1,1,4])
    ('EEIEI', 2)
   """

    if W==[]:
        return ("",0)
    elif len(W)==1:
        return ("E",1)
    W = sorted(W)
    i = 0
    trees = []
    signature = ""
    previous = 'E'
    alternation = 0
    while i<len(W) or len(trees)>1:
        if len(trees) == 0 or (i<len(W) and W[i] <= trees[0][0]):
            left = [W[i]]
            i += 1
            signature = signature + "E"
            previous = 'E'
        else:
            left = trees[0]
            trees = trees[1:]
            signature = signature + "I"
            if previous == 'E':
                alternation += 1
            previous = 'I'
        if len(trees) == 0 or (i<len(W) and W[i] <= trees[0][0]):
            right = [W[i]]
            i += 1
            signature = signature + "E"
            previous = 'E'
        else:
            right = trees[0]
            trees = trees[1:]
            signature = signature + "I"
            if previous == 'E':
                alternation += 1
            previous = 'I'
        parent = [left[0] + right[0], left,right]
        trees.append(parent)
    signature = signature + "I"
    if previous == 'E':
        alternation += 1
    return (signature,alternation)

class EISignatureAndAlternationTest(unittest.TestCase):
    def test_empty(self):
        """Empty input."""
        self.assertEqual(EISignatureAndAlternation([]),("",0))
    def test_singleton(self):
        """Singleton input."""
        self.assertEqual(EISignatureAndAlternation([1]),("E",1))
    def test_twoWeights(self):
        """Two Weights."""
        self.assertEqual(EISignatureAndAlternation([1,1]),("EEI",1))
    def test_threeWeights(self):
        """Three Weights."""
        self.assertEqual(EISignatureAndAlternation([1,1,4]),("EEIEI",2))
    def test_exponentialSequence(self):
        """ExponentialSequence."""
        w = [1,2,4,8,16,32]
        (s,a) = EISignatureAndAlternation(w)
        self.assertEqual(s,"EEIEIEIEIEI")
        self.assertEqual(a,5)



def EISignature(W):
    """Given a list of weights, return the EI signature of the instance recording the result of each comparison performed by Huffman's algorithm or van Leeuwen's algorithm.
 
    >>> EISignature([1,1,4])
    'EEIEI'
   """

    if W==[]:
        return ""
    elif len(W)==1:
        return "E"
    W = sorted(W)
    i = 0
    trees = []
    signature = ""
    while i<len(W) or len(trees)>1:
        if len(trees) == 0 or (i<len(W) and W[i] <= trees[0][0]):
            left = [W[i]]
            i += 1
            signature = signature + "E"
        else:
            left = trees[0]
            trees = trees[1:]
            signature = signature + "I"
        if len(trees) == 0 or (i<len(W) and W[i] <= trees[0][0]):
            right = [W[i]]
            i += 1
            signature = signature + "E"
        else:
            right = trees[0]
            trees = trees[1:]
            signature = signature + "I"
        parent = [left[0] + right[0], left,right]
        trees.append(parent)
    signature = signature + "I"
    return signature


class EISignatureTest(unittest.TestCase):
    def test_empty(self):
        """Empty input."""
        self.assertEqual(EISignature([]),"")
    def test_singleton(self):
        """Singleton input."""
        self.assertEqual(EISignature([1]),"E")
    def test_twoWeights(self):
        """Two Weights."""
        self.assertEqual(EISignature([1,1]),"EEI")
    def test_threeWeights(self):
        """Three Weights."""
        self.assertEqual(EISignature([1,1,4]),"EEIEI")
    def test_exponentialSequence(self):
        """ExponentialSequence."""
        w = [1,2,4,8,16,32,64]
        s = EISignature(w)
        self.assertEqual(s,"EEIEIEIEIEIEI")


def EIAlternation(W):
    """Given a list of weights, return the EI signature of the instance recording the result of each comparison performed by Huffman's algorithm or van Leeuwen's algorithm.
 
    >>> EIAlternation([1,1,4])
    2
   """

    if W==[]:
        return 0
    elif len(W)==1:
        return 1
    W = sorted(W)
    i = 0
    trees = []
    previous = 'E'
    alternation = 0
    while i<len(W) or len(trees)>1:
        if len(trees) == 0 or (i<len(W) and W[i] <= trees[0][0]):
            left = [W[i]]
            i += 1
            previous = 'E'
        else:
            left = trees[0]
            trees = trees[1:]
            if previous == 'E':
                alternation += 1
            previous = 'I'
        if len(trees) == 0 or (i<len(W) and W[i] <= trees[0][0]):
            right = [W[i]]
            i += 1
            previous = 'E'
        else:
            right = trees[0]
            trees = trees[1:]
            if previous == 'E':
                alternation += 1
            previous = 'I'
        parent = [left[0] + right[0], left,right]
        trees.append(parent)
    if previous == 'E':
        alternation += 1
    return alternation    

    
class EIAlternationTest(unittest.TestCase):
    def test_empty(self):
        """Empty input."""
        self.assertEqual(EIAlternation([]),0)
    def test_singleton(self):
        """Singleton input."""
        self.assertEqual(EIAlternation([1]),1)
    def test_twoWeights(self):
        """Two Weights."""
        self.assertEqual(EIAlternation([1,1]),1)
    def test_threeWeights(self):
        """Three Weights."""
        self.assertEqual(EIAlternation([1,1,4]),2)
    def test_exponentialSequence(self):
        """ExponentialSequence."""
        w = [1,2,4,8,16,32]
        a = EIAlternation(w)
        self.assertEqual(a,5)
    def test_manyEqualWeights(self):
        w = [1]*32
        a = EIAlternation(w)
        self.assertEqual(a,1)


def main():
    unittest.main()
if __name__ == '__main__':
    doctest.testmod()
    main()
