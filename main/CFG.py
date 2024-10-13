numberListOnSTR = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30',
                   '31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59',
                   '60','61','62','63','64','65','66','67','68','69','70','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88',
                   '89','90','91','92','93','94','95','96','97','98','99','100','101','102','103','104','105','106','107','108','109','110','111','112','113','114',
                   '115','116','117','118','119','120','121','122','123','124','125','126','127','128']


alfabetMayus = [chr(i) for i in range(65, 91)]  # 'A' - 'Z' Los no terminales
alfabetMinus = [chr(i) for i in range(97, 123)]  # 'a' - 'z' los terminales


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
        self.idsNonTerminals = {}
    
    def __repr__(self):
        return (f"CFG(Non-terminals: {self.non_terminals}, "
                f"Terminals: {self.terminals}, "
                f"Productions: {self.productions}, "
                f"Start Symbol: {self.start_symbol})")
    
    def replaceCompleteWordsToLetters(self):
        self.non_terminalsOG = self.non_terminals
        self.newNonTerminals = set()
        self.idsNonTerminals = {}
        for key, value in self.productions.items():
            for prod in value:
                lstProds = prod.split(' ')
                for item in lstProds:
                    if len(item) > 1:
                        if item not in self.newNonTerminals:
                            self.newNonTerminals.add(item)
                            self.idsNonTerminals[item] = f"{alfabetMayus.pop(0)}"
        for key, value in self.productions.items():
            new_productions = []
            for prod in value:
                lstProds = prod.split(' ')
                newProd = ""
                for item in lstProds:
                    if item in self.newNonTerminals:
                        newProd += self.idsNonTerminals[item]
                    else:
                        newProd += item
                new_productions.append(newProd)
            self.productions[key] = new_productions

        # reemplaza las llaves de productions por las nuevas llaves
        for key, value in self.idsNonTerminals.items():
            self.productions[value] = self.productions.pop(key)

        self.non_terminals = set()
        for k in self.productions.keys():
            self.non_terminals.add(k)
    
    
    def delProductionsEpsilon(self):
        self.replaceCompleteWordsToLetters()

        # Identificar no terminales que pueden generar epsilon
        noTerminalesEpsilon = {key for key, value in self.productions.items() if 'ε' in value}

        # Eliminar producciones epsilon
        for key in noTerminalesEpsilon:
            self.productions[key] = [prod for prod in self.productions[key] if prod != 'ε']

        new_productions = {}

        # Iterar sobre las producciones para crear nuevas producciones eliminando epsilon
        for key, value in self.productions.items():
            current_productions = set(value)  # Usar un conjunto para evitar duplicados
            new_productions[key] = list(current_productions)

            for production in value:
                nullable_positions = [i for i, symbol in enumerate(production) if symbol in noTerminalesEpsilon]

                # Número de combinaciones posibles para los no terminales que pueden ser epsilon
                num_combinations = 1 << len(nullable_positions)

                # Generar nuevas producciones eliminando epsilon en las posiciones nullable
                for comb in range(1, num_combinations):
                    new_prod = list(production)
                    for pos_index, prod_index in enumerate(nullable_positions):
                        if comb & (1 << pos_index):
                            new_prod[prod_index] = ''  # Eliminar el símbolo

                    # Unir la producción y agregarla si no está vacía
                    new_prod_str = ''.join(filter(lambda x: x != '', new_prod))
                    if new_prod_str:
                        new_productions[key].append(new_prod_str)

        # Actualizar las producciones con las nuevas
        self.productions = {key: list(set(value)) for key, value in new_productions.items()}

        return self.cleanBlankSpaces()
    
    def deriveAllNonTerminals(self):
        nullable = {key: False for key in self.non_terminals}
        nullable_productions = {key: [] for key in self.non_terminals}
        print("Producciones")
        print(self.non_terminals)
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
    
        
        for key, value in self.productions.items():
            if key in generators:
                continue
            for prod in value:
                if ((symbol in self.terminals or symbol in generators) for symbol in prod):
                    generators.add(key)
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

        # Si no hubo cambios en las producciones, retornar el CFG sin cambios
        if new_productions == self.productions:
            return self

        # Actualizar las producciones si hubo cambios
        self.productions = new_productions

        # Limpiar no terminales que no sean alcanzables
        self.non_terminals = {nt for nt in self.productions.keys()}

        return self


    def chomsky(self):
        newProds = {}
        idsDict = {}
        count = 0
        listlistSymbols = []

        # Paso 1: Crear las nuevas producciones para los terminales
        for terminal in self.terminals:
            # Agregar una nueva producción de la forma X0 -> terminal
            self.productions[f"X_{count}"] = [f'{terminal}']
            newProds[terminal] = f"X_{count}"
            count += 1

        # Paso 2: Reemplazar terminales por los no terminales auxiliares
        updated_productions = {}

        for key, value in self.productions.items():
            updated_productions[key] = []  # Crear lista de producciones actualizada
            for prod in value:
                newProd = prod
                for char in prod:
                    # Verifica si el carácter es un terminal y que no sea la producción actual
                    if char in self.terminals and newProds[char] != key:
                        newProd = newProd.replace(char, newProds[char])
                
                # Agregar la nueva producción a la lista actualizada
                updated_productions[key].append(newProd)

        # Actualizar las producciones
        self.productions = updated_productions

        # Paso 3: Eliminar producciones de más de 2 símbolos
        new_productions = {}

        for key, value in self.productions.items():
            dict_podsmas2 = {}
            for prod in value:
                symbols = []
                item = ""  # Reiniciamos 'item' para cada producción
                for char in prod:
                    # Si encontramos una X, empezamos a armar el símbolo auxiliar
                    if char == 'X':
                        item = char  # Empezamos con 'X'
                    elif char == '_':
                        if item == 'X':  # Solo concatenamos '_' si ya hemos encontrado 'X'
                            item += char
                    elif char in numberListOnSTR:
                        if item == 'X_':  # Solo agregamos números si hemos encontrado 'X_'
                            item += char
                            symbols.append(item)  # Agregamos el símbolo completo
                            item = ""  # Reiniciamos 'item' para procesar el siguiente símbolo
                        else:
                            symbols.append(char)  # Agregamos números sueltos como símbolos
                    else:
                        # Si no es parte de un símbolo 'X_#', simplemente lo agregamos
                        symbols.append(char)

                if len(symbols)>2:
                    dict_podsmas2[f"{key}_{len(dict_podsmas2) + 1}"] = symbols
                    listlistSymbols.append(symbols)
                
            new_dict = {}
            count2 = 1
            for key2, value2 in dict_podsmas2.items():
                new_dict[key2] = [value2[0], f"{key2}_{count2}"]

                for i in range(1, len(value2)):
                    newKey = f"{key2}_{count2}"
                    new_dict[newKey] = [value2[i], f"{key2}_{count2 + 1}"]
                    count2 += 1

            
            for keyde,valuede in dict_podsmas2.items():
                res = ""
                for i in valuede:
                    res += i

                dict_podsmas2[keyde] = res

            for key3, value3 in dict_podsmas2.items():
                idsDict[key3] = value3
            new_dict = {k: v for k,v in new_dict.items() if v[1] is not None or len(v) > 1}
            for key3, value3 in new_dict.items():
                new_productions[key3] = value3

        for key, value in new_productions.items():
            self.productions[key] = value
        

        # Paso 4: Reemplazar las producciones de más de 2 símbolos que estaban en lista y ahora son un String
        for key,value in new_productions.items():
            res = ""
            for i in value:
                res += i
            new_productions[key] = res
        for key, value in self.productions.items():
            for prod in value:
                for key2, value2 in idsDict.items():
                    if prod == value2:
                        try:
                            self.productions[key][self.productions[key].index(prod)] = new_productions[key2]
                        except:
                            continue

        for key, value in idsDict.items():
            self.productions.pop(key)

        self.updateInfoInBaseProds()
        return self.delProdsRepetidas()
    
    def updateInfoInBaseProds(self):
        self.non_terminals = {key for key in self.productions.keys()}
        

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
    
    def replaceProductions(self):
        # Crear un nuevo diccionario para las producciones actualizadas
        updated_productions = {}

        # Crear un mapa de las producciones existentes
        production_map = {key: value for key, value in self.productions.items()}

        # Reemplazar las producciones en las producciones originales
        for key, productions in self.productions.items():
            updated_productions[key] = []  # Inicializa una lista para las nuevas producciones

            for production in productions:
                new_production = []
                for symbol in production:
                    # Si el símbolo es un no terminal que tiene producciones, reemplázalo
                    if symbol in production_map:
                        # Agregar las producciones correspondientes en lugar del símbolo
                        new_production.extend(production_map[symbol])
                    else:
                        new_production.append(symbol)  # Mantener el terminal o símbolo no reemplazable

                # Agregar la nueva producción al conjunto de producciones
                updated_productions[key].append(''.join(new_production))

        # Limpiar las producciones para eliminar duplicados
        self.productions = {key: list(set(value)) for key, value in updated_productions.items()}

        return self




    def convertToNormalForm(self):
        self = self.delProductionsEpsilon().delProductionsUnit().cleanBlankSpaces()
        return self
    
    def separate_symbols(self, productions):
        # Haz que verifique cada produccion y separe los simbolos no terminales y terminales por espacio, recuerda que hay simbolos que tienen una structura como X_# X_#_#
        new_productions = {}

        for key, value in productions.items():
            new_productions[key] = []
            for prod in value:
                symbols = []
                item = ""
                for char in prod:
                    if char == 'X':
                        item = char
                    elif char == '_':
                        if item == 'X':
                            item += char
                    elif char in numberListOnSTR:
                        if item == 'X_':
                            item += char
                            symbols.append(item)
                            item = ""
                        else:
                            symbols.append(char)
                    else:
                        symbols.append(char)
                new_productions[key].append(symbols)
        return new_productions

    
    def printProductions(self):
        # Si idsNonTerminals está definido
        if self.idsNonTerminals:
            # Invertir las llaves y valores de idsNonTerminals
            idsDict = {value: key for key, value in self.idsNonTerminals.items()}

            # Imprimir producciones con los reemplazos
            for key, value in self.productions.items():
                if value:
                    # Reemplazar solo si la clave no tiene guion bajo
                    key_replaced = idsDict.get(key, key) if "_" not in key else key

                    # Reemplazar los valores solo si no tienen guion bajo
                    value_replaced = []
                    for prod in value:
                        replaced_prod = ""
                        i = 0
                        while i < len(prod):
                            # Detectar y tratar símbolos con guion bajo como bloques
                            if "_" in prod[i:]:
                                # Si hay un guion bajo, tomar el bloque completo hasta el próximo símbolo o espacio
                                block_end = i + 1
                                while block_end < len(prod) and (prod[block_end].isalnum() or prod[block_end] == '_'):
                                    block_end += 1
                                symbol = prod[i:block_end]
                                i = block_end
                            else:
                                # Si no hay guion bajo, tratarlo como símbolo normal
                                if i < len(prod) - 1 and prod[i:i+2] in idsDict:
                                    symbol = prod[i:i+2]  # Tomar dos caracteres si es un símbolo concatenado
                                    i += 2  # Saltar dos caracteres
                                else:
                                    symbol = prod[i]  # Tomar un solo carácter
                                    i += 1
                            
                            # Reemplazar si no tiene guion bajo
                            replaced_symbol = idsDict.get(symbol, symbol) if "_" not in symbol else symbol
                            replaced_prod += " "+replaced_symbol

                        value_replaced.append(replaced_prod)

                    # Imprimir la producción con los valores reemplazados
                    print(f"{key_replaced} → {' | '.join(value_replaced)}")

        # Si idsNonTerminals no está definido, imprime las producciones tal cual
        else:
            for key, value in self.productions.items():
                if value:
                    print(f"{key} → {' | '.join(value)}")
    """
    def printProductions(self):
            if self.idsNonTerminals:
                # Invertir las llaves y valores de idsNonTerminals
                idsDict = {value: key for key, value in self.idsNonTerminals.items()}
                print("******************")
                print("Diccionario:")
                for key, value in idsDict.items():
                    print(f"{key} es {value}")
                print("******************")

            for key, value in self.productions.items():
                if value:
                    print(f"{key} → {' | '.join(value)}")
    """