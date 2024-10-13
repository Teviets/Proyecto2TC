# Diccionario de producciones
productions = {
    'S': ['X_1X_0A', 'X_1X_0B', 'X_1X_0AB', 'X_1X_0'],
    'A': ['X_0X_1', 'X_0AX_1'],
    'B': ['X_0AX_1', 'X_1', 'AX_1', 'X_0X_1', 'BAX_1', 'BX_1'],
    'X_0': ['b'],
    'X_1': ['a'],
    'S_1': ['X_1', 'S_1_1'],
    'S_1_1': ['X_0', 'S_1_2'],
    'S_1_2': ['A', 'S_1_3'],
    'S_2': ['X_1', 'S_2_3'],
    'S_2_3': ['X_0', 'S_2_4'],
    'S_2_4': ['B', 'S_2_5'],
    'S_3': ['X_1', 'S_3_5'],
    'S_3_5': ['X_0', 'S_3_6'],
    'S_3_6': ['A', 'S_3_7'],
    'S_3_7': ['B', 'S_3_8'],
    'A_1': ['X_0', 'A_1_1'],
    'A_1_1': ['A', 'A_1_2'],
    'A_1_2': ['X_1', 'A_1_3'],
    'B_1': ['X_0', 'B_1_1'],
    'B_1_1': ['A', 'B_1_2'],
    'B_1_2': ['X_1', 'B_1_3'],
    'B_2': ['B', 'B_2_3'],
    'B_2_3': ['A', 'B_2_4'],
    'B_2_4': ['X_1', 'B_2_5']
}

# Filtrar las producciones que comienzan con 'S_' seguido de un número
filtered_productions = {
    key: value for key, value in productions.items()
    if key.startswith('S_') and key[2:].isdigit()
}

# Imprimir las producciones filtradas
for key, value in filtered_productions.items():
    print(f"{key} -> {value}")
