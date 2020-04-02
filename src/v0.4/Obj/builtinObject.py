class BuiltinObject(object):

    def __init__(self, source_ast):
        self.exec_str = ""
        self.ast = source_ast['builtin_function']


    def transpile(self):
        for ast in self.ast:
            
            try: func = ast['function']
            except: pass
            try: arg = ast['argument']
            except: pass

        if str(func) == 'echo':
            self.exec_str += "print(" + str(arg) + ")"

        elif str(func) == 'print':
            self.exec_str += "print(" + str(arg) + ", end='')"

        elif str(func) == 'input':
            self.exec_str += "{}=input()".format (arg)

        elif str(func) == 'system':
            self.exec_str += "os.system(" + str(arg) + ")"

        elif str(func) == 'input':
            self.exec_str += "<script>alert("+ str(arg) +"</script>"


        return self.exec_str