import re

class Lexer(object):

    def __init__(self, source_code):
        self.source_code = source_code

    
    def getMatcher(self, matcher, current_index, source_code):

        if source_code[current_index].count('"') == 2:

            word = source_code[current_index].partition('"')[-1].partition('"'[0])

            if word[2] != '': return [ '"' + word[0] + '"', '', word[2] ]

            else:  return [ '"' + word[0] + '"', '', '' ]
        
        else:

            source_code = source_code[current_index:len(source_code)]

            word = ""

            iter_count = 0

            for item in source_code:

                iter_count += 1

                word += item + " "

                if matcher in item and iter_count != 1: 

                    return ['"' + word.partition('"')[-1].partition('"'[0])[0] + '"',word.partition('"')[-1].partition('"'[0])[2],iter_count - 1]

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
            
            elif word == "Type":tokens.append(["TP",word])
            
            elif word == "echo":tokens.append(["ECHO",word])

            elif word == "input":tokens.append(["INPUT",word])
            
            elif word == "system":tokens.append(["SYSTEM",word])
            
            elif word[4:] == "sqrt(":tokens.append(["ROOT",word])
            
            
            elif word == "if":tokens.append(["IF",word])
            
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
                    tokens.append(["COMPLEX_NUM"])
                else:
                    tokens.append(["INT",word])
            
            elif word in "+-*/**%=":
                tokens.append(["OP",word])
            
            elif word in "==" or word in "!=" or word in ">" or word in "<" or word in "<=" or word in ">=":
                tokens.append(["COMP_OP", word])
            
            elif word == "::":
                tokens.append(["COMP",word])
            
            elif word[:-2] == "++":
                tokens.append(["INCREMENT",word])
             
            elif word in ",":
                tokens.append(["COMMA"])
            
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

            if word[len(word) -1]==";":
                tokens.append(["SEMIC",';'])
            
            elif word in "()":
                tokens.append(["BRACKET",word])
            
            
            source_index += 1

        
        return tokens
