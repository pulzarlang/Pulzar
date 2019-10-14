from Lib.fmath import *
from Obj.varObject import VarObject
from Obj.builtinObject import BuiltinObject
from Obj.loopObject import LoopObject
from Obj.functionObject import FuncObject
from Obj.conditionalObject import ConditionalObject
from Obj.libObject import libObject

import math
import os
class Generation(self):
    def __init__(self,ast):
        self.transpiled_code = ""
        self.ast = ast['main_scope']
    
    def generate(self):
        for ast in self.source_ast:


            if self.check_ast('variable_declaration', ast):
                var = VariableObject(ast)
                self.exec_string += var.transpile() + '\n'

            if self.check_ast('conditional_statement', ast):
                condition = ConditionObject(ast, 1)
                self.exec_string += condition.transpile() + '\n'

            if self.check_ast('builtin_function', ast):
                builtin = BuiltInFunctionObject(ast)
                self.exec_string += builtin.transpile() + "\n"

            if self.check_ast('comment', ast):
                comment = CommentObject(ast)
                self.exec_string += comment.transpile() + "\n"

            if self.check_ast('loop', ast):
                loop = LoopObject(ast, 1)
                self.exec_string += loop.transpile() + "\n"

        return self.exec_string


    def check_ast(self, astName, ast):
        try:
            if ast[astName]: return True
        except: return False
