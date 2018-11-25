class echoObject(object):

    def __init__(self):
        self.exec_str = ""
    #Print function
    def transpile_print(self,value):
        self.exec_str += "print("+value+")" + "\n"
        
        return self.exec_str
    
    def transpile_input(self,value):
        self.exec_str += "input("+value+")" + "\n"
        
        return self.exec_str

    def transpile_system(self,value):
        self.exec_str += "os.system("+value+")" + "\n"
        
        return self.exec_str
