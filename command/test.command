function iterfib n
    set numeros [0, 1]

    set na 0
    set nb 1
    set numero n
    while n > 0
        if (n % 2) = 0
            set na na+nb
            edit add numeros na
        else
            set nb na+nb
            edit add numeros nb
        set n n-1

    result numeros


set count 0
get count -->
set result []
execute iterfib count
apply result


set i 0
while i < count
    set pos i@result
    show Numero i : pos
    set i i+1