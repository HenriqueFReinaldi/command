set variavel to []

set i to 0
set size to 25

while i < size
    edit variavel at -1 insert 0
    set i to i+1

edit variavel at 5 set 10
edit variavel at 9 delete

set i to 0
while i < size-1
    set pos to i@variavel
    show pos
    set i to i+1