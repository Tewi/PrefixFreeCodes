from heapq import *
import math


def code(elements, D):
    N = len(elements)
    #Casos bordes
    if D < 2:
        raise Exception("Output alphabet must be at least 2 symbols")
    if D > 10:
        raise Exception("Output alphabet must not exceed 10 symbols")
    if N == 0:
        return {}
    if N == 1:
        return {elements[0][0]: '0'}

    result = dict()
    #armamos arbol D-ary de prefijos
    tree = Tree(elements, D)
    #asignamos los codigos a las hojas del arbol
    assignCodeWords(tree.root, "", result)
    return result

#Average message length
def averageMessageLength(elements, D):
    averageLength = 0
    #sumamos los pesos para calcular la probabilidad de cada mensage
    totalWeights = 0
    for elem in elements:
        totalWeights = totalWeights + elem[1]
    #armamos un diccionario con las probabilidades
    messages = {}
    for elem in elements:
        messages[elem[0]] = elem[1] / float(totalWeights)

    #calculamos el largo buscando en ambos diccionarios
    codes = code(elements, D)
    for key, value in codes.iteritems():
        averageLength += len(value) * messages[key]

    return averageLength

def assignCodeWords(node, prefix, dictionary):
    elem = node[1]
    if type(elem) == type(list()): #Nodo Interno
        for x in range(len(elem)):
            assignCodeWords(elem[x], prefix + str(x), dictionary)
    else: #Hoja
        dictionary[elem] = prefix

#Arbol de Huffman
class Tree:
    def __init__(self, elements, D):
        self.elements = elements
        self.D = D
        # Numero de elementos
        N = len(elements)

        #heap que mantiene ordenados los elementos
        heap = []
        for e in elements:
            heappush(heap, (e[1], e[0])) #poblamos el heap, ordenados por el peso
        # Creamos el primer ensamble auxiliar con mensages de menor probabilidad
        n0 = (N - 2) % (D-1) + 2 # 2 <= n0 <= D
        if n0 > 0:
            children = [] #elementos con pesos decrecientes
            w = 0
            for x in range(n0):
                elem = heappop(heap)
                children.insert(0, elem) #insertamos de forma decreciente
                w += elem[0]
            heappush(heap, (w, children)) #reinsertamos
        # Ahora el resto de los nodos
        while len(heap) > 1:
            children = []
            w = 0
            for x in range(D): # D elementos
                elem = heappop(heap)
                children.insert(0, elem)
                w += elem[0]
            heappush(heap, (w, children))
        #raiz con probabilidad 1 (suma de todos los pesos)
        self.root = heappop(heap)
