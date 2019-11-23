class VarObject(object):

    def __init__(self,source_ast):
        self.exec_str = ""
        self.ast = source_ast['variable_declaration']
    
    def transpile(self):

        for ast in self.ast: 

            try: name = ast['name']
            except: pass

            try: value = ast['value']
            except: pass

        self.exec_str += name + " = " + str(value)

        return self.exec_str
        