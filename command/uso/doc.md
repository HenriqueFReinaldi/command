# Operações 

<details>
<summary> Uso </summary>

* Uma operação é uma expressão lógico-matemática que obedece a uma ordem específica de prioridade ( Exemplo: Multiplicações são executadas antes de somas... ). 

* Operações podem envolver números, variáveis e em alguns casos, texto. Também podem ser compostos por apenas um elemento:

        12
        Pera
        1 + (VariavelA - VariavelB)
        fruta + maca

</details>

<details>
<summary> Operadores </summary>

* Todos os operadores abaixo estão organizados da seguinte forma: símbolo, ordem de execução (quanto maior o número, antes executado), função e um exemplo. 

* Operadores unários: 
        
        ! : 7 : Not lógico   : !0 = 1
        - : 7 : Negação      : -1 = 1 * -1

* Operadores binários:

        | : 1 : Ou lógico    : 0 | 1 = 1
        & : 2 : And lógico   : 0 & 1 = 0
        + : 4 : Soma         : 1 + 2 = 3
        - : 4 : Subtração    : 1 - 2 = -1
        * : 5 : Multiplicação: 2 * 2 = 4
        / : 5 : Divisão      : 2 / 2 = 1
        % : 5 : Módulo       : 2 % 2 = 0
        ^ : 6 : Potência     : 5 ^ 3 = 125
        ~ : 0 : Arredondação : 0~10.6 = 11 (a ~ b → arredonda o número a com b casas decimais)
        @ : 7 : Posição      : i @ x → Selecionará e corresponderá à posição "i" de uma variável x.  

* Comparadores:

        > : 3 : Maior          : 10 > 5 = 1 (Retorna 1 caso (a>b), 0 caso contrário.)
        < : 3 : Menor          : 10 < 5 = 0 (Retorna 1 caso (a<b), 0 caso contrário.)
        = : 3 : Igualdade      : 10 = 10 = 1 (Retorna 1 caso (a=b), 0 caso contrário.)

        Nota: Se os dois primeiros comparadores (>,<) forem usados com strings, a comparação será feita com base na quantidade de caracteres: abc > abdc será executado como 3 > 4

* Parênteses:

        Usados para "roubar" prioridade. O que está entre parênteses será executado antes.:

        2*2+2 = 6
        2*(2+2) = 8

</details>

<br>




# Variáveis:
<details>
<summary>Tipos de variaveis (dados) </summary>


* Existem três tipos de dados simples nessa linguagem:

        Tipo numérico (num): Qualquer número.
        Tipo string   (str): Qualquer sequência de texto.
        Tipo nenhum   (nil): Representa uma ausência de valor.
                
* Via-de-regra, o número 1 representa `Verdadeiro`. Qualquer coisa diferente representa `Falso`.

* Existem também dois tipos de dados compostos nessa linguagem:

        Tipo lista    (lst): Uma sequência de tipos simples
        Tipo mapa     (map): Um mapeamento x -> y de tipos simples

  

</details>

<details>
<summary>Comando <b>set</b></summary>

* Este comando serve para criar e/ou modificar o valor de uma variável. Segue a seguinte estrutura:

        set VARIAVEL to VALOR.


  `VARIAVEL` deve ser nomeada usando apenas letras (maiúsculas ou minúsculas).<br>
  `VALOR` é uma [operação](#operações).

  Para criar uma variável do tipo lista, substitui-se `VALOR` por braquetes duplos, como:

        set VARIAVEL to []

</details>

<details>
<summary>Comando <b>edit</b></summary>

* Este comando serve para modificar uma posição de uma variável de tipo sequencial ou associativo (listas, mapas, strings...), segue a seguinte estrutura:

        edit VARIAVEL at POSICAO MODO VALOR

  `POSICAO` é uma [operação](#operações). Representa o lugar dentro de `VARIAVEL` que será editado. Pode-se usar `end` para declarar que a posição editada é a ultima. <br>
  `VARIAVEL` é o nome da variável a ser editada.<br>
  `VALOR` também é uma [operação](#operações). Representa o que será posto em `POSICAO`

  `MODO` deve ser um dos seguintes:

        Para variáveis do tipo lista e string:
                set   : muda o que está em POSICAO para VALOR.   
                insert: põe VALOR logo antes de POSICAO.
                delete: remove o que está em POSICAO. Não precisa de VALOR.

</details>

<br>

# Condicionais

<details>
<summary>Comando <b> if </b></summary>


* Este comando serve para executar condicionalmente uma porção de código. Segue a seguinte estrutura: 

        if OPERACAO
            CODIGO

  `OPERACAO` é uma [operação](#operações). Quando o comando if é executado, ela é avaliada. <br>
  `CODIGO` é o trecho que será executado somente se `OPERACAO` equivaler a 1.<br><br>
</details>


<details>
<summary>Comando <b> elif </b></summary>

* Este comando é usado para executar uma porção de código condicional alternativa, caso a condicional anterior seja diferente de 1. Segue a seguinte estrutura:

        if 0
            nothing
        elif OPERACAO
            CODIGO

  `OPERACAO` é uma [operação](#operações). Quando o comando elif é executado, ela é avaliada. <br>
  `CODIGO` é o trecho que será executado somente se `OPERACAO` equivaler a 1 e se a condicional prévia for diferente de 1.<br><br>
</details>


<details>
<summary>Comando <b> else </b></summary>

* Este comando serve para executar uma porção de código alternativo, caso a condicional anterior seja diferente de 1. Segue a seguinte estrutura:

        if 0
            nothing
        else
            CODIGO

  `CODIGO` é o trecho que será executado somente se a condicional prévia for diferente de 1.<br><br>
</details>

<details>
<summary>Casos especiais </b></summary>

* O comando [while](#loops), por também funcionar condicionalmente, pode entrar em um encadeamento de condicionais:

        set a to 5
        while a > 0
            set a to a-1
        elif a = 0
            show zero!

        SAÍDA:

        zero!

</details>

<br>

# Loops
<details>
<summary> Comando <b> while </b> </summary>

* Um loop, ou ciclo, é uma estrutura que repete uma porção de código.
* Este comando serve para criar ciclos. Segue a seguinte estrutura?

        while OPERACAO
            CODIGO

  `OPERACAO` é uma [operação](#operações). <br>
  `CODIGO` é a porção de código do ciclo que será executada enquanto `OPERCAO` equivaler a 1.<br><br>

  Após cada execução, `OPERACAO` é reavaliada. Se por ventura deixar de valer 1, o ciclo é quebrado e o programa segue sem executar `CODIGO`.

* O subcomando <b>break</b> serve para terminar a execução de um ciclo, independentemente do valor de `OPERACAO`. Exemplo:

        while 1
            show ola!
            break

        SAÍDA:

        ola!


</details>



<br>

# Funções
<details>
<summary>Comando <b> function </b> </summary>

* Usado para definir funções, segue a seguinte estrutura:

        function NOME VARIAVEIS
            CÓDIGO
            result


  `NOME` é o identificador da função. <br>
  `VARIAVEIS` são os valores de entrada. Segue um exemplo de uso:

        f(x) = x+1

        function incremento x
            result x + 1

* O subcomando <b>result</b> é opicional e declara que a função terminou de executar. Pode também retornar uma [operação](#operações) (como visto acima), que será enviada ao comando chamador dad função.


</details>



<details>
<summary>Comando <b> execute </b> </summary>

* Este comando é usado para executar uma função, segue a seguinte estrutura:

        execute NOMEFUNCAO VARIAVEIS

  `NOMEFUNCAO` deve referenciar uma função.<br>
  `VARIAVEIS` são os valores de entrada solicitados pela função chamada. Exemplo:

        function soma x y
            result x + y

        execute soma 10 20            


</details>



<details>
<summary>Comando <b> apply </b> </summary>

* Este comando atribui o valor retornado por uma função a uma variável. Segue a seguinte estrutura:

        execute FUNCAO
        apply to VARIAVEL

  Caso `FUNCAO` retorne algo, o valor retornado será armazenado em `VARIAVEL`.

</details>
<br>


# Usando o Console:
<details>
<summary>Comando <b> show </b></summary>

* Este comando serve para jogar dados no console. Segue a seguinte estrutura: 

        show ARGUMENTOS

  `ARGUMENTOS` pode ser composto por texto e variáveis:

        set variavel to 12
        show Numero: variavel

        SAÍDA:

        Numero: 12

</details>



<details>
<summary>Comando <b> get </b></summary>

* Este comando serve para coletar dados do console. Segue a seguinte estrutura:

        get VARIAVEL TEXTO

  `VARIAVEL` deve ser o nome de uma variável já declarada
  `TEXTO` é um argumento opicional, um texto que aparece no console quando o comando é executado.


</details>
<br>

# Miscelâneos:

<details>
<summary>Comando <b>load</b></summary>

* Este comando carrega funções de outros scripts. Segue a seguinte estrutura:

        load NOMESCRIPT

  `NOMESCRIPT` deve ser o nome de um arquivo .command dentro do mesmo diretório que o script procurador.<br>
  Se `NOMESCRIPT` for encontrado, suas funções subistituirão o comando load. Tudo fora de funções será ignorado.


</details>

<details>
<summary>Comando <b>check</b></summary>

* Este comando serve para testar se um bloco de código suspeito causará erros. Segue a seguinte estrutura:

        check VARIAVEL
            CODIGO SUSPEITO

  `VARIAVEL` é um argumento opcional. Caso seja usado, o veredito do comando check será armazenado nele.<br>
  `CODIGO SUSPEITO` é uma sequência de código identado que pode causar erros de execução.

* Ao executar um check, se `VARIAVEL` for usada, seu valor é inicialmente definido como 0.
* Se um erro ocorrer por causa do `CODIGO SUSPEITO` a execução do bloco é encerrada, e se `VARIAVEL` for usada, recebe 1.

</details>
<br>


* Comando <b>exit</b>    : Serve para terminar a execução do script;
* Comando <b>nothing</b> : Serve principalmente para testes. Não faz nada.
