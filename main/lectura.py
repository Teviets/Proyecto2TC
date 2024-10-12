class Lectura:
    alfabetMayus = [chr(i) for i in range(65, 91)]  # 'A' - 'Z'
    alfabetMinus = [chr(i) for i in range(97, 123)]  # 'a' - 'z'

    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        self.archivo = open(nombre_archivo, 'r')

    def read(self):
        productions = {}
        non_terminals = set()
        terminals = set()
        start_symbol = None

        for line in self.archivo:
            line = line.strip()
            if '->' in line: 
                nt, prods = line.split('->')
                nt = nt.strip()

                if start_symbol is None:
                    start_symbol = nt

                non_terminals.add(nt)

                prods = prods.split('|')
                productions[nt] = [prod.strip() for prod in prods if prod.strip()] 

                for prod in productions[nt]:
                    for symbol in prod:
                        if symbol not in self.alfabetMayus and symbol not in self.alfabetMinus and symbol != 'ε':
                            terminals.add(symbol)

        self.archivo.close()

        return (non_terminals, terminals, productions, start_symbol)
