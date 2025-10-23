from nos import Erro

class Operacao:
    def __init__(self, operador, es, di, askNode):
        self.operador = operador
        self.es = es
        self.di = di
        self.askNode = askNode
        
    def getValor(self,token,variaveis):
        valor = variaveis[token].valor
        while isinstance(valor, str) and valor in variaveis:
            valor = variaveis[valor].valor
        return valor 

    def tipo(self, item):
        tipos = {int:"num",float:"num",str:"str",list:"lst",dict:"dic"}
        if item == None:
            return("nil")
        return(tipos[type(item)])

    def operate(self, variaveis):
        esquerda = self.es
        direita = self.di

        if esquerda in variaveis:
            esquerda = self.getValor(esquerda, variaveis)
        if direita in variaveis:
            direita = self.getValor(direita, variaveis)

        if isinstance(self.es, Operacao):
            esquerda = self.es.operate(variaveis)
        if isinstance(self.di, Operacao):
            direita = self.di.operate(variaveis)

        if isinstance(esquerda, str) and len(esquerda) > 1:
            if esquerda[0] == esquerda[-1] == "'":
                esquerda = esquerda[1:-1]
        if isinstance(direita, str) and len(direita) > 1:
            if direita[0] == direita[-1] == "'":
                direita = direita[1:-1]

        if isinstance(esquerda, Erro):
            return esquerda
        elif isinstance(direita, Erro):
            return direita
        
        te = self.tipo(esquerda)
        td = self.tipo(direita)
        if te != td and self.operador not in {"*","@","$",">","<","=","u-","!"}:
            return(Erro(linha=self.askNode.linha, tipo=f'Operador "{self.operador}" não pode ser usado com tipos diferentes.'))
        if self.operador in {"~","|","&",">","<","=","+","-","*","/","%","^","@","$"} and (te == "nil" or td == "nil"):
            return(Erro(linha=self.askNode.linha, tipo=f'Operador "{self.operador}" não pode ser usado com tipo nulo.'))
        if self.operador in {"!","u-"} and td == "nil":
            return(Erro(linha=self.askNode.linha, tipo=f'Operador "{self.operador}" não pode ser usado com tipo nulo.'))
        match self.operador:
            #Acesso
            case "@":
                if isinstance(direita, (int, float)):
                    return(Erro(linha=self.askNode.linha, tipo="Variável acessada deve ser posicional."))
                elif isinstance(direita, (list,str)):
                    if not isinstance(esquerda, int):
                        return(Erro(linha=self.askNode.linha, tipo="O índice de acesso deve ser um inteiro."))
                    elif esquerda < -len(direita) or esquerda >= len(direita):
                        return(Erro(linha=self.askNode.linha, tipo="Índice maior que quantia de elementos."))
                elif isinstance(direita, dict):
                    if isinstance(esquerda, (dict, list)):
                        return(Erro(linha=self.askNode.linha, tipo="Elemento não pode ser chave."))
                    elif esquerda not in direita:
                        return(Erro(linha=self.askNode.linha, tipo="Elemento fora do mapa."))
                return(direita[esquerda])
            case "$":
                if isinstance(direita, (int, float)):
                    return(Erro(linha=self.askNode.linha, tipo="Variável acessada deve ser posicional."))
                if isinstance(direita, str) and not isinstance(esquerda, str):
                    return(Erro(linha=self.askNode.linha, tipo="Ambos operandos devem ser strings."))
                if esquerda in direita:
                    return 1
                else:
                    return 0

            #Operadores unários
            case "u-":
                return(direita * -1)
            case "!":
                if direita == 1:
                    return(0.0)
                if direita == 0:
                    return(1.0)
                if isinstance(direita, (str, float)):
                    return(Erro(linha=self.askNode.linha, tipo="Negação de não-inteiro"))
                return(~ direita)
            
            #Logica binária
            case "&":
                esquerda = int(esquerda)
                direita = int(direita)
                return(float(esquerda&direita))
            case "|":
                esquerda = int(esquerda)
                direita = int(direita)
                return(float(esquerda|direita))

            #Operadores binários
            case "~":
                if isinstance(esquerda, (float,int)):
                    esquerda = int(esquerda)
                    return(round(direita, esquerda))
            case "^":
                return(esquerda**direita)
            case "+":
                return(esquerda + direita)
            case "-":
                return(esquerda - direita)
            case "*":
                if isinstance(esquerda, dict) or isinstance(direita, dict):
                    return(Erro(linha=self.askNode.linha, tipo=f'Operador "{self.operador}" não pode ser usado com mapas.'))
                if (type(esquerda) in {float, list, str} and type(direita) != int) or (type(direita) in {float, list, str} and type(esquerda) != int):
                    return(Erro(linha=self.askNode.linha, tipo=f'Operador "{self.operador}" não pode ser usado com tipos diferentes.'))
                return(esquerda * direita)
            case "/":
                if direita == 0:
                    return(Erro(linha=self.askNode.linha, tipo="Divisão por zero."))
                return(esquerda / direita)
            case "%":
                if direita == 0:
                    return(Erro(linha=self.askNode.linha, tipo="Modulo com zero."))
                return(esquerda%direita)

            #Comparadores
            case ">":
                newDir = len(direita) if isinstance(direita, (str,list,dict)) else direita
                newEsq = len(esquerda) if isinstance(esquerda, (str,list,dict)) else esquerda
                return(1.0 if newEsq > newDir else 0.0)
            case "<":
                newDir = len(direita) if isinstance(direita, (str,list,dict)) else direita
                newEsq = len(esquerda) if isinstance(esquerda, (str,list,dict)) else esquerda
                return(1.0 if newEsq < newDir else 0.0)
            case "=":
                if direita == esquerda:
                    return(1.0)
                else:
                    return(0.0)

class Eval:
    def __init__(self,variaveis, askNode):
        self.variaveis = variaveis
        self.askNode = askNode
        self.ordem = {"~":0, #aproximacao ( 1~10.07 arredonde 10.07 para a primeira casa : 10.1)
                      "|":1, #ou
                      "&":2, #ands
                      ">":3, "<":3, "=":3,
                      "+":4,"-":4,
                      "*":5,"/":5,"%":5,
                      "^":6,
                      "!":7,"u-":7,
                      "@":8,"$":8
                      }
        self.binario = {"~","|","&",">","<","=","+","-","*","/","%","^","@","$"}
        self.unario = {"!","u-"}

    def createOperationAst(self, operation):
        tokens = operation[:]

        def transform(tokens):
            i = 0
            while i < len(tokens):
                token = tokens[i]
                lastchar = None
                if i-1 >= 0:
                    lastchar = tokens[i-1]

                if token == "-" and ((lastchar in self.ordem or lastchar in {"(",")"}) or (lastchar == None)):
                    tokens[i] = "u-"
                i+=1
            return(tokens)

        def revPolNot(tokens):
            final = []
            stacksinal = []
            for token in tokens: #poe em ordem reversa polonesa
                if isinstance(token, (float, int)):
                    final.append(token)
                elif token in self.ordem:
                    while stacksinal and (stacksinal[-1] not in "()") and (self.ordem[stacksinal[-1]] >= self.ordem[token]):
                        final.append(stacksinal.pop())
                    stacksinal.append(token)
                elif token == "(":
                    stacksinal.append("(")
                elif token == ")":
                    while stacksinal and stacksinal[-1] != "(":
                        final.append(stacksinal.pop())
                    if stacksinal:
                        stacksinal.pop()
                    else:
                        Erro(linha=self.askNode.linha, tipo="Parenteses não-balanceados.").parseErr()
                else:
                    final.append(token)
            while stacksinal:
                final.append(stacksinal.pop())
            return(final)

        def createAST(tokens):
            tokens = revPolNot(transform(tokens))

            resultado = [] #AST root
            for token in tokens: #Cria a AST
                if token in self.binario:
                    if len(resultado) < 2:
                        Erro(linha=self.askNode.linha, tipo="Operação malformada").parseErr()
                    b = resultado.pop()
                    a = resultado.pop()
                    resultado.append(Operacao(operador=token, es=a, di=b, askNode=self.askNode))
                elif token in self.unario:
                    if len(resultado) < 1:
                        Erro(linha=self.askNode.linha, tipo="Operação malformada").parseErr()
                    b = resultado.pop()
                    resultado.append(Operacao(operador=token, es=None, di=b, askNode=self.askNode))
                else:
                    resultado.append(token)

            if len(resultado) > 1:
                Erro(linha=self.askNode.linha, tipo="Operação malformada").parseErr()
            return(resultado[0])

        if len(tokens) == 1 and isinstance(tokens[0], (list, dict)):
            return(tokens[0])
        
        return(createAST(tokens))
    
    def executeAst(self, operationAst, variaveis):
        if isinstance(operationAst, (list, dict)):
            return(operationAst)
        resultado = operationAst
        if isinstance(operationAst, Operacao):
            resultado = operationAst.operate(variaveis)
        if resultado in variaveis:
            return(variaveis[resultado].valor)
        elif isinstance(resultado, float) and int(resultado) == float(resultado):
            return(int(resultado))
        return(resultado)