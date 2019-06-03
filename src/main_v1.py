import numpy as np
import csv
import sys
import math
from pprint import pprint

# vetor de observações
fatores = []

# abre o arquivo de fatores
with open(sys.argv[1]) as arq:
    reader = csv.DictReader(arq)
    for i, row in enumerate(reader):
        row['alias'] = i+1
        fatores.append(row)

# numero de fatores
numberOfK = len(fatores)
# cria a matriz com 1's
matrix = np.ones((2 ** numberOfK, 2 ** numberOfK))

# converte um numero intero para binario


def intToBinary(maxValue, size):
    ans = [int(d) for d in str(bin(maxValue)[2:].zfill(size))]
    return ans
    str.zfill()


# preenche as k+1 primeiras colunas da matriz com o binário do numero e os troca para -1 ou 1
for line in range(0, 2**numberOfK):
    matrix[line][1:numberOfK + 1] = intToBinary(line, numberOfK)
    lineMatrix = matrix[line][1:numberOfK + 1]
    # transforma 0 do numero binario em -1
    matrix[line][1:numberOfK +
                 1] = [-1 if (number == 0) else 1 for number in lineMatrix]


def anagrams(s):
    # Return the list of anagrams for s
    if s == "":
        return [s]
    else:
        ans = []
        for w in anagrams(s[1:]):
            for pos in range(len(w) + 1):
                ans.append(w[:pos] + s[0] + w[pos:])
        return ans


# monta o número para gerar as combinações
number = ''
for i in range(1, numberOfK + 1):
    number += str(i)

# pega todas as combinações de números, de 1 até k
lst = []
lst.append(number)  # inclui a combinação maior, que é o proprio número
for perm in range(0, numberOfK - 1):
    for anagram in anagrams(number):
        lst.append(anagram[0:perm + 1])

# ordena numeros gerados nas combinações, para excluir numeros repetidos
# ex: 12 e 21, apos ordenar ficaria 12, 12
lstOrdered = []
lstAux = []
for number in lst:
    for n in number:
        lstAux.append(n)
    lstAux = sorted(lstAux)
    lstAux = ''.join(lstAux)
    lstOrdered.append(lstAux)
    lstAux = []


def removeDuplicates(lst):
    return list(dict.fromkeys(lst))


# remove duplicatas
setOrdered = sorted(removeDuplicates(lstOrdered), key=len)
setOrdered = [number if len(number) > 1 else '' for number in setOrdered]
while ('' in setOrdered):
    setOrdered.remove('')

setOrdered = sorted([int(num) for num in setOrdered])

# multiplica indices
for line in range(0, 2**numberOfK):
    mult = 1
    for i, num in enumerate(setOrdered):
        # para cada combinação, acessa o indice na matriz e o multiplica
        for idx in str(num):
            mult *= matrix[line][int(idx)]
        # recebe o resultado da multiplicação, o vetor de combinações tem o mesmo
        # tamanho que o vetor de [numberOfK + 1:] presente na matriz
        matrix[line][numberOfK + 1:][i] = mult
        mult = 1


def getFator(alias):
    """
    função que recupera o fator de acordo com seu apelido
    ex de apelido: 1, 2, 3 ...
    """
    for fator in fatores:
        if (fator['alias'] == alias):
            return fator


# faz as perguntas para as observações e armazena os valores
obs = []
stringPergunta = ''
print('Digite os valores do experimento:')
for pergunta in matrix:
    pergunta = pergunta[1:numberOfK + 1]
    for i, numberAlias in enumerate(pergunta):
        fator = getFator(i+1)
        stringPergunta += '%s=%s; \n' % (
            fator['nomeFator'], fator['valorMinimo'] if numberAlias == -1 else fator['valorMaximo'])
    stringPergunta += "??? \nDigite pause, para parar de digitar os valores. \n"
    print(stringPergunta)

    valores = float(input())
    obsAux = []
    while (valores != "pause"):
        mean += float(valores)
        obsAux.append(float(valores))
        valores = input()

    # guarda os valores dos experimentos em um vetor de vetores
    obs.append(obsAux)
    stringPergunta = ''

# tira a media dos valores dos experimentos e os salva em um vetor
obsMean = np.array([np.array(numArr).mean() for numArr in obs])
# multiplica as colunas com o vetor de y, somando os valores ao final
matrixTranspose = matrix.transpose()
newResult = []
for line in matrixTranspose:
    aux = line * obsMean
    pesoAtual = np.sum(aux)
    pesoAtual = pesoAtual / len(obsMean)
    newResult.append(pesoAtual)

# criando o novo conjunto de combinações, com os numeros 1, 2, 3, ...
# e as combinações, 12, 13, 123, 1234 ...
newSetOrdered = []
for n in range(1, numberOfK+1):
    newSetOrdered.append(n)
for n in setOrdered:
    newSetOrdered.append(n)

# calculo do sst, pagina 23 do slide de AVD
mediaObs = obsMean.mean()
sst = 0
for n in range(0, len(obs)):
    sst += (obsMean[n] - mediaObs) ** 2

importancia = []
# exlui a primeira posição, pois é a importancia da coluna I
newResult = newResult[1:]
for n in newResult:
    importancia.append(2 ** numberOfK * n ** 2)  # pagina 20 do slide de AVD

importancia = (importancia / sst) * 100  # transforma em porcentagem
importancia = [round(n, 2) for n in importancia]


def getNomeInteracao(num):
    """
    Retorna uma string com o nome das interações dos fatores
    ex:
    memória;
    cache;
    memoria;cache;
    """
    num = str(num)
    nameFator = ''
    for numFator in num:
        for fator in fatores:
            if (int(numFator) == fator['alias']):
                nameFator += fator['nomeFator'] + ';'
    return nameFator


# cálculo do erro
matrixError = np.matrix(obs)  # transforma o vetor de observações em matriz
erro = 0
for i, line in enumerate(matrixError):
    # diferença do valor estimado para o valor medido, valor estimado é a média
    erroAux = np.subtract(line, obsMean[i])
    erroAux = np.power(erroAux, 2)  # eleva todos os valores ao quadrado
    erro += np.sum(erroAux)  # soma todos os valores

# adiciona o erro ao SST, como mostrado no slide 32
sst += erro

print('Resultado das importâncias dos valores são:')
print('------')
for i, interacao in enumerate(newSetOrdered):
    print(getNomeInteracao(interacao), str(importancia[i]) + "%")
print('erro;', str(round((erro/sst)*100, 2)) + "%")
print('------')
