class LoopObject(object):
    
    def __init__(self, ast):
        self.exec_str = ""

    def transpile(self):
        for ast in self.ast:
            try:
                if str(ast["function"]) == "for":
                    self.exec_str += "for "+ ast['name'] + "in range("+ str(ast['start_value']) + ", " + str(ast['end_value']) + ", " + str(ast['increment']) + str(ast['arguments']) + "):"

                elif str(ast['function']) == 'while':
                    self.exec_str += "while "+ ast['name'] + str(ast['condition']) + ", " + str(ast['value']) + ":"

            except: pass


        return self.exec_str