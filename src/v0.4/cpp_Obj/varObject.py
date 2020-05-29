class VarObject(object):

    def __init__(self,source_ast):
        self.exec_str = ""
        self.ast = source_ast['variable_declaration']
    
    def transpile(self):

        for ast in self.ast: 

            try: typ8 = ast['type']
            except: pass

            try: name = ast['name']
            except: pass

            try: value = ast['value']
            except: pass

        if typ8 == "str":
            self.exec_str += "std::string" + " " + name + " = " + str(value) + ";"
        else:
            self.exec_str += str(typ8) + " " + name + " = " + str(value) + ";"

        return self.exec_str
        