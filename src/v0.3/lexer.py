import re

class Lexer(object):

    def __init__(self, source_code):
        self.source_code = source_code

    
    def getMatcher(self, matcher, current_index, source_code):

        if source_code[current_index].count(matcher) == 2:

            word = source_code[current_index].partition(matcher)[-1].partition(matcher[0])

            if word[2] != '': 
                return [ matcher + word[0] + matcher, '', word[2] ]

            else:
                return [ matcher + word[0] + matcher, '', '' ]
        
        else:

            source_code = source_code[current_index:len(source_code)]

            word = ""

            iter_count = 0

            for item in source_code:

                iter_count += 1

                word += item + " "

                if matcher in item and iter_count != 1: 

                    return [matcher + word.partition(matcher)[-1].partition(matcher[0])[0] + matcher,word.partition(matcher)[-1].partition(matcher[0])[2],iter_count - 1]
                    break


    def token(self):
        tokens = []
        source_code = self.source_code.split()

        source_index = 0

        for source_index in range(len(source_code)):
            
            word = source_code[source_index]

            if "\n" in word:
                pass
            
            elif word == "include":tokens.append(["INCLUDE",word])
            
            elif word == "var":tokens.append(["VAR",word])
            
            elif word == "Program":tokens.append(["PM",word])
            
            elif word == "echo":tokens.append(["ECHO",word])

            elif word == "print":tokens.append(["PRINT",word])

            elif word == "input":tokens.append(["INPUT",word])
            
            elif word == "system":tokens.append(["SYSTEM",word])
            
            elif word[4:] == "sqrt(":tokens.append(["ROOT",word])
            
            
            elif word == "if":tokens.append(["IF",word])

            elif word == "elif":tokens.append(["ELSE_IF",word]) 

            elif word == "else":tokens.append(["ELSE",word])          
            
            elif word == "for":tokens.append(["FOR",word])

            elif word == "while":tokens.append(["WHILE",word])
            
            elif word == "func":tokens.append(["FUNC",word])
            
            elif word == "run":tokens.append(["RUN_FUNC",word])

            elif word in "\t":tokens.append(["TAB",'    '])
            
            elif word == ":":tokens.append(["COLON",":"])
            
#----------------------------BROWSER---------------------------------

            elif word == "alert":tokens.append(["ALERT",word])

#--------------------------------------------------------------------

#------------------------------MATH---------------------------------

            elif word == "factorial":tokens.append(["FACTORIAL",word])

            
            
            elif word == "complex":tokens.append(["COMPLEX",word])

#--------------------------------------------------------------------

            
            elif re.match("[a-z]",word) or re.match("[A-Z]",word):
                if word[len(word) - 1] == ';':
                    tokens.append(["ID", word[:-1]])
                else:
                    tokens.append(["ID", word])
                
            elif re.match("[0-9]",word):
                if word[len(word) - 1] == ';':
                    tokens.append(["INT",word[:-1]])
                elif word[len(word) - 1] == "i":
                    tokens.append(["COMPLEX_NUM",word])
                elif word[len(word) - 1] == "!":
                    tokens.append(["FACT",word])
                else:
                    tokens.append(["INT",word])
            
            elif word in "+-*/**%=":
                tokens.append(["OP",word])
            
            elif word in "==" or word in "!=" or word in ">" or word in "<" or word in "<=" or word in ">=":
                tokens.append(["COMP_OP", word])
            
            elif word == "::":
                tokens.append(["SEPARATOR",word])
            
            elif word[:-2] == "++":
                tokens.append(["INCREMENT",word])
             
            elif word == ",":
                tokens.append(["COMMA"],",")
            
            elif word== "|**" or word[:3] == "|**" or word == "**|" or word[:-3] == "**|":
                tokens.append(["COMMENT",word])
            
            elif word in "{}":
                tokens.append(["SCOPE",word])

            elif ('"') in word: 

                matcherReturn = self.getMatcher('"', source_index, source_code)
                
                if matcherReturn[1] == '': tokens.append(["STR", matcherReturn[0].replace("\s"," ")])

                else:

                    tokens.append(["STR", matcherReturn[0].replace("\s"," ") ])
                    
                    if ';' in matcherReturn[1]: tokens.append(["SEMIC", ";"])

                    source_index += matcherReturn[2]
                    pass
            
            elif ("'") in word:

                matcherReturn = self.getMatcher("'", source_index, source_code)
                
                if matcherReturn[1] == '': tokens.append(["STR", matcherReturn[0].replace("\s"," ")])

                else:

                    tokens.append(["STR", matcherReturn[0].replace("\s"," ") ])
                    
                    if ';' in matcherReturn[1]: tokens.append(["SEMIC", ";"])

                    source_index += matcherReturn[2]
                    pass

            if word[len(word) - 1] == ";":
                tokens.append(["SEMIC",';'])
            
            elif  word[:1] == "(" or  word[len(word) - 1] == ")" or word == "(" or word == ")" or word in "()":
                tokens.append(["BRACKET",word])
            
            elif word.startswith("\t"):
                tokens.append(["TAB","\t"])
            
            
            source_index += 1

        
        return tokens
