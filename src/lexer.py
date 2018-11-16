import re

class Lexer(object):

    def __init__(self, source_code):
        self.source_code = source_code

    def token(self):
        tokens = []
        source_code = self.source_code.split()

        source_index = 0

        for source_index in range(len(source_code)):
            
            word = source_code[source_index]

            if "\n" in word:
                pass

            if word =="var":tokens.append(["VAR",word])
            
            elif word == "Type":tokens.append(["TP",word])
            
            elif word == "echo":tokens.append(["ECHO",word])

            elif word == "input":tokens.append(["INPUT",word])
            
            elif word[4:] == "sqrt(":tokens.append(["ROOT",word])
            
            elif word == "if":tokens.append(["IF",word])
            
            elif word == "for":tokens.append(["FOR",word])

            elif word == "while":tokens.append(["WHILE",word])
            
            elif word == "func":tokens.append(["FUNC",word])

            

            elif re.match("[a-z]",word) or re.match("[A-Z]",word):
                if word[len(word) - 1] == ';':
                    tokens.append(["ID", word[:-1]])
                else:
                    tokens.append(["ID", word])
                
            elif re.match("[0-9]",word):
                if word[len(word) - 1] == ';':
                    tokens.append(["INT",word[:-1]])
                else:
                    tokens.append(["INT",word])
            
            elif word in '""':
                if word[len(word) - 1] == ';':
                    tokens.append(["STR",word[:-1]])
                else:
                    tokens.append(["STR",word])
            
            elif word in "+-*/%=":
                tokens.append(["OP",word])
            
            elif word in "==" or word in "!=" or word in ">" or word in "<" or word in "<=" or word in ">=":
                tokens.append(["COMPARISON_OP", word])
            
            elif word[2:] == "/*" or word[:-2] == "*/":
                tokens.append(["COMMENT",word])

            if word[len(word) -1]==";":
                tokens.append(["SEMIC",';'])

            source_index +=1

        
        return tokens
