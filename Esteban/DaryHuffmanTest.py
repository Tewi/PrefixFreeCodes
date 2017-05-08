import unittest
from DaryHuffman import huffman
from functionsToTestPrefixFreeCodes import testPFCAlgorithm, compressByRunLengths


class TestBorder(unittest.TestCase):

    """Empty input."""
    def test_empty(self):
        elements = []
        expected = []
        for d in xrange(2, 12):
            result = (huffman(elements, d))
            self.assertEqual(result, expected)

    """Singleton input."""
    def test_oneElement(self):
        elements = [4]
        expected = [0]
        for d in xrange(2, 10):
            result = (huffman(elements, d))
            self.assertEqual(result, expected)

    """Unusual weights: negative, zero and float-point number."""
    def test_unusualWeights(self):
        elements = [-4, 0, 18.3, 9]
        result = compressByRunLengths(huffman(elements, 2))
        expected = [(3,2), (2,1), (1,1)]
        self.assertEqual(result, expected)

    """Invalid alphabet size """
    def test_lowOutputAlphabet(self):
        with self.assertRaises(Exception) as context:
            huffman([], 1)


class TestBinary(unittest.TestCase):

    """Generic test"""
    def test(self):
        testPFCAlgorithm(huffman, "Huffman")

    def test_twoElements(self):
        elements = [4, 2]
        result = compressByRunLengths(huffman(elements, 2))
        expected = [(1,2)]
        self.assertEqual(result, expected)

    def test_threeElements(self):
        elements = [4, 3, 6]
        result = compressByRunLengths(huffman(elements, 2))
        expected = [(2,2), (1,1)]
        self.assertEqual(result, expected)

    def test_fourElements(self):
        elements = [4, 3, 6, 8]
        result = compressByRunLengths(huffman(elements, 2))
        expected = [(3,2),(2,1),(1,1)]
        self.assertEqual(result, expected)

    """Example from the 1952 paper with a binary output alphabet"""
    def test_paperExample(self):
        elements = [0.20, 0.18, 0.10, 0.10, 0.10, 0.06, 0.06,
                    0.04, 0.04, 0.04, 0.04, 0.03, 0.01]
        result = huffman(elements, 2)
        elements.sort()
        result.sort(reverse=True)
        avgLength = 0
        for i in range(len(elements)):
            avgLength += result[i]*elements[i]
        expected = 3.42
        self.assertAlmostEqual(avgLength, expected) #test by optimal average message length

class TestGeneralized(unittest.TestCase):

    """"Same element D times, every leaf should be on the same level"""
    def test_sameWeigths(self):
        for d in range(2, 15):
            elements = [1] * d
            result = compressByRunLengths(huffman(elements, d))
            expected = [(1,d)]
            self.assertEqual(result, expected)

    def test_fourTernary(self):
        elements = [4, 3, 6, 8]
        result = compressByRunLengths(huffman(elements, 3))
        expected = [(2,2), (1,2)]
        self.assertEqual(result, expected)

    """Example from the 1952 paper with a quaternary output alphabet"""
    def test_paperExample(self):
        elements = [0.22, 0.20, 0.18, 0.15, 0.10, 0.08, 0.05, 0.02]
        result = compressByRunLengths(huffman(elements, 4   ))
        expected = [(3,2),(2,3),(1,3)]
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
