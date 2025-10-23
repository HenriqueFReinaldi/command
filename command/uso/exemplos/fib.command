function fib n
    if n < 2
        result 1
    else
        set m to _
        set k to _
        execute fib [n-1]
        apply to m
        execute fib [n-2]
        apply to k

        result m+k

set a to _
execute fib [25]
apply to a
show a