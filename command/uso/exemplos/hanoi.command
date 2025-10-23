function torre n a b c
    if n = 0
        result
    execute torre [n-1, a, c, b]
    show Mova n de a para b
    execute torre [n-1, c, b, a]


set n to 3
execute torre [n, 'a', 'c', 'b']

while 1
    nothing