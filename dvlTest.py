import unittest, doctest, copy
from functionsToTestPrefixFreeCodes import testPFCAlgorithm, compressByRunLengths
from partiallySortedArrayWithPartialSumPrecomputed import PartiallySortedArray
from collections import namedtuple
from vanLeeuwen import vanLeeuwen
from codeTree import ExternalNode, InternalNode,  nodeListToStringOfWeights, nodeListToString, nodeListToWeightList
from dvl import WRAPUP, dvlCodeTree, dvl 

class GeneralTest(unittest.TestCase):
    def test_TREE1(self):
        """Empty input."""
        frequencies = PartiallySortedArray([])
        self.assertEqual(dvlCodeTree(frequencies),None)
        
    def test_TREE2(self):
        """Alpha Equal One. Singleton input."""
        frequencies = PartiallySortedArray([10])
        self.assertEqual(dvlCodeTree(frequencies),ExternalNode(frequencies,0))
        
    def test_TREE3(self):
        """Alpha Equal One. Two Weights."""
        W = PartiallySortedArray([10,10])
        T = dvlCodeTree(W)
        self.assertEqual(str(T),"(20,[select(0)],[select(1)])")
        L = T.depths()
        self.assertEqual(L,[1]*2)
        
    def test_TREE4(self):
        """Alpha Equal One. Four Equal Weights."""
        W = PartiallySortedArray([10]*4)
        T = dvlCodeTree(W)
        self.assertEqual(str(T),'(40,(20,[select(0)],[select(1)]),(rangeSum(2,4),[select(2)],[select(3)]))')
        L = T.depths()
        self.assertEqual(L,[2]*4)
        
    def test_TREE5(self):
        """Alpha Equal One. Sixteen Equal Weights."""
        W = PartiallySortedArray([10]*16)
        T = dvlCodeTree(W)
        self.assertEqual(T.weight(),W.rangeSum(0,len(W)))        
        L = T.depths()
        self.assertEqual(L,[4]*16)
        
    def test_TREE6(self):
        """Alpha Equal One. Eight Similar Weights."""
        W = PartiallySortedArray([10,11,12,13,14,15,16,17])
        T = dvlCodeTree(W)
        L = T.depths()
        self.assertEqual(L,[3]*8)
        
    def test_TREE7(self):
        """Alpha Equal One. Three Equal Weights."""
        W = PartiallySortedArray([10]*3)
        T = dvlCodeTree(W)
        self.assertEqual(str(T),"(30,[10],(20,[select(0)],[select(1)]))")
        L = T.depths()
        self.assertEqual(L,[1,2,2])
        
    def test_TREE8(self):
        """Alpha Equal One. Three Similar Weights."""
        W = PartiallySortedArray([12,11,10])
        T = dvlCodeTree(W)
        self.assertEqual(str(T),"(33,[12],(21,[select(0)],[select(1)]))")
        L = T.depths()
        self.assertEqual(L,[1,2,2])
        
    def test_TREE9(self):
        """Alpha Equal Two. Single very small weight."""
        W = PartiallySortedArray([1]+[8]*3)
        T = dvlCodeTree(W)
        L = T.depths()
        self.assertEqual(L,[2]*4)
        
    def test_TREE10(self):
        """Exponential Sequence."""
        W = PartiallySortedArray([1,2,4])
        T = dvlCodeTree(W)
        self.assertEqual(str(T),'(7,(3,[select(0)],[select(1)]),[4])')
        L = T.depths()
        self.assertEqual(sorted(L),[1,2,2])

    def test_TREE12(self):
        """Exponential Sequence."""
        W = PartiallySortedArray([1,2,4,8,16,32,64,128,256])
        T = dvlCodeTree(W)
        self.assertEqual(T.toStringWithAllWeightsCalculated(),'(511,(255,(127,(63,(31,(15,(7,(3,[1],[2]),[4]),[8]),[16]),[32]),[64]),[128]),[256])')
        L = T.depths()
        self.assertEqual(sorted(L),[1,2,3,4,5,6,7,8,8])

    
class DVLTest(unittest.TestCase):
    """Basic tests for the DVL algorithm computing optimal prefix free codes.

    """        
    def test(self):
        """Generic test"""
        testPFCAlgorithm(dvl, "DVL")
    def testFourEqualWeights(self):
        """Four Equal Weights"""
        self.assertEqual(dvl([1,1,1,1]),[2,2,2,2])
    def testEightEqualWeights(self):
        """Eight Equal Weights"""
        self.assertEqual(dvl([1]*8),[3]*8)
    def test_ExponentialSequence(self):
        """Exponential Sequence. (No docking required ever)"""
        W = [1,2,4,8,16,32,64,128,256]
        self.assertEqual(sorted(dvl(W)),sorted(vanLeeuwen(W)))
    def test_SuperExponentialSequence(self):
        """Super Exponential Sequence. (Still no docking required ever)"""
        W = [1,4,16,64,256]
        self.assertEqual(sorted(dvl(W)),sorted(vanLeeuwen(W)))
    def test_ExponentialSequenceWithLongSteps(self):
        """Exponential Sequence With Long Steps."""
        W = [1,1,2,2,4,4,8,8,16,16,32,32,64,64,128,128,256,256]
        self.assertEqual(sorted(dvl(W)),sorted(vanLeeuwen(W)))
    def test_ExponentialSequenceWithVeryLongSteps(self):
        """Exponential Sequence With Very Long Steps."""
        W = [1,1,1,1,2,2,2,2,4,4,4,4,8,8,8,8,16,16,16,16,32,32,32,32,64,64,64,64,128,128,128,128,256,256,256,256]
        self.assertEqual(sorted(dvl(W)),sorted(vanLeeuwen(W)))
    def test_SequenceRequiringMixing(self):
        """Sequence requiring Mixing."""
        W = [32,33,33,34,34,35,35,36,36,37,37,38,38,39,39,40,40,63,63,64,64,66,68,70,72,74,126]
        self.assertEqual(sorted(dvl(W)),sorted(vanLeeuwen(W)))
    def test_AlphaEqualTwoWithMinorMixing(self):
        """Alpha Equal Two. Minor Mixing between Internal Nodes and External Nodes"""
        W = [1]*8+[7]*3
        L = dvl(W)
        self.assertEqual(sorted(L),[2]*3+[5]*8)
    def test_AlphaEqualTwoTightMatch(self):
        """Alpha Equal Two. Tight match between Internal Node and External Node"""
        W = [1]*8+[8]*3
        L = dvl(W)
        self.assertEqual(sorted(L),[2]*3+[5]*8)
    def test_AlphaEqualTwoLargeGap(self):
        """Alpha Equal Two. Large gab between the weight of the Internal Node and the weights of the largest external nodes."""
        W = [1]*8+[32]*3
        L = dvl(W)
        self.assertEqual(sorted(L),[2]*3+[5]*8)
    def test_AlphaEqualThreeWithoutMixing(self):
        """Alpha Equal Three with no Mixing."""
        W = [1]*4+[4]*3+[16]*3
        L = dvl(W)
        self.assertEqual(sorted(L),[2]*3+[4]*3+[6]*4)
    def test_AlphaEqualFourWithoutMixing(self):
        """Alpha Equal Three with no Mixing."""
        W = [1]*4+[4]*3+[16]*3+[128]*3
        L = dvl(W)
        self.assertEqual(sorted(L),sorted(vanLeeuwen(W)))

        
def main():
    unittest.main()
if __name__ == '__main__':
    doctest.testmod()
    main()
            
        

