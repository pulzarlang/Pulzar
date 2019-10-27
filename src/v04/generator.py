from Lib.fmath import *
from Obj.varObject import VarObject
from Obj.builtinObject import BuiltinObject
from Obj.loopObject import LoopObject
from Obj.functionObject import FuncObject
from Obj.conditionalObject import ConditionalObject
from Obj.libObject import libObject

import math
import os
class Generation(object):
    def __init__(self,source_ast):
        self.transpiled_code = ""

        self.source_ast = source_ast['main_scope']
    
    def generate(self):

        for ast in self.source_ast:

            if self.check_ast('variable_declaration', ast):
                var = VarObject(ast)
                self.transpiled_code += var.transpile() + "\n"

            if self.check_ast('conditional_statement', ast):
                condition = ConditionalObject(ast, 1)
                self.transpiled_code += condition.transpile() + "\n"

            if self.check_ast('builtin_function', ast):
                builtin = BuiltinObject(ast)
                self.transpiled_code += builtin.transpile() + "\n"

            if self.check_ast('comment', ast):
                comment = CommentObject(ast)
                self.transpiled_code += comment.transpile() + "\n"

            if self.check_ast('loop', ast):
                loop = LoopObject(ast, 1)
                self.transpiled_coder += loop.transpile() + "\n"

        return self.exec_string


    def check_ast(self, astName, ast):
        try:
            if ast[astName]: return True
        except: return False
