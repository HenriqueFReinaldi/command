import sys

class Variavel:
    def __init__(self, nome: str, valor: any, linha: list) -> None:
        self.nome = nome
        self.valor = valor
        self.linha = linha

    def copy(self) -> "Variavel":
        return Variavel(nome=self.nome, valor=self.valor, linha=self.linha)
class Erro:
    def __init__(self, linha: list, tipo: str) -> None:
        self.linha = linha
        self.tipo = tipo

    def parseErr(self) -> None:
        print(f"""\033[31mErro\033[0m : {self.tipo} --> "\033[1m{self.linha[0]}\033[0m", \033[31mlinha {self.linha[1]}\033[0m""")
        sys.exit(1)

    def execErr(self) -> None:
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
class Setter:
    def __init__(self, setwho: str, setto: any, depth: int, linha: list) -> None:
        self.setwho = setwho
        self.setto = setto
        self.depth = depth
        self.linha = linha
class Show:
    def __init__(self, content: str, depth: int, linha: list) -> None:
        self.content = content
        self.depth = depth
        self.linha = linha

    def show(self, variaveis: dict) -> object | None:
        content = self.content.copy()
        for i, c in enumerate(content):
            if c in variaveis:
                if not isinstance(variaveis[c].valor, (list, dict)):
                    content[i] = variaveis[content[i]].valor
                else:
                    return(Erro(linha=self.linha, tipo="Não é possível por no console lista e/ou mapas."))
        for i, c in enumerate(content):
            if isinstance(c, (float, int)):
                continue
            if c is None:
                content[i] = "nil"
                continue
            if len(c) > 1:
                content[i] = c[1:-1] if c[0] == c[-1] == "'" else c

        print(''.join([str(x) for x in content]))
class Get:
    def __init__(self, content: str, setwho: str, depth: int, linha: list) -> None:
        self.content = content
        self.setwho = setwho
        self.depth = depth
        self.linha = linha

    def get(self) -> any:
        if self.content is not None:
            got = (input(''.join(self.content)))
        else:
            got = (input())
        try:
            got = float(got)
            if int(got) == got:
                got = int(got)
        except:
            got = "'"+got+"'"
        return(got)
class Exit:
    def __init__(self, depth: int, linha: list) -> None:
        self.depth = depth
        self.linha = linha
class Nothing:
    def __init__(self, depth: int, linha: list) -> None:
        self.depth = depth
        self.linha = linha

#CheckErros
class Check(TemCorpo):
    def __init__(self, corpo: object, fim: object, resultVar: str, depth: int, linha: list) -> None:
        self.corpo = corpo
        self.fim = fim
        self.resultVar = resultVar
        self.depth = depth
        self.linha = linha
class EndCheck(Dummy):
    def __init__(self, checkPai: object, depth: int) -> None:
        self.checkPai = checkPai
        self.depth = depth     

#Funcoes
class Function(TemCorpo):
    def __init__(self, nome: str, argumentos: list, corpo: object, fim: object, environment: dict, caller: list, depth: int, linha: list) -> None:
        self.nome = nome
        self.argumentos = argumentos
        self.corpo = corpo
        self.fim = fim
        self.environment = environment
        self.caller = caller
        self.depth = depth
        self.linha = linha
class Result:
    def __init__(self, retorno: object | None, valor: any, funcaoPai: object, depth: int, linha: list) -> None:
        self.retorno = retorno
        self.valor = valor
        self.funcaoPai = funcaoPai
        self.depth = depth
        self.linha = linha
class Execute:
    def __init__(self, execWho: str, argumentos: list | None, valor: any, depth: int, linha: list) -> None:
        self.execWho = execWho
        self.argumentos = argumentos
        self.valor = valor
        self.depth = depth
        self.linha = linha
class Apply:
    def __init__(self, variavel: str, depth: int, linha: list) -> None:
        self.variavel = variavel
        self.depth = depth
        self.linha = linha
class Adopt:
    def __init__ (self, variavel: str, depth: int, linha: list) -> None:
        self.variavel = variavel
        self.depth = depth
        self.linha = linha


#Loops
class WhileLoop(Loop):
    def __init__(self, pergunta: any, corpo: object, fim: object, depth: int, linha: list) -> None:
        self.pergunta = pergunta
        self.corpo = corpo
        self.fim = fim
        self.depth = depth
        self.linha = linha
class EndLoop(Dummy):
    def __init__(self, loopPai: object, depth: int) -> None:
        self.loopPai = loopPai
        self.depth = depth        
class BreakLoop(Dummy):
    def __init__(self, loopPai: object, depth: int, linha: list) -> None:
        self.loopPai = loopPai
        self.depth = depth
        self.linha = linha
        
#Condicionais
class ConditionalIf(Conditional):
    def __init__(self, pergunta: any, corpo: object, fim: object, depth: int, linha: list) -> None:
        self.pergunta = pergunta
        self.corpo = corpo
        self.fim = fim
        self.depth = depth
        self.linha = linha
class ConditionalElse(Conditional):
    def __init__(self, pergunta: any, corpo: object, fim: object, depth: int, linha: list) -> None:
        self.pergunta = pergunta
        self.corpo = corpo
        self.fim = fim
        self.depth = depth
        self.linha = linha
class Else(Conditional):
    def __init__(self, corpo: object, fim: object, depth: int, linha: list) -> None:
        self.corpo = corpo
        self.fim = fim
        self.depth = depth
        self.linha = linha