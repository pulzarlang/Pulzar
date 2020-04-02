class VarObject(object):

    def __init__(self):
        self.exec_str = ""
    
    def transpile(self,name,operator,value):

        self.exec_str += name + " " + operator + " " + value + "\n"

        return self.exec_str
        