class BuiltinObject(object):

    def __init__(self, source_ast):
        self.exec_str = ""
        self.ast = source_ast['builtin_function']
        self.execute = False


    def transpile(self):
        for ast in self.ast:
            try: func = ast['function']
            except: pass
            try: type_ = ast['type']
            except: pass
            try: arg = ast['argument']
            except: pass

        if str(func) == 'echo':
            self.exec_str += "print(" + str(arg) + ")"

        elif str(func) == 'print':
            self.exec_str += "print(" + str(arg) + ", end='')"

        elif str(func) == 'input':
            if type_ in ["var", None]:
                self.exec_str += f"{arg} = input()"
            else:
                self.exec_str += f"{arg} = {type_}(input())"

        elif str(func) == 'system':
            self.exec_str += "os.system(" + str(arg) + ")"

        elif str(func) == 'alert':
            self.exec_str += "<script>alert("+ str(arg) +"</script>"

        elif str(func) == "execute":
            self.exec_str += str(arg)
            self.execute = True

        return [self.exec_str, self.execute]