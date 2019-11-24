from Lib.fmath import *
from Obj.varObject import VarObject
from Obj.builtinObject import BuiltinObject
from Obj.loopObject import LoopObject
from Obj.functionObject import FuncObject
from Obj.conditionalObject import ConditionalObject
from Obj.libObject import libObject
from Obj.returnObject import ReturnObject

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
                condition = ConditionalObject(ast)
                self.transpiled_code += condition.transpile() + "\n"

            if self.check_ast('builtin_function', ast):
                builtin = BuiltinObject(ast)
                self.transpiled_code += builtin.transpile() + "\n"

            if self.check_ast('loop', ast):
                loop = LoopObject(ast)
                self.transpiled_code += loop.transpile() + "\n" + "\t"
            
            if self.check_ast('function_declaration', ast):
                func = FuncObject(ast)
                self.transpiled_code += func.transpile() + "\n" + "\t"
            
            if self.check_ast('return', ast):
                return_ = ReturnObject(ast)
                self.transpiled_code += return_.transpile() + "\n"

        return self.transpiled_code
        
    def check_ast(self, astName, ast):
        try:
            if ast[astName]: return True
        except: return False
