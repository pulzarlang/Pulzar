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

        self.exec_str += "def " + name + "(" + arg + ")" + ":"
        return self.exec_str

class RunFuncObject(object):
    
    def __init__(self, source_ast):
        self.exec_str = ""
        self.ast = source_ast['main_scope']
    
    def transpile(self):
        name = ""
        arg = ""
        for ast in self.ast:

            try: name = ast['name']
            except: pass
            try: arg = ast['argument']
            except: pass
            
        if arg == "":
            self.exec_str += name + "()"
        else:
            self.exec_str += name + "(" + arg + ")"
        
        return self.exec_str