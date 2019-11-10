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

            try: start_value = ast['start_value']
            except: pass

			# Get the endValue
            try: end_value = ast['end_value']
            except: pass

			# Get the incrementer
            try: incrementer = ast['incrementer']
            except: pass

            if str(keyword) == "for":
                self.exec_str += "for "+ name + "in range("+ str(start_value) + ", " + str(end_value) + ", " + str(incrementer) + "):"

            if str(keyword) == 'while':
                self.exec_str += "while "+ name + " " + condtion + ":"
        
        return self.exec_str