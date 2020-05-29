import ctypes
import pyfiglet
from colorama import *
import os

import constants
import lexer
import mparser
import generator

def shell():
    init(convert=True)
    print(Fore.WHITE + "(c) Brian Turza 2018 - 20 Pulzar v0.4\n ")
    print(Fore.WHITE + "Welcome to \n")
    result = pyfiglet.figlet_format("Pulzar", font="slant")
    print(Fore.GREEN, result)
    print(Fore.WHITE + "Type 'help' for more information")
    symbol_tree = ""
    stack = ""
    command = ""
    while command != "exit()" or  command != "quit()":
        if command == "cls":
            os.system("cls")
        command = input(">")

        if command in ["help", "help()"]:
            print("basic bulitin functions:")
            print("echo - prints value or text with new line")
            print("print - To print value or text without new line")
            print("system - eqivalent to os.system from python")
            print("----------------------------------------------")
            print("list of keywords:")
            print("if\nelseif\nelse\nfor\nwhile\nfunc\nclass\n")
            print("Exit screen by commands exit or exit()")
            print("for more open https://docs.pulzar.org")
            
        elif command == "exit" or command == "exit()" or command == "quit()":
            quit()
        else:

            if "var" in command or "str" in command or "int" in command or "bool" in command or "complex" in command:
                symbol_tree += command + "\n"

            elif "func" and "{" in command:
                temp = ""
                while temp != "}":
                    temp = input(" ")
                    command += "\n" + temp
                stack += command + "\n"

            elif "if" in command or "if" in command or "else" in command or "for" in command or "while" and "{" in command:
                temp = ""
                while temp != "}":
                    temp = input(" ")
                    command += "\t" + temp + "\n"
                command = "Program Console;\n" + symbol_tree + stack + command
                lex = lexer.Lexer(command)
                tokens = lex.tokenize()
                # Parser
                parse = mparser.Parser(tokens, False)
                ast = parse.parse(tokens)
                obj = generator.Generation(ast[0], ast[1])
                gen = obj.generate()
                exec(gen)

            else:
                code = command = "Program Console;\n" + symbol_tree + stack + command + "\n"
                # Lexer
                lex = lexer.Lexer(code)
                tokens = lex.tokenize()
                # Parser
                parse = mparser.Parser(tokens, False)
                ast = parse.parse(tokens)
                obj = generator.Generation(ast[0], ast[1])
                gen = obj.generate()
                exec(gen)

if __name__ == "__main__":
    shell()
