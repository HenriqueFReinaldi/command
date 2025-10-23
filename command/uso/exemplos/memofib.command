set memo to {}

function fib n
    adopt memo

    if n < 3
        result 1
    if n$memo
        result n@memo
    set m to _
    set k to _

    execute fib [n-1]
    apply to m
    execute insert [memo, n-1, m]
    apply to memo

    execute fib [n-2]
    apply to k
    execute insert [memo, n-2, k]
    apply to memo

    result m+k

while 1
    set c to _
    get c -->
    execute fib [c]
    apply to c
    show c