load std

function twosum nums target
    set seen to {}
    set l to 0
    execute length nums
    apply to l

    set i to 0
    while i < l
        edit seen at i@nums set i
        set i to i+1

    set i to 0
    while i < l
        set comp to target - i@nums
        set found to 0
        check found
            set find to comp@seen
        if found = 0
            if !(comp@seen = i)
                set comp to comp@seen
                show achei!: [i, comp]

                set a to i@nums
                set b to comp@nums
                result
        set i to i+1
    show sem resultado.
    result

set n to []
while 1
    set c to 0
    get c Adicione um numero (para parar, digite "parou")-->
    set status to 0
    check status
        if c = parou
            nothing
    if status = 0
        break
    edit n at end insert c

execute showList n
set t to 0
while 1 
    get t -->
    execute twosum n t