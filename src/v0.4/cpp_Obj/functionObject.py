from cpp_Obj.varObject import VarObject
from cpp_Obj.builtinObject import BuiltinObject
from cpp_Obj.conditionalObject import ConditionalObject
from cpp_Obj.loopObject import LoopObject
from cpp_Obj.returnObject import ReturnObject

class FuncObject(object):

    def __init__(self, source_ast, nesting_count):
        self.exec_str = ""
        self.ast = source_ast['function_declaration']
        self.nesting_count = nesting_count

    def transpile(self):
        name = ""
        arg = ""
        for ast in self.ast:

            try: name = ast['name']
            except: pass
            try: arg = ast['argument']
            except: pass
            try: scope = ast['scope']
            except: pass

        self.exec_str += "void " + str(name) + "(" + str(arg) + ")" + "{\n" + self.transpile_scope(scope, self.nesting_count, 2) + "\n}"
        return self.exec_str

    def transpile_scope(self, body_ast, nesting_count, items):

        body_exec_string = ""

        # Loop through each ast item in the body dictionary
        for ast in body_ast:

            # This will parse variable declerations within the body
            if self.check_ast('variable_declaration', ast):
                var_obj = VarObject(ast)
                transpile = var_obj.transpile()
                if self.should_dedent_trailing(ast, self.ast, items):
                    body_exec_string += ("    " * (nesting_count - 1)) + transpile + "\n"
                else:
                    body_exec_string += ("    " * nesting_count) + transpile + "\n"

            # This will parse built-in within the body
            if self.check_ast('builtin_function', ast):
                gen_builtin = BuiltinObject(ast)
                transpile = gen_builtin.transpile()
                if self.should_dedent_trailing(ast, self.ast, 2):
                    body_exec_string += ("    " * (nesting_count - 1)) + transpile[0] + "\n"
                else:
                    body_exec_string += ("    " * nesting_count) + transpile[0] + "\n"

            if self.check_ast('return', ast):
                gen_return = ReturnObject(ast)
                transpile = gen_return.transpile()
                if self.should_dedent_trailing(ast, self.ast, 2):
                    body_exec_string += ("    " * (nesting_count - 1)) + transpile + "\n"
                else:
                    body_exec_string += ("    " * nesting_count) + transpile + "\n"

            # This will parse nested conditional statement within the body
            if self.check_ast('conditional_statement', ast):
                # Increase nesting count because this is a condition statement inside a conditional statement
                # Only increase nest count if needed
                if self.should_increment_nest_count(ast, self.ast):
                    nesting_count += 1
                # Create conditional statement exec string
                condition_obj = ConditionalObject(ast, nesting_count)
                # The second nested statament only needs 1 indent not 2
                if nesting_count == 2:
                    # Add the content of conditional statement with correct indentation
                    body_exec_string += "    " + condition_obj.transpile()
                else:
                    # Add the content of conditional statement with correct indentation
                    body_exec_string += ("    " * (nesting_count - 1)) + condition_obj.transpile()

            # This will parse nested conditional statement within the body
            if self.check_ast('loop', ast):
                # Increase nesting count because this is a condition statement inside a conditional statement
                # Only increase nest count if needed
                if self.should_increment_nest_count(ast, self.ast):
                    nesting_count += 1
                # Create conditional statement exec string
                loop_obj = LoopObject(ast, nesting_count)
                body_exec_string += ("    " * (nesting_count - 1)) + loop_obj.transpile()

        return body_exec_string

    def check_ast(self, astName, ast):

        try:
            # In some cases when method is called from should_Dedent_trailing metho ast
            # comes back with corret key but empty list value because it is removed. If
            # this is removed this method returns None instead and causes condition trailing
            # code to be indented one more than it should
            if ast[astName] == []: return True
            if ast[astName]: return True
        except:
            return False

    def should_dedent_trailing(self, ast, full_ast, items):

        new_ast = full_ast[len(full_ast) - 1]['scope']
        new_ast = full_ast[len(full_ast) - 1]['scope']
        # This will know whether it should dedent
        dedent_flag = False

        # Loop through body ast's and when a conditonal statement is founds set
        # the dedent flag to 'true'
        for x in new_ast:

            # When a conditional statemenet AST is found set the dedent trailing to true
            if self.check_ast('conditional_statement', x):
                dedent_flag = True

            if ast == x and dedent_flag == True:
                return True

        return False

    def should_increment_nest_count(self, ast, full_ast):
        # Counts of the number of statements in that one scope
        statement_counts = 0
        # Loops through the body to count the number of conditional statements
        for x in full_ast[len(full_ast) - 1]['scope']:
            # If a statement is found then increment statement count variable value by 1
            if self.check_ast('loop', x): statement_counts += 1
            # If the statement being checked is the one found then break
            if ast == x: break

        # Return false if there were less then 1 statements
        if statement_counts > 1:
            return False
        # Returen true if there were more than 1 statements
        else:
            return True

class RunFuncObject(object):
    
    def __init__(self, source_ast):
        self.exec_str = ""
        self.ast = source_ast['call_function']
    
    def transpile(self):
        name = ""
        arg = ""
        for ast in self.ast:

            try: name = ast['name']
            except: pass
            try: arg = ast['argument']
            except: pass
            
        if arg == "":
            self.exec_str += name + "();"
        else:
            self.exec_str += name + "(" + arg + ");"
        
        return self.exec_str
