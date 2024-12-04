# -*- coding: utf-8 -*-
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None

    def selectNext(self):
        palavras_reservadas = [
            "choix",        # if
            "alors",        # then
            "sinon",        # else
            "si",           # para else if
            "tant_que",     # while
            "affiche",      # print
            "demande",      # scanf
            "entier",       # int
            "paroles",      # str
            "retourne",     # return
            "rien",         # void
            "chanson",      # function
            "je_taime",     # continue
            "je_te_hais",   # break
            "meilleure",    # max
            "pire",         # min
            "sentiment",    # bool
            "amour",        # true
            "haine",        # false
            "refrain",      # for
            "ajoute",       # +
            "moins",        # -
            "fois",         # *
            "sur",          # /
            "ou",           # or
            "et",           # and
            "non",          # not
            "prend",        # =
            "egal",         # ==
            "superieur_a",  # >
            "moins_que"     # <
        ]

        while (self.position < len(self.source)) and (self.source[self.position] == " " or self.source[self.position] == "\n"):
            self.position += 1

        value = ""
        type = ""

        if len(self.source) > self.position:
            if self.source[self.position] == '"':
                self.position += 1
                start_pos = self.position
                while self.position < len(self.source) and self.source[self.position] != '"':
                    self.position += 1
                if self.position >= len(self.source):
                    raise Exception("La douceur de tes mots ne trouve pas de fin, comme un amour non résolu")
                value = self.source[start_pos:self.position]
                self.position += 1
                type = "STRING"

            elif self.source[self.position].isalpha():
                value += self.source[self.position]
                self.position += 1
                while (len(self.source) > self.position) and (self.source[self.position].isalnum()) or (self.source[self.position] == "_"):
                    value += self.source[self.position]
                    self.position += 1

               # Verifica palavras reservadas ao invés de strings
                if value in palavras_reservadas:
                    type = value

                else:
                    type = "ID"  # Caso contrário, trata como identificador


            elif self.source[self.position].isdigit():
                type = "INT"  # se começar com número é um int
                while len(self.source) > self.position and self.source[self.position].isdigit():
                    value += self.source[self.position]
                    self.position += 1
                value = int(value)

            elif self.source[self.position] == "(":
                type = "LP"
                self.position += 1

            elif self.source[self.position] == ")":
                type = "RP"
                self.position += 1

            elif self.source[self.position] == "{":
                type = "LCB"  # left curly bracket
                self.position += 1

            elif self.source[self.position] == "}":
                type = "RCB"  # right curly bracket
                self.position += 1

            elif self.source[self.position] == ";":
                type = "SC"  # semicolon
                self.position += 1

            elif self.source[self.position] == ',':
                type = "COMMA" # vírgula
                self.position += 1

            elif self.source[self.position] == ":":
                type = "COLON"
                self.position += 1

            # se não for nenhum, símbolo inválido
            else:
                raise Exception("Ce symbole est une malédiction, il ne devrait pas exister ici")

            self.next = Token(type, value)

        else:
            type = "EOF"
            self.next = Token(type, value)
            self.position += 1

class Parser:
    tokenizer = None

    @staticmethod
    def run(source):
        Parser.tokenizer = Tokenizer(source)
        Parser.tokenizer.selectNext()
        return Parser.parseProgram()

    @staticmethod
    def parseProgram():
        node = Statements(None, [])

        while Parser.tokenizer.next.type != "EOF":
            node.children.append(Parser.parseFunction())

        node.children.append(FuncCall("ma_meilleure_ennemie", []))

        return node

    @staticmethod
    def parseFunction():
        if Parser.tokenizer.next.type == "chanson":
            Parser.tokenizer.selectNext()

            if Parser.tokenizer.next.type == "ID":
                func_name = Parser.tokenizer.next.value
                Parser.tokenizer.selectNext()

                if Parser.tokenizer.next.type == "LP":
                    Parser.tokenizer.selectNext()
                    var_decs = []

                    while Parser.tokenizer.next.type != "RP":
                        if Parser.tokenizer.next.type in ["entier", "paroles", "sentiment"]:
                            var_type = Parser.tokenizer.next.type
                            Parser.tokenizer.selectNext()

                            if Parser.tokenizer.next.type == "ID":
                                var_name = Parser.tokenizer.next.value
                                var_decs.append(VarDec(var_type, [Identifier(var_name, [])]))
                                Parser.tokenizer.selectNext()

                                if Parser.tokenizer.next.type == "COMMA":
                                    # Permitir mais parâmetros
                                    Parser.tokenizer.selectNext()
                                    if Parser.tokenizer.next.type == "RP":
                                        raise Exception("Entre nous, il manque quelque chose, une virgule ou peut-être une parenthèse, pour compléter notre histoire")
                                elif Parser.tokenizer.next.type != "RP":
                                    raise Exception("Ton nom se cache dans l'espace, comme une blessure qui ne s'apaise pas")
                            else:
                                raise Exception("Ton nom se cache dans l'espace, comme une blessure qui ne s'apaise pas")
                        else:
                            raise Exception("La pire des bénédictions est de choisir un type qui ne correspond pas à tes attentes")

                    Parser.tokenizer.selectNext()

                    if Parser.tokenizer.next.type == "COLON":
                        Parser.tokenizer.selectNext()

                        if Parser.tokenizer.next.type in ["entier", "paroles", "rien", "sentiment"]:
                            func_type = Parser.tokenizer.next.type
                            Parser.tokenizer.selectNext()

                            if Parser.tokenizer.next.type == "LCB":
                                statements = Parser.parseBlock()
                                resultado = FuncDec(func_name, [VarDec(func_type, var_decs), statements])
                                return resultado
                            else:
                                raise Exception("L'absence de tes bras, comme l'absence de '{' dans ta définition")
                        else:
                            raise Exception("Un détail oublié, une douce malédiction dans la définition de ta fonction")
                    else:
                        raise Exception("Un détail oublié, une douce malédiction dans la définition de ta fonction")
                else:
                    raise Exception("Le début de notre histoire manque, comme '(' dans la définition de ta fonction")
            else:
                raise Exception("Ton nom se cache dans l'espace, comme une blessure qui ne s'apaise pas")
        else:
            raise Exception("Un mot de trop, comme une malédiction qui s'abat sur nous")

    @staticmethod
    def parseBlock():
        if Parser.tokenizer.next.type == "LCB":
            Parser.tokenizer.selectNext()
            node = Block(None, [])

            while Parser.tokenizer.next.type != "RCB":
                child = Parser.parseStatement()  # guardar no node
                node.children.append(child)
            Parser.tokenizer.selectNext()

        else:
            raise Exception("Ce symbole est une malédiction, il ne devrait pas exister ici")

        return node

    @staticmethod
    def parseStatement():
        if Parser.tokenizer.next.type == "SC":  # caminho do semicolon
            Parser.tokenizer.selectNext()
            resultado = NoOp("", "")
        
        elif Parser.tokenizer.next.type in ["entier", "paroles", "rien", "sentiment"]:  # caminho do tipo
            var_type = Parser.tokenizer.next.type
            Parser.tokenizer.selectNext()

            declarations = []
            assignments = []

            while True:
                if Parser.tokenizer.next.type == "ID":
                    identifier = Identifier(Parser.tokenizer.next.value, [])
                    declarations.append(identifier)
                    Parser.tokenizer.selectNext()

                    if Parser.tokenizer.next.type == "prend":
                        Parser.tokenizer.selectNext()
                        expression = Parser.parseExpression()
                        assignments.append(Assignment("", [identifier, expression]))

                    if Parser.tokenizer.next.type == "COMMA":
                        Parser.tokenizer.selectNext()
                    else:
                        break
                else:
                    raise Exception("Ce symbole est une malédiction, il ne devrait pas exister ici")

            resultado = VarDec(var_type, declarations + [Block("", assignments)])

            if Parser.tokenizer.next.type == "SC":
                Parser.tokenizer.selectNext()
            else:
                raise Exception("Ce petit détail qui manque, comme un mot non dit entre nous ;")

        elif Parser.tokenizer.next.type == "ID":  # caminho do identifier para atribuição ou chamada de função
            identifier = Identifier(Parser.tokenizer.next.value, [])
            Parser.tokenizer.selectNext()

            if Parser.tokenizer.next.type == "prend":
                Parser.tokenizer.selectNext()
                expression = Parser.parseExpression()
                resultado = Assignment("", [identifier, expression])

                if Parser.tokenizer.next.type == "SC":
                    Parser.tokenizer.selectNext()
                else:
                    raise Exception("Ce petit détail qui manque, comme un mot non dit entre nous ;")
            elif Parser.tokenizer.next.type == "LP":
                Parser.tokenizer.selectNext()
                args = []

                while Parser.tokenizer.next.type != "RP":
                    args.append(Parser.parseRelativeExpression())

                    if Parser.tokenizer.next.type == "COMMA":
                        Parser.tokenizer.selectNext()
                    elif Parser.tokenizer.next.type != "RP":
                        raise Exception("Entre nous, il manque quelque chose, une virgule ou peut-être une parenthèse, pour compléter notre histoire")

                Parser.tokenizer.selectNext()
                resultado = FuncCall(identifier.value, args)

                if Parser.tokenizer.next.type == "SC":
                    Parser.tokenizer.selectNext()
                else:
                    raise Exception("Ce petit détail qui manque, comme un mot non dit entre nous ;")
            else:
                raise Exception("Ce symbole est une malédiction, il ne devrait pas exister ici")

        elif Parser.tokenizer.next.type == "affiche":  # caminho do Print
            Parser.tokenizer.selectNext()

            if Parser.tokenizer.next.type == "LP":
                Parser.tokenizer.selectNext()
                resultado = Print("", [Parser.parseRelativeExpression()])

                if Parser.tokenizer.next.type == "RP":
                    Parser.tokenizer.selectNext()

                    if Parser.tokenizer.next.type == "SC":
                        Parser.tokenizer.selectNext()
                    else:
                        raise Exception("Ce petit détail qui manque, comme un mot non dit entre nous ;")
                else:
                    raise Exception("Ne regarde pas en arrière, mais n'oublie pas de fermer notre histoire avec un ')'")

            else:
                raise Exception("Ce symbole est une malédiction, il ne devrait pas exister ici")

        elif Parser.tokenizer.next.type == "tant_que":  # caminho do while
            Parser.tokenizer.selectNext()
            condicao = Parser.parseRelativeExpression()
            resultado = While('', [condicao, Parser.parseStatement()])

        elif Parser.tokenizer.next.type == "choix":  # caminho do if
            Parser.tokenizer.selectNext()

            if Parser.tokenizer.next.type == "LP":
                Parser.tokenizer.selectNext()
                condicao = Parser.parseRelativeExpression()

                if Parser.tokenizer.next.type == "RP":
                    Parser.tokenizer.selectNext()

                    if Parser.tokenizer.next.type == "alors":
                        Parser.tokenizer.selectNext()
                        acao = Parser.parseStatement()

                        elif_statements = []

                        while Parser.tokenizer.next.type == "sinon":
                            Parser.tokenizer.selectNext()
                            if Parser.tokenizer.next.type == "si":
                                Parser.tokenizer.selectNext()

                                if Parser.tokenizer.next.type == "LP":
                                    Parser.tokenizer.selectNext()
                                    elif_condicao = Parser.parseRelativeExpression()

                                    if Parser.tokenizer.next.type == "RP":
                                        Parser.tokenizer.selectNext()

                                        if Parser.tokenizer.next.type == "alors":
                                            Parser.tokenizer.selectNext()
                                            elif_acao = Parser.parseStatement()
                                            elif_statements.append((elif_condicao, elif_acao))
                                        else:
                                            raise Exception("'alors' est comme une promesse douce, sans elle notre histoire ne peut pas continuer")
                                    else:
                                        raise Exception("Ne regarde pas en arrière, mais n'oublie pas de fermer notre histoire avec un ')'")
                                else:
                                    raise Exception("Le début de notre histoire manque, comme '(' dans la définition de ta fonction")
                            else:
                                else_acao = Parser.parseStatement()
                                return Choix('', [condicao, acao, elif_statements, else_acao])

                        resultado = Choix('', [condicao, acao, elif_statements])
                    else:
                        raise Exception("Sans 'alors', l'histoire ne peut pas continuer...")
                else:
                    raise Exception("Ne regarde pas en arrière, mais n'oublie pas de fermer notre histoire avec un ')'")
            else:
                raise Exception("Le début de notre histoire manque, comme '(' dans la définition de ta fonction")

        elif Parser.tokenizer.next.type == "retourne":  # caminho do return
            Parser.tokenizer.selectNext()
            expression = Parser.parseRelativeExpression()

            if Parser.tokenizer.next.type == "SC":
                Parser.tokenizer.selectNext()
                resultado = Return("", [expression])
            else:
                raise Exception("Ce petit détail qui manque, comme un mot non dit entre nous ;")
            
        elif Parser.tokenizer.next.type == "je_taime":  # caminho do continue
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "SC":
                Parser.tokenizer.selectNext()
                resultado = Continue("")
            else:
                raise Exception("Ce petit détail qui manque, comme un mot non dit entre nous ;")

        elif Parser.tokenizer.next.type == "je_te_hais":  # caminho do break
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "SC":
                Parser.tokenizer.selectNext()
                resultado = Break("")
            else:
                raise Exception("Ce petit détail qui manque, comme un mot non dit entre nous ;")
        
        elif Parser.tokenizer.next.type == "refrain":  # caminho do for
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "INT":
                loop_count = Parser.tokenizer.next.value
                Parser.tokenizer.selectNext()
                loop_body = Parser.parseStatement()
                resultado = Refrain(loop_count, [loop_body])

            else:
                raise Exception("Le refrain manque un nombre, comme une danse sans rythme, indéfinie et perdue")
            
        else:
            resultado = Parser.parseBlock()

        return resultado

    @staticmethod
    def parseRelativeExpression():
        resultado = Parser.parseExpression()
        while Parser.tokenizer.next.type == "egal" or Parser.tokenizer.next.type == "superieur_a" or Parser.tokenizer.next.type == "moins_que":

            if Parser.tokenizer.next.type == "egal":
                Parser.tokenizer.selectNext()
                resultado = BinOp("egal", [resultado, Parser.parseExpression()])

            if Parser.tokenizer.next.type == "superieur_a":
                Parser.tokenizer.selectNext()
                resultado = BinOp("superieur_a", [resultado, Parser.parseExpression()])

            if Parser.tokenizer.next.type == "moins_que":
                Parser.tokenizer.selectNext()
                resultado = BinOp("moins_que", [resultado, Parser.parseExpression()])

        return resultado

    @staticmethod
    def parseExpression():
        resultado = Parser.parseTerm()
        while Parser.tokenizer.next.type == "ajoute" or Parser.tokenizer.next.type == "moins" or Parser.tokenizer.next.type == "ou":

            if Parser.tokenizer.next.type == "ajoute":
                Parser.tokenizer.selectNext()
                resultado = BinOp("ajoute", [resultado, Parser.parseTerm()])

            if Parser.tokenizer.next.type == "moins":
                Parser.tokenizer.selectNext()
                resultado = BinOp("moins", [resultado, Parser.parseTerm()])

            if Parser.tokenizer.next.type == "ou":
                Parser.tokenizer.selectNext()
                resultado = BinOp("ou", [resultado, Parser.parseTerm()])

        return resultado

    @staticmethod
    def parseTerm():
        resultado = Parser.parseFactor()
        while Parser.tokenizer.next.type == "fois" or Parser.tokenizer.next.type == "sur" or Parser.tokenizer.next.type == "et":

            if Parser.tokenizer.next.type == "fois":
                Parser.tokenizer.selectNext()
                resultado = BinOp("fois", [resultado, Parser.parseFactor()])

            if Parser.tokenizer.next.type == "sur":
                Parser.tokenizer.selectNext()
                resultado = BinOp("sur", [resultado, Parser.parseFactor()])

            if Parser.tokenizer.next.type == "et":
                Parser.tokenizer.selectNext()
                resultado = BinOp("et", [resultado, Parser.parseFactor()])

        return resultado

    @staticmethod
    def parseFactor():
        if Parser.tokenizer.next.type == "INT":
            resultado = IntVal(Parser.tokenizer.next.value, [])
            Parser.tokenizer.selectNext()

        elif Parser.tokenizer.next.type == "STRING":
            resultado = StringVal(Parser.tokenizer.next.value, [])
            Parser.tokenizer.selectNext()

        elif Parser.tokenizer.next.type == "ajoute":
            Parser.tokenizer.selectNext()
            resultado = UnOp("ajoute", [Parser.parseFactor()])

        elif Parser.tokenizer.next.type == "moins":
            Parser.tokenizer.selectNext()
            resultado = UnOp("moins", [Parser.parseFactor()])

        elif Parser.tokenizer.next.type == "non":
            Parser.tokenizer.selectNext()
            resultado = UnOp("non", [Parser.parseFactor()])

        elif Parser.tokenizer.next.type == "LP":
            Parser.tokenizer.selectNext()
            resultado = Parser.parseRelativeExpression()

            if Parser.tokenizer.next.type == "RP":
                Parser.tokenizer.selectNext()
            else:
                raise Exception("Ne regarde pas en arrière, mais n'oublie pas de fermer notre histoire avec un ')'")

        elif Parser.tokenizer.next.type == "demande":
            Parser.tokenizer.selectNext()
            resultado = Read('', [])

            if Parser.tokenizer.next.type == "LP":
                Parser.tokenizer.selectNext()

                if Parser.tokenizer.next.type == "RP":
                    Parser.tokenizer.selectNext()
                else:
                    raise Exception("Ne regarde pas en arrière, mais n'oublie pas de fermer notre histoire avec un ')'")

            else:
                raise Exception("Le début de notre histoire manque, comme '(' dans la définition de ta fonction")

        elif Parser.tokenizer.next.type == "ID":
            identifier = Identifier(Parser.tokenizer.next.value, [])
            Parser.tokenizer.selectNext()

            if Parser.tokenizer.next.type == "LP":
                Parser.tokenizer.selectNext()
                args = []

                while Parser.tokenizer.next.type != "RP":
                    args.append(Parser.parseExpression())

                    if Parser.tokenizer.next.type == "COMMA":
                        Parser.tokenizer.selectNext()
                    elif Parser.tokenizer.next.type != "RP":
                        raise Exception("Entre nous, il manque quelque chose, une virgule ou peut-être une parenthèse, pour compléter notre histoire")

                Parser.tokenizer.selectNext()
                resultado = FuncCall(identifier.value, args)
            else:
                resultado = identifier
        
        elif Parser.tokenizer.next.type == "meilleure":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "LP":
                Parser.tokenizer.selectNext()
                args = []

                while Parser.tokenizer.next.type != "RP":
                    args.append(Parser.parseRelativeExpression())

                    if Parser.tokenizer.next.type == "COMMA":
                        Parser.tokenizer.selectNext()
                    elif Parser.tokenizer.next.type != "RP":
                        raise Exception("Entre nous, il manque quelque chose, une virgule ou peut-être une parenthèse, pour compléter notre histoire")

                Parser.tokenizer.selectNext()
                resultado = MaxFunc(args)
            else:
                raise Exception("Le début de notre histoire manque, comme '(' dans la définition de ta fonction")

        elif Parser.tokenizer.next.type == "pire":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "LP":
                Parser.tokenizer.selectNext()
                args = []

                while Parser.tokenizer.next.type != "RP":
                    args.append(Parser.parseRelativeExpression())

                    if Parser.tokenizer.next.type == "COMMA":
                        Parser.tokenizer.selectNext()
                    elif Parser.tokenizer.next.type != "RP":
                        raise Exception("Entre nous, il manque quelque chose, une virgule ou peut-être une parenthèse, pour compléter notre histoire")

                Parser.tokenizer.selectNext()
                resultado = MinFunc(args)
            else:
                raise Exception("Le début de notre histoire manque, comme '(' dans la définition de ta fonction")
            
        elif Parser.tokenizer.next.type == "amour":
            resultado = BoolVal(True, [])
            Parser.tokenizer.selectNext()

        elif Parser.tokenizer.next.type == "haine":
            resultado = BoolVal(False, [])
            Parser.tokenizer.selectNext()
        
        else:
            raise Exception("Ce symbole est une malédiction, il ne devrait pas exister ici")

        return resultado


class PrePro:
    @staticmethod
    def filter(string):
        resultado = ""
        i = 0
        length = len(string)
        
        while i < length:
            if i < length - 1 and string[i] == '/' and string[i + 1] == '*':
                # Encontrou o início de um comentário /*, então pula para o fim do comentário
                i += 2  # Pular os caracteres /*
                while i < length - 1 and not (string[i] == '*' and string[i + 1] == '/'):
                    i += 1
                    if i == length - 1:
                        # Se chegar ao final da string sem encontrar o fechamento do comentário
                        raise RuntimeError("Erreur: Le commentaire ouvert n'a pas été correctement fermé.")
                i += 2  # Pular os caracteres */
            else:
                resultado += string[i]
                i += 1

        return resultado


class Node:
    def __init__(self, value, children):
        self.value = value  # variant
        self.children = children  # list of nodes

    def Evaluate(self):  # variant
        pass


class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        val_f1, type_f1 = self.children[0].Evaluate()
        val_f2, type_f2 = self.children[1].Evaluate()

        if self.value == "ajoute":
            if type_f1 == 'paroles' or type_f2 == 'paroles':
                return str(val_f1) + str(val_f2), 'paroles'
            elif type_f1 == 'entier' and type_f2 == 'entier':
                return val_f1 + val_f2, 'entier'
            else:
                raise Exception(f"Incohérence de type : L'opération d'ajout nécessite des opérandes 'entier' ou 'paroles', mais a reçu '{type_f1}' et '{type_f2}'. Comme l'amour et la haine, ces types ne peuvent se mêler.")

        elif self.value == "moins":
            if type_f1 == 'entier' and type_f2 == 'entier':
                return val_f1 - val_f2, 'entier'
            else:
                raise Exception(f"Incohérence de type : L'opération de soustraction nécessite des opérandes 'entier', mais a reçu '{type_f1}' et '{type_f2}'. Comme une promesse qui se perd entre l'amour et la haine.")

        elif self.value == "fois":
            if type_f1 == 'entier' and type_f2 == 'entier':
                return val_f1 * val_f2, 'entier'
            else:
                raise Exception(f"Incohérence de type : L'opération de multiplication nécessite des opérandes 'entier', mais a reçu '{type_f1}' et '{type_f2}'. Comme des souvenirs qui ne s'accordent pas, ces types ne peuvent être combinés.")

        elif self.value == "sur":
            if type_f1 == 'entier' and type_f2 == 'entier':
                if val_f2 == 0:
                    raise Exception("Diviser par zéro, comme s'attendre à ce que l'amour et la haine se rencontrent sans fin")
                return val_f1 // val_f2, 'entier'
            else:
                raise Exception(f"Incohérence de type : L'opération de division nécessite des opérandes 'entier', mais a reçu '{type_f1}' et '{type_f2}'. Comme tenter de diviser nos souvenirs entre amour et haine, cela ne peut être fait.")

        elif self.value == "egal":
            if type_f1 == type_f2:
                return int(val_f1 == val_f2), 'sentiment'
            else:
                raise Exception(f"Incohérence de type : L'opération d'égalité nécessite des types identiques, mais a reçu '{type_f1}' et '{type_f2}'. Comme l'amour et la haine, ces types ne peuvent être comparés équitablement.")

        elif self.value == "superieur_a":
            if type_f1 == type_f2:
                return int(val_f1 > val_f2), 'entier'
            else:
                raise Exception(f"Incohérence de type : L'opération 'superieur_a' nécessite des types identiques, mais a reçu '{type_f1}' et '{type_f2}'. Comme comparer des rêves et des souvenirs, cela ne peut être fait.")

        elif self.value == "moins_que":
            if type_f1 == type_f2:
                return int(val_f1 < val_f2), 'entier'
            else:
                raise Exception(f"Incohérence de type : L'opération 'moins_que' nécessite des types identiques, mais a reçu '{type_f1}' et '{type_f2}'. Comme vouloir toucher les étoiles sans les comprendre, cela ne peut être comparé.")

        elif self.value == "et":
            if type_f1 == 'entier' or 'sentiment' and type_f2 == 'entier' or 'sentiment':
                return int(bool(val_f1) and bool(val_f2)), 'entier'
            else:
                raise Exception(f"Incohérence de type : L'opération 'et' nécessite des opérandes 'sentiment', mais a reçu '{type_f1}' et '{type_f2}'. Comme unir deux âmes qui ne se comprennent pas.")

        elif self.value == "ou":
            if type_f1 == 'entier' or 'sentiment' and type_f2 == 'entier' or 'sentiment':
                return int(bool(val_f1) or bool(val_f2)), 'entier'
            else:
                raise Exception(f"Incohérence de type : L'opération 'ou' nécessite des opérandes 'sentiment', mais a reçu '{type_f1}' et '{type_f2}'. Comme essayer de réconcilier le jour et la nuit.")

        else:
            raise Exception("Ce symbole est une malédiction, il ne devrait pas exister ici")


class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        val, type_val = self.children[0].Evaluate()

        if self.value == "moins":
            if type_val == 'entier':
                return -val, 'entier'
            else:
                raise Exception(f"Incohérence de type : L'opération de négation nécessite un opérande 'entier', mais a reçu '{type_val}'. Comme un cœur cherchant à se libérer de ses propres chaînes, cela ne peut être fait.")
        
        elif self.value == "non":
            if type_val == 'sentiment':
                return int(not bool(val)), 'sentiment'
            else:
                raise Exception(f"Incohérence de type : L'opération 'non' nécessite un opérande 'sentiment', mais a reçu '{type_val}'. Comme nier un sentiment qui ne peut être ignoré, cela ne peut être supporté.")

        else:
            return val, type_val


class IntVal(Node):  # Integer value. Não contem filhos
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        return self.value, 'entier'  # Retorna o valor e o tipo

class StringVal(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        return self.value, 'paroles'  # Retorna o valor e o tipo

class BoolVal(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        return self.value, 'sentiment'  # Retorna o valor e o tipo

class NoOp(Node):  # No Operation (Dummy). Não contem filhos
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        return super().Evaluate()

class Block(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
        
    def Evaluate(self):
        last_result = None  # Para armazenar o último resultado avaliado
        for child in self.children:
            result = child.Evaluate()  # Avalia o nó atual
            if isinstance(child, Return):  # Retorna imediatamente ao encontrar um Return
                return result
            if result is not None:  # Armazena o último resultado válido
                last_result = result
        return last_result  # Retorna o último resultado avaliado, se nenhum Return for encontrado



class Assignment(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        identifier = self.children[0].value
        value, value_type = self.children[1].Evaluate()
        if identifier in SymbolTable.table:
            var_type = SymbolTable.table[identifier][1]
            if var_type == value_type:
                SymbolTable.table[identifier][0] = value  # Atualiza o valor da variável na tabela de símbolos
            else:
                raise Exception(f"Incohérence de type: La variable '{identifier}' est de type '{var_type}' mais a reçu '{value_type}'")
        else:
            raise Exception(f"'{identifier}' est comme un nom oublié, jamais déclaré dans nos souvenirs")

class Identifier(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        if self.value in SymbolTable.table:
            value, var_type = SymbolTable.table[self.value]
            return value, var_type  # Retorna o valor e o tipo da variável
        else:
            raise Exception(f"'{self.value}' est comme un nom oublié, jamais déclaré dans nos souvenirs")


class Print(Node):  # só tem um child
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        value, _ = self.children[0].Evaluate()
        print(value)


class Read(Node):  # não tem children e nem value, seu evaluate que retorna o valor de um input
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        user_input = input()
        if user_input.isdigit():
            return int(user_input), 'entier'
        else:
            raise Exception("Ce que tu dis ne correspond pas, j'attendais un entier, mais tes mots me blessent")


class While(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        while self.children[0].Evaluate()[0]:
            try:
                self.children[1].Evaluate()
            except ContinueException:
                continue
            except BreakException:
                break


class Choix(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        condition_result, _ = self.children[0].Evaluate()
        if condition_result:
            return self.children[1].Evaluate()
        elif len(self.children) > 2:
            for elif_condicao, elif_acao in self.children[2]:
                elif_result, _ = elif_condicao.Evaluate()
                if elif_result:
                    return elif_acao.Evaluate()
            if len(self.children) > 3:
                return self.children[3].Evaluate()


class VarDec(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        var_type = self.value
        for child in self.children[:-1]:  # Exclui o último filho (bloco de assignments)
            if var_type == 'entier':
                initial_value = 0
            elif var_type == 'paroles':
                initial_value = ""
            elif var_type == 'sentiment':
                initial_value = False
            else:
                raise Exception(f"Type non supporté : '{var_type}' est comme un rêve qui ne trouve pas sa place dans notre réalité.")
            
            # Define variável apenas no escopo atual
            SymbolTable.set_table(child.value, initial_value, var_type)
        
        if self.children:  # Se houver bloco de assignments
            self.children[-1].Evaluate()


class FuncDec(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        func_name = self.value
        # Verifica se a função já está declarada
        if func_name in SymbolTable.table:
            raise Exception(f"La fonction '{func_name}' a déjà été déclarée, comme un amour déjà exprimé, inutile de le répéter")
        # Adiciona a função na SymbolTable
        SymbolTable.set_table(func_name, self, "FUNCTION")


class FuncCall(Node):
    def Evaluate(self):
        func_name = self.value
        if func_name not in SymbolTable.table:
            raise Exception(f"'{func_name}' n'est pas une fonction, mais peut-être un souvenir d'un amour passé")
        func_dec, func_type = SymbolTable.get_table(func_name)

        if func_type != "FUNCTION":
            raise Exception(f"'{func_name}' n'est pas une fonction, mais peut-être un souvenir d'un amour passé")

        var_decs = func_dec.children[0].children
        func_body = func_dec.children[1]

        if len(var_decs) != len(self.children):
            raise Exception(f"La fonction '{func_name}' attend {len(var_decs)} arguments, mais a reçu {len(self.children)}.")

        SymbolTable.push_scope()

        try:
            # Avalia os argumentos e define no escopo local
            for var_dec, arg_node in zip(var_decs, self.children):
                arg_value, arg_type = arg_node.Evaluate()
                var_name = var_dec.children[0].value
                var_type = var_dec.value
                if arg_type != var_type:
                    raise Exception(f"Incohérence de type pour l'argument '{var_name}': attendu {var_type}, mais reçu {arg_type}.")
                SymbolTable.set_table(var_name, arg_value, var_type)

            # Avalia o corpo da função e captura retorno
            return func_body.Evaluate()
        finally:
            SymbolTable.pop_scope()


class Statements(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        for child in self.children:
            child.Evaluate()

class Return(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        return self.children[0].Evaluate()

class Continue(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def Evaluate(self):
        raise ContinueException()

class Break(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def Evaluate(self):
        raise BreakException()

class MaxFunc(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def Evaluate(self):
        values = [child.Evaluate()[0] for child in self.children]
        return max(values), 'entier'


class MinFunc(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def Evaluate(self):
        values = [child.Evaluate()[0] for child in self.children]
        return min(values), 'entier'

class Refrain(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        loop_count = self.value
        for _ in range(loop_count):
            self.children[0].Evaluate()

class SymbolTable:
    table = {}
    stack = []

    @staticmethod
    def get_table(key):
        """Busca uma entrada na tabela de símbolos."""
        if key in SymbolTable.table:
            return SymbolTable.table[key]
        else:
            raise Exception(f"'{key}' n'est pas défini dans le contexte actuel.")

    @staticmethod
    def set_table(key, value, entry_type):
        """Define uma nova entrada na tabela de símbolos."""
        if key in SymbolTable.table and key not in SymbolTable.stack[-1]:  # Verifica apenas no escopo atual
            raise Exception(f"'{key}' est déjà déclaré dans le contexte actuel.")
        SymbolTable.table[key] = [value, entry_type]


    @staticmethod
    def push_scope():
        SymbolTable.stack.append(SymbolTable.table.copy())

    @staticmethod
    def pop_scope():
        if SymbolTable.stack:
            SymbolTable.table = SymbolTable.stack.pop()
        else:
            raise Exception("Il n'y a plus rien à retirer, comme si le passé nous rattrapait.")

class ContinueException(Exception):
    pass

class BreakException(Exception):
    pass

# main
with open("test2.mme", "r", encoding="utf-8") as f:
    Parser.run(PrePro.filter(f.read())).Evaluate()