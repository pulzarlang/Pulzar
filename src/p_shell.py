from colorama import *
import re

import lexer
import mparser
import generator
import constants
result = '''
    ____        __                
   / __ \__  __/ /___  ____ ______ 
  / /_/ / / / / /_  / / __ `/ ___/
 / ____/ /_/ / / / /_/ /_/ / /
/_/    \__,_/_/ /___/\__,_/_/
'''

def shell():
    init(convert=True)
    print(Fore.WHITE + "(c) Brian Turza 2018 - 20 Pulzar v0.4\n ")
    print(Fore.WHITE + "Welcome to \n")
    print(Fore.GREEN, result)
    print(Fore.WHITE + "Type 'help()' for more information")
    symbol_tree = ""
    stack = ""
    command = ""
    def checkAssignment(command):
        for token in command.split():
            if token == "=":
                return True
        return False

    while command != "exit()" or  command != "quit()":
        command = input(">")

        if command == "": continue

        if command in ["help", "help()"]:
            print("basic bulitin functions:")
            print("echo - prints value or text with new line")
            print("print - To print value or text without new line")
            print("system - equivalent to os.system from python")
            print("----------------------------------------------")
            print("list of keywords:")
            print("if\nelseif\nelse\nfor\nwhile\nfunc\nclass\n")
            print("Exit screen by commands exit or exit()")
            print("for more open https://docs.pulzar.org")

        elif command == "symbol_tree()":
            print(symbol_tree)
            
        elif command == "exit" or command == "exit()" or command == "quit()":
            quit()
        else:
            if "var" in command or "str" in command or "int" in command or "bool" in command or "complex" in command:
                lex = lexer.Lexer(f"Program Console;\n{command}")
                tokens = lex.tokenize()
                # Parser
                parse = mparser.Parser(tokens, False)
                ast = parse.parse(tokens)
                error = ast[2]
                if error == False:
                    symbol_tree += command + "\n"
            elif checkAssignment(command) == True:
                symbol_tree += command + "\n"

            elif "func" in command and "{" in command:
                temp = ""
                while temp != "}":
                    temp = input(" ")
                    command += "\n" + temp
                stack += command + "\n"

            elif "if" in command or "elseif" in command or "else" in command or "for" in command or "while" in command:
                temp = ""
                while temp != "}":
                    temp = input(" ")
                    command += "\t" + temp + "\n"
                code = f"Program Console;\n{symbol_tree}{stack}{command}"
                lex = lexer.Lexer(code)
                tokens = lex.tokenize()
                # Parser
                parse = mparser.Parser(tokens, False)
                ast = parse.parse(tokens)
                error = ast[2]
                if error == False:
                    obj = generator.Generation(ast[0], ast[1], False, '')
                    gen = obj.generate()
                    try:
                        # mycode
                        exec(gen)
                    except Exception as exc:
                        print(gen)
                        print("Error at line 1:")
                        print(exc)

            else:
                def checkExpression(command):
                    math_sym = "0123456789" + "".join([operator for operator in constants.OPERATORS])
                    for symbol in command.split():
                        if symbol in constants.KEYWORDS or symbol in constants.BUILT_IN or symbol == "=":
                            return False

                        elif isinstance(symbol, str) or isinstance(symbol, list) or symbol in math_sym or symbol in constants.SPECIAL_OPERATORS:
                            continue
                    return True

                if checkExpression(command): command = f"echo {command}"
                code = "Program Console;\n" + symbol_tree + stack + command
                # Lexer
                lex = lexer.Lexer(code)
                tokens = lex.tokenize()
                # Parser
                parse = mparser.Parser(tokens, False)
                ast = parse.parse(tokens)
                error = ast[2]
                if error == False:
                    obj = generator.Generation(ast[0], ast[1], False, '')
                    gen = obj.generate()
                    try:
                        # mycode
                        exec(gen)
                    except Exception as exc:
                        print("Error at line 1:")
                        print(exc)


if __name__ == "__main__":
    shell()