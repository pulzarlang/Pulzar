class FuncObject(object):

    def __init__(self):
        self.exec_str = ""

    def transpile_func(self,v1,arg):
        self.exec_str += "def" + " " + v1 + "("+arg+")" + ":\n" + "\t"
        return self.exec_str
    
    def transpile_run_func(self,v1,arg):
        self.exec_str += v1 + "("+arg+")" + "\n"
        return self.exec_str