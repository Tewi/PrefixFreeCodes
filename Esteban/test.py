import unittest
import Huffman


class TestBorder(unittest.TestCase):

    def test_empty(self):
        elements = []
        expected = {}
        for x in xrange(2, 10):
            result = (Huffman.code(elements, x))
            self.assertEqual(result, expected)

    def test_oneElement(self):
        elements = [('a', 4)]
        expected = {'a': "0"}
        for x in xrange(2, 10):
            result = (Huffman.code(elements, x))
            self.assertEqual(result, expected)

    # tests con algunos pesos sin sentido, el algoritmo deberia seguir
    # funcionando pero cosas como el largo promedio de los mensages no pueden
    # dar un valor correcto (no tendria sentido)
    def test_unusualWeights(self):
        elements = [
            ('a', -4),
            ('b', 0),
            ('c', 18.3),
            ('d', 9)
        ]
        expected = {
            'a': "111",
            'b': "110",
            'c': "0",
            'd': "10"
        }
        result = (Huffman.code(elements, 2))
        self.assertEqual(result, expected)

    # D = 1 -> invalido
    def test_lowOutputAlphabet(self):
        with self.assertRaises(Exception) as context:
            Huffman.code([], 1)
    # D = 11 -> invalido
    def test_highOutputAlphabet(self):
        with self.assertRaises(Exception) as context:
            Huffman.code([], 11)


class TestBinary(unittest.TestCase):

    def test_oneElement(self):
        elements = [('a', 4)]
        expected = {'a': "0"}
        result = (Huffman.code(elements, 2))
        self.assertEqual(result, expected)

    def test_twoElements(self):
        elements = [
            ('a', 4),
            ('b', 3)
        ]
        expected = {
            'a': '0',
            'b': '1'
        }
        result = (Huffman.code(elements, 2))
        self.assertEqual(result, expected)

    def test_threeElements(self):
        elements = [
            ('a', 4),
            ('b', 3),
            ('c', 6)
        ]
        expected = {
            'a': "00",
            'b': "01",
            'c': "1"
        }
        result = (Huffman.code(elements, 2))
        self.assertEqual(result, expected)

    def test_fourElements(self):
        elements = [
            ('a', 4),
            ('b', 3),
            ('c', 6),
            ('d', 8)
        ]
        expected = {
            'a': "000",
            'b': "001",
            'c': "01",
            'd': "1"
        }
        result = (Huffman.code(elements, 2))
        self.assertEqual(result, expected)

    # test binario del paper, se compara usando el largo optimo
    def test_paperExample(self):
        elements = [
            ('1', 0.20),
            ('2', 0.18),
            ('3', 0.10),
            ('4', 0.10),
            ('5', 0.10),
            ('6', 0.06),
            ('7', 0.06),
            ('8', 0.04),
            ('9', 0.04),
            ('10', 0.04),
            ('11', 0.04),
            ('12', 0.03),
            ('13', 0.01)
        ]
        expected = 3.42
        result = (Huffman.averageMessageLength(elements, 2))
        self.assertAlmostEqual(result, expected) #comparacion de floats

class TestGeneralized(unittest.TestCase):

    #  mismo numero de elementos que D con la misma probabilidad,
    # deberian estar todos a la misma altura
    def test_sameWeigths(self):
        elements = []
        for x in range(10):
            elements.append( (str(x), 1) )
        expected = 1
        result = Huffman.averageMessageLength(elements, 10)
        self.assertAlmostEqual(result, expected)

    def test_fourTernary(self):
        elements = [
            ('a', 4),
            ('b', 3),
            ('c', 6),
            ('d', 8)
        ]
        expected = {
            'a': "10",
            'b': "11",
            'c': "2",
            'd': "0"
        }
        result = (Huffman.code(elements, 3))
        self.assertEqual(result, expected)

    # test cuaternario del paper
    def test_paperExample(self):
        elements = [
            ('1', 0.22),
            ('2', 0.20),
            ('3', 0.18),
            ('4', 0.15),
            ('5', 0.10),
            ('6', 0.08),
            ('7', 0.05),
            ('8', 0.02)
        ]
        expected = {
            '1': "1",
            '2': "2",
            '3': "3",
            '4': "00",
            '5': "01",
            '6': "02",
            '7': "030",
            '8': "031"
        }
        result = (Huffman.code(elements, 4))
        self.assertEqual(result, expected)




if __name__ == '__main__':
    unittest.main()
