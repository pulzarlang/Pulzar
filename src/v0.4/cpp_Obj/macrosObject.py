class MacrosObject(object):

    def __init__(self, source_ast):
        self.exec_str = ""
        self.ast = source_ast['macros']
        self.execute = False

    def transpile(self):
        for ast in self.ast:
            try:
                scope = ast['scope']
            except:
                pass
        self.exec_str += self.transpile_scope(scope)

        return self.exec_str

    def transpile_scope(self, scope_ast):
        for ast in scope_ast:
            try:
                func = ast['define'][0]['function']
            except:
                pass
            try:
                name = ast['define'][1]['name']
            except:
                pass

            try:
                value = ast['define'][2]['value']
            except:
                pass

            if str(func) == "define":
                self.exec_str += f"#define {name} {value}\n"

        return self.exec_str