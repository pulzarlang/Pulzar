class ConditionalObject(object):

    def __init__(self, source_ast):
        self.exec_str = ""
        self.ast = source_ast['conditional_statement']

    def transpile(self):
        keyword = ""
        condition = ""
        
        for ast in self.ast:

            try: keyword = ast['keyword']
            except: pass
            try: condition = ast['condition']
            except: pass

        if keyword != "else":
            self.exec_str += keyword + " " + condition + ":"
        else:
            self.exec_str += "else:"

        return self.exec_str