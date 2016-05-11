import doctest,os
from collections import Counter
from alternationMeasure import EISignature,EIAlternation

def countFrequenciesInFile(filename):
    """Given a file name, compute the frequencies of the words in the corresponding file.

>>> f = countFrequenciesInFile("../DataSets/shakespeare.txt")
>>> print(f[0])
('the', 23407)
"""
    words = Counter()
    with open(filename) as f:
        for line in f:      
            words.update(line.split())
    return words.most_common()

