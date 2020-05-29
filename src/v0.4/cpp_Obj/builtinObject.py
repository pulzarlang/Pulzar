class BuiltinObject(object):

    def __init__(self, source_ast):
        self.exec_str = ""
        self.ast = source_ast['builtin_function']
        self.execute = False


    def transpile(self):
        for ast in self.ast:
            try: func = ast['function']
            except: pass
            try: arg = ast['argument']
            except: pass
        if str(func) == 'echo':
            self.exec_str += "std::cout << " + str(arg) + r' << "\n";'

        elif str(func) == 'print':
            self.exec_str += "std::cout <<" + str(arg) + ";"

        elif str(func) == 'input':
            self.exec_str += "std::cin >> " + str(arg) + ";"

        elif str(func) == 'system':
            self.exec_str += "os.system(" + str(arg) + ")"

        elif str(func) == 'alert':
            self.exec_str += "<script>alert("+ str(arg) +"</script>"

        elif str(func) == "execute":
            self.exec_str += str(arg)
            self.execute = True

        return [self.exec_str, self.execute]