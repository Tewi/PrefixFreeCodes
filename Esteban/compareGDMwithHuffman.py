import unittest
import random
from DaryGDM import GDM
from DaryHuffman import huffman
from functionsToTestPrefixFreeCodes import testPFCAlgorithm, compressByRunLengths


"""Returns the average message length given the weights and the codes associated.
An optimal pregix free code minimizes this."""
def averageMessageLength(weights, codes):
    weights.sort()
    codes.sort(reverse=True)
    avgLength = 0
    for i in range(len(weights)):
        avgLength += weights[i]*codes[i]
    return avgLength


""""Compare the optimal prefix free codes of Huffman and GDM over a group of
random weights"""

class TestGeneralized(unittest.TestCase):



    def test_averageMessageLengths(self):

        for i in range(10):

            weights = [random.randrange(2*20) for x in range(1000)]

            for D in range(2, 15):
                huff_codes = huffman(weights, D)
                gdm_codes = GDM(weights, D)

                huff_avg = averageMessageLength(weights, huff_codes)
                gdm_avg = averageMessageLength(weights, gdm_codes)
                self.assertEqual(huff_avg, gdm_avg)


if __name__ == '__main__':
    unittest.main()
