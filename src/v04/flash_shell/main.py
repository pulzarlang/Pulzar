import ctypes
#import pyfiglet
#from colorama import *
import re
import math
import os

import lexer
import mparser


try:
    def shell():
        init(convert=True)
        print(Fore.WHITE+"(c) Brian Turza 2018 - 19 Flash v02\n ")
        print(Fore.WHITE+"Welcome to \n")
        result = pyfiglet.figlet_format("flash shell", font = "slant")
        print(Fore.GREEN,result)
        print(Fore.WHITE+"Type 'help' for more information")
        command = ""
        while command != "exit()" or  command != "quit()":
            command = input(">>>")
            if command=="help()":
                print("basic bultin functions:")
                print("print() - To print value or text")
                print("for more open https://flash-lang.org")
            
            else:
                lex = lexer.Lexer(command)
                tokens = lex.token()
                parse = mparser.Parser(tokens,command)
                parse.parse()
                continue
except:
    pass
if __name__ == "__main__":
    main()
