# Operações 

<details>
<summary> Uso </summary>

* Uma operação é uma expressão lógico-matemática que obedece a uma ordem específica de prioridade ( Exemplo: Multiplicações são executadas antes de somas... ). 

* Operações podem envolver números, variáveis e em alguns casos, texto. Também podem ser compostos por apenas um elemento:

        12
        Pera
        1 + (VariavelA - VariavelB)
        'fruta' + 'maca'

</details>

<details>
<summary> Operadores </summary>

* Todos os operadores abaixo estão organizados da seguinte forma: símbolo, ordem de execução (quanto maior o número, antes executado), função e um exemplo. 

* Operadores unários: 
        
        ! | 7 | Not lógico    | !0 = 1
        - | 7 | Oposição      | -x = x * -1

* Operadores binários:

        | | 1 | Ou lógico     | 0 | 1 = 1
        & | 2 | And lógico    | 0 & 1 = 0
        + | 4 | Soma          | 1 + 2 = 3
        - | 4 | Subtração     | 1 - 2 = -1
        * | 5 | Multiplicação | 2 * 2 = 4
        / | 5 | Divisão       | 2 / 2 = 1
        % | 5 | Módulo        | 2 % 2 = 0
        ^ | 6 | Potência      | 5 ^ 3 = 125
        ~ | 0 | Arredondação  | 0~10.6 = 11 (a ~ b → arredonda o número a com b casas decimais)
        @ | 8 | Posição       | i @ x -> Selecionará e corresponderá à posição "i" de uma variável x.
        $ | 8 | Dentro        | i $ x -> Responderá com 1 caso i esteja dentro de x. 0 caso contrário.

* Comparadores:

        > | 3 | Maior         | 10 > 5 = 1 (Retorna 1 caso (a>b), 0 caso contrário.)
        < | 3 | Menor         | 10 < 5 = 0 (Retorna 1 caso (a<b), 0 caso contrário.)
        = | 3 | Igualdade     | 10 = 10 = 1 (Retorna 1 caso (a=b), 0 caso contrário.)

        Nota: Se os dois primeiros comparadores (>,<) forem usados com textos, listas ou mapas, a comparação será feita com base na quantidade de caracteres / membros: 
        
                'abc' > 'abdc' será executado como 3 > 4.
                [1,2,3] > {abc -> 2, def -> 4} será executado como 3 > 2

* Parênteses:

        Usados para "roubar" prioridade. O que está entre parênteses será executado antes:

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

  <br><br>

  Para criar uma variável do tipo lista, substitui-se `VALOR` por braquetes duplos, como:

        set VARIAVEL to []

  Adicionalmente, a lista também pode ser criada já contendo elementos. Para isso, basta colocá-los entre os braquetes e separá-los por vírgulas. 

        set VARIAVEL to [1, 13.5, 'Tinha: ornintorrinco skrrr']

  <br><br>

  Para criar uma variável do tipo mapa, substitui-se `VALOR`por chaves duplas, como: 

        set VARIAVEL to {}

  Adicionalmente, como a lista, o apa pode ser criado já contendo elementos. Para isso, é usada a seguinte estrutura:

        set VARIAVEL to {chave -> valor, chave2 -> valor2}




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
            show 'zero!'

        SAÍDA:

        zero!

</details>

<br>

# Loops
<details>
<summary> Comando <b> while </b> </summary>

* Um loop, ou ciclo, é uma estrutura que repete uma porção de código.
* Este comando serve para criar ciclos. Segue a seguinte estrutura:

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

        execute NOMEFUNCAO [VARIAVEIS]

  `NOMEFUNCAO` deve referenciar uma função.<br>
  `VARIAVEIS` é uma lista de valores de entrada solicitados pela função chamada. Exemplo:

        function soma x y
            result x + y

        execute soma [10, 20]           


</details>



<details>
<summary>Comando <b> apply </b> </summary>

* Este comando atribui o valor retornado por uma função a uma variável. Segue a seguinte estrutura:

        execute FUNCAO
        apply to VARIAVEL

  Caso `FUNCAO` retorne algo, o valor retornado será armazenado em `VARIAVEL`.

</details>


<details>
<summary>Comando <b> adopt </b> </summary>

* Este comando serve para pegar uma variável do escopo global e colocar no escopo local. Exemplo:

        set valor to 10
        function incremento
            adopt valor
            set valor to valor+1

        execute incremento
        show valor

        SAÍDA:

        11

* Variáveis do escopo global são aquelas definidas fora de qualquer função.

</details>


<details>
<summary>Funções <b> built-in </b></summary>

* São funções que vem com todo script .command. Exemplo:

        set a to [1,2,3,4]
        execute showList [a]

        SAÍDA:

        [1, 2, 3, 4]

* Por padrão, retoram "-1" em caso de erros.

* Lista de built-ins:

        objLength -> Mostra o comprimento de uma lista/ texto/ mapa.
        objSort   -> Organiza uma lista/ texto.
        showList  -> Põe no console o conteúdo de uma lista.
        showMap   -> Põe no console o conteúdo de um mapa.
        sumList   -> Mostra a soma do conteúdo de uma lista.
        objType   -> Mostra o tipo de dado do objeto.
        stripMarc -> Tira tira marcadores de um texto.
        indexOf   -> Mostra onde que o primeiro argumento está dentro do segundo.
        randomNum -> Gera um número aleatório inteiro entre argumento 0 e 1.
        add       -> Adiciona ao fim de uma lista / texto (primeiro arg) o conteudo do segundo argumento.
        delete    -> Deleta de uma lista/texto/dicionario (primeiro arg) a posição "segundo argumento".
        set       -> Altera o valor da posição "segundo argumento" dentro do mapa/lista/texto "primeiro argumento" para "terceiro argumento"
        insert    -> Insere na posição "segundo argumento" dentro do mapa/lista/texto "primeiro argumento" o conteúdo de "terceiro argumento"
        


</details>
<br>


# Usando o Console:
<details>
<summary>Comando <b> show </b></summary>

* Este comando serve para jogar dados no console. Segue a seguinte estrutura: 

        show ARGUMENTOS

  `ARGUMENTOS` pode ser composto por texto e variáveis:

        set variavel to 12
        show 'Numero: 'variavel

        SAÍDA:

        Numero: 12

</details>



<details>
<summary>Comando <b> get </b></summary>

* Este comando serve para coletar dados do console. Segue a seguinte estrutura:

        get VARIAVEL 'TEXTO'

  `VARIAVEL` deve ser o nome de uma variável já declarada
  `TEXTO` é um argumento opicional, um texto que aparece no console quando o comando é executado.


</details>
<br>

# Miscelâneos:

<details>
<summary>Comando <b>load</b></summary>

* Este comando põe outro script dentro do atual. Segue a seguinte estrutura:

        load NOMESCRIPT

  `NOMESCRIPT` deve ser o nome de um arquivo .command dentro do mesmo diretório que o script procurador.<br>
  Se `NOMESCRIPT` for encontrado, seu código subistituitá o comando.s


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
