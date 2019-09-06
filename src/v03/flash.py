#©Flash 2018-19

#Author : Brian Turza
#Created : 30/6/2018

import lexer
import mparser
#from flash_shell.main import main as shell

import os
import sys

li = 0
#Title
os.system("title Flash v0.3")

def main(): 
    try:
        arg = sys.argv[1]
    except:
        print("Flash shell")
    
    if sys.argv[1][-4:] != ".fls":
        print("FileError with file '{}':\nMust be .fls file".format (sys.argv[1]))
        quit()
    try:
        arg = sys.argv[2]
    except:
        with open(sys.argv[1], "r") as f:
                    code = f.read()
                    lex = lexer.Lexer(code)
                    
                    tokens = lex.token()
                    #Parser
                    parse = mparser.Parser(tokens,code,li)
                            
                    parse.parse()
                    quit()
    if sys.argv[2] == "-t" or sys.argv[2] == "--t":
        with open(sys.argv[1], "r") as f:
            code = f.read()
        print("ORIGINAL CODE:")
        print(code)
        #Lexer
        print("--------------LEXICAL ANALYSYS---------------------\n")
        lex = lexer.Lexer(code)
                    
        tokens = lex.token()
        print(tokens)
        print("\n--------------------------------------------------")
        #Parser
        print("--------------CODE GENERATION-----------------------")
        parse = mparser.Parser(tokens,code,li)
        parser = parse.parse()
        quit()
    
    elif sys.argv[2] == "-l" or sys.argv[2] == "--l":
        with open(sys.argv[1], "r") as f:
            code = f.read()
        #Lexer
        print("--------------LEXICAL ANALYSYS---------------------\n")
        lex = lexer.Lexer(code)
                    
        tokens = lex.token()
        print(tokens)
        print("\n--------------------------------------------------")
        #Parser
        print("--------------CODE GENERATION-----------------------")
        parse = mparser.Parser(tokens,code,li)
        parser = parse.parse()
        quit()
#---------------------------------------------------------------------------

if __name__ == "__main__":
    main()

