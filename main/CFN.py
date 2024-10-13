class CFN:
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
    
    def printProductions(self):
        for key, value in self.productions.items():
            print(f"{key} -> {value}")




    

    
