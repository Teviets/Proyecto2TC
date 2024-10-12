
class CFG:

    """
        Ejemplo de valores esperados:
            - non_terminals = {'S', 'A', 'B'}
            - terminals = {'a', 'b'}
            - productions = {
                'S': ['aA', 'bB'],
                'A': ['aA', 'a'],
                'B': ['bB', 'b']
            }
            - start_symbol = 'S'
    """

    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.non_terminals = non_terminals  # Variables N
        self.terminals = terminals          # Terminales Σ
        self.productions = productions      # Producciones P
        self.start_symbol = start_symbol    # Símbolo inicial S
    
    def __repr__(self):
        return (f"CFG(Non-terminals: {self.non_terminals}, "
                f"Terminals: {self.terminals}, "
                f"Productions: {self.productions}, "
                f"Start Symbol: {self.start_symbol})")
    
    def delProductionsEpsilon(self):
        self.finalEpsilon()
        noTerminalesEpsilon = {key for key, value in self.productions.items() if 'ε' in value}

        for key in noTerminalesEpsilon:
            self.productions[key] = [prod for prod in self.productions[key] if prod != 'ε']

        new_productions = {}

        for key, value in self.productions.items():
            current_productions = set(value) 
            new_productions[key] = list(current_productions)

            for production in value:
                nullable_positions = [i for i, symbol in enumerate(production) if symbol in noTerminalesEpsilon]

                num_combinations = 1 << len(nullable_positions)

                for comb in range(1, num_combinations):
                    new_prod = list(production)
                    for pos_index, prod_index in enumerate(nullable_positions):
                        if comb & (1 << pos_index):
                            new_prod[prod_index] = ''
                    
                    new_prod_str = ''.join(filter(lambda x: x != '', new_prod))
                    if new_prod_str:
                        new_productions[key].append(new_prod_str)
        self.productions = {key: list(set(value)) for key, value in new_productions.items()} 

        return self.cleanBlankSpaces()


    def deriveAllNonTerminals(self):
        nullable = {key: False for key in self.non_terminals}
        nullable_productions = {key: [] for key in self.non_terminals}

        for key, value in self.productions.items():
            for prod in value:
                if prod == 'ε':  # Verifica si hay producción epsilon
                    nullable[key] = True
                    nullable_productions[key].append(prod)

        # Paso 2: Iterar hasta que no haya más cambios
        changed = True
        while changed:
            changed = False
            for key, value in self.productions.items():
                for prod in value:
                    # Comprobar si todos los símbolos en la producción son terminales o pueden ser epsilon
                    if all(symbol in self.terminals or nullable.get(symbol, False) for symbol in prod):
                        if not nullable[key]:
                            nullable[key] = True
                            # Añadir la producción a la lista si se derivó a epsilon
                            nullable_productions[key].append(prod)
                            changed = True

        # Paso 3: Construir el resultado final
        result = []
        for key, productions in nullable_productions.items():
            if nullable[key]:  # Solo incluir los no terminales que pueden ser epsilon
                # Filtrar las producciones para excluir ε en sí
                result.append({key: [prod for prod in productions if prod != 'ε']})

        return result

    def finalEpsilon(self):
        epsilons = self.deriveAllNonTerminals()
        for item in epsilons:
            for key,value in item.items():
                for key2, value2 in self.productions.items():
                    for prod in value2:
                        if key in prod:
                            self.productions[key2].append(prod.replace(key, '',1))
        return self

    
    def delProductionsUnit(self):
        new_productions_dict = {}
        
        # Inicializamos el nuevo diccionario de producciones
        for key, value in self.productions.items():
            new_productions_dict[key] = set(value)  # Usamos un conjunto para evitar duplicados

        # Un conjunto para rastrear las producciones unitarias
        unitary_productions = {prod for key, value in self.productions.items() for prod in value if len(prod) == 1 and prod in self.non_terminals}

        # Iteramos sobre las producciones unitarias
        for unary in unitary_productions:
            # Añadimos las producciones del no terminal correspondiente a cada clave que tiene la producción unitaria
            for key in new_productions_dict.keys():
                if unary in new_productions_dict[key]:
                    new_productions_dict[key].remove(unary)  # Eliminamos la producción unitaria
                    new_productions_dict[key].update(self.productions[unary])  # Añadimos las producciones del no terminal correspondiente

        # Actualizamos las producciones en la clase
        self.productions = {key: list(value) for key, value in new_productions_dict.items()}

        return self


    """
    
    def delProductionsUnit(self):
        new_productions_dict = {}
        
        for key, value in self.productions.items():
            new_productions = set(value)
            unaries = {prod for prod in value if len(prod) == 1 and prod in self.non_terminals} 
            
            for unary in unaries:
                new_productions.remove(unary) 
                new_productions.update(self.productions[unary]) 
            
            new_productions_dict[key] = list(new_productions)
        
        self.productions = new_productions_dict
        return self.derivateAndReplace()#.delProdsRepetidas()
    """
    
    def delProdsRepetidas(self):
        for key, value in self.productions.items():
            new_productions = set() 
            for prod in value: 
                if prod not in new_productions:
                    new_productions.add(prod)
            self.productions[key] = list(new_productions)
        return self
    
    def delUnreachableAndNonGeneratingSymbols(self):
        # Paso 1: Encontrar símbolos alcanzables
        reachable = {self.start_symbol}
        new_reachable = set()

        while new_reachable != reachable:
            new_reachable = reachable.copy()
            for key, value in self.productions.items():
                if key in reachable:
                    for production in value:
                        reachable.update(production)  # Añadir todos los símbolos de la producción

        # Paso 2: Encontrar símbolos generadores
        generators = set()
        change = True

        while change:
            change = False
            for key, value in self.productions.items():
                if key in generators:
                    continue  # Ya es generador
                for prod in value:
                    if all(symbol in self.terminals or symbol in generators for symbol in prod):
                        generators.add(key)
                        change = True
                        break

        # Paso 3: Crear un nuevo diccionario para las producciones
        new_productions = {}

        # Solo agregamos producciones de símbolos alcanzables y generadores
        for nt in self.productions.keys():
            if nt in reachable and nt in generators:
                # Filtrar producciones que son válidas
                valid_prods = [
                    p for p in self.productions[nt] 
                    if all(symbol in self.terminals or symbol in reachable for symbol in p)
                ]
                if valid_prods:  # Asegurarse de que no esté vacío
                    new_productions[nt] = valid_prods

        # Actualizar las producciones
        self.productions = new_productions

        # Limpiar no terminales que no sean alcanzables
        self.non_terminals = {nt for nt in self.productions.keys()}

        return self


    def chomsky(self):
        new_productions = {}
        new_non_terminals = set(self.non_terminals)
        new_terminals = set(self.terminals)
        new_start_symbol = 'S0'

        # Paso 1: Crear una nueva producción para el nuevo símbolo inicial
        new_productions[new_start_symbol] = [self.start_symbol]
        new_non_terminals.add(new_start_symbol)

        # Paso 2: Eliminar producciones largas (más de 2 símbolos en el lado derecho)
        for A, productions in self.productions.items():
            new_productions[A] = []
            for production in productions:
                if len(production) > 2:
                    new_symbol = A
                    for i, symbol in enumerate(production[:-1]):  # Ajustado para evitar duplicados
                        next_symbol = f"{A}_{i}"
                        new_productions.setdefault(new_symbol, []).append(f"{symbol}{next_symbol}")
                        new_non_terminals.add(next_symbol)
                        new_symbol = next_symbol
                    new_productions.setdefault(new_symbol, []).append(production[-1])  # Agregar el último símbolo
                else:
                    new_productions[A].append(production)

        # Paso 3: Eliminar producciones unitarias
        # Crear un diccionario para rastrear cambios
        unitary_mapping = {A: set() for A in new_productions.keys()}
        for A in list(new_productions.keys()):
            for production in new_productions[A]:
                if len(production) == 1 and production[0] in new_non_terminals:
                    unitary_mapping[A].update(new_productions[production[0]])

        # Procesar los cambios de las producciones unitarias
        for A, productions in unitary_mapping.items():
            new_productions[A].extend(productions)

        # Eliminar duplicados en las producciones
        for A in new_productions.keys():
            new_productions[A] = list(set(new_productions[A]))

        # Paso 4: Eliminar producciones con terminales mezclados con no terminales
        terminal_dict = {}
        for A in list(new_productions.keys()):
            new_prods = []
            for production in new_productions[A]:
                new_prod = []
                for symbol in production:
                    if symbol in new_terminals:
                        if symbol not in terminal_dict:
                            new_symbol = f"T_{symbol}"
                            terminal_dict[symbol] = new_symbol
                            new_productions[new_symbol] = [symbol]
                            new_non_terminals.add(new_symbol)
                        new_prod.append(terminal_dict[symbol])
                    else:
                        new_prod.append(symbol)
                new_prods.append(''.join(new_prod))
            new_productions[A] = new_prods

        self.non_terminals = new_non_terminals
        self.productions = new_productions
        self.start_symbol = new_start_symbol

        return self


    
    def cleanBlankSpaces(self):
        for key, value in self.productions.items():
            new_productions = set() 
            for prod in value: 
                if prod != '':
                    new_productions.add(prod)
            self.productions[key] = list(new_productions)
        return self
    
    def derivateAndReplace(self):
        for key, value in self.productions.items():
            for prod in value:
                if len(prod) == 1 and prod in self.non_terminals:
                    self.productions[key].remove(prod)
                    self.productions[key].extend(self.productions[prod])

        return self



    def convertToNormalForm(self):
        self = self.delProductionsEpsilon().delProductionsUnit().cleanBlankSpaces()
        return self

    def printProductions(self):
        for key, value in self.productions.items():
            print(f"{key} -> {value}")


