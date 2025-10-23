from nos import *
from eval import *
from stds import stdFuncs, stdHandler

def execute(nodes: list, variaveis: dict, funcoes: dict, nodesIndex: dict) -> None:
    environment = [variaveis]
    lastConditionalResult = {}
    errorImmunity = []

    def execErro(erro: Erro) -> None|int:
        if not errorImmunity:
            erro.execErr()
        else:
            nodePos = nodesIndex[errorImmunity[-1].fim]
            if errorImmunity[-1].resultVar is not None:
                environment[-1][errorImmunity[-1].resultVar].valor = 1
            errorImmunity.pop()
            return nodePos

    def evaluate(node: object, operation: object) -> any:
        return Eval(variaveis=environment[-1], askNode=node).executeAst(operationAst=operation, variaveis=environment[-1])

    nodePos = 0
    while nodePos < len(nodes):
        node = nodes[nodePos]
        
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
                    nodePos = execErro(Erro(linha=node.linha, tipo="Result sem função."))
                else:
                    if node.retorno is not None:
                        node.valor = evaluate(node, node.retorno)
                    if isinstance(node.valor, Erro):
                        nodePos = execErro(node.valor)
                    else:
                        if node.valor is not None:
                            funcoes[node.funcaoPai].caller[-1].valor = node.valor
                        environment.pop()
                        nodePos = nodesIndex[funcoes[node.funcaoPai].caller[-1]]
                        funcoes[node.funcaoPai].caller.pop()

            case Function():
                nodePos = nodesIndex[node.fim]

            case Execute():
                nodeArgumentosExist = node.argumentos is None
                foundErrorInArgs = False
                args = None
                if not nodeArgumentosExist:
                    args = []
                    for arg in node.argumentos:
                        if arg in environment[-1]:
                            args.append(environment[-1][arg].valor)
                        elif isinstance(arg, Operacao):
                            args.append(evaluate(node, arg))
                            if isinstance(args[-1], Erro):
                                nodePos = execErro(args[-1])
                                foundErrorInArgs = True
                        else:
                            args.append(arg)
                            if isinstance(args[-1], Erro):
                                nodePos = execErro(args[-1])
                                foundErrorInArgs = True

                if not foundErrorInArgs:
                    if node.execWho not in funcoes:
                        if node.execWho in stdFuncs():
                            result = stdHandler(node, environment[-1], args)
                            if isinstance(result, Erro):
                                nodePos = execErro(result)
                            else:
                                node.valor = result
                        else:
                            nodePos = execErro(Erro(linha=node.linha, tipo="Funcao inexistente."))
                    elif (funcoes[node.execWho].argumentos is None) != (nodeArgumentosExist):
                        nodePos = execErro(Erro(linha=node.linha, tipo="Quantia de argumentos indevida."))
                    elif (not nodeArgumentosExist) and (type(funcoes[node.execWho].argumentos) != type(args)):
                        nodePos = execErro(Erro(linha=node.linha, tipo="Quantia de argumentos indevida."))
                    elif (not nodeArgumentosExist) and (len(funcoes[node.execWho].argumentos) != len(args)):
                        nodePos = execErro(Erro(linha=node.linha, tipo="Quantia de argumentos indevida."))
                    else:
                        newEnv = {}
                        for var in funcoes[node.execWho].environment:
                            newEnv[var] = funcoes[node.execWho].environment[var].copy()
                            newEnv[var].valor = None
                        if args is not None:
                            for i, var in enumerate(funcoes[node.execWho].argumentos):
                                if args[i] in environment[-1]:
                                    newEnv[var].valor = environment[-1][args[i]].valor
                                else:
                                    newEnv[var].valor = args[i]

                        environment.append(newEnv)
                        funcoes[node.execWho].caller.append(node)
                        nodePos = nodesIndex[funcoes[node.execWho].corpo]-1

            case Apply():
                prevIndex = nodesIndex[node]-1
                if node.variavel not in environment[-1]:
                    nodePos = execErro(Erro(linha=node.linha, tipo="Apply em variavel não declarada."))
                elif not isinstance(nodes[prevIndex], Execute):
                    nodePos = execErro(Erro(linha=node.linha, tipo="Comando antes de apply não é execute."))
                else:
                    if nodes[prevIndex].valor is not None:
                        environment[-1][node.variavel].valor = nodes[prevIndex].valor

            case Adopt():
                if node.variavel not in environment[0]:
                    nodePos = execErro(Erro(linha=node.linha, tipo="Tentativa de adopt com variavel fora do escopo global."))
                else:
                    environment[-1][node.variavel] = environment[0][node.variavel]
                pass

            case WhileLoop():
                sucessoCondicional = evaluate(node, node.pergunta)
                if isinstance(sucessoCondicional, Erro):
                    nodePos = execErro(sucessoCondicional)
                else:
                    lastConditionalResult[node.depth] = sucessoCondicional
                    if sucessoCondicional != 1:
                        nodePos = nodesIndex[node.fim]
            
            case BreakLoop():
                if node.loopPai == None:
                    nodePos = execErro(Erro(linha=node.linha, tipo="Comando break fora de loop."))
                else:
                    nodePos = nodesIndex[node.loopPai.fim]
                    
            case EndLoop():
                nodePos = nodesIndex[node.loopPai]-1

            case Setter():
                foundErrorInData = False
                processed = node.setto
                if isinstance(node.setto, list):
                    processed = []
                    for j in range(len(node.setto)):
                        processed.append(evaluate(node, node.setto[j]))
                        if isinstance(processed[-1], Erro):
                            nodePos = execErro(processed[-1])
                            foundErrorInData = True

                elif isinstance(node.setto, dict):
                    processed = {}
                    for key in node.setto:
                        processedValue = evaluate(node, node.setto[key])
                        if isinstance(processedValue, Erro):
                            nodePos = execErro(processedValue)
                            foundErrorInData = True
                        processed[key] = processedValue
                        
                if not foundErrorInData:
                    valor = evaluate(node, processed)
                    if isinstance(valor, Erro):
                        nodePos = execErro(valor)
                    else:
                        environment[-1][node.setwho].valor = valor

            case Show():
                result = node.show(environment[-1])
                if isinstance(result, Erro):
                    nodePos = execErro(result)
        
            case Get():
                environment[-1][node.setwho].valor = node.get()

            case ConditionalIf():
                sucessoCondicional = evaluate(node, node.pergunta)
                if isinstance(sucessoCondicional, Erro):
                    nodePos = execErro(sucessoCondicional)
                else:
                    lastConditionalResult[node.depth] = sucessoCondicional
                    if sucessoCondicional == 1:
                        nodePos = nodesIndex[node.corpo]-1
                    else:
                        nodePos = nodesIndex[node.fim]

            case ConditionalElse():
                if node.depth in lastConditionalResult:
                    if lastConditionalResult[node.depth] != 1:
                        sucessoCondicional = evaluate(node, node.pergunta)
                        if isinstance(sucessoCondicional, Erro):
                            nodePos = execErro(sucessoCondicional)
                        else:
                            lastConditionalResult[node.depth] = sucessoCondicional
                            if sucessoCondicional == 1:
                                nodePos = nodesIndex[node.corpo]-1
                            else:
                                nodePos = nodesIndex[node.fim]
                    else:
                        nodePos = nodesIndex[node.fim]
                else:
                    nodePos = nodesIndex[node.fim]

            case Else():
                if node.depth in lastConditionalResult:
                    if lastConditionalResult[node.depth] != 1:
                        lastConditionalResult[node.depth] = 1
                        nodePos = nodesIndex[node.corpo]-1
                    else:
                        nodePos = nodesIndex[node.fim]
                else:
                    nodePos = nodesIndex[node.fim]
            
            case Exit():
                return

        nodePos += 1
    return