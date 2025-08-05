# Operações 
* Uma operação é uma expressão lógica-matemática que segue uma ordem de precedência.

<details>
<summary> Operadores </summary>

* Todos os operadores abaixo estão organizados da seguinte forma: símbolo, ordem de precedência (quanto maior, mais prioridade), função e um exemplo. 

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
        ~ : 0 : Aproximação  : 0~10.6 = 11 (a ~ b → arredonda o número a com b casas decimais)
        @ : 7 : Posição      : ( i @ x ) Seleciona a posição "i" de uma variável x.  

* Comparadores:

        > : 3 : Maior          : 10 > 5 = 1 (Retorna 1 caso (a>b), 0 caso contrário.)
        < : 3 : Menor          : 10 < 5 = 0 (Retorna 1 caso (a<b), 0 caso contrário.)
        = : 3 : Igualdade      : 10 = 10 = 1 (Retorna 1 caso (a=b), 0 caso contrário.)

        Nota: Se os dois primeiros comparadores (>,<) forem usados com strings, a comparação será feita com base na quantidade de caracteres: abc > abdc será executado como 3 > 4

* Parenteses:

        Usados para "roubar" prioridade:

        2*2+2 = 6
        2*(2+2) = 8

</details>

<details>
<summary> Uso </summary>

* Operações podem envolver números, variáveis e em alguns casos, texto. Também podem ser compostos por apenas um elemento:

        12
        Pera
        1 + (VariavelA - VariavelB)
        fruta + maca

</details>

<br>




# Variáveis:
<details>
<summary>Tipos de variaveis (dados) </summary>


* Existem três tipos de dados simples nessa linguagem:

        Tipo numérico (num): Qualquer número.
        Tipo string   (txt): Qualquer sequência de texto.
        Tipo nenhum   (nil): Representa uma ausência de valor.
                
* Para representar valores booleanos (verdadeiro / falso), é usado um tipo numérico. O valor 1 representa a verdade, enquanto qualquer outro é interpretado como falso.

* Existem também dois tipos de dados compostos nessa linguagem:

        Tipo lista         : Uma sequência de tipos simples
        Tipo mapa          : Um mapeamento x -> y de tipos simples

  

</details>

<details>
<summary>Comando <b>set</b></summary>

* Para criar e/ou modificar o valor de uma variável, utiliza-se a seguinte estrutura:

        set VARIAVEL to VALOR.


  "VARIAVEL" deve ser nomeada usando apenas letras (maiúsculas ou minúsculas).<br>
  "VALOR" é uma [OPERAÇÃO](#operações)

  Para criar uma variável do tipo lista, usa se como VALOR braquetes duplos, como:

        set VARIAVEL to []

</details>

<details>
<summary>Comando <b>edit</b></summary>

* Para modificar uma posição de uma variável de tipo lista, utiliza-se a seguinte estrutura:

        edit VARIAVEL at POSICAO MODO VALOR

  "POSICAO" é uma [OPERAÇÃO](#operações). Representa o lugar dentro de "VARIAVEL" que será editado.<br>
  "VARIAVEL" é o nome da variável a ser editada.<br>
  "VALOR" também é uma [OPERAÇÃO](#operações)

  "MODO" deve ser um dos seguintes:

        Para variáveis do tipo lista:
                set   : muda o que está em POSICAO para VALOR.   
                insert: põe VALOR logo antes de POSICAO.
                delete: remove o que está em POSICAO. Não precisa de VALOR.

</details>

<br>

# Condicionais

<details>
<summary>Comando <b> if </b></summary>


* Esse comando segue a seguinte estrutura: 

        if OPERAÇÃO
            código condicional

* Ao ser executado, o comando avalia a [OPERAÇÃO](#operações). Se o resultado for 1, e SOMENTE 1, o bloco identado (código condicional) é executado.

</details>


<details>
<summary>Comando <b> elif </b></summary>

* Esse comando segue a seguinte estrutura: 

        if 10-10
            set a to 0
        elif OPERAÇÃO
            código condicional

* Ao ser executado, o comando avalia a [OPERAÇÃO](#operações). Se o resultado for 1 e o resultado do comando condicional passado não for 1, o bloco identado (código condicional) é executado.
* É possível criar encadeamentos com esse comando:

        if 0
            show ok!
        elif 0
            show ok!
        elif 1
            show EXECUTADO!
        elif 1
            show ok!

        SAÍDA:

        EXECUTADO!



</details>


<details>
<summary>Comando <b> else </b></summary>

* Esse comando segue a seguinte estrutura: 

        if 10-10
            set a to 0
        else
            código condicional

* Caso o resultado do comando condicional passado não seja 1, o bloco de código identado (código condicional) será executado.
</details>

<details>
<summary>Casos especiais </b></summary>

* O comando [while](#loops), por também conter uma "condicional", pode entrar em um encadeamento de condicionais:

        set a to 5
        while a > 0
            set a to a-1
        elif a = 0
            show Agora, `a` e nulo!

        SAÍDA:

        Agora, a e nulo!

</details>

<br>

# Loops
<details>
<summary> Comando <b> while </b> </summary>

* Um loop, ou ciclo, é uma estrutura que repete uma porção de código.
* Para criar um loop, usa-se a seguinte estrutura:

        while OPERAÇÃO
            código

* Enquanto o valor da [OPERAÇÃO](#operações) for igual a 1, o código identado será executado.
* Após cada execução, a operação é reavaliada. Se por ventura deixar de valer 1, o ciclo é quebrado e o programa segue.


</details>



<br>

# Funções
<details>
<summary>Comando <b> function </b> </summary>

* Usado para definir funções, segue a seguinte estrutura:

        function NOME VARIAVEIS
            código
            result


  Nele, "NOME" é o identificador da função. "VARIAVEIS" são os valores de entrada. Segue um exemplo de uso:

        f(x) = x+1

        function incremento x
            result x + 1

* O subcomando <b>result</b> é opicional e finaliza a função. Pode também retornar uma [operação](#operações) (como visto acima), que será enviada ao comando chamador.


</details>



<details>
<summary>Comando <b> execute </b> </summary>

* Usado para executar uma função, segue a seguinte estrutura:

        execute NOMEFUNCAO VARIAVEIS

* VARIAVEIS são os valores de entrada solicitados pela função chamada:

        function soma x y
            result x + y

        execute soma 10 20            


</details>



<details>
<summary>Comando <b> apply </b> </summary>

* Usado para aplicar o valor retornado de uma função a uma variavel. Segue a seguinte estrutura:

        set variavel to 0
        execute funcao
        apply variavel

* O valor retornado de funcao é aplicado a variavel.

</details>
<br>


# Usando o Console:
<details>
<summary>Comando <b> show </b></summary>

* Para jogar dados no console, utiliza-se a seguinte estrutura:

        show ARGUMENTOS

* "ARGUMENTOS" pode ser composto por texto e variáveis:

        set variavel to 12
        show Numero: variavel

        SAÍDA:

        Numero: 12



* Para poder mostrar o nome de uma variável, envolve-se o termo com "`", chamado de indicador:

        set variavel to 12
        show Valor de `variavel`: variavel

        SAÍDA:

        Valor de variavel: 12
</details>



<details>
<summary>Comando <b> get </b></summary>

* Para jogar dados no console, utiliza-se a seguinte estrutura:

        get VARIAVEL ARGUMENTOS

* VARIAVEL deve ser o nome de uma variável já declarada
* ARGUMENTOS é um trecho opicional, um texto que aparece no console quando o comando é executado.
</details>
<br>

# Miscelâneos:

* Comando <b>exit</b>    : Serve para terminar a execução do script;
* Comando <b>nothing</b> : Serve principalmente para testes. Não faz nada.
