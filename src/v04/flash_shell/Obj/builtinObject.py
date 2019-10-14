class builtinObject(object):

    def __init__(self):
        self.exec_str = ""

    def transpile_print(self,value):
        self.exec_str += "print("+value+")" + "\n"
        
        return self.exec_str
    
    def transpile_input(self,var,typ):
        if typ != "":
            self.exec_str += var + " = "+typ+"(input())" + "\n"
        else:
            self.exec_str += var + " = input()" + "\n"
        
        return self.exec_str

    def transpile_system(self,value):
        self.exec_str += "os.system("+value+")" + "\n"
        
        return self.exec_str
#---------------------BROWSER---------------------------

    def transpile_alert(self,value):
        self.exec_str += "<script>alert("+value+")</script>" + "\n"
        
        return self.exec_str
