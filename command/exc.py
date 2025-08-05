import sys
from nos import *
from eval import *
import time as Time

def execute(nodes, variaveis, funcoes, nodesIndex):
    environment = [variaveis]
    lastConditionalResult = {}
    i = 0 
    while i < len(nodes):
        node = nodes[i]
        if not isinstance(node, (Conditional, Loop, Dummy)):
            lastConditionalResult[node.depth] = 1
        match node:
            case Result():
                if node.funcaoPai is None:
                    Erro(linha=node.linha, tipo="Result sem função.")
                if node.retorno is not None:
                    node.valor = Eval(variaveis=environment[-1], askNode=node).executeAst(operationAst=node.retorno, variaveis=environment[-1])

                funcoes[node.funcaoPai].caller[-1].valor = node.valor
                #print(funcoes[node.funcaoPai].caller[-1].linha)

                environment.pop()
                i = nodesIndex[funcoes[node.funcaoPai].caller[-1]]
                funcoes[node.funcaoPai].caller.pop()

            case Function():
                i = nodesIndex[node.fim]

            case Execute():
                if node.execWho in funcoes:
                    newEnv = {}
                    for env in funcoes[node.execWho].environment:
                        newEnv[env] = funcoes[node.execWho].environment[env].copy()


                    if type(funcoes[node.execWho].argumentos) != type(node.argumentos) or len(funcoes[node.execWho].argumentos) != len(node.argumentos):
                        Erro(linha=node.linha, tipo="Quantia de argumentos indevida.")
                    else:
                        for i, var in enumerate(funcoes[node.execWho].argumentos):
                            if node.argumentos[i] in environment[-1]:
                                newEnv[var].valor = environment[-1][node.argumentos[i]].valor
                            else:
                                newEnv[var].valor = node.argumentos[i]

                    environment.append(newEnv)
                    funcoes[node.execWho].caller.append(node)
                    i = nodesIndex[funcoes[node.execWho].corpo]-1
                else:
                    Erro(linha=node.linha, tipo="Funcao inexistente.")

            case Apply():
                prevIndex = nodesIndex[node]-1
                if node.variavel not in environment[-1]:
                    Erro(linha=node.linha, tipo="Apply em variavel não declarada.")
                if not isinstance(nodes[prevIndex], Execute):
                    Erro(linha=node.linha, tipo="Comando antes de apply não é execute.")
                if nodes[prevIndex].valor is not None:
                    environment[-1][node.variavel].valor = nodes[prevIndex].valor

            case WhileLoop():
                sucessoCondicional = Eval(variaveis=environment[-1], askNode=node).executeAst(operationAst=node.pergunta, variaveis=environment[-1])
                lastConditionalResult[node.depth] = sucessoCondicional
                if sucessoCondicional != 1:
                    i = nodesIndex[node.fim]

            case Setter():
                environment[-1][node.setwho].valor = Eval(variaveis=environment[-1], askNode=node).executeAst(operationAst=node.setto, variaveis=environment[-1])

            case Edit():
                if node.setwho not in environment[-1]:
                    Erro(linha=node.linha, tipo="Comando edit com variável não declarada.")
                if not(isinstance(environment[-1][node.setwho].valor, (list, dict))):
                    Erro(linha=node.linha, tipo="Comando edit com variável de tipo proibído.") 

                if node.index != None and node.setto != None:
                    index = Eval(variaveis=environment[-1], askNode=node).executeAst(operationAst=node.index, variaveis=environment[-1])
                    setto = Eval(variaveis=environment[-1], askNode=node).executeAst(operationAst=node.setto, variaveis=environment[-1])
                    if not isinstance(index, int):
                        Erro(linha=node.linha, tipo="Posição deve ser um número inteiro.")

                if node.mode == "insert":
                    if index == -1:
                        environment[-1][node.setwho].valor.append(setto)
                    else:
                        environment[-1][node.setwho].valor.insert(index, setto)
                if node.mode == "delete":
                    if (index < 0 and abs(index) > len(environment[-1][node.setwho].valor)) or index >= len(environment[-1][node.setwho].valor):
                        Erro(linha=node.linha, tipo="Posição maior que tamanho da variável.")
                    del environment[-1][node.setwho].valor[index]


                if node.mode == "set":
                    if (index < 0 and abs(index) > len(environment[-1][node.setwho].valor)) or index >= len(environment[-1][node.setwho].valor):
                        Erro(linha=node.linha, tipo="Posição maior que tamanho da variável.")
                    environment[-1][node.setwho].valor[index] = setto

            case Show():
                node.show(environment[-1])
        
            case Get():
                environment[-1][node.setwho].valor = node.get()

            case ConditionalIf():
                sucessoCondicional = Eval(variaveis=environment[-1], askNode=node).executeAst(operationAst=node.pergunta, variaveis=environment[-1])
                lastConditionalResult[node.depth] = sucessoCondicional
                if sucessoCondicional == 1:
                    i = nodesIndex[node.corpo]-1
                else:
                    i = nodesIndex[node.fim]

            case ConditionalElse():
                if lastConditionalResult[node.depth] != 1:
                    sucessoCondicional = Eval(variaveis=environment[-1], askNode=node).executeAst(operationAst=node.pergunta, variaveis=environment[-1])
                    lastConditionalResult[node.depth] = sucessoCondicional
                    if sucessoCondicional == 1:
                        i = nodesIndex[node.corpo]-1
                    else:
                        i = nodesIndex[node.fim]
                else:
                    i = nodesIndex[node.fim]

            case Else():
                if lastConditionalResult[node.depth] != 1:
                    lastConditionalResult[node.depth] = 1
                    i = nodesIndex[node.corpo]-1
                else:
                    i = nodesIndex[node.fim]

            case Exit():
                return

            case EndLoop():
                i = nodesIndex[node.loopPai]-1

        i += 1
    return