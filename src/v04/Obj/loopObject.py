class LoopObject(object):
    
    def __init__(self, source_ast):
        self.exec_str = ""
        self.ast = source_ast['loop']

    def transpile(self):
        for ast in self.ast:
            try: keyword = ast['keyword']
            except: pass
            
            try: name = ast['name']
            except: pass

            try: 
                start_value = ast['start_value']
                if start_value == None: start_value = "0"
            except: pass

            try: end_value = ast['end_value']
            except: pass

            try: increment = ast['increment']
            except: pass

            try: condition = ast['condition']
            except: pass

        if str(keyword) == "for":
            self.exec_str += "for "+ name + " in range("+ str(start_value) + ", " + str(end_value) + ", " + str(increment) + "):"

        if str(keyword) == 'while':
            self.exec_str += "while "+ name + " " + condition + ":"
        
        return self.exec_str