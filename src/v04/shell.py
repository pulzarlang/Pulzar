import ctypes
import pyfiglet
from colorama import *

import constants
import lexer
import mparser
import generator

try:
    def shell():
        init(convert=True)
        print(Fore.WHITE + "(c) Brian Turza 2018 - 20 Pulzar v0.4\n ")
        print(Fore.WHITE + "Welcome to \n")
        result = pyfiglet.figlet_format("Pulzar shell", font="slant")
        print(Fore.GREEN, result)
        print(Fore.WHITE + "Type 'help' for more information")
        code = "Program Console;" + "\n"
        command = ""
        while command != "exit()" or  command != "quit()":
            command = input(">")
            if command in ["help", "help()"]:
                print("basic bultin functions:")
                print("print() - To print value or text")
                print("for more open https://docs.pulzar.org")
            
            elif command == "exit" or command ==  "exit()" or command ==  "quit()":
                quit()

            else:
                if "var" in command or "str" in command or "int" in command or "bool" in command or "complex" in command:
                    code += command + "\n"

                else:
                    code = "Program Console;" + "\n" + command
                # Lexer
                lex = lexer.Lexer(code)
                tokens = lex.tokenize()
                # Parser
                parse = mparser.Parser(tokens, False)
                ast = parse.parse(tokens)
                obj = generator.Generation(ast)
                gen = obj.generate()
                exec(gen)
except:
    pass
if __name__ == "__main__":
    shell()
