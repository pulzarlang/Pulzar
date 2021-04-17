"""
©Pulzar 2018-20

#Author : Brian Turza
version: 0.4
#Created : 14/9/2019
"""
import cgi
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import StringIO
import contextlib
import sys

isConsole = True
plz_output = ""
PORT = 8080
PATH = ''
file_name = ''
@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

def execute(code):
    """
    This function executes generated python code and returns the output
    :param code:
    :return output:
    """
    with stdoutIO() as s:
        try:
            exec(code)
        except:
            return "Error occured in your code"
    return s.getvalue()

def exec_plz(code, isServer, compile=False, execute=False):
    import lexer
    import mparser
    isConsole = False
    lex = lexer.Lexer(code)
    tokens = lex.tokenize()
    parse = mparser.Parser(tokens, False)
    ast = parse.parse(tokens)
    if isServer:
        gen = Generation(ast[0], ast[1], False, file_name, execute).generate_browser()
    else:
        gen = Generation(ast[0], ast[1], compile, file_name, execute).generate()
        isConsole = True
    return [gen, isConsole]

#------------- PROGRAM BROWSER ----------
class Serv(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        error = False
        plz = False
        if PATH == "":
            if self.path == '/':
                try:
                    file_to_open = open('index.html')
                    self.path = '/index.html'
                except:
                    self.path = '/index.plz'

            elif self.path[-1:] == "/":
                try:
                    file_to_open = open('index.html')
                    self.path += '/index.html'
                except:
                    self.path += 'index.plz'

            if self.path[-4:] == ".plz":
                plz = True
        else:
            file_to_open = open(file_name)
            if self.path.replace('/', '') == PATH.replace('"', '').replace('/', '').replace("'", ""):
                self.path = file_name
                plz = True

        if "?" in self.path and ".plz" in self.path:
            from urllib.parse import urlparse, parse_qs
            parsed_url = urlparse(self.path)
            global get_requests
            get_requests = parse_qs(parsed_url.query)
            plz = True
            self.path = parsed_url.path

        try:
            if self.path[:1] in ["/", "\\"]:
                file_to_open = open(self.path[1:]).read()
            else:
                file_to_open = open(self.path).read()
            self.send_response(200)
        except:
            file_to_open = "<!DOCTYPE html>\n"
            file_to_open += "<html>\n"
            file_to_open += "<head><title>HTTP ERROR 404 - Page not found</title></head>\n"
            file_to_open += "<body>\n"
            file_to_open += "<h1>Error 404 Page not found</h1>\n"
            file_to_open += "</body>\n"
            file_to_open += "</html>\n"
            self.send_response(404)
            error = True
        self.end_headers()
        if plz and error == False:
            gen_py = exec_plz(file_to_open, True)
            #print(gen_py[0])
            if gen_py[1] == False:
                pulzar_output = execute(gen_py[0])
                output = '<!DOCTYPE html>\n'
                output += "<html>\n"
                output += "<head><title>Pulzar web</title></head>\n"
                output += "<body>{}</body>\n".format(pulzar_output)
                output += "</html>\n"
                self.wfile.write(bytes(output, 'utf-8'))
            else:
                self.wfile.write(bytes(file_to_open, 'utf-8'))
        else:
            self.wfile.write(bytes(file_to_open, 'utf-8'))

    def do_POST(self):
        error = False
        plz = False
        if self.path == '/':
            try:
                file_to_open = open('index.html')
                self.path = '/index.html'
            except:
                self.path = '/index.plz'

        elif self.path[-1:] == "/":
            try:
                file_to_open = open('index.html')
                self.path += '/index.html'
            except:
                self.path += '/index.plz'

        if self.path[-4:] == ".plz":
            plz = True
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = "<!DOCTYPE html>\n"
            file_to_open += "<html>\n"
            file_to_open += "<head><title>HTTP ERROR 404 - Page not found</title></head>\n"
            file_to_open += "<body>\n"
            file_to_open += "<h1>Error 404 Page not found</h1>\n"
            file_to_open += "</body>\n"
            file_to_open += "</html>\n"
            self.send_response(404)
            error = True
        self.end_headers()
        if plz and error == False:
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            global post_requests
            post_requests = []
            for item in form.list:
                post_requests.append([item.name, item.value])
            gen_py = exec_plz(file_to_open, True)
            pulzar_output = execute(gen_py)
            output = '<!DOCTYPE html>\n'
            output += "<html>\n"
            output += "<head><title>Pulzar web</title></head>\n"
            output += "<body>{}</body>\n".format(pulzar_output.replace('\n', '<br>'))
            output += "</html>\n"
            self.wfile.write(bytes(output, 'utf-8'))
        else:
            self.wfile.write(bytes(file_to_open, 'utf-8'))

#--------------------------------------------------------------------------

class Generation:
    def __init__(self, source_ast, isConsole, compile, filename, execute_plz=False):
        self.transpiled_code = ""
        self.isConsole = isConsole
        self.compile = compile
        self.filename = filename
        self.execute = execute_plz

        self.source_ast = source_ast['main_scope']

    def generate_browser(self):
        from Obj.varObject import VarObject
        from Obj.builtinObject import BuiltinObject
        from Obj.loopObject import LoopObject
        from Obj.functionObject import FuncObject, RunFuncObject
        from Obj.conditionalObject import ConditionalObject
        from Obj.libObject import libObject
        from Obj.returnObject import ReturnObject
        from Obj.macrosObject import MacrosObject
        self.transpiled_code = "from Lib.browser.main import *\n"
        get_request, post_request = False, False
        global file_name
        file_name = self.filename
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
                    gen = exec_plz(code[0], False)
                    self.transpiled_code += "print(" + execute(gen) + ")\n"
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
                x = ast['call_function']
                if x[0]['name'] == "set_port":
                    global PORT
                    PORT = int(x[1]['argument'])
                elif x[0]['name'] == "POST":
                    post_request = True
                    self.transpiled_code += "POST(%s, post_requests)\n" % (x[1]['argument'])
                elif x[0]['name'] == "GET":
                    get_request = True
                    self.transpiled_code += "GET(%s, get_requests)\n" % (x[1]['argument'])
                elif x[0]['name'] == "set_path":
                    global PATH
                    PATH = '{}'.format(x[1]['argument'])
                else:
                    self.transpiled_code += func.transpile() + "\n"

            if self.check_ast('return', ast):
                return_ = ReturnObject(ast)
                self.transpiled_code += return_.transpile() + "\n"

        if post_request:
            self.transpiled_code = "post_requests = {}\n{}".format(str(post_requests), self.transpiled_code)
        elif get_request:
            self.transpiled_code = "get_requests = {}\n{}".format(str(get_requests), self.transpiled_code)

        global plz_output
        plz_output = execute(self.transpiled_code)

        return self.transpiled_code


    def generate(self):
        global isConsole
        isConsole = self.isConsole
        if self.isConsole == True and self.compile == False:
            from Obj.varObject import VarObject
            from Obj.builtinObject import BuiltinObject
            from Obj.loopObject import LoopObject
            from Obj.functionObject import FuncObject, RunFuncObject
            from Obj.classObject import ClassObject
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
                        gen = exec_plz(code.replace('"', ''), False)
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
                        gen = exec_plz(code[0].replace('"', '').replace("'", ""), False)
                        self.transpiled_code += gen[0] + "\n"
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

                if self.check_ast('class', ast):
                    oop = ClassObject(ast, 1)
                    self.transpiled_code += oop.transpile() + "\n"


                if self.check_ast('macros', ast):
                    macro = MacrosObject(ast)
                    self.transpiled_code += macro.transpile() + "\n"

            return self.transpiled_code

        elif self.isConsole == False and self.compile == False:
            from Obj.functionObject import RunFuncObject
            global file_name
            file_name = self.filename
            get_request, post_request = False, False
            for ast in self.source_ast:
                if self.check_ast('call_function', ast):
                    func = RunFuncObject(ast)
                    x = ast['call_function']
                    if x[0]['name'] == "set_port":
                        global PORT
                        PORT = int(x[1]['argument'])
                    elif x[0]['name'] == "POST":
                        post_request = True
                        self.transpiled_code += "POST(%s, post_requests)\n" % (x[1]['argument'])
                    elif x[0]['name'] == "GET":
                        get_request = True
                        self.transpiled_code += "GET(%s, get_requests)\n" % (x[1]['argument'])
                    elif x[0]['name'] == "set_path":
                        global PATH
                        PATH = '{}'.format(x[1]['argument'])
                    else:
                        self.transpiled_code += func.transpile() + "\n"

            if post_request:
                self.transpiled_code = "post_requests = {}\n{}".format(str(post_requests), self.transpiled_code)
            elif get_request:
                self.transpiled_code = "get_requests = {}\n{}".format(str(get_requests), self.transpiled_code)

            print(f"* Pulzar Server running at: localhost:{PORT}")
            httpd = HTTPServer(('localhost', PORT), Serv)
            httpd.serve_forever()

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
                        code[0] = "Program Console;\n" + code[0]
                        gen = exec_plz(code[0].replace('"', '').replace("'", ''), False, True)
                        body += "\t" + gen[0] + "\n"
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
            if self.execute == False:
                self.transpiled_code = "#include <iostream>\n" + header + functions
                self.transpiled_code += "int main() {\n" + body + "\treturn 0;\n}"
            else:
                self.transpiled_code = body

            return self.transpiled_code



    def check_ast(self, astName, ast):
        try:
            if ast[astName]: return True
        except:
            return False
