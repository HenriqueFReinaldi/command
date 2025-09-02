import sys

class Variavel:
    def __init__(self, nome, valor, linha):
        self.nome = nome
        self.valor = valor
        self.linha = linha

    def copy(self):
        return Variavel(nome=self.nome, valor=self.valor, linha=self.linha)
class Erro:
    def __init__(self, linha, tipo):
        self.linha = linha
        self.tipo = tipo

    def parseErr(self):
        print(f"""\033[31mErro\033[0m : {self.tipo} --> "\033[1m{self.linha[0]}\033[0m", \033[31mlinha {self.linha[1]}\033[0m""")
        sys.exit(1)

    def execErr(self):
        print(f"""\033[31mErro\033[0m : {self.tipo} --> "\033[1m{self.linha[0]}\033[0m", \033[31mlinha {self.linha[1]}\033[0m""")
        sys.exit(1)

#SuperClasses
class Dummy:
    pass
class TemCorpo:
    pass
class Loop(TemCorpo):
    pass
class Conditional(TemCorpo):
    pass

#Comandos
class Edit:
    def __init__(self,setwho, index, setto, mode, depth, linha):
        self.setwho = setwho
        self.index = index
        self.setto = setto
        self.mode = mode
        self.depth = depth
        self.linha = linha
class Setter:
    def __init__(self, setwho, setto, depth, linha):
        self.setwho = setwho
        self.setto = setto
        self.depth = depth
        self.linha = linha
class Show:
    def __init__(self, content, depth, linha):
        self.content = content
        self.depth = depth
        self.linha = linha

    def show(self, variaveis):
        content = self.content

        l = len(content)
        i = 0 
        while i < l:
            if isinstance(content[i], str) and '`' in content[i]:
                print(content[i].strip("`"), end="")
                i += 1
            if i < l:
                if content[i] in variaveis and variaveis[content[i]].valor is not None:
                    value = variaveis[content[i]].valor
                    if isinstance(value, (list, dict)):
                        #print(value, end="")
                        return(Erro(linha=self.linha, tipo="Não é possível por no console uma listas e/ou mapas."))
                    else:
                        print(value, end="")
                else:
                    print(content[i], end="")
                i+=1
        print()     
class Get:
    def __init__(self, content, setwho, depth, linha):
        self.content = content
        self.setwho = setwho
        self.depth = depth
        self.linha = linha

    def get(self):

        if self.content is not None:
            got = (input(''.join(self.content)))
        else:
            got = (input())
        try:
            got = float(got)
            if int(got) == got:
                got = int(got)
        except:
            pass
        return(got)
class Exit:
    def __init__(self, depth, linha):
        self.depth = depth
        self.linha = linha
class Nothing:
    def __init__(self, depth, linha):
        self.depth = depth
        self.linha = linha

#Erros
class Check(TemCorpo):
    def __init__(self, corpo, fim, resultVar, depth, linha):
        self.corpo = corpo
        self.fim = fim
        self.resultVar = resultVar
        self.depth = depth
        self.linha = linha
class EndCheck(Dummy):
    def __init__(self, checkPai, depth):
        self.checkPai = checkPai
        self.depth = depth     

#Funcoes
class Function(TemCorpo):
    def __init__(self, nome, argumentos, corpo, fim, environment, caller, depth, linha):
        self.nome = nome
        self.argumentos = argumentos
        self.corpo = corpo
        self.fim = fim
        self.environment = environment
        self.caller = caller
        self.depth = depth
        self.linha = linha
class Result:
    def __init__(self, retorno, valor, funcaoPai, depth, linha):
        self.retorno = retorno
        self.valor = valor
        self.funcaoPai = funcaoPai
        self.depth = depth
        self.linha = linha
class Execute:
    def __init__(self, execWho, argumentos, valor, depth, linha):
        self.execWho = execWho
        self.argumentos = argumentos
        self.valor = valor
        self.depth = depth
        self.linha = linha
class Apply:
    def __init__(self, variavel, depth, linha):
        self.variavel = variavel
        self.depth = depth
        self.linha = linha

#Loops#aaa
class WhileLoop(Loop):
    def __init__(self, pergunta, corpo, fim, depth, linha):
        self.pergunta = pergunta
        self.corpo = corpo
        self.fim = fim
        self.depth = depth
        self.linha = linha
class EndLoop(Dummy):
    def __init__(self, loopPai, depth):
        self.loopPai = loopPai
        self.depth = depth        
class BreakLoop(Dummy):
    def __init__(self, loopPai, depth, linha):
        self.loopPai = loopPai
        self.depth = depth
        self.linha = linha
        
#Condicionais
class ConditionalIf(Conditional):
    def __init__(self, pergunta, corpo, fim, depth, linha):
        self.pergunta = pergunta
        self.corpo = corpo
        self.fim = fim
        self.depth = depth
        self.linha = linha
class ConditionalElse(Conditional):
    def __init__(self, pergunta, corpo, fim, depth, linha):
        self.pergunta = pergunta
        self.corpo = corpo
        self.fim = fim
        self.depth = depth
        self.linha = linha
class Else(Conditional):
    def __init__(self, corpo, fim, depth, linha):
        self.corpo = corpo
        self.fim = fim
        self.depth = depth
        self.linha = linha