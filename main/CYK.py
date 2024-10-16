from collections import defaultdict
import time

class Cell():
    def __init__(self):
        self.cellruleset = []
        self.backtrack = []

    def addToRules(self, ruleitem, cfgrules):
        for item in ruleitem:
            if item not in self.cellruleset:
                self.cellruleset.append(item)
                self.backtrack.append(item)
                self.propagate_unit_rules(item, cfgrules)

    def propagate_unit_rules(self, rule, cfgrules):
        for lhs, rhs_list in cfgrules.items():
            if [rule] in rhs_list and lhs not in self.cellruleset:
                self.cellruleset.append(lhs)
                self.propagate_unit_rules(lhs, cfgrules)

    def __repr__(self):
        return str(self.cellruleset)

class CYK():
    def __init__(self, folderpath):
        self.cfgrules = self.rules(folderpath)

    def rules(self, folderpath):
        unterminaldict = defaultdict(list)
        with open(folderpath, 'r') as grammarfile:
            for line in grammarfile.readlines():
                line = line.strip().split(" -> ")
                if len(line) == 2:
                    lhs = line[0].strip()
                    rhs = [item.strip() for item in line[1].split('|')]
                    unterminaldict[lhs].extend(rhs)
        
        return unterminaldict

    def get_left(self, right):
        lv = []
        right_tokens = right.split()
        for k, v in self.cfgrules.items():
            for rhs in v:
                rhs_tokens = rhs.split()
                if rhs_tokens == right_tokens:
                    lv.append(k)
                elif len(rhs_tokens) == len(right_tokens):
                    match = True
                    for i in range(len(rhs_tokens)):
                        if rhs_tokens[i] not in self.cfgrules.keys() and rhs_tokens[i] != right_tokens[i]:
                            match = False
                            break
                    if match:
                        lv.append(k)
        return lv

    def create_init_matrix(self, test_sentencelist):
        length_sentence = len(test_sentencelist)
        matrix = [[Cell() for _ in range(length_sentence)] for _ in range(length_sentence)]

        for x in range(length_sentence):
            word = test_sentencelist[x]
            for k, v in self.cfgrules.items():
                if word in v:
                    matrix[x][x].addToRules([k], self.cfgrules)
                for rhs in v:
                    if rhs == word:
                        matrix[x][x].addToRules([k], self.cfgrules)

        return matrix

    def build_parse_tree(self, matrix, start, end):
        cell = matrix[start][end]
        if not cell.backtrack:
            return None

        trees = []
        for rule in cell.backtrack:
            if len(rule.split()) == 1:
                trees.append(rule)
            else:
                left_part, right_part = rule.split()[:2]
                left_tree = self.build_parse_tree(matrix, start, start)
                right_tree = self.build_parse_tree(matrix, start + 1, end)
                trees.append(f"({rule} -> {left_tree} {right_tree})")

        return trees

    def CYKParser(self, test_sentence):
        start_time = time.time()
        test_sentencelist = test_sentence.strip().split()

        lentest = len(test_sentencelist)
        cykmatrix = self.create_init_matrix(test_sentencelist)

        for length in range(2, lentest + 1):
            for start in range(lentest - length + 1):
                end = start + length - 1
                for split in range(start, end):
                    left_rules1 = cykmatrix[start][split].cellruleset
                    left_rules2 = cykmatrix[split + 1][end].cellruleset

                    for r1 in left_rules1:
                        for r2 in left_rules2:
                            combined_rule = f"{r1} {r2}"
                            left_side = self.get_left(combined_rule)

                            if left_side:
                                cykmatrix[start][end].addToRules(left_side, self.cfgrules)

        final_cell = cykmatrix[0][lentest - 1].cellruleset
        
        end_time = time.time()

        if 'S' in final_cell:
            print("Si")
            print("Tiempo de ejecución:", end_time - start_time)
            print("Árbol de análisis:", self.build_parse_tree(cykmatrix, 0, lentest - 1))
        else:
            print("No")
            print("Tiempo de ejecución:", end_time - start_time)
