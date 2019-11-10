class FuncObject(object):

    def __init__(self, source_ast):
        self.exec_str = ""
        self.ast = source_ast['variable_declaration']

    def transpile(self):
        for ast in self.ast:
            try: name = ast['name']
            except: pass
            try: arg = ast['argument']
            except: pass
        self

    def transpile_func(self,v1,arg):
        self.exec_str += "def" + " " + v1 + "("+arg+")" + ":\n" + "\t"
        return self.exec_str
    
    def transpile_run_func(self,v1,arg):
        self.exec_str += v1 + "("+arg+")" + "\n"
        return self.exec_str

        for ast in self.ast:
            try: self.exec_str += ast['name'] + " = " + str(ast['value'])
            except: pass

        return self.exec_str