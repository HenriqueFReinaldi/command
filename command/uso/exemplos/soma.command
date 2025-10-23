function soma a b
    if b = 0
        result a
    set c to _
    execute soma [a+1, b-1]
    apply to c
    result c

set c to _
execute soma [10, 300]
apply to c
show c