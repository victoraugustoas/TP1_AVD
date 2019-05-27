import numpy as np
import csv
import sys
import math
from pprint import pprint

# vetor de observações
fatores = []

with open(sys.argv[1]) as arq:
    # reader = csv.reader(arq)
    reader = csv.DictReader(arq)
    for i, row in enumerate(reader):
        # aux = {
        #     "name": row[0],
        #     "alias": i+1,
        #     "min": row[1],
        #     "max": row[2]
        # }
        row['alias'] = i+1
        fatores.append(row)

numberOfK = len(fatores)
matrix = np.ones((2 ** numberOfK, 2 ** numberOfK))


def intToBinary(maxValue, size):
    ans = [int(d) for d in str(bin(maxValue)[2:].zfill(size))]
    return ans
    str.zfill()


# preenche as k+1 primeiras colunas da matriz com o binário do numero e os troca para -1 ou 1
for line in range(0, 2**numberOfK):
    matrix[line][1:numberOfK + 1] = intToBinary(line, numberOfK)
    lineMatrix = matrix[line][1:numberOfK + 1]
    # transforma 0 em -1
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

# pega todas as combinações de numeros, de zero até k
lst = []
lst.append(number)
for perm in range(0, numberOfK - 1):
    for anagram in anagrams(number):
        lst.append(anagram[0:perm + 1])

# ordena numeros
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
        for idx in str(num):
            mult *= matrix[line][int(idx)]
        matrix[line][numberOfK + 1:][i] = mult
        mult = 1


def getFator(alias):
    for fator in fatores:
        if (fator['alias'] == alias):
            return fator


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

    valores = int(input())
    mean = 0
    tam = 0
    while (valores != "pause"):
        mean += int(valores)
        tam += 1
        valores = input()

    obs.append(mean/tam)
    stringPergunta = ''

obs = np.array([int(num) for num in obs])
matrixTranspose = matrix.transpose()
newResult = []
for line in matrixTranspose:
    aux = line * obs
    pesoAtual = 0
    for n in aux:
        pesoAtual += n
    pesoAtual = pesoAtual / len(obs)
    newResult.append(pesoAtual)

# criando o novo conjunto de combinações
newSetOrdered = []
for n in range(1, numberOfK+1):
    newSetOrdered.append(n)
for n in setOrdered:
    newSetOrdered.append(n)

# print(newResult, newSetOrdered)

mediaObs = obs.mean()
sst = 0
for n in range(0, len(obs)):
    sst += (obs[n] - mediaObs) ** 2

importancia = []
newResult = newResult[1:]
for n in newResult:
    importancia.append(2 ** numberOfK * n ** 2)

importancia = (importancia / sst) * 100
importancia = [round(n, 2) for n in importancia]


def getNomeInteracao(num):
    num = str(num)
    nameFator = ''
    for numFator in num:
        for fator in fatores:
            if (int(numFator) == fator['alias']):
                nameFator += fator['nomeFator'] + ';'
    return nameFator


print('Resultado das importâncias dos valores são:')
print('------')
for i, interacao in enumerate(newSetOrdered):
    print(getNomeInteracao(interacao), str(importancia[i]) + "%")
print('------')
