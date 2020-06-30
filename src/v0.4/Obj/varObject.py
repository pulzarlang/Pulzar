class VarObject(object):

    def __init__(self,source_ast):
        self.exec_str = ""
        self.ast = source_ast['variable_declaration']
    
    def transpile(self):
        brackets = False
        for ast in self.ast: 

            try: name = ast['name']
            except: pass

            try: value = ast['value']
            except: pass
        if ":" in str(value):
            value = value.split(':')
            if len(value) == 2:
                value[1] = value[1].replace('(', '').replace(')', '')
                if value[0] == "POST":
                    self.exec_str += f"{name} = { value[0] }({ value[1] }, post_requests)"
                elif value[0] == "GET":
                    self.exec_str += f"{name} = { value[0] }({ value[1] }, get_requests)"
                else:
                    self.exec_str += name + " = " + str(value[0]) + "(" + value[1] + ")"
            elif len(value) > 2:
                #TODO multiple function calls in variable
                self.exec_str += name + " = " + str(value[0]) + "(" + value[1] + ")"
        else:
            print(value)
            self.exec_str += name + " = " + str(value).replace(':', '')

        return self.exec_str
        