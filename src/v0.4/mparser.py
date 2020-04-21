"""
©Pulzar 2018-20

#Author : Brian Turza
version: 0.4
#Created : 14/9/2019 (this version)
"""
import Lib.fmath as fmath

class Parser:

    def __init__(self, token_stream, include):

        self.tokens = token_stream
        self.include = include
        self.ast = {'main_scope': []}
        self.symbol_table = []
        self.isConsole = True
        self.token_index = 0

    def parse(self, token_stream):
        """
        This function takes tokens from lexer and procces them #TODO
        """
        count = 0
        while self.token_index < len(token_stream):

            token_type = self.tokens[self.token_index][0]
            token_value = self.tokens[self.token_index][1]

            # If token == echo add tokens to parse_include()
            if token_type == "KEYWORD" and token_value == "include":
                self.parse_include(token_stream[self.token_index:len(token_stream)], False)

            elif token_type == "KEYWORD" and token_value == "Program":
                self.parse_program(token_stream[self.token_index:len(token_stream)], False)
                count += 1

            elif token_type == "DATATYPE":
                self.parse_variable(token_stream[self.token_index:len(token_stream)], False, True)
            # Check if it was already dececlared

            # elif token_type == "IDENTIFIER" and self.tokens[self.token_index + 1][0] == "OPERATOR":
            # self.parse_variable(token_stream[self.token_index:len(token_stream)], False, False)

            elif token_type == "BUILT_IN_FUNCTION":
                self.parse_builtin(token_stream[self.token_index:len(token_stream)], False)

            elif token_type == "MATH_FUNCTION":
                self.parse_math(token_stream[self.token_index:len(token_stream)], False)

            elif token_type == "KEYWORD" and token_value == "if" or token_value == "else" or token_value == "elseif":
                self.parse_conditional_statements(token_stream[self.token_index:len(token_stream)], False)

            elif token_type == "KEYWORD" and token_value == "for":
                self.parse_loop(token_stream[self.token_index:len(token_stream)], False)

            elif token_type == "KEYWORD" and token_value == "while":
                self.parse_loop(token_stream[self.token_index:len(token_stream)], False)

            elif token_type == "KEYWORD" and token_value == "func":
                self.parse_func(token_stream[self.token_index:len(token_stream)], False)

            elif token_type == "KEYWORD" and token_value == "return":
                self.parse_return(token_stream[self.token_index:len(token_stream)], False)

            elif token_type == "KEYWORD" and token_value == "class":
                self.parse_class(token_stream[self.token_index:len(token_stream)], False)

            elif token_type == "COMMENT":
                self.parse_comment(token_stream[self.token_index:len(token_stream)], False)

            elif token_type == "KEYWORD" and token_value == "macros":
                self.parse_macros(token_stream[self.token_index:len(token_stream)])

            try:  # If last token pass to this, it would throw error
                if token_type == "IDENTIFIER" and token_stream[self.token_index + 1][0] == "COLON":
                    self.call_func(token_stream[self.token_index:len(token_stream)], False)
            except:
                pass

            if token_type == "UNDEFINIED":
                # TODO Identify better errors
                self.error_message("SyntaxError: \n Undefinied")

            self.token_index += 1

        # If no Program declaration is found in code, calls a error message
        if count == 0:
            self.error_message("Program Error: \nType must be included in code")

        return [self.ast, self.isConsole]

    def parse_include(self, token_stream, inScope):

        tokens_checked = 0
        list_lib = ["math", "tools"]
        lib = ""
        ast = {'Include': []}
        for token in range(0, len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token_type == "SEMIC": break

            if token == 1 and token_value == "math":
                lib = "Lib.fmath"
                ast['Include'].append({'libary': token_value})

            elif token == 1 and token_value not in list_lib:
                msg = "IncludeError:\n'{}' is not definied".format(token_value)
                self.error_message(msg)

            tokens_checked += 1

        if inScope == False:
            self.ast['main_scope'].append(ast)

        return [ast, tokens_checked]

        self.token_index += tokens_checked

    def parse_math(self, token_stream, inScope):

        value = ""
        tokens_checked = 0
        ast = {'math': []}
        for token in range(0, len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token_type == "SEMIC": break

            if token == 0: ast.append({'function': token_value})

            if token == 1 and token_type in ["INT", "ID"]:
                value = token_value

            elif token == 1 and token_type not in ["INTEGER", "IDENTIFIER"]:
                msg = "Error: '" + token_value + "' must be int"
                self.error_message(msg)

            elif token > 1 and token % 2 == 0:
                value += token_value

            tokens_checked += 1

        ast['math'].append({'arguments': value})

        if inScope == False:
            self.ast['main_scope'].append(ast)

        self.token_index += tokens_checked

        return [ast, tokens_checked]

    def parse_program(self, token_stream, inScope):

        tokens_checked = 0
        ast = {'program': []}

        for token in range(0, len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token_type == "SEMIC": break

            elif token == 1 and token_value in ["Program", "Console", "Browser"]:
                ast['program'].append({'type': token_value})
                if token_value == "Browser":
                    self.isConsole = False

            elif token == 1 and token_value not in ["Program", "Console", "Browser"]:
                self.error_message("Program error: undefinied program '{}'".format(token_value))

            tokens_checked += 1

        self.token_index += tokens_checked

        if inScope == False:
            self.ast['main_scope'].append(ast)

        return [ast, tokens_checked]

    def parse_variable(self, token_stream, inScope, decl):
        tokens_checked = 0
        ast = {'variable_declaration': []}
        value = ""
        typ8 = ""
        c = False
        var_decl = False

        for token in range(0, len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            # If  semic is found loop breaks
            if token_type == "SEMIC":
                break

            elif token == 0 and token_stream[2][0] == "SEMIC":
                ast['variable_declaration'].append({'type': token_value})
                typ8 = token_value

                ast['variable_declaration'].append({'name': token_stream[1][1]})

                if token == 0 and token_value in ["var", "int", "float"]:
                    ast['variable_declaration'].append({'value': '0'})

                elif token == 0 and token_value == "bool":
                    ast['variable_declaration'].append({'value': 'None'})

                elif token == 0 and token_value == "str":
                    ast['variable_declaration'].append({'value': '""'})

                elif token == 0 and token_value == "char":
                    ast['variable_declaration'].append({'value': "''"})

                var_decl = True
                break

            elif token == 0 and token_stream[2][0] != "SEMIC":
                ast['variable_declaration'].append({'type': token_value})
                typ8 = token_value

            elif token == 1 and token_type == "IDENTIFIER":
                ast['variable_declaration'].append({'name': token_value})

            elif token == 1 and token_type != "IDENTIFIER":
                msg = ("NameError\nInvalid variable name '" + token_value + "'")
                self.error_message(msg)

            elif token == 2 and token_type not in ["OPERATOR", "INCREMENT_OPERATOR"]:
                msg = "OperatorError\nInvalid operator '{}'".format(token_value)
                self.error_message(msg)

            elif token == 3 and token_type == "IDENTIFIER":
                value = self.get_token_value(token_value)

            elif token == 3 and token_type == "STRING":
                value = token_value.replace('\s', ' ')

            elif token == 3 and token_type == "COMPLEX_NUMBER":
                value = token_value + "j"
                c = True

            elif token == 3 and token_type not in ["COMPLEX_NUMBER", "STRING"]:
                value = str(token_value)

            elif token > 3 and token_type != "COMPLEX_NUMBER":
                value += str(token_value)

            tokens_checked += 1
        # Throws an error when the value is diffrent than declared type
        """
        if typ8 != "complex" and type(value) != typ8:
            print(type(value),"\n",typ8)
            msg = "TypeError:\n isnt %s" % typ8
            self.error_message(msg)
        """
        if type(value) == int:
            try:
                value = eval(value)
            except:
                pass

        elif type(value) == float:
            value = float(value)

        if c == True:
            try:
                value = complex(value)
            except:
                pass

        if var_decl == False:
            ast['variable_declaration'].append({'value': value})

        if inScope == False:
            self.ast['main_scope'].append(ast)

        self.symbol_table.append(['variable', ast['variable_declaration'][0], ast['variable_declaration'][1]])

        self.token_index += tokens_checked
        return [ast, tokens_checked]

    def get_scope(self, token_stream):

        nesting_count = 0
        tokens_checked = 0
        scope_tokens = []

        for token in token_stream:
            tokens_checked += 1

            token_value = token[1]
            token_type = token[0]

            if token_type == "SCOPE_DEFINIER" and token_value == "{":
                nesting_count += 1
            elif token_type == "SCOPE_DEFINIER" and token_value == "}":
                nesting_count -= 1
            if nesting_count == 0:
                scope_tokens.append(token)
                break

            else:
                scope_tokens.append(token)
        return [scope_tokens, tokens_checked]

    def parse_scope(self, token_stream, statement_ast, astName, isNested, macros):
        ast = {'scope': []}
        tokens_checked = 0
        nesting_count = 0

        while tokens_checked < len(token_stream):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]
            # If token is echo add tokens to parse_include()
            if token_type == "KEYWORD" and token_value == "include":
                include = self.parse_include(token_stream[tokens_checked:len(token_stream)])
                ast['scope'].append(include[0])
                tokens_checked += include[1]

            elif token_type == "DATATYPE":
                var = self.parse_variable(token_stream[tokens_checked:len(token_stream)], True, True)
                ast['scope'].append(var[0])
                tokens_checked += var[1]

            # Check if it was already dececlared
            # elif token_type == "IDENTIFIER" and token_value in self.symbol_table:
            # var = self.parse_variable(self.tokens[tokens_checked:len(token_stream)],True,False)
            # ast['scope'].append(var[0])
            # tokens_checked += var[1]

            elif token_type == "BUILT_IN_FUNCTION":

                builtin = self.parse_builtin(token_stream[tokens_checked:len(token_stream)], True)
                ast['scope'].append(builtin[0])
                tokens_checked += builtin[1]

            elif token_type == "MATH_FUNCTION":
                math = self.parse_math(token_stream[tokens_checked:len(token_stream)], True)
                ast['scope'].append(math[0])
                tokens_checked += math[1]

            elif token_type == "KEYWORD" and token_value == "if" or token_value == "else" or token_value == "elseif":
                condtitional = self.parse_conditional_statements(token_stream[tokens_checked:len(token_stream)], True)
                ast['scope'].append(condtitional[0])
                tokens_checked += condtitional[1] - 1

            elif token_type == "KEYWORD" and token_value == "for":
                loop = self.parse_loop(token_stream[tokens_checked:len(token_stream)], True)
                ast['scope'].append(loop[0])
                tokens_checked += loop[1]

            elif token_type == "KEYWORD" and token_value == "while":
                loop = self.parse_loop(token_stream[tokens_checked:len(token_stream)], True)
                ast['scope'].append(loop[0])
                tokens_checked += loop[1]

            elif token_type == "KEYWORD" and token_value == "func":
                function = self.parse_func(token_stream[tokens_checked:len(token_stream)], True)
                ast['scope'].append(function[0])
                tokens_checked += function[1]

            elif token_type == "KEYWORD" and token_value == "return":
                return_statment = self.parse_return(token_stream[tokens_checked:len(token_stream)], True)
                ast['scope'].append(return_statment[0])
                tokens_checked += return_statment[1]

            elif token_type == "KEYWORD" and token_value == "run":
                run = self.call_func(token_stream[tokens_checked:len(token_stream)], True)
                ast['scope'].append(run[0])
                tokens_checked += run[1]

            elif token_type == "COMMENT":
                comment = self.parse_comment(token_stream[tokens_checked:len(token_stream)], True)
                ast['scope'].append(comment[0])
                tokens_checked += comment[1]

            elif macros == True and token_value == "define":
                define = self.parse_macros_define(token_stream[tokens_checked:len(token_stream)], True)
                ast['scope'].append(define[0])
                tokens_checked += define[1]

            tokens_checked += 1

            if token_type == '}':
                nesting_count += 1

        self.token_index += nesting_count + 1

        statement_ast[astName].append(ast)
        if isNested == False:
            self.ast['main_scope'].append(statement_ast)

    def parse_builtin(self, token_stream, inScope):

        tokens_checked = 0
        value = ""
        ast = {'builtin_function': []}
        for token in range(0, len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token_type == "SEMIC": break

            if token == 0 and token_type == "BUILT_IN_FUNCTION":
                ast['builtin_function'].append({'function': token_value})

            elif token == 1 and token_type == "IDENTIFIER":
                # TODO value = self.get_token_value(token_value)
                value = token_value

            elif token == 1 and token_type != "IDENTIFIER":
                value = token_value

            elif token > 1:
                value += token_value

            tokens_checked += 1

        if type(value) == int:
            try:
                value = eval(value)
            except:
                pass

        elif type(value) == float:
            value = float(value)

        elif type(value) == complex:
            try:
                value = complex(value)
            except:
                pass

        ast['builtin_function'].append({'argument': value})

        if inScope == False:
            self.ast['main_scope'].append(ast)

        self.token_index += tokens_checked

        return [ast, tokens_checked]

    def parse_return(self, token_stream, inScope):

        tokens_checked = 0
        value = ""
        ast = {'return': []}
        for token in range(0, len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token_type == "SEMIC": break

            if token == 1 and token_type == "IDENTIFIER":
                # TODO value = self.get_token_value(token_value)
                value = token_value

            elif token == 1 and token_type != "IDENTIFIER":
                value = token_value

            elif token > 1:
                value += token_value

            tokens_checked += 1

        if type(value) in [int, float]:
            try:
                value = eval(value)
            except:
                pass

        elif type(value) == float:
            value = float(value)

        elif type(value) == complex:
            try:
                value = complex(value)
            except:
                pass

        ast['return'].append({'argument': value})

        if inScope == False:
            self.ast['main_scope'].append(ast)

        self.token_index += tokens_checked

        return [ast, tokens_checked]

    def parse_conditional_statements(self, token_stream, isNested):

        tokens_checked = 0
        condition = ""
        els = False
        tokens = []
        ast = {'conditional_statement': []}

        for token in range(0, len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token_type == "SCOPE_DEFINIER" and token_value == "{":
                break

            elif token == 0 and token_value == "if":
                ast['conditional_statement'].append({'keyword': token_value})

            elif token == 0 and token_value == "else":
                ast['conditional_statement'].append({'keyword': token_value})
                els = True

            elif token == 1:
                condition = token_value

            elif token > 1:
                condition += token_value.replace("mod", "%")

            elif token == 1 and token_type == "SCOPE_DEFINIER":
                msg = "CondtionalError:\nelse function doesnt take arguments"
                print(token_stream[tokens_checked + 1][0])
                self.error_message(msg)

            tokens_checked += 1

        if els == False:
            ast['conditional_statement'].append({'condition': condition})

        self.token_index += tokens_checked - 1
        scope_tokens = self.get_scope(token_stream[tokens_checked:len(token_stream)])

        if isNested == False:
            self.parse_scope(scope_tokens[0], ast, 'conditional_statement', False, False)
        else:
            self.parse_scope(scope_tokens[0], ast, 'conditional_statement', True, False)

        tokens_checked += scope_tokens[1]

        return [ast, tokens_checked]

    def get_token_value(self, token):
        for variable in self.symbol_table:
            if variable[0] == token: return variable[1]

    def parse_loop(self, token_stream, isNested):
        # for x :: x < 10 :: x++ {
        tokens_checked = 0
        keyword = ""
        condition = ""
        value = ""
        increment = ""
        var_decl = False
        ast = {'loop': []}

        for token in range(0, len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token_type == "SCOPE_DEFINIER" and token_value == "{":
                break

            if token == 0:
                ast['loop'].append({'keyword': token_value})
                keyword = token_value

            if token == 1 and keyword == "while":
                condition = token_value

            if token == 1 and token_type in "IDENTIFIER" and keyword != "while":
                self.get_token_value(token_value)
                ast['loop'].append({'name': token_value})
                ast['loop'].append({'start_value': self.get_token_value(token_value)})

            elif token == 1 and token_type == "DATATYPE" and keyword != "while":
                # check variale declaration
                if token_stream[token + 1][0] == "IDENTIFIER" and token_stream[token + 2][0] == "OPERATOR" and \
                        token_stream[token + 3][0] in ["INTEGER", "IDENTIFIER", ]:
                    ast['loop'].append({'name': token_value})
                    ast['loop'].append({'start_value': token_stream[token + 3][1]})

            elif token == [2, 5] and token_type != "SEPARATOR"  and keyword != "while":
                msg = "SEPARATORError: at line:\nMust be '::'"
                self.error_message(msg)

            elif token == 2 and token_type in ["OPERATOR", "COMPARTION_OPERATOR"] and keyword == "while":
                if token_value == "mod":
                    condition += "%"
                else:
                    condition += token_value

            elif token > 2 and keyword == "while":
                condition += token_value

            # elif (token == 4 and token_value != str([ast['loop'][2]['start_value']])):
            # print(token_value, str([ast['loop'][2]['start_value']]))
            # msg = ("ValueError: at line:\nMust be same as ", [ast['loop'][2]['start_value']])
            # self.error_message(msg)

            elif token == [4, 7] and token_type != "COMPARTION_OPERATOR"  and keyword != "while":
                msg = token_value + "CompertionError at line:\nMust be operator"
                self.error_message(msg)


            elif token in [5, 8] and token_type in ["INTEGER", "IDENTIFIER"]  and keyword != "while":
                ast['loop'].append({'end_value': token_value})

            elif token == [6, 9] and token_type != "SEPARATOR"  and keyword != "while":
                msg = "SeparatorError: at line:\nMust be '::'"
                self.error_message(msg)

            elif token == 7 and token_type in ["INCREMENT", "INDETIFIER"]  and keyword != "while":
                ast['loop'].append({'increment': "1"})

            elif token == 7 and token_type in ["DECREMENT", "IDENTIFIER"] and keyword != "while":
                ast['loop'].append({'increment': "1"})

            tokens_checked += 1

        self.token_index += tokens_checked - 1
        scope_tokens = self.get_scope(token_stream[tokens_checked:len(token_stream)])
        if keyword == "while": ast['loop'].append({'condition': condition})
        if isNested == False:
            self.parse_scope(scope_tokens[0], ast, 'loop', False, False)
        else:
            self.parse_scope(scope_tokens[0], ast, 'loop', True, False)

        tokens_checked += scope_tokens[1]

        return [ast, tokens_checked]

    def parse_func(self, token_stream, isNested):
        tokens_checked = 0
        value = ""
        ast = {'function_declaration': []}

        for token in range(0, len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token_type == "SCOPE_DEFINIER" and token_value == "{": break

            if token == 1 and token_type in ["IDENTIFIER", "INNER_FUNC"]:
                ast['function_declaration'].append({'name': token_value})

            elif token == 2 and token_type != "COLON":
                self.error_message("SyntaxError:\nCollon missing")

            elif token == 3 and token_value == "0":
                value = token_value

            elif token == 3 and token_type in ["IDENTIFIER", "COMMA"]:
                value = token_value

            elif token > 3 and token_type in ["IDENTIFIER", "COMMA"]:
                value += token_value

            tokens_checked += 1

        self.token_index += tokens_checked - 1

        ast['function_declaration'].append({'argument': value})

        scope_tokens = self.get_scope(token_stream[tokens_checked:len(token_stream)])

        if isNested == False:
            self.parse_scope(scope_tokens[0], ast, 'function_declaration', False, False)
        else:
            self.parse_scope(scope_tokens[0], ast, 'function_declaration', True, False)

        tokens_checked += scope_tokens[1]

        self.symbol_table.append(['function', ast['function_declaration'][0]['name'], ast['function_declaration'][1]['argument']])

        return [ast, tokens_checked]

    def parse_class(self, token_stream, isNested):
        tokens_checked = 0
        value = ""
        ast = {'class': []}

        for token in range(0, len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]
            if token_type == "SCOPE_DEFINIER" and token_value == "{": break

            if token == 1 and token_type == "IDENTIFIER":
                ast['class'].append({'name': token_value})

            elif token == 2 and token_type != "COLON":
                self.error_message(["SyntaxError:", "':' is missing"])

            elif token == 3 and token_value == "object":
                ast['class'].append({'argument': token_value})

            tokens_checked += 1

        self.token_index += tokens_checked - 1

        ast['class'].append({'argument': value})

        scope_tokens = self.get_scope(token_stream[tokens_checked:len(token_stream)])

        if isNested == False:
            self.parse_scope(scope_tokens[0], ast, 'class', False, False)
        else:
            self.parse_scope(scope_tokens[0], ast, 'class', True, False)

        tokens_checked += scope_tokens[1]

        self.symbol_table.append(['function', ast['class'][0]['name'], ast['class'][1]['argument']])

        return [ast, tokens_checked]

    def parse_comment(self, token_stream, inScope):
        tokens_checked = 0
        comment_str = ""
        ast = {'comment': []}

        for token in range(0, len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token_type == "COMMENT" and token_value == "**|": break

            if token >= 1:
                comment_str += str(token_value) + " "

            tokens_checked += 1
        ast['comment'].append({'Comment_str': comment_str})

        if inScope == False:
            self.ast['main_scope'].append(ast)

        self.token_index += tokens_checked

        return [ast, tokens_checked]

    def parse_macros(self, token_stream):
        """
		macros
		{
			define x : 10;

			redefine @echo : "print";
		}
        """
        tokens_checked = 0
        ast = {'macros': []}
        for token in range(0, len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token_type == "SCOPE_DEFINIER" and token_value == "{": break

            tokens_checked += 1

        # tokens_checked is increased by one so '{' token doesnt go there
        scope_tokens = self.get_scope(token_stream[tokens_checked + 1:len(token_stream)])

        self.parse_scope(scope_tokens[0], ast, 'macros', False, True)

    def parse_macros_define(self, token_stream, inScope):

        tokens_checked = 0
        ast = {'define': []}
        value = ""

        for token in range(len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token_type == "SEMIC":
                break

            elif token == 0:
                ast['define'].append({'function': token_value})

            elif token == 1 and token_type == "IDENTIFIER":
                ast['define'].append({'name': token_value})

            # elif token == 2 and token_type != "COLON":
            # msg = "SyntaxError:\n':' is missing, {}".format (token_value)
            # self.error_message(msg)

            elif token == 3 and token_type in ["IDENTIFIER", "STRING", "INTEGER", "BOOLEAN", "COMPLEX_NUMBER"]:
                value = str(token_value)

            elif token > 3:
                value += str(token_value)

            tokens_checked += 1

        self.token_index += tokens_checked

        ast['define'].append({"value": value})

        if inScope == False:
            self.ast['main_scope'].append(ast)

        return [ast, tokens_checked]

    # ---------------------------BROWSER------------------------------------
    # -------------------------------CALL FUNCTION------------------------------
    def call_func(self, token_stream, inScope):
        tokens_checked = 0

        name = ""
        argument = ""
        ast = {'call_function': []}

        for token in range(0, len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token_type == "SEMIC": break

            if token == 0:
                ast['call_function'].append({'name': token_value})

            elif token == 1 and token_type != "COLON":
                self.error_message("SyntaxError:")

            elif token == 2:
                if token_value == "();": argument = ""
                else: argument = token_value

            elif token > 2 and token_type in ['COMMA', 'INTEGER', 'STRING', 'BOOL']:
                argument += token_value

            tokens_checked += 1

        self.token_index += tokens_checked

        ast['call_function'].append({'argument': argument})
        self.ast['main_scope'].append(ast)

        return [ast, tokens_checked]

    # --------------------------------------------------------------------------

    def error_message(self, msg):
        print(msg)
        quit()
