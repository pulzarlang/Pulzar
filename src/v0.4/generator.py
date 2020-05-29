"""
©Pulzar 2018-20

#Author : Brian Turza
version: 0.4
#Created : 14/9/2019
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import StringIO
import contextlib
import sys

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

def execute(code):
    with stdoutIO() as s:
        try:
            exec(code)
        except:
            return "Error occured in your code"
    return s.getvalue()

def exec_plz(code):
    import lexer
    import mparser
    lex = lexer.Lexer(code)
    tokens = lex.tokenize()
    parse = mparser.Parser(tokens, False)
    ast = parse.parse(tokens)
    gen = Generation(ast[0], ast[1]).generate()
    return gen

#------------- PROGRAM BROWSER ----------
class Serv(BaseHTTPRequestHandler):

    def do_GET(self):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            stdout = "Hello Brian!"
            output = ''
            output += "<html>"
            output += "<head><title>Pulzar web</title></head>"
            output += f"<body>{stdout}</body>"
            output += "</html>"
            self.wfile.write(output.encode())
#--------------------------------------------------------------------------

class Generation:
    def __init__(self, source_ast, isConsole, compile=False):
        self.transpiled_code = ""
        self.isConsole = isConsole
        self.compile = compile

        self.source_ast = source_ast['main_scope']


    def generate(self):
        if self.isConsole == True and self.compile == False:
            from Obj.varObject import VarObject
            from Obj.builtinObject import BuiltinObject
            from Obj.loopObject import LoopObject
            from Obj.functionObject import FuncObject, RunFuncObject
            from Obj.conditionalObject import ConditionalObject
            from Obj.libObject import libObject
            from Obj.returnObject import ReturnObject
            from Obj.macrosObject import MacrosObject

            for ast in self.source_ast:
                if self.check_ast('Include', ast):
                    inc = libObject(ast)
                    filename =  inc.transpile()
                    if filename[1] == True:
                        with open(filename[0], 'r') as f:
                            code = f.read()
                        gen = exec_plz(code.replace('"', ''))
                        self.transpiled_code += gen
                    else:
                        self.transpiled_code += filename[0] + "\n"

                if self.check_ast('variable_declaration', ast):
                    var = VarObject(ast)
                    self.transpiled_code += var.transpile() + "\n"

                if self.check_ast('conditional_statement', ast):
                    condition = ConditionalObject(ast, 1)
                    self.transpiled_code += condition.transpile() + "\n"

                if self.check_ast('builtin_function', ast):
                    builtin = BuiltinObject(ast)
                    code = builtin.transpile()
                    if code[1] == True:
                        code[0] = "Program Console;\n" + code[0]
                        gen = exec_plz(code[0])
                        self.transpiled_code += gen + "\n"
                    else:
                        self.transpiled_code += code[0] + "\n"

                if self.check_ast('loop', ast):
                    loop = LoopObject(ast, 1)
                    self.transpiled_code += loop.transpile() + "\n"

                if self.check_ast('function_declaration', ast):
                    func = FuncObject(ast, 1)
                    self.transpiled_code += func.transpile() + "\n"

                if self.check_ast('call_function', ast):
                    func = RunFuncObject(ast)
                    self.transpiled_code += func.transpile() + "\n"

                if self.check_ast('return', ast):
                    return_ = ReturnObject(ast)
                    self.transpiled_code += return_.transpile() + "\n"

                if self.check_ast('macros', ast):
                    macro = MacrosObject(ast)
                    self.transpiled_code += macro.transpile() + "\n"

            return self.transpiled_code

        elif self.isConsole == False and self.compile == False:
            from Obj.varObject import VarObject
            from Obj.builtinObject import BuiltinObject
            from Obj.loopObject import LoopObject
            from Obj.functionObject import FuncObject, RunFuncObject
            from Obj.conditionalObject import ConditionalObject
            from Obj.libObject import libObject
            from Obj.returnObject import ReturnObject
            from Obj.macrosObject import MacrosObject
            for ast in self.source_ast:
                if self.check_ast('variable_declaration', ast):
                    var = VarObject(ast)
                    self.transpiled_code += var.transpile() + "\n"

                if self.check_ast('conditional_statement', ast):
                    condition = ConditionalObject(ast, 1)
                    self.transpiled_code += condition.transpile() + "\n"

                if self.check_ast('builtin_function', ast):
                    builtin = BuiltinObject(ast)
                    code = builtin.transpile()
                    if code[1] == True:
                            gen = exec_plz(code[0])
                            self.transpiled_code += "print(" + execute(gen) + ")\n"
                    else:
                        self.transpiled_code += code[0] + "\n"

                if self.check_ast('loop', ast):
                    loop = LoopObject(ast, 1)
                    self.transpiled_code +=  loop.transpile() + "\n"

                if self.check_ast('function_declaration', ast):
                    func = FuncObject(ast, 1)
                    self.transpiled_code += func.transpile() + "\n"

                if self.check_ast('call_function', ast):
                    func = RunFuncObject(ast)
                    self.transpiled_code += func.transpile() + "\n"

                if self.check_ast('return', ast):
                    return_ = ReturnObject(ast)
                    self.transpiled_code += return_.transpile() + "\n"

                output = execute(self.transpiled_code)
                httpd = HTTPServer(('localhost', 8080), Serv)
                httpd.serve_forever()

            return self.transpiled_code

        elif self.compile == True:
            from cpp_Obj.varObject import VarObject
            from cpp_Obj.builtinObject import BuiltinObject
            from cpp_Obj.loopObject import LoopObject
            from cpp_Obj.functionObject import FuncObject, RunFuncObject
            from cpp_Obj.conditionalObject import ConditionalObject
            from cpp_Obj.libObject import libObject
            from cpp_Obj.returnObject import ReturnObject
            from cpp_Obj.macrosObject import MacrosObject
            header, functions, body = "", "", ""
            for ast in self.source_ast:

                if self.check_ast('Include', ast):
                    inc = libObject(ast)
                    header += inc.transpile() + "\n"

                if self.check_ast('macros', ast):
                    macro = MacrosObject(ast)
                    header += macro.transpile() + "\n"

                if self.check_ast('function_declaration', ast):
                    func = FuncObject(ast, 1)
                    functions += func.transpile() + "\n"


                if self.check_ast('variable_declaration', ast):
                    var = VarObject(ast)
                    body += "\t" + var.transpile() + "\n"

                if self.check_ast('conditional_statement', ast):
                    condition = ConditionalObject(ast, 2)
                    body += "\t" + condition.transpile() + "\n"

                if self.check_ast('builtin_function', ast):
                    builtin = BuiltinObject(ast)
                    code = builtin.transpile()
                    if code[1] == True:
                        gen = exec_plz(code[0])
                        body += "\t" + gen + "\n"
                    else:
                        body += "\t" + code[0] + "\n"

                if self.check_ast('loop', ast):
                    loop = LoopObject(ast, 2)
                    body += "\t" + loop.transpile() + "\n"

                if self.check_ast('call_function', ast):
                    func = RunFuncObject(ast)
                    body += "\t" + func.transpile() + "\n"

                if self.check_ast('return', ast):
                    return_ = ReturnObject(ast)
                    body += "\t" + return_.transpile() + "\n"

            self.transpiled_code = "#include <iostream>\n" + header + functions
            self.transpiled_code += "int main() {\n" + body + "}"

            return self.transpiled_code



    def check_ast(self, astName, ast):
        try:
            if ast[astName]: return True
        except:
            return False
