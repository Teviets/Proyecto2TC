class Lectura:
    alfabetMayus = [chr(i) for i in range(65, 91)]  # 'A' - 'Z' Los no terminales
    alfabetMinus = [chr(i) for i in range(97, 123)]  # 'a' - 'z' los terminales

    def __init__(self, nombre_archivo: str):
        self.nombre_archivo = nombre_archivo

    def theSpliptline(self, line: str) -> tuple:
        """ Divide la línea por el símbolo '->' o '→' """
        if '->' in line:
            return line.split('->')
        elif '→' in line:
            return line.split('→')
        raise ValueError("La línea no contiene una producción válida.")

    def read(self) -> tuple:
        productions = {}
        non_terminals = set()
        terminals = set()
        start_symbol = None

        with open(self.nombre_archivo, 'r') as archivo:
            for line in archivo:
                line = line.strip()
                if '->' in line or '→' in line:
                    nt, prods = self.theSpliptline(line)
                    nt = nt.strip()

                    if start_symbol is None:
                        start_symbol = nt  # Asignar el primer no terminal como símbolo inicial

                    non_terminals.add(nt)  # El lado izquierdo siempre es un no terminal

                    prods = prods.split('|')
                    productions[nt] = [prod.strip() for prod in prods if prod.strip()]

        # Segundo paso: identificar terminales
        for nt, rhs_list in productions.items():
            for prod in rhs_list:
                # Dividimos la producción por espacios para identificar las unidades
                symbols = prod.split()

                for symbol in symbols:
                    if symbol not in non_terminals and symbol != 'ε':
                        terminals.add(symbol)  # Si no es no terminal, es terminal

        return non_terminals, terminals, productions, start_symbol
