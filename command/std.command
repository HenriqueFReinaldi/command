function length object
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

function sum object
    set type to 0
    execute type object
    apply to type
    if !(type = lst)
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

function showList object
    set index to 0
    set achouFim to 0
    while 1
        if achouFim = 1
            break
        check achouFim
            set pos to index@object
            show pos  
        set index to index+1

function type object
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
    result lst