class libObject(object):

    def __init__(self, source_ast):
        self.exec_str = ""
        self.ast = source_ast['Include']
        self.execute = False

    def transpile(self):
        for ast in self.ast:
            try: lib = ast['libary']
            except: pass

        self.exec_str = "from " + lib + " import *" + "\n"

        return self.exec_str