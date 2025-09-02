import sys
from par import run

print("command","="*80, "\n\n")
if len(sys.argv) < 2:
    print("Por favor, escolha algum modo! : run, ajuda")
    sys.exit(1)

elif sys.argv[1] == "run":
    if len(sys.argv) < 3:
        print("Por favor, selecione algum script! : command run script.command")
        sys.exit(1)
    nome = sys.argv[2]
    modo = sys.argv[3] if len(sys.argv) > 3 else 0
    with open(nome, 'r') as f:
        codigo = f.read()
    run(codigo, modo)

elif sys.argv[1] == "ajuda":
    print("Confira a página do github para ver a documentação!")
    sys.exit(1)