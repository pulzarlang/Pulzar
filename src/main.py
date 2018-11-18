#Copyright Flash 2018

#Author : Brian Turza
#30/6/18
import lexer
import mparser


import os
import sys
import ctypes
import pyfiglet
from colorama import *
#Title
os.system("title Flash v01")

def main():
    try:
        with open(sys.argv[1], "r") as f:
            li=0
            code = f.read()
            for i in range(len(code)):
                li = str(i+1)
                
        #print("-"*13,"CODE","-"*13)
        #print(code)
        #print("-"*26)
        #Lexer
        #print("--------------LEXICAL ANALYSYS---------------------\n")
        lex = lexer.Lexer(code)
        
        tokens = lex.token()
        #print(tokens)
        #print("\n--------------------------------------------------")
        #Parser
        #print("--------------CODE GENERATION-----------------------")
        parse = mparser.Parser(tokens,li,code)
        
        parse.parse()
#---------------------------------------------------------------------------

    except IndexError:
        init(convert=True)
        print(Fore.WHITE+"(c) Brian Turza 2018 Flash v02\n ")
        print(Fore.WHITE+"Welcome to \n")
        result = pyfiglet.figlet_format("flash shell", font = "slant")
        print(Fore.GREEN,result)
        print(Fore.WHITE+"Type 'help' for more information")
        command=""
        while command!="exit()":
            command = input(">>>")
            #shell = io.StringIO(command)
            #shell.readline()
            if command=="help()":
                print("basic bultin functions:")
                print("print() - To print value or text")
                print("input() - Like print but it ")
                print("for more open https://flash-lang.org")

            elif command=="exit()" or command=="exit":
                quit()
            elif comand == "cls":
                os.system("cls")

            

if __name__ == "__main__":
    main()
