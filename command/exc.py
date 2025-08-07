import sys
from nos import *
from eval import *
import time as Time

def execute(nodes, variaveis, funcoes, nodesIndex):    
    #for i, node in enumerate(nodes):
        #print(i+1, ":", node)
    environment = [variaveis]
    lastConditionalResult = {}
    errorImmunity = []

    def execErro(erro):
        if not errorImmunity:
            erro.execErr()
        else:
            i = nodesIndex[errorImmunity[-1].fim]
            if errorImmunity[-1].resultVar is not None:
                environment[-1][errorImmunity[-1].resultVar].valor = 1
            errorImmunity.pop()
            return i

    i = 0
    while i < len(nodes):
        node = nodes[i]
        if not isinstance(node, (Conditional, Loop, Dummy)):
            lastConditionalResult[node.depth] = 1
        match node:
            case Check():
                errorImmunity.append(node)
                if node.resultVar is not None:
                    environment[-1][node.resultVar].valor = 0

            case EndCheck():
                if errorImmunity:
                    errorImmunity.pop()

            case Result():
                if node.funcaoPai is None:
                    i = execErro(Erro(linha=node.linha, tipo="Result sem função."))
                if node.retorno is not None:
                    node.valor = Eval(variaveis=environment[-1], askNode=node).executeAst(operationAst=node.retorno, variaveis=environment[-1])
                    if isinstance(node.valor, Erro):
                        i = execErro(node.valor)


                funcoes[node.funcaoPai].caller[-1].valor = node.valor

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


                    if not(funcoes[node.execWho].argumentos is None and node.argumentos is None):
                        if type(funcoes[node.execWho].argumentos) != type(node.argumentos):
                            i = execErro(Erro(linha=node.linha, tipo="Quantia de argumentos indevida."))
                        elif len(funcoes[node.execWho].argumentos) != len(node.argumentos):
                            i = execErro(Erro(linha=node.linha, tipo="Quantia de argumentos indevida."))
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
                    i = execErro(Erro(linha=node.linha, tipo="Funcao inexistente."))

            case Apply():
                prevIndex = nodesIndex[node]-1
                if node.variavel not in environment[-1]:
                    i = execErro(Erro(linha=node.linha, tipo="Apply em variavel não declarada."))
                if not isinstance(nodes[prevIndex], Execute):
                    i = execErro(Erro(linha=node.linha, tipo="Comando antes de apply não é execute."))
                if nodes[prevIndex].valor is not None:
                    environment[-1][node.variavel].valor = nodes[prevIndex].valor

            case WhileLoop():
                sucessoCondicional = Eval(variaveis=environment[-1], askNode=node).executeAst(operationAst=node.pergunta, variaveis=environment[-1])
                if isinstance(sucessoCondicional, Erro):
                    i = execErro(sucessoCondicional)
                lastConditionalResult[node.depth] = sucessoCondicional
                if sucessoCondicional != 1:
                    i = nodesIndex[node.fim]
            
            case BreakLoop():
                if node.loopPai == None:
                    i = execErro(Erro(linha=node.linha, tipo="Comando break fora de loop."))
                i = nodesIndex[node.loopPai.fim]

            case EndLoop():
                i = nodesIndex[node.loopPai]-1

            case Setter():
                valor = Eval(variaveis=environment[-1], askNode=node).executeAst(operationAst=node.setto, variaveis=environment[-1])
                if isinstance(valor, Erro):
                    i = execErro(valor)
                environment[-1][node.setwho].valor = valor

            case Edit():
                if node.setwho not in environment[-1]:
                    i = execErro(Erro(linha=node.linha, tipo="Comando edit com variável não declarada."))
                if not(isinstance(environment[-1][node.setwho].valor, (list, dict, str))):
                    i = execErro(Erro(linha=node.linha, tipo="Comando edit com variável de tipo proibído."))

                if node.index != None and node.setto != None:
                    index = Eval(variaveis=environment[-1], askNode=node).executeAst(operationAst=node.index, variaveis=environment[-1])
                    setto = Eval(variaveis=environment[-1], askNode=node).executeAst(operationAst=node.setto, variaveis=environment[-1])
                    if isinstance(index, Erro):
                        i = execErro(index)
                    elif isinstance(setto, Erro):
                        i = execErro(setto)
                    elif not isinstance(index, int):
                        i = execErro(Erro(linha=node.linha, tipo="Posição deve ser um número inteiro."))
                    elif isinstance(environment[-1][node.setwho].valor, str) != isinstance(setto, str) and node.mode not in {"delete"}:
                        i = execErro(Erro(linha=node.linha, tipo="Valor deve ser também uma string."))
                    elif (index < 0 and abs(index) > len(environment[-1][node.setwho].valor)) or index >= len(environment[-1][node.setwho].valor):
                        i = execErro(Erro(linha=node.linha, tipo="Posição maior que tamanho da variável."))
                    else:
                        if node.mode == "insert":
                            if isinstance(environment[-1][node.setwho].valor, str):
                                valor = list(environment[-1][node.setwho].valor)
                                valor.insert(index, setto)
                                environment[-1][node.setwho].valor = ''.join(valor)
                            else:
                                environment[-1][node.setwho].valor.insert(index, setto)

                        if node.mode == "delete":
                            if isinstance(environment[-1][node.setwho].valor, str):
                                valor = list(environment[-1][node.setwho].valor)
                                del valor[index]
                                environment[-1][node.setwho].valor = ''.join(valor)
                            else:
                                del environment[-1][node.setwho].valor[index]

                        if node.mode == "set":
                            if isinstance(environment[-1][node.setwho].valor, str):
                                valor = list(environment[-1][node.setwho].valor)
                                valor[index] = setto
                                environment[-1][node.setwho].valor = ''.join(valor)
                            else:
                                environment[-1][node.setwho].valor[index] = setto

            case Show():
                result = node.show(environment[-1])
                if isinstance(result, Erro):
                    i = execErro(result)
        
            case Get():
                environment[-1][node.setwho].valor = node.get()

            case ConditionalIf():
                sucessoCondicional = Eval(variaveis=environment[-1], askNode=node).executeAst(operationAst=node.pergunta, variaveis=environment[-1])
                if isinstance(sucessoCondicional, Erro):
                    i = execErro(sucessoCondicional)
                lastConditionalResult[node.depth] = sucessoCondicional
                if sucessoCondicional == 1:
                    i = nodesIndex[node.corpo]-1
                else:
                    i = nodesIndex[node.fim]

            case ConditionalElse():
                if lastConditionalResult[node.depth] != 1:
                    sucessoCondicional = Eval(variaveis=environment[-1], askNode=node).executeAst(operationAst=node.pergunta, variaveis=environment[-1])
                    if isinstance(sucessoCondicional, Erro):
                        i = execErro(sucessoCondicional)
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

        i += 1
    return