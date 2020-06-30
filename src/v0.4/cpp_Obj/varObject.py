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

        if "[" in str(value) and "]" in str(value):
            name = f"{name}[]"

        value = str(value).replace('[', '{').replace(']', '}')
        if ":" in value:
            value = value.split(':')
            value[1] = value[1].replace('(', '').replace(')', '')
            if typ8 == "str":
                self.exec_str += f"std::string {name} = { value[0] }({ value[1] });"
            elif typ8 == "var":
                self.exec_str += f"int {name} = { value[0] }({ value[1] });"
            else:
                self.exec_str += f"{typ8} {name} = { value[0] }({ value[1] });"

        else:
            if typ8 == "str":
                self.exec_str += f"std::string" + " " + name + " = " + str(value) + ";"
            elif typ8 == "var":
                self.exec_str += "int" + " " + name + " = " + str(value) + ";"
            else:
                self.exec_str += str(typ8) + " " + name + " = " + str(value) + ";"

        return self.exec_str
        