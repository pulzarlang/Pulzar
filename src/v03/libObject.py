class libObject(object):

    def __init__(self):
        self.exec_str = ""

    def transpile_include(self,libary):
        self.exec_str = "from "+libary+" import *" + "\n"
        return self.exec_str
        
    def transpile_math(self,value):
        self.exec_str += value + "\n"
        
        return self.exec_str