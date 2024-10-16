from CFG import CFG
from CFN import CFN
from lectura import Lectura
from CYK import CYK  # Import the CYK class

def main():
    # Read the grammar file and obtain a list of CFGs
    cfgs = Lectura("./cfg1.txt").read()
    print("Contenido del archivo leído:", cfgs)

    # Create CFG object
    cfg = CFG(cfgs[0], cfgs[1], cfgs[2], cfgs[3])

    print("Gramatica original")
    cfg.printProductions()
    print("---------------------")
    
    print("Gramatica sin epsilon")
    cfg = cfg.delProductionsEpsilon()
    cfg.printProductions()
    print("---------------------")
    
    print("Gramatica sin producciones unitarias")
    cfg = cfg.delProductionsUnit()
    cfg.printProductions()
    print("---------------------")
    
    print("Gramatica sin producciones inaccesibles")
    cfg = cfg.delUnreachableAndNonGeneratingSymbols()
    cfg.printProductions()
    print("---------------------")
    
    print("Forma normal de Chomsky")
    cfg = cfg.chomsky()
    cfg.printProductions()
    print("---------------------")
    print("---------------------")

    cyk_model = CYK("./cfg1.txt")


    string_to_parse = input("Introduce la cadena a analizar: ")
    cyk_model.CYKParser(string_to_parse)

if __name__ == "__main__":
    main()
