class VarObject(object):

    def __init__(self,source_ast):
        self.exec_str = ""
        self.ast = source_ast['variable_declaration']
    
    def transpile(self):

        for ast in self.ast:
            try: self.exec_str += ast['name'] + " = " + str(ast['value'])
            except: pass

        return self.exec_str
        