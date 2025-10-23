import sys
import os
from nos import *
from eval import *
from exc import execute
import time as Time
sys.set_int_max_str_digits(2147483647)

class Parser:
    def __init__(self, varnodes, nodes, variaveis, funcoes, indexNodes, loadedNodes, path):
        self.varnodes = varnodes
        self.nodes = nodes
        self.variaveis = variaveis
        self.funcoes = funcoes
        self.indexNodes = indexNodes
        self.loadedNodes = loadedNodes
        self.path = path

    def createList(self, tokens: list, node: object) -> list:
        itens = []
        atual = []
        for valor in tokens:
            if valor == ",":
                if atual:
                    itens.append(Eval(variaveis=self.variaveis, askNode=node).createOperationAst(atual))
                    atual = []
            else:
                atual.append(valor)
        if atual:
            itens.append(Eval(variaveis=self.variaveis, askNode=node).createOperationAst(atual))
        return itens

    def parse(self, code, loaders=set()):
        linhas = [x for x in code.split("\n")]
        for i, linha in enumerate(linhas):
            if linha != "":
                tokens = self.getTokens(linha, i)
                if not tokens:
                    continue
                depth = tokens.pop(0)
                if not tokens:
                    continue

                match tokens[0]:
                    case "check":
                        tokens = tokens[2:]
                    
                        resultVar = None
                        if len([x for x in tokens if x != " "]) > 1:
                            Erro(linha=[linha, i+1], tipo="Comando check malformado.").parseErr()
                        if len(tokens) == 1:
                            resultVar = tokens[0]
                            if resultVar not in self.variaveis:
                                Erro(linha=[linha, i+1], tipo="Comando check com variável não-declarada.").parseErr()

                        self.nodes.append(Check(corpo=None, fim=None, resultVar=resultVar, depth=depth, linha=[linha, i+1]))

                    case "load":
                        tokens = tokens[2:]
                        if len([x for x in tokens if x != " "]) != 1:
                            Erro(linha=[linha, i+1], tipo="Comando load malformado.").parseErr()
                        if not os.path.exists(f"{self.path}\\{tokens[0]}.command"):
                            Erro(linha=[linha, i+1], tipo="Script não existe.").parseErr()
                        if tokens[0] in loaders:
                            Erro(linha=[linha, i+1], tipo="Load circular.").parseErr()
                        loaders.add(tokens[0])

                        loaded = Parser(varnodes=[], nodes=[],variaveis={},funcoes={}, indexNodes={}, loadedNodes={}, path=self.path).parse(open(f"{self.path}\\{tokens[0]}.command").read(), loaders=loaders)
                        for node in loaded.nodes:
                            self.nodes.append(node)
                            self.loadedNodes[node] = 0

                        for func in loaded.funcoes:
                            if func in  self.funcoes:
                                Erro(linha=[linha, i+1], tipo=f'Função carregada "{func}" já dentro do script.').parseErr()
                            self.funcoes[func] = loaded.funcoes[func]

                    case "function":
                        tokens = [x for x in tokens if x != " "][1:]

                        argumentos = None
                        environment = {}

                        if len(tokens) == 0:
                            Erro(linha=[linha, i+1], tipo="Funcao sem argumento.").parseErr()
                        if len(tokens) > 1:
                            argumentos = tokens[1:]
                            for var in argumentos:
                                if any(not char.isalpha() for char in var):
                                    Erro(linha=[linha, i+1], tipo="Numero em nome de variável.").parseErr()
                                if var not in self.variaveis:
                                    varNode = Variavel(nome=var, valor=None, linha=[linha, i+1])
                                    self.varnodes.append(varNode)
                                    self.variaveis[var] = varNode
                                if var not in environment:
                                    environment[var] = varNode
                        funcNode = (Function(nome=tokens[0], argumentos=argumentos, corpo=None, fim=None, environment=environment, caller=[], depth=depth, linha=[linha, i+1]))
                        if funcNode.nome in self.funcoes:
                            Erro(linha=[linha, i+1], tipo="Uma função com tal nome já existe.").parseErr()
                        self.funcoes[funcNode.nome] = funcNode 

                        self.nodes.append(funcNode)
                    
                    case "result":
                        tokens = [x for x in tokens if x != " "][1:]

                        resultNode = Result(retorno=None, valor=None, funcaoPai=None, depth=depth, linha=[linha, i+1])
                        if len(tokens) >= 1:
                            resultNode.retorno = Eval(variaveis=self.variaveis, askNode=resultNode).createOperationAst(tokens)
                        self.nodes.append(resultNode)

                    case "execute":
                        tokens = [x for x in tokens if x != " "][1:]
                        argumentos = None
                        if len(tokens) == 0:
                            Erro(linha=[linha, i+1], tipo="Execute sem nome.").parseErr()

                        executeNode = Execute(execWho=tokens[0], argumentos=None, valor=None, depth=depth, linha=[linha, i+1])
                        if len(tokens) > 1:
                            argumentos = (self.createList(tokens=tokens[2:-1], node=executeNode))
                        executeNode.argumentos = argumentos
                        self.nodes.append(executeNode)

                    case "apply":
                        tokens = tokens[2:]

                        if len([x for x in tokens if x != " "]) != 2 or tokens[0:2] != ["to", " "]:
                            Erro(linha=[linha, i+1], tipo="Comando apply malformado.").parseErr()
                        self.nodes.append(Apply(variavel=tokens[2], depth=depth, linha=[linha, i+1]))

                    case "adopt":
                        tokens = tokens[2:]

                        if len([x for x in tokens if x != " "]) != 1:
                            Erro(linha=[linha, i+1], tipo="Comando adopt malformado.").parseErr()
                        self.nodes.append(Adopt(variavel=tokens[0], depth=depth, linha=[linha, i+1]))

                    case "while":
                        tokens = [x for x in tokens if x != " "] 
                        if 1 >= len(tokens):
                            Erro(linha=[linha, i+1], tipo="Loop sem argumento.").parseErr()
                        whileNode = (WhileLoop(pergunta=tokens[1:],corpo=None, fim=None, depth=depth, linha=[linha, i+1]))
                        whileNode.pergunta = Eval(variaveis=self.variaveis, askNode=whileNode).createOperationAst(whileNode.pergunta)
                        self.nodes.append(whileNode)

                    case "break":
                        self.nodes.append(BreakLoop(loopPai=None, depth=depth, linha=[linha, i+1]))

                    case "if":
                        tokens = [x for x in tokens if x != " "] 
                        if 1 >= len(tokens):
                            Erro(linha=[linha, i+1], tipo="Condicional sem argumento.").parseErr()
                        ifNode = (ConditionalIf(pergunta=tokens[1:],corpo=None ,fim=None, depth=depth, linha=[linha, i+1]))
                        ifNode.pergunta = Eval(variaveis=self.variaveis, askNode=ifNode).createOperationAst(ifNode.pergunta)
                        self.nodes.append(ifNode)

                    case "elif":
                        tokens = [x for x in tokens if x != " "]
                        if 1 >= len(tokens):
                            Erro(linha=[linha, i+1], tipo="Condicional sem argumento.").parseErr()
                        elifNode = ConditionalElse(pergunta=tokens[1:],corpo=None, fim=None, depth=depth, linha=[linha, i+1])
                        elifNode.pergunta = Eval(variaveis=self.variaveis, askNode=elifNode).createOperationAst(elifNode.pergunta)
                        self.nodes.append(elifNode)

                    case "else":
                        self.nodes.append(Else(corpo=None, fim=None, depth=depth, linha=[linha, i+1]))

                    case "set":
                        tokens = tokens[2:]
                        if len(tokens) < 5 or tokens[1:4] != [" ","to"," "]:
                            Erro(linha=[linha, i+1], tipo="Comando set malformado.").parseErr()
                        else:
                            varNome = tokens[0]
                            varValor = [x for x in tokens[4:] if x != " "]
                            if any(not char.isalpha() for char in varNome):
                                Erro(linha=[linha, i+1], tipo=f"Caractere proibído em nome de variável.").parseErr()

                            setNode = (Setter(setwho=varNome, setto=varValor, depth=depth, linha=[linha, i+1]))

                            if varValor[0] == "[" and varValor[-1] == "]":
                                varValor = varValor[1:-1]                                
                                setNode.setto = self.createList(tokens=varValor, node=setNode)

                            elif varValor[0] == "{" and varValor[-1] == "}":
                                if len(varValor) == 2:
                                    setNode.setto = {}
                                else:
                                    varValor = varValor[1:-1]
                                    itens = []
                                    atual = []
                                    mapa = {}

                                    for valor in varValor:
                                        if valor == ",":
                                            if atual:
                                                itens.append(atual)
                                                atual = []
                                        else:
                                            atual.append(valor)
                                    itens.append(atual)
                                    
                                    for item in itens:
                                        foundArrow = False
                                        arrowIndex = 0
                                        for k in range(len(item)):
                                            if item[k:k+2] == ["-",">"]:
                                                arrowIndex = k
                                                foundArrow = True
                                                break
                                        if foundArrow == False or item[:arrowIndex] == [] or item[arrowIndex+2:] == []:
                                            Erro(linha=[linha, i+1], tipo=f"Mapa malformado.").parseErr()

                                        key = ''.join([str(x) for x in item[:arrowIndex]])
                                        value = Eval(variaveis=self.variaveis, askNode=setNode).createOperationAst(item[arrowIndex+2:])
                                        mapa[key] = value
                                    setNode.setto = mapa
                            
                            elif varValor[0] == "_" and len(varValor) == 1:
                                setNode.setto = None

                            else:
                                setNode.setto = Eval(variaveis=self.variaveis, askNode=setNode).createOperationAst(setNode.setto)
                            self.nodes.append(setNode)
                    
                            if tokens[1] not in self.variaveis:
                                varNode = Variavel(nome=varNome, valor=None, linha=[linha, i+1])
                                self.varnodes.append(varNode)
                                self.variaveis[varNome] = varNode

                    case "show":
                        if " " in tokens:
                            tokens.remove(" ")
                        if 1 >= len(tokens):
                            Erro(linha=[linha, i+1], tipo="Comando show sem argumentos.").parseErr()
                        if tokens.count('`') % 2 != 0:
                            Erro(linha=[linha, i+1], tipo="Quantia indevida de indicadores.").parseErr()
                        self.nodes.append(Show(content=tokens[1:], depth=depth, linha=[linha, i+1]))

                    case "get":
                        if " " in tokens:
                            tokens.remove(" ")
                        tokens = tokens[1:]
                        if 0 >= len(tokens):
                            Erro(linha=[linha, i+1], tipo="Comando get sem variável.").parseErr()
                        variavelNome = tokens[0]
                        conteudo = None
                        if len(tokens) > 1 and tokens[1] == " ":
                            conteudo = tokens[2:]
                        elif len(tokens) > 1 and tokens[1] != " ":
                            Erro(linha=[linha, i+1], tipo="Comando get com argumentos misturados.").parseErr()

                        if variavelNome not in self.variaveis:
                            Erro(linha=[linha, i+1], tipo="Comando get em variável não declarada.").parseErr()

                        self.nodes.append(Get(content=conteudo, setwho=variavelNome, depth=depth, linha=[linha, i+1]))

                    case "nothing":
                        self.nodes.append(Nothing(depth=depth, linha=[linha, i+1]))

                    case "exit":
                        self.nodes.append(Exit(depth=depth, linha=[linha, i+1]))

                    case "#":
                        pass

                    case _:
                        Erro(linha=[linha, i+1], tipo="Comando desconhecido.").parseErr()
    
        self.meaningParse()
        return self
    
    def meaningParse(self):
        def handleFunction(i, node):
            if isinstance(self.nodes[i], Setter):
                return(self.variaveis[self.nodes[i].setwho])
            elif isinstance(self.nodes[i], Result):
                self.nodes[i].funcaoPai = node.nome
            elif isinstance(self.nodes[i], Function) and self.nodes[i].depth > nodeDepth:
                Erro(linha=self.nodes[i].linha, tipo="Funcao dentro de funcao.").parseErr()
            return None
            
        i = 0
        nodeCount = len(self.nodes)
        while i < nodeCount:
            if self.nodes[i] not in self.loadedNodes:
                if isinstance(self.nodes[i], TemCorpo):
                    nodeDepth = self.nodes[i].depth
                    if i+1 >= nodeCount or self.nodes[i+1].depth <= nodeDepth:
                        Erro(self.nodes[i].linha, tipo="Comando sem corpo").parseErr()
                    else:
                        if isinstance(self.nodes[i], Function):
                            funcEnvironment = self.nodes[i].environment
                            result = handleFunction(i+1, self.nodes[i])
                            if result is not None:
                                funcEnvironment[self.nodes[i+1].setwho] = result
                            
                        elif isinstance(self.nodes[i] , Loop) and isinstance(self.nodes[i+1], BreakLoop) and (self.nodes[i+1].depth > nodeDepth): 
                            self.nodes[i+1].loopPai = self.nodes[i]

                        self.nodes[i].corpo = self.nodes[i+1]
                        j = i+2
                        while j < nodeCount:
                            if self.nodes[j].depth <= nodeDepth:
                                self.nodes[i].fim = self.nodes[j-1]
                                break

                            elif isinstance(self.nodes[i], Function):
                                result = handleFunction(j, self.nodes[i])
                                if result is not None:
                                    funcEnvironment[self.nodes[j].setwho] = result

                            elif isinstance(self.nodes[i] , Loop) and isinstance(self.nodes[j], BreakLoop) and (self.nodes[j].depth > nodeDepth): 
                                self.nodes[j].loopPai = self.nodes[i]

                            j += 1
                        
                        if isinstance(self.nodes[i], Function):
                            self.nodes[i].environment = funcEnvironment

                        if self.nodes[i].fim == None:
                            self.nodes[i].fim = self.nodes[j-1]

                if isinstance(self.nodes[i], Loop):
                    endNodeIndex = self.nodes.index(self.nodes[i].fim)+1
                    self.nodes.insert(endNodeIndex, EndLoop(loopPai=self.nodes[i], depth=self.nodes[i].depth))
                    self.nodes[i].fim = self.nodes[endNodeIndex]
                    nodeCount+=1

                elif isinstance(self.nodes[i], Check):
                    endNodeIndex = self.nodes.index(self.nodes[i].fim)+1
                    self.nodes.insert(endNodeIndex, EndCheck(checkPai=self.nodes[i], depth=self.nodes[i].depth))
                    self.nodes[i].fim = self.nodes[endNodeIndex]

                    nodesInsideCheck = self.nodes[i+1:endNodeIndex]
                    minWhiles = float("+inf")
                    minBreaks = float("+inf")

                    breakNode = None
                    for node in nodesInsideCheck:
                        if isinstance(node, WhileLoop):
                            minWhiles = min(minWhiles, node.depth)
                        if isinstance(node, BreakLoop):
                            if minBreaks > node.depth:
                                minBreaks = node.depth
                                breakNode = node

                    if minBreaks != float("+inf") and minBreaks <= minWhiles:
                        Erro(linha=breakNode.linha, tipo="Comando break separado do loop pai por comando check.").parseErr()

                    nodeCount+=1

                elif isinstance(self.nodes[i], Function):
                    if not isinstance(self.nodes[i].fim, Result): 
                        endNodeIndex = self.nodes.index(self.nodes[i].fim)+1
                        self.nodes.insert(endNodeIndex, Result(retorno=None, valor=None, funcaoPai=self.nodes[i].nome, depth=self.nodes[i].depth, linha=None))
                        self.nodes[i].fim = self.nodes[endNodeIndex]
                        nodeCount+=1

            i += 1

        for i, node in enumerate(self.nodes):
            self.indexNodes[node] = i

    def getTokens(self, linha, pos):
        tokens = []
        current = ""
        i = 0 
        def format(token):
            try:
                token = float(token)
                if token.is_integer():
                    return(int(token))
                else:
                    return(float(token))
            except:
                return(token)

        while i < len(linha):
            char = linha[i]
            if char.isnumeric() or char in {"."}:
                current+=char
            elif char.isalpha():
                current+=char
            elif char == "'":
                i+=1
                while i < len(linha) and linha[i] != "'":
                    current+=linha[i]
                    i+=1
                current = "'" + current + "'"    
                if i >= len(linha):
                    Erro(linha=[linha, pos+1], tipo="Quantia indevida de indicadores.").parseErr()
            elif char == "#":
                i = len(linha)
            else:
                if current != "":
                    tokens.append(format(current))
                current = ""
                if char != "":
                    tokens.append(char)
            i += 1
        if current != "" and current != " ":
            tokens.append(format(current))

        depth = 0
        spaceCount = 0
        while len(tokens) > 0 and tokens[0] == " ":
            tokens.pop(0)
            spaceCount += 1
            if spaceCount == 4:
                depth += 1
                spaceCount = 0
        tokens.insert(0, depth)
        return(tokens)

def run(codigo, modo, path):
    modo = "clock"
    if modo == "clock":
        astCommands = Parser(varnodes=[], nodes=[],variaveis={},funcoes={}, indexNodes={}, loadedNodes={}, path=path).parse(codigo)
        startTime = Time.perf_counter()
        execute(nodes=astCommands.nodes, variaveis=astCommands.variaveis, funcoes=astCommands.funcoes, nodesIndex=astCommands.indexNodes)
        execTime = Time.perf_counter()-startTime
        print("Tempo de execução:" ,execTime, "s")
    else:
        astCommands = Parser(varnodes=[], nodes=[],variaveis={},funcoes={}, indexNodes={}, loadedNodes={}, path=path).parse(codigo)
        execute(nodes=astCommands.nodes, variaveis=astCommands.variaveis, funcoes=astCommands.funcoes, nodesIndex=astCommands.indexNodes)