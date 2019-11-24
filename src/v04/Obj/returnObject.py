class ReturnObject(object):

    def __init__(self, source_ast):
        self.exec_str = ""
        self.ast = source_ast['return']
    
    def transpile(self):

        for ast in self.ast:

            arg = ast['argument']
        
        self.exec_str += "return " + arg
        
        return self.exec_str