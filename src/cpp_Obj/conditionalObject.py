from cpp_Obj.varObject import VarObject
from cpp_Obj.builtinObject import BuiltinObject
from cpp_Obj.returnObject import ReturnObject
import cpp_Obj.loopObject

class ConditionalObject:

    def __init__(self, source_ast, nesting_count):
        self.exec_str = ""
        self.ast = source_ast['conditional_statement']
        self.nesting_count = nesting_count

    def transpile(self):
        keyword = ""
        condition = ""
        
        for ast in self.ast:

            try: keyword = ast['keyword']
            except: pass
            try: condition = ast['condition']
            except: pass
            try: scope = ast['scope']
            except: pass

        if keyword != "else":
            self.exec_str += keyword + "(" + condition + ") {\n" + self.transpile_scope(scope, self.nesting_count, 2) + "\t" * (self.nesting_count - 1) + "}" + "\n"
        else:
            self.exec_str += "else {\n" + self.transpile_scope(scope, self.nesting_count, 1) + "\t" * (self.nesting_count - 1) + "}" + "\n"

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
                if self.should_dedent_trailing(ast, self.ast, items):
                    body_exec_string += ("    " * (nesting_count - 1)) + transpile[0] + "\n"
                else:
                    body_exec_string += ("    " * nesting_count) + transpile[0] + "\n"

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
                loop_obj = cpp_Obj.loopObject.LoopObject(ast, nesting_count)
                body_exec_string += ("    " * (nesting_count - 1)) + loop_obj.transpile()

            if self.check_ast('return', ast):
                gen_return = ReturnObject(ast)
                transpile = gen_return.transpile()
                if self.should_dedent_trailing(ast, self.ast, items):
                    body_exec_string += ("    " * (nesting_count - 1)) + transpile + "\n"
                else:
                    body_exec_string += ("    " * nesting_count) + transpile + "\n"

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
        #print(full_ast, items)
        new_ast = full_ast[len(full_ast) - 1]['scope']
        # This will know whether it should dedent
        dedent_flag = False

        # Loop through body ast's and when a conditonal statement is founds set
        # the dedent flag to 'true'
        for x in new_ast:

            # When a conditional stateemenet AST is found set the dedent trailing to true
            if self.check_ast('ConditionalStatement', x):
                dedent_flag = True

            if ast == x and dedent_flag == True:
                return True

        return False

    def should_increment_nest_count(self, ast, full_ast):
        """ Should dedent trailing

        This method will check if the ast item being checked is outside a conditional statement e.g.

        if a == 11 {
            if name == "Ryan Maugin" {
                print "Not it";
            }
            if 1 != 2 { <--- This is the statement that should not be nested more
                print "Yo"
            }
        }

        args:
            ast       (list) : The ConditionalStatement ast we are looking for
            full_ast  (list) : The full ast being parsed
        return:
            True  : If the nesting should increase by 1
            False : If the nesting ahould not be increased
        """

        # Counts of the number of statements in that one scope
        statement_counts = 0

        # Loops through the body to count the number of conditional statements
        for x in full_ast[len(full_ast) - 1]['scope']:

            # If a statement is found then increment statement count variable value by 1
            if self.check_ast('ConditionalStatement', x): statement_counts += 1
            # If the statement being checked is the one found then break
            if ast == x: break

        # Return false if there were less then 1 statements
        if statement_counts > 1:
            return False
        # Returen true if there were more than 1 statements
        else:
            return True