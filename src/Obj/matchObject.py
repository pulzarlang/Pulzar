from Obj.varObject import VarObject
from Obj.builtinObject import BuiltinObject
from Obj.returnObject import ReturnObject
import Obj.loopObject


class MatchlObject:

    def __init__(self, source_ast, nesting_count):
        self.exec_str = ""
        self.ast = source_ast['conditional_statement']
        self.nesting_count = nesting_count

    def transpile(self):
        keyword = ""
        condition = ""

        for ast in self.ast:

            try:
                var = ast['variable']
            except:
                pass
            try:
                case = ast['condition']
            except:
                pass
            try:
                scope = ast['scope']
            except:
                pass

        if keyword != "else":
            self.exec_str += keyword + " " + condition + ":\n" + self.transpile_scope(scope, self.nesting_count, 2)
        else:
            self.exec_str += "else:\n" + self.transpile_scope(scope, self.nesting_count, 1)

        return self.exec_str

    def transpile