class LoopObject(object):
    
    def __init__(self):
        self.exec_str = ""
    
    def transpile_for(self,value,value2,v3):
        self.exec_str += "for" + " " + value + " in range(0,"+value2+","+v3+")" + ":\n" + "\t"
        return self.exec_str
    
    def transpile_while(self,value,op,value2):
        self.exec_str += "while" + " " + value + " " + op + " " + value2 + ":\n" + "\t"

    def transpile_func(self,v1,arg):
        self.exec_str += "def" + " " + v1 + "("+arg+")" + ":\n" + "\t"
        return self.exec_str
    
    def transpile_run_func(self,v1,arg):
        self.exec_str += v1 + "("+arg+")" + "\n"
        return self.exec_str