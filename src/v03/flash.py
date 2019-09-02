#©Flash 2018-19

#Author : Brian Turza
#Created : 30/6/2018

import lexer
import mparser
import flash_shell.main as shell

import os
import sys

li = 0
#Title
#os.system("title Flash v0.2")

def main():
    try:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        if arg1[-4:] != ".fls":
            print("FileError with file '{}':\nMust be .fls file".format (arg))
            quit()
        with open(arg1, "r") as f:
            code = f.read()

        if arg2 == "-t": 
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
            
            parse.parse()

        else:
            #Lexer
            lex = lexer.Lexer(code)
            
            tokens = lex.token()
            #Parser
            parse = mparser.Parser(tokens,code,li)
            
            parse.parse()
#---------------------------------------------------------------------------

    except IndexError:
        pass


if __name__ == "__main__":
    main()
