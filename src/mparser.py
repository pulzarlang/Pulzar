"""
©Pulzar 2018-20

#Author : Brian Turza
version: 0.4
#Created : 14/9/2019 (this version)
"""
from Lib.math.main import *
import numpy as np
import re


class Parser:

    def __init__(self, token_stream, include):

        self.tokens = token_stream
        self.include = include
        self.ast = {'main_scope': []}
        self.symbol_table = []
        self.isConsole = True
        self.lines = 1
        self.token_index = 0
        self.nesting_count = 0
        self.error = False

    def parse(self, token_stream):
        """
        This function takes tokens from lexer and procces them #TODO
        """
        count = 0
        while self.token_index < len(token_stream):

            token_type = self.tokens[self.token_index][0]
            token_value = self.tokens[self.token_index][1]
            # If token == echo add tokens to parse_include()
            if self.error:
                return [self.ast, self.isConsole, self.error]
            if token_type == "KEYWORD" and token_value == "include":
                self.parse_include(token_stream[self.token_index:len(token_stream)], False)

            elif token_type == "KEYWORD" and token_value == "Program":
                self.parse_program(token_stream[self.token_index:len(token_stream)], False)
                count += 1

            elif token_type == "DATATYPE":
                self.parse_decl_variable(token_stream[self.token_index:len(token_stream)], False)
            # Check if it was already dececlared

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

            elif token_type == "KEYWORD" and token_value == "class":
                self.parse_class(token_stream[self.token_index:len(token_stream)], False)

            elif token_type == "COMMENT" and token_value == r"\\":
                self.parse_single_line_comment(token_stream[self.token_index:len(token_stream)], False)

            elif token_type == "COMMENT" and token_value == "|**":
                self.parse_multi_line_comment(token_stream[self.token_index:len(token_stream)], False)

            elif token_type == "KEYWORD" and token_value == "macros":
                self.parse_macros(token_stream[self.token_index:len(token_stream)])

            elif token_type == "KEYWORD" and token_value == "match":
                self.parse_match(token_stream[self.token_index:len(token_stream)], False)

            elif token_type == "NEWLINE": self.lines += 1

            try:  # If last token pass to this, it would throw error
                if token_type == "IDENTIFIER" and token_stream[self.token_index + 1][0] == "COLON":
                    self.call_func(token_stream[self.token_index:len(token_stream)], False)
            except:
                pass

            try:
                if token_type == "IDENTIFIER" and self.tokens[self.token_index + 1][1] == "=" or token_type == "IDENTIFIER" and self.tokens[self.token_index + 1][0] == "INCREMENT_OPERATOR":
                    self.parse_variable(token_stream[self.token_index:len(token_stream)], False)
            except IndexError: pass

            if token_type == "UNDEFINIED":
                # TODO Identify better errors
                self.error_message("SyntaxError: \n Undefinied")

            self.token_index += 1

        # If no Program declaration is found in code, calls a error message
        if count == 0:
            msg = "SyntaxError at line {}:\nProgram must be definied".format(self.lines)
            self.error_message(msg, token_stream, self.token_index)

        return [self.ast, self.isConsole, self.error]

    def parse_include(self, token_stream, inScope):

        tokens_checked = 0
        lib = ""
        ast = {'Include': []}
        for token in range(0, len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token_type in ["SEMIC"]: break

            if token == 1 and token_type != "STRING":
                lib = "Lib.{}.main".format(token_value)
                try:
                    import importlib
                    importlib.import_module(lib)
                except ImportError:
                    msg = "IncludeError at line {}:\n'{}' isnt recognized as libary or pulzar file".format(self.lines, token_value)
                    self.error_message(msg, token_stream, token)

            elif token == 1 and token_type == "STRING":
                lib = token_value

            tokens_checked += 1

        ast['Include'].append({'libary': lib})

        if inScope == False:
            self.ast['main_scope'].append(ast)

        self.token_index += tokens_checked

        return [ast, tokens_checked]

    def parse_math(self, token_stream, inScope):

        value = ""
        tokens_checked = 0
        ast = {'math': []}
        for token in range(0, len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token_type == "SEMIC": break

            if token == 0: ast['math'].append({'function': token_value})

            if token == 1 and token_type in ["INT", "ID"]:
                value = token_value

            elif token == 1 and token_type not in ["INTEGER", "IDENTIFIER"]:
                msg = "Error: '" + token_value + "' must be int"
                self.error_message(msg, token_stream, token)

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

        if inScope == False:
            self.ast['main_scope'].append(ast)

        self.token_index += tokens_checked

        return [ast, tokens_checked]

    def parse_decl_variable(self, token_stream, inScope):
        tokens_checked = 0
        ast = {'variable_declaration': []}
        value = ""
        typ8 = ""
        c = False
        var_decl = False
        square_root = False
        dots = False
        for token in range(0, len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            # If  semic is found loop breaks

            if token_type in ["SEMIC", "NEWLINE"]:
                break

            elif token == 0 and token_stream[2][0] == "SEMIC":
                ast['variable_declaration'].append({'type': token_value})
                typ8 = token_value

                ast['variable_declaration'].append({'name': token_stream[1][1]})

                if token == 0 and token_value in ["var", "int", "float"]:
                    ast['variable_declaration'].append({'value': '0'})

                elif token == 0 and token_value == "complex":
                    ast['variable_declaration'].append({'value': 'Complex()'})

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
                msg = "SyntaxError at line"+ str(self.lines) +":\nInvalid variable name '" + token_value + "'"
                self.error_message(msg, token_stream, token)

            elif token == 2 and token_type not in ["OPERATOR", "INCREMENT_OPERATOR"]:
                msg = "SyntaxError at line {}\n:Invalid operator '{}'".format(self.lines, token_value)
                self.error_message(msg, token_stream, token)

            elif token == 3 and token_type == "IDENTIFIER" and token_value not in constants and token_stream[tokens_checked + 1][1] != ":":
                value = str(token_value)

            elif token == 3 and token_type == "IDENTIFIER" and token_value in constants:
                value = "constants['{}']".format(token_value)

            elif token == 3 and token_type == "STRING":
                value = token_value.replace('\s', ' ')

            elif token == 3 and token_type == "COMPLEX_NUMBER":
                value = str(token_value) + "j"
                c = True

            elif token == 3 and token_type == "SQUARE_ROOT":
                if re.match("[a-z]", token_value) or re.match("[A-Z]", token_value):
                    token_value = self.get_token_value(token_value)
                if token_value[len(token_value) - 1] in ["i", "j"]:
                    value = str(np.sqrt(complex(token_value)))
                else:
                    value = str(np.sqrt(float(token_value)))

            elif token == 3 and token_type not in ["COMPLEX_NUMBER", "STRING", "FACTORIAL"]:
                value = str(token_value)

            elif token > 3 and token_type not in ["COMPLEX_NUMBER", "FACTORIAL", "OPERATOR", "SQUARE_ROOT", "IDENTIFIER", "ELLIPSIS_OPERATOR"]:
                value += str(token_value)

            elif token > 3 and token_type == "OPERATOR":
                value += str(token_value.replace('^', '**'))

            elif token > 3 and token_type == "ELLIPSIS_OPERATOR":
                value += str(token_value)
                dots = True

            elif token == 3 and token_type == "FACTORIAL":
                math = MathModule()
                value = str(math.factorial(int(token_value)))

            elif token > 3 and token_type == "COMPLEX_NUMBER":
                value += str(token_value) + "j"
                c = True

            elif token > 3 and token_type == "FACTORIAL":
                math = MathModule()
                value += str(math.factorial(int(token_value)))

            elif token > 3 and token_type == "IDENTIFIER" and token_value in constants:
                value += "constants['{}']".format(token_value)

            elif token > 3 and token_type == "IDENTIFIER":
                value += str(token_value)

            elif token > 3 and token_type == "SQUARE_ROOT":
                if re.match("[a-z]", token_value) or re.match("[A-Z]", token_value):
                    token_value = self.get_token_value(token_value)
                if token_value[len(token_value) - 1] in ["i", "j"]:
                    value += str(np.sqrt(complex(token_value)))
                else:
                    value += str(np.sqrt(float(token_value)))

            elif token >= 3 and token_type in ["DATATYPE", "KEYWORD"]:
                msg = "SyntaxError at line "+ str(self.lines) +":\nInvalid variable value '" + token_value + "'"
                self.error_message(msg, token_stream, token)

            tokens_checked += 1

        if dots:
            value = str(self.get_tokens_range(value))

        #----------------------------------------------------------
        #TYPE CHECKING & EVALUATION:
        def type_check(value):
            string = True
            if "[" in value and "]" in value:
                return
            if re.match("[0-9]", value) or value in ["True", "False", "None"] or "constants" in value:
                string = False

            if typ8 == "str" and string:
                value = str(value)

            elif typ8 == "str" and string == False:
                msg = "TypeError at line %s:\nDeclared wrong data type, %s is not string" % (self.lines, value)
                self.error_message(msg, token_stream, token)

            if typ8 == "char" and string and len(value) == 1:
                value = str(value)

            elif typ8 == "char" and string == False or typ8 == "char" and len(value) > 3:
                msg = "TypeError at line %s:\nDeclared wrong data type, %s is not char" % (self.lines, value)
                self.error_message(msg, token_stream, token)

            if typ8 == "int" and string == False and value not in ["True", "False", "None"]:
                try:
                    value = eval(value)
                    value = int(value)
                except NameError:
                    pass
            elif typ8 == "int" and string == True or typ8 == "int" and value in ["True", "False", "None"]:
                msg = "TypeError at line %s:\nDeclared wrong data type, '%s' is not integer" % (self.lines, value)
                self.error_message(msg, token_stream, token)

            if typ8 == "float" and string == False and value not in ["True", "False", "None"]:
                try:
                    value = eval(value)
                    value = float(value)
                except NameError:
                    pass

            elif typ8 == "float" and string == True or typ8 == "float" and value in ["True", "False", "None"]:
                msg = "TypeError at line %s:\nDeclared wrong data type, '%s' is not float" % (self.lines, value)
                self.error_message(msg, token_stream, token)

            if typ8 == "complex" and string == False and value not in ["True", "False", "None"]:
                try:
                    value = eval(value)
                    value = 'Complex({}, {})'.format(value.real, value.imag)
                except NameError:
                    pass

            elif typ8 == "complex" and string == True or typ8 == "complex" and value in ["True", "False", "None"]:
                msg = "TypeError at line %s:\nDeclared wrong data type, '%s' is not complex number" % (
                self.lines, value)
                self.error_message(msg, token_stream, token)

            if typ8 == "bool" and value in ["True", "False", "None"]:
                try:
                    value = bool(value)
                except NameError:
                    pass
            elif typ8 == "bool" and value not in ["True", "False", "None"]:
                msg = "TypeError at line %s:\nDeclared wrong data type, '%s' is not boolean" % (self.lines, value)
                self.error_message(msg, token_stream, token)

        if var_decl == False:
            string = True
            type_check(value)
        #---------------------------------------------------------

        if var_decl == False:
            ast['variable_declaration'].append({'value': value})

        if inScope == False:
            self.ast['main_scope'].append(ast)

        self.symbol_table.append([ast['variable_declaration'][0]['type'], ast['variable_declaration'][1]['name'], ast['variable_declaration'][2]['value']]) # type, name, value

        self.token_index += tokens_checked

        return [ast, tokens_checked]

    def parse_variable(self, token_stream, inScope):
        tokens_checked = 0
        ast = {'variable_declaration': []}
        value = ""
        typ8 = ""
        c = False
        var_decl = False
        square_root = False
        dots = False
        for token in range(0, len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            # If  semic is found loop breaks
            if token_type in ["SEMIC", "NEWLINE"]:
                break

            elif token == 0 and token_type == "IDENTIFIER":
                typ8 = self.get_token_type(token_value)
                ast['variable_declaration'].append({'type': typ8})
                ast['variable_declaration'].append({'name': token_value})

            elif token == 0 and token_type != "IDENTIFIER":
                msg = ("SyntaxError at line "+ str(self.lines) +"\nInvalid variable name '" + token_value + "'")
                self.error_message(msg, token_stream, token)

            elif token == 1 and token_type not in ["OPERATOR", "INCREMENT_OPERATOR"]:
                msg = "SyntaxError at line {}:\nInvalid operator '{}'".format(self.lines, token_value)
                self.error_message(msg, token_stream, token)

            elif token == 2 and token_type == "IDENTIFIER" and token_value not in constants and token_stream[tokens_checked + 1][1] != ":":
                value = str(token_value)

            elif token == 2 and token_type == "IDENTIFIER" and token_value in constants:
                value = "constants['{}']".format(token_value)

            elif token == 2 and token_type == "STRING":
                value = token_value.replace('\s', ' ')

            elif token == 2 and token_type == "COMPLEX_NUMBER":
                value = str(token_value) + "j"
                c = True

            elif token == 2 and token_type == "SQUARE_ROOT":
                if re.match("[a-z]", token_value) or re.match("[A-Z]", token_value):
                    token_value = self.get_token_value(token_value)
                if token_value[len(token_value) - 1] in ["i", "j"]:
                    value = str(np.sqrt(complex(token_value)))
                else:
                    value = str(np.sqrt(float(token_value)))

            elif token == 2 and token_type not in ["COMPLEX_NUMBER", "STRING", "FACTORIAL"]:
                value = str(token_value)

            elif token > 2 and token_type not in ["COMPLEX_NUMBER", "FACTORIAL", "OPERATOR", "SQUARE_ROOT", "ELLIPSIS_OPERATOR"]:
                value += str(token_value)

            elif token > 2 and token_type == "OPERATOR":
                value += str(token_value.replace('^', '**'))

            elif token > 2 and token_type == "ELLIPSIS_OPERATOR":
                value += str(token_value)
                dots = True

            elif token == 2 and token_type == "FACTORIAL":
                math = MathModule()
                value = str(math.factorial(int(token_value)))

            elif token > 2 and token_type == "COMPLEX_NUMBER":
                value += str(token_value) + "j"
                c = True

            elif token > 2 and token_type == "FACTORIAL":
                math = MathModule()
                value += str(math.factorial(int(token_value)))

            elif token > 2 and token_type == "IDENTIFIER" and token_value in constants:
                value += "constants['{}']".format(token_value)

            elif token > 2 and token_type == "SQUARE_ROOT":
                if re.match("[a-z]", token_value) or re.match("[A-Z]", token_value):
                    token_value = self.get_token_value(token_value)
                if token_value[len(token_value) - 1] in ["i", "j"]:
                    value += str(np.sqrt(complex(token_value)))
                else:
                    value += str(np.sqrt(float(token_value)))

            tokens_checked += 1

        if dots:
            value = str(self.get_tokens_range(value))

        #TYPE CHECKING & EVALUATION:
        #----------------------------------------------------------
        string = True
        def type_check(value):
            if re.match("[0-9]", value) or value in ["True", "False", "None"]:
                string = False

            if typ8 == "str" and string:
                value = str(value)

            elif typ8 == "str" and string == False:
                msg = "TypeError at line %s:\nDeclared wrong data type, %s is not string" % (self.lines, value)
                self.error_message(msg, token_stream, token)

            if typ8 == "char" and string and len(value) == 1:
                value = str(value)

            elif typ8 == "char" and string == False or typ8 == "char" and len(value) > 3:
                msg = "TypeError at line %s:\nDeclared wrong data type, %s is not char" % (self.lines, value)
                self.error_message(msg, token_stream, token)

            if typ8 == "int" and string == False and value not in ["True", "False", "None"]:
                try:
                    value = eval(value)
                    value = int(value)
                except NameError:
                    pass
            elif typ8 == "int" and string == True or typ8 == "int" and value in ["True", "False", "None"]:
                msg = "TypeError at line %s:\nDeclared wrong data type, '%s' is not integer" % (self.lines, value)
                self.error_message(msg, token_stream, token)

            if typ8 == "float" and string == False and value not in ["True", "False", "None"]:
                try:
                    value = eval(value)
                    value = float(value)
                except NameError:
                    pass

            elif typ8 == "float" and string == True or typ8 == "float" and value in ["True", "False", "None"]:
                msg = "TypeError at line %s:\nDeclared wrong data type, '%s' is not float" % (self.lines, value)
                self.error_message(msg, token_stream, token)

            if typ8 == "bool" and value in ["True", "False", "None"]:
                try:
                    value = bool(value)
                except NameError:
                    pass
            elif typ8 == "bool" and value not in ["True", "False", "None"]:
                msg = "TypeError at line %s:\nDeclared wrong data type, '%s' is not boolean" % (self.lines, value)
                self.error_message(msg, token_stream, token)
        #---------------------------------------------------------

        if var_decl == False:
            ast['variable_declaration'].append({'value': value})

        if inScope == False:
            self.ast['main_scope'].append(ast)

        for i in self.symbol_table:
            if i[1] == ast['variable_declaration'][1]['name']:
                #Change delcared varaible value to this one
                i[2] = ast['variable_declaration'][2]['value']

        self.token_index += tokens_checked

        return [ast, tokens_checked]

    def get_scope(self, token_stream):

        nesting_count = 1
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

    def parse_scope(self, token_stream, statement_ast, astName, isNested, macros, match_case=False):
        ast = {'scope': []}
        tokens_checked = 0
        lines = 1
        while tokens_checked < len(token_stream):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if match_case:
                case = self.parse_case(token_stream[tokens_checked + 1:len(token_stream)])
                ast['scope'].append(case[0])
                tokens_checked += case[1]

            # If token is echo add tokens to parse_include()
            if token_type == "KEYWORD" and token_value == "include":
                include = self.parse_include(token_stream[tokens_checked:len(token_stream)])
                ast['scope'].append(include[0])
                tokens_checked += include[1]

            elif token_type == "DATATYPE":
                var = self.parse_decl_variable(token_stream[tokens_checked:len(token_stream)], True)
                ast['scope'].append(var[0])
                tokens_checked += var[1]

            elif token_type == "IDENTIFIER" and token_stream[tokens_checked + 1][1] == "=" or token_type == "IDENTIFIER" and token_stream[tokens_checked + 1][0] == "INCREMENT_OPERATOR":
                varx = self.parse_variable(token_stream[tokens_checked:len(token_stream)], True)
                ast['scope'].append(varx[0])
                tokens_checked += varx[1]

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
                return_statement = self.parse_return(token_stream[tokens_checked:len(token_stream)], True)
                ast['scope'].append(return_statement[0])
                tokens_checked += return_statement[1]


            elif token_type == "COMMENT" and token_value == r"\\":
                comment = self.parse_single_line_comment(token_stream[tokens_checked:len(token_stream)], True)
                ast['scope'].append(comment[0])
                tokens_checked += comment[1]

            elif token_type == "COMMENT" and token_value == "|**":
                comment = self.parse_multi_line_comment(token_stream[tokens_checked:len(token_stream)], True)
                ast['scope'].append(comment[0])
                tokens_checked += comment[1]

            elif macros == True and token_value == "define":
                define = self.parse_macros_define(token_stream[tokens_checked:len(token_stream)], True)
                ast['scope'].append(define[0])
                tokens_checked += define[1]

            try:  # If last token pass to this, it would throw error
                if token_type == "IDENTIFIER" and token_stream[tokens_checked + 1][0] == "COLON":
                    run = self.call_func(token_stream[tokens_checked:len(token_stream)], True)
                    ast['scope'].append(run[0])
                    tokens_checked += run[1]
            except:
                pass

            if token_type == "NEWLINE":
                self.lines += 1

            if token_value == "}":
                self.nesting_count += 1

            tokens_checked += 1

        self.token_index += self.nesting_count + 1

        self.lines -= 1

        statement_ast[astName].append(ast)
        if isNested == False:
            self.ast['main_scope'].append(statement_ast)

    def parse_builtin(self, token_stream, inScope):

        tokens_checked = 0
        value = ""
        ast = {'builtin_function': []}
        execute = False
        for token in range(0, len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token_type == "SEMIC": break

            if token == 0 and token_type == "BUILT_IN_FUNCTION":
                ast['builtin_function'].append({'function': token_value})

            elif token == 1 and token_type == "IDENTIFIER" and token_value not in constants:
                if token_stream[0][1] == "execute":
                    value = self.get_token_value(token_value)
                elif token_stream[0][1] == "input":
                    ast['builtin_function'].append({'type' : self.get_token_type(token_value)})
                    value = str(token_value)
                else:
                    value = str(token_value)

            elif token == 1 and token_type == "IDENTIFIER" and token_value in constants:
                value = "constants['{}']".format(token_value)

            elif token == 1 and token_type not in ["IDENTIFIER", "FACTORIAL", "SQUARE_ROOT"]:
                value = token_value

            elif token == 1 and token_type == "FACTORIAL":
                math = MathModule()
                value = str(math.factorial(int(token_value)))

            elif token == 1 and token_type == "SQUARE_ROOT":
                if re.match("[a-z]", token_value) or re.match("[A-Z]", token_value):
                    token_value = str(self.get_token_value(token_value))
                if "Complex(" in token_value and ")" in token_value:
                    value = str(np.sqrt(token_value))
                else:
                    value = str(np.sqrt(float(token_value)))

            elif token > 1 and token_type == "FACTORIAL":
                math = MathModule()
                value += str(math.factorial(int(token_value)))

            elif token > 1 and token_type not in ["FACTORIAL", "OPERATOR", "IDENTIFIER"]:
                value += str(token_value)

            elif token > 1 and token_type == "OPERATOR":
                value += str(token_value.replace('^', '**'))

            elif token > 1 and token_type == "IDENTIFIER" and token_value not in constants:
                if token_stream[0][1] == "execute":
                    value += self.get_token_value(token_value)
                else:
                    value += str(token_value)

            elif token > 1 and token_type == "IDENTIFIER" and token_value in constants:
                value += "constants['{}']".format(token_value)

            tokens_checked += 1

        if type(value) == int:
            value = int(value)

        elif type(value) == float:
            value = float(value)

        elif type(value) == complex:
            fmath = MathModule()
            value = fmath.complex(value)

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
                value = token_value

            elif token == 1 and token_type == "IDENTIFIER" and token_stream[tokens_checked + 1][0] == "COLON":
                value = token_value

            elif token == 1 and token_type != "IDENTIFIER":
                value = token_value

            elif token == 1 and token_type == "FACTORIAL":
                math = MathModule()
                value = str(math.factorial(int(token_value)))

            elif token > 1 and token_type == "FACTORIAL":
                math = MathModule()
                value += str(math.factorial(int(token_value)))

            elif token > 1 and token_type != "FACTORIAL":
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

            elif token == 1 and token_type != "FACTORIAL":
                condition = token_value

            elif token == 1 and token_type == "FACTORIAL":
                math = MathModule()
                condition = str(math.factorial(int(token_value)))
            elif token > 1 and token_type == "FACTORIAL":
                math = MathModule()
                condition += str(math.factorial(int(token_value)))

            elif token > 1 and token_type != "FACTORIAL":
                condition += token_value.replace("mod", "%")

            tokens_checked += 1

        if els == False:
            ast['conditional_statement'].append({'condition': condition})

        self.token_index += tokens_checked

        scope_tokens = self.get_scope(token_stream[tokens_checked + 1:len(token_stream)])

        if isNested == False:
            self.parse_scope(scope_tokens[0], ast, 'conditional_statement', False, False)
        else:
            self.parse_scope(scope_tokens[0], ast, 'conditional_statement', True, False)

        tokens_checked += scope_tokens[1]

        return [ast, tokens_checked]

    def get_token_value(self, token):
        for variable in self.symbol_table:
            if variable[1] == token: return variable[2]

    def get_token_type(self, token):
        for variable in self.symbol_table:
            if variable[1] == token: return variable[0]

    def find_token_type(self, token):
        #int
        try:
            token = int(token)
            datatype = 'int'
        except:
            pass


    def get_tokens_range(self, value):
        amount = 0
        if "..." in value:
            value = value.split('...')
            amount = 1
        elif ".." in value:
            value = value.split('..')
            amount = 0
        arr = []
        try:
            value[0], value[1] = int(value[0]), int(value[1])

            for i in range(value[0], value[1] + amount): # startValue to endValue
                arr.append(i)

        except:
            startValue, endValue = value[0].replace("'", "").replace('"', ''), value[1].replace("'", "").replace('"', '')
            for i in range(ord(startValue), ord(endValue) + amount):
                arr.append(chr(i))

        return arr

    def get_token_match(self, start_matcher, end_matcher, token_stream):
        tokens = []
        tokens_checked = 0
        for token in token_stream:
            tokens_checked += 1

            if token[1] == end_matcher:
                return [tokens, tokens_checked - 1]
            else:
                tokens.append(token)

        return False


    def parse_loop(self, token_stream, isNested):
        # for x :: x < 10 :: x++ {
        tokens_checked = 0
        keyword = ""
        condition = ""
        value = ""
        increment = ""
        var_decl = False
        ast = {'loop': []}

        while tokens_checked < len(token_stream):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token_type == "SCOPE_DEFINIER" and token_value == "{":
                break

            if tokens_checked == 0:
                ast['loop'].append({'keyword': token_value})
                keyword = token_value

            if tokens_checked == 1 and keyword == "for":
                tokens = self.get_token_match("::", "{", token_stream)
                inner_tokens = [i[1] for i in tokens[0]]
                if "in" in inner_tokens:
                    array = ""
                    data_type = self.get_token_type(inner_tokens[3])
                    ast['loop'].append({'name': inner_tokens[1]})
                    ast['loop'].append({'type': data_type})
                    ast['loop'].append({'array': ''.join(inner_tokens[3:])})
                    self.symbol_table.append([data_type, inner_tokens[1], inner_tokens[3:]])
                else:
                    if len([i for i, x in enumerate(inner_tokens) if x == "::"]) != 2:
                        self.error_message("SyntaxError:\nSymbol '::' is missing in a for loop", token_stream, tokens_checked)
                    inner_tokens[:] = [x for x in inner_tokens if x != '::']
                    ast['loop'].append({'name': inner_tokens[1]})
                    ast['loop'].append({'start_value': self.get_token_value(inner_tokens[2])})
                    ast['loop'].append({'end_value': inner_tokens[4]})
                    if "++" in inner_tokens[5]:
                        ast['loop'].append({'increment': "1"})
                    elif "--" in inner_tokens[5]:
                        ast['loop'].append({'increment': "-1"})

                tokens_checked += tokens[1]
                break

            tokens_checked += 1

        self.token_index += tokens_checked
        scope_tokens = self.get_scope(token_stream[tokens_checked + 1:len(token_stream)])

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
                msg = "SyntaxError at line "+ str(self.lines) +":\n':' is missing"
                self.error_message(msg, token_stream, token)

            elif token == 3 and token_value == "0":
                value = token_value

            elif token == 3 and token_type in ["IDENTIFIER", "COMMA"]:
                value = token_value

            elif token > 3 and token_type in ["IDENTIFIER", "COMMA"]:
                value += token_value

            tokens_checked += 1

        ast['function_declaration'].append({'argument': value})

        self.token_index += tokens_checked - 1

        scope_tokens = self.get_scope(token_stream[tokens_checked + 1:len(token_stream)])

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
                msg = f"SyntaxError at line {self.lines}\n':' is missing."
                self.error_message(msg, token_stream, token)

            elif token == 3 and token_value == "object":
                ast['class'].append({'argument': token_value})
                decl = True

            tokens_checked += 1

        scope_tokens = self.get_scope(token_stream[tokens_checked + 1:len(token_stream)])

        self.token_index += tokens_checked - 1

        if isNested == False:
            self.parse_scope(scope_tokens[0], ast, 'class', False, False)
        else:
            self.parse_scope(scope_tokens[0], ast, 'class', True, False)

        tokens_checked += scope_tokens[1]

        self.symbol_table.append(['function', ast['class'][0]['name'], ast['class'][1]['argument']])

        return [ast, tokens_checked]

    def parse_single_line_comment(self, token_stream, inScope):
        tokens_checked = 0
        comment_str = ""
        ast = {'comment': []}

        for token in range(0, len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token_type == "NEWLINE": break

            if token >= 1:
                comment_str += str(token_value) + " "

            tokens_checked += 1
        ast['comment'].append({'Comment_str': comment_str})

        if inScope == False:
            self.ast['main_scope'].append(ast)

        self.token_index += tokens_checked

        return [ast, tokens_checked]

    def parse_multi_line_comment(self, token_stream, inScope):
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

    def parse_match(self, token_stream, isNested):
        """
        var stdin;
        input stdin;
        match stdin {
            1 -> echo "One";
        }
        """
        tokens_checked = 0
        ast = {'match': []}
        scope_ast = {'scope': []}
        for token in range(0, len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]
            if token_type == "SCOPE_DEFINIER" and token_value == "{": break

            if token == 1:
                ast['match'].append({'variable': token_value})

            tokens_checked += 1

        self.token_index += tokens_checked - 1

        scope_tokens = self.get_scope(token_stream[tokens_checked + 1:len(token_stream)])

        if isNested == False:
            self.parse_scope(scope_tokens[0], ast, 'match', False, False, True)
        else:
            self.parse_scope(scope_tokens[0], ast, 'match', True, False, True)

        tokens_checked += scope_tokens[1]


    def parse_case(self, token_stream):
        tokens_checked = 0
        value = ""
        ast = {'current_case' : []}
        while tokens_checked < len(token_stream):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            print(tokens_checked, token_type, token_value)

            if token_type == "SEMIC" and token_value == ";": break

            if tokens_checked == 0:
                ast['current_case'].append({'case': token_value})

            elif tokens_checked == 1 and token_type != "ARROW":
                msg = f"SyntaxError at line {self.lines}\n{token_type, token_value} !='->' symbol is missing."
                self.error_message(msg, token_stream, tokens_checked)
                break

            elif tokens_checked == 2:
                value = token_value

            elif tokens_checked > 2:
                value += f" {token_value}"

            tokens_checked += 1

        self.token_index += tokens_checked

        ast['current_case'].append({'command' : value})

        return [ast, tokens_checked]

    def parse_macros(self, token_stream):
        """
		macros
		{
			define x, 10;

			redefine @echo, "print";
		}
        """
        tokens_checked = 0
        ast = {'macros': []}
        for token in range(0, len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token_type == "SCOPE_DEFINIER" and token_value == "{": break

            tokens_checked += 1

        scope_tokens = self.get_scope(token_stream[tokens_checked + 1:len(token_stream)])

        self.parse_scope(scope_tokens[0], ast, 'macros', False, True)

    def parse_macros_define(self, token_stream, inScope):

        tokens_checked = 0
        ast = {'define': []}
        value = ""
        for token in range(len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]



            if token_type == "SEMIC":break

            if token == 0:
                ast['define'].append({'function': token_value})

            elif token == 1 and token_type == "IDENTIFIER":
                ast['define'].append({'name': token_value})

            elif token == 2 and token_type in ["IDENTIFIER", "STRING", "INTEGER", "BOOLEAN", "COMPLEX_NUMBER"]:
                value = str(token_value)

            elif token > 2:
                value += str(token_value)

            tokens_checked += 1

        self.token_index += tokens_checked

        ast['define'].append({"value": value})

        if inScope == False:
            self.ast['main_scope'].append(ast)

        self.symbol_table.append([type(ast['define'][2]['value']), ast['define'][1]['name'], ast['define'][2]['value']])

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
                self.error_message("SyntaxError at line {}: ':' is missing".format(self.lines))

            elif token == 2:
                if token_value == "()": argument = ""
                else: argument = token_value

            elif token > 2 and token_type in ['COMMA', 'INTEGER', 'STRING', 'BOOL']:
                argument += token_value

            tokens_checked += 1

        self.token_index += tokens_checked

        ast['call_function'].append({'argument': argument})
        self.ast['main_scope'].append(ast)

        return [ast, tokens_checked]

    # --------------------------------------------------------------------------

    def error_message(self, msg, token_stream, token):
        tokens_checked = 1
        length = 0
        #This for loop will get amount of tokens in the error line
        for token in range(len(token_stream)):
            if token_stream[token][0] in ["SEMIC", "NEWLINE"]: break
            tokens_checked += 1

        print(msg)
        error_msg = " ".join(str(token[1]) for token in token_stream[:tokens_checked] if token[0] not in ["SEMIC", "NEWLINE"]) # Loops through each token in token_stream and forms a error line
        print("".join(error_msg[:-2] + ";" if error_msg[-1:] == ";" else error_msg))
        for i in range(len(token_stream)):
            if i == token: break
            else: length += len(token_stream[i][1])
        print(" " * length + "^")
        self.error = True