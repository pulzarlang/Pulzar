class BuiltinObject(object):

    def __init__(self, ast):
        self.exec_str = ""
        self.ast = ['builtin_function']


    def transpile(self):
        for ast in self.ast:
            try:
                if str(ast["function"]) == "echo":
                    self.exec_str += "print(" + str(ast['arguments']) + ")"

                elif str(ast['function']) == 'print':
                    self.exec_str += "print(" + str(ast['arguments']) + ", end='')"

                elif str(ast['function']) == 'input':
                    self.exec_str += "input(" + str(ast['arguments']) + ")"

                elif str(ast['function']) == 'system':
                    self.exec_str += "os.system(" + str(ast['arguments']) + ")"

                elif str(ast['function']) == 'input':
                    self.exec_str += "<script>alert("+ str(ast['arguments']) +"</script>"
            except: pass


        return self.exec_str
