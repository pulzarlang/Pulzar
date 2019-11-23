class FuncObject(object):

    def __init__(self, source_ast):
        self.exec_str = ""
        self.ast = source_ast['function_declaration']

    def transpile(self):
        name = ""
        arg = ""
        for ast in self.ast:

            try: name = ast['name']
            except: pass
            try: arg = ast['argument']
            except: pass

        self.exec_str += "def " + name + "(" + arg + ")" + ":" + "pass"

        return self.exec_str