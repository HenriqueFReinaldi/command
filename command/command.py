import sys
import os
from par import run
version = "2.1.1"
data = "02/10/2025"

def main() -> None:
    print("="*80)
    print(f"Command {version} - {data}")
    if len(sys.argv) <= 1:
        print(f"Use 'run' para executar o script, 'run clock' para cronometar o tempo de execução, 'quit' para sair.")
        line = 1
        codigo = ""
        while 1:
            newLine = input(f"{line:<3} - ")
            if newLine[:3] == "run":
                modo = "clock" if newLine[3:9] == " clock" else ""
                try:
                    run(codigo, modo, "\\")
                except SystemExit as e:
                    pass
                codigo = ""
                line = 1
            elif newLine == "quit":
                sys.exit(1)
            else:
                processNewLine = []
                for char in newLine:
                    if char == "\t":
                        processNewLine.extend([" "] * 4)
                    else:
                        processNewLine.append(char)
                codigo += ''.join(processNewLine)+"\n"
                line+=1
        sys.exit(1)

    else:
        nome = sys.argv[1]
        modo = sys.argv[2] if len(sys.argv) > 2 else "normal"
        if nome.endswith(".ccommand"):
            modo = "clock"
        elif not nome.endswith(".command"):
            print("tipo de arquivo errado! O script deve ser .command ou .ccommand!")
            sys.exit(1)
        try:
            path = os.path.dirname(os.path.abspath(nome))
            with open(nome, 'r') as f:
                codigo = f.read()
        except:
            print("Esse arquivo não existe!")
            sys.exit(1)
        run(codigo, modo, path)
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise 
    except:
       print("\nUm erro ocorreu.")
       sys.exit(1)