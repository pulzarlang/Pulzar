class ReturnObject(object):

    def __init__(self, source_ast):
        self.exec_str = ""
        self.ast = source_ast['return']
        self.OPERATORS = ["+", "-", "*", "/", "**", "^", "√", "++", "--", "%", "mod", "//"]
        self.type = ''
    def transpile(self):

        for ast in self.ast:

            try:
                arg = ast['argument']
            except: pass

        self.exec_str += f"return {arg.replace(':', '')};"
        
        return self.exec_str