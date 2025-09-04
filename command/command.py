import sys
import os
from par import run

print("command","="*80, "\n\n")
if len(sys.argv) <= 1:
    print("Command funcionando! Por favor, declare o script a ser executado! : command script.command")
    sys.exit(1)

nome = sys.argv[1]
modo = sys.argv[2] if len(sys.argv) > 2 else 0
if ".command" != nome[-8:]:
    print("tipo de arquivo errado! O script deve ser .command!")
    sys.exit(1)

try:
    path = os.path.dirname(os.path.abspath(nome))
    with open(nome, 'r') as f:
        codigo = f.read()
except:
    print("Esse arquivo não existe!")
    sys.exit(1)

run(codigo, modo, path)