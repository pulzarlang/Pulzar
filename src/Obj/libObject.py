class libObject(object):

    def __init__(self, source_ast):
        self.exec_str = ""
        self.ast = source_ast['Include']
        self.file = False

    def transpile(self):
        for ast in self.ast:
            try: lib = ast['libary']
            except: pass

        if '"' in lib:
            self.exec_str = lib.replace('"', '')
            self.file = True
        else:
            self.exec_str = "from " + lib + " import *"


        return [self.exec_str, self.file]