from CFG import CFG
from CFN import CFN
from lectura import Lectura

# Leer el archivo y obtener una lista de CFGs
cfgs = Lectura("./cfg1.txt").read()

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


