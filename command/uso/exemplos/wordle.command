load std

set correto to carro
set length to 0
execute length correto
apply to length

function getGuess length
    set tentativa to 0
    get tentativa -->

    set tentTipo to 0
    execute type tentativa  
    apply to tentTipo
    if !(tentTipo = str)
        show 'tentativa' deve ser texto
        result . 

    set tamanhoTentativa to 0
    execute length tentativa
    apply to tamanhoTentativa
    if !(tamanhoTentativa = length)
        show tamanho indvido!
        result .     
    result tentativa

set att to length+2
show tamanho: length
show ===============
while 1 
    set chave to correto
    show tentativas: att
    set t to .
    while t = .
        execute getGuess length
        apply to t
    set att to att-1

    set gabarito to o
    set i to 0
    while i < length-1
        edit gabarito at end insert o
        set i to i +1

    set i to 0
    set correctCount to 0
    while i < length
        if i@t = i@chave
            edit gabarito at i set C
            edit chave at i set .
            edit t at i set ,
            set correctCount to correctCount + 1
        set i to i+1
    if correctCount = length
        show vitoria!
        break
    if att = 0
        show acabou...
        break

    set i to 0
    while i < length
        set j to 0
        while j < length
            if i@t = j@chave
                edit gabarito at i set P
                edit chave at j set .
                edit t at i set ,
            set j to j+1
        set i to i+1

    show -->gabarito