function length object                    #Retorna o tamanho de uma lista / str "object"
    set size to 0
    set achouFim to 0
    while 1
        if achouFim = 1
            set size to size-1
            break
        check achouFim
            if size@object
                nothing       
        set size to size + 1
    result size

function sum object                       #Retorna a soma dos valores de uma lista "object"
    set type to 0
    execute type object
    apply to type
    if !(type = lista)
        result `objeto deve ser uma lista de numeros...`
    else
        set l to 0
        execute length object
        apply to l
        set l to l-1
        if l < 0 | l = 0
            result `lista não contem itens...`

        set result to 0
        while l > -1
            set result to result+l@object
            set l to l-1

    result result

function showList object                  #Mostra o conteúdo de uma lista.
    set index to 0
    set achouFim to 0
    while 1
        if achouFim = 1
            break
        check achouFim
            set pos to index@object
            show pos  
        set index to index+1

function type object                      #Classifica o tipo de "object". Retorna num / str / mapa / lista
    set status to 0

    check status
        if 1+object
            nothing
    if status = 0
        result num

    check status
        if object+a
            nothing
    if status = 0
        result str

    check status
        edit object at 0 insert 0
        edit object at 0 delete
    if status = 1
        result mapa
    result lista

function indexOf target object            #Procura por "target" dentro de uma lista "object". Retorna o index se achar, caso contrário -1.
    set type to 0
    execute type object
    apply to type
    if !(type = lista)
        result `objeto deve ser uma lista...`
    else
        set l to 0
        execute length object
        apply to l
        set i to 0
        while i < l
            set n to i@object
            if target = i@object
                result i
            set i to i+1

        result -1