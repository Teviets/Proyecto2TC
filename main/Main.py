from CFG import CFG
from lectura import Lectura

# Leer el archivo y obtener una lista de CFGs
cfgs = Lectura("cfg1.txt").read()

cfg = CFG(cfgs[0], cfgs[1], cfgs[2], cfgs[3])

print("Grama original")
cfg.printProductions()
print("---------------------")
print("Grama sin epsilon")
cfg = cfg.delProductionsEpsilon()
cfg.printProductions()
print("---------------------")
print("Grama sin producciones unitarias")
cfg = cfg.delProductionsUnit()
cfg.printProductions()
print("---------------------")
print("Grama sin producciones inaccesibles")
cfg = cfg.delUnreachableAndNonGeneratingSymbols()
cfg.printProductions()
print("---------------------")
print("Grama sin producciones inútiles")
cfg = cfg.chomsky()
cfg.printProductions()

