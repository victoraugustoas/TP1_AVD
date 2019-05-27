# TP1 - Avaliação de Desempenho
## Como utilizar
#### Entradas
O programa aceita como entrada um arquivo csv separado por vírgula. Nesse arquivo estarão os nomes dos fatores e os valores mínimos e máximos respectivamente. O arquivo é fornecido como argumento para a execução do programa.

Ex:
```
nomeFator,valorMinimo,valorMaximo
memória,4,16
cache,1,2
processador,1,2
```
## Execução do Programa
O programa pode ser executado com o seguinte comando no terminal de sistemas unix, passando como argumento o arquivo que contém as informações dos fatores.
```console
python3 main.py fatores.csv
```
## Utilização do programa
A utilização do programa é feita da seguinte forma:
1. Deverá existir um arquivo que descreve os fatores, com seus valores minimos e máximos
1. Durante a execução do programa, haverá uma série de perguntas que serão feitas ao usuário, essas perguntas são referentes aos experimentos feitos com aquela combinação de valores.
Ex. de pergunta:
```
Digite os valores do experimento:
memória=4; 
cache=1; 
processador=1; 
??? 
Digite pause, para parar de digitar os valores.
14
```
**Obs: Como o programa implementa a versão 2^(K)r, então o usuário irá digitar quantos valores necessários feitos durante o experimento, o *r* será calculado durante a introdução de valores do usuário**
**
Para r=2**
Ex. de pergunta:
```
Digite os valores do experimento:
memória=4; 
cache=1; 
processador=1; 
??? 
Digite pause, para parar de digitar os valores.
14
25
pause
```
**Para r=3**
Ex. de pergunta:
```
Digite os valores do experimento:
memória=4; 
cache=1; 
processador=1; 
??? 
Digite pause, para parar de digitar os valores.
14
25
18
pause
```
1. Após as perguntas, o programa exibirá os respectivos valores de importância que cada fator tem no sistema.
Exemplo de saída:
```
Resultado das importâncias dos valores são:
memória; 17.73%
cache; 4.43%
processador; 70.92%
memória;cache; 4.43%
memória;processador; 0.71%
cache;processador; 1.6%
memória;cache;processador; 0.18%
```