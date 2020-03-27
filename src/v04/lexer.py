"""
©Pulzar 2018-20

#Author : Brian Turza
version: 0.4
#Created : 14/9/2019
"""
import re
import constants

class Lexer:

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


    def tokenize(self):
        tokens = []
        source_code = self.source_code.split()

        source_index = 0

        for source_index in range(len(source_code)):
            
            word = source_code[source_index]

            if "\n" in word:
                tokens.append(["NEWLINE",word])
            
            elif word in constants.KEYWORDS: tokens.append(["KEYWORD",word])

            elif word in constants.DATATYPE: tokens.append(["DATATYPE",word])

            elif word in constants.BUILT_IN: tokens.append(["BUILT_IN_FUNCTION",word])
            
            elif word in constants.MATH: tokens.append(["MATH_FUNCTION",word])


            elif word in constants.OPERATORS and word[:2] not in ["++", "--"]: tokens.append(["OPERATOR",word])
            
            elif word in constants.COMARTION_OPERATORS: tokens.append(["COMPARTION_OPERATOR", word])
            
            elif word in constants.LOGICAL_OPERATORS: tokens.append(["LOGIC_OPERATOR", word])
            
            elif word in constants.INCREMENT_OPERATORS: tokens.append(["INCREMENT_OPERATOR", word])


            elif re.match("[a-z]",word) or re.match("[A-Z]",word):
                if word[len(word) - 1] == ';':
                    tokens.append(["IDENTIFIER", word[:-1]])
                elif word[len(word) - 1] == ",":
                    tokens.append(["IDENTIFIER", word[:-1]])
                elif word[len(word) - 2] == "++" or word[:2] == "++":
                    tokens.append(["INCREMENT",word])
                elif word[len(word) - 2] == "--" or word[:2] == "--":
                    tokens.append(["DECREMENT", word])
                else:
                    tokens.append(["IDENTIFIER", word])
                
            elif re.match("[0-9]",word):
                if word[len(word) - 1] == ';' and word[len(word) - 2] not in  ["!", "i"]:
                    tokens.append(["INTEGER",word[:-1]])

                elif word[len(word) - 1] == ',' and word[len(word) - 2] not in  ["!", "i"]:
                    tokens.append(["INTEGER",word[:-1]])

                elif word[len(word) - 1] == ";" and word[len(word) - 2] == "i":
                    tokens.append(["COMPLEX_NUMBER",word[:-2]])

                elif word[len(word) - 1] == ";" and word[len(word) - 2] == "!":
                    tokens.append(["FACTORIAL",word[:-2]])

                elif word[len(word) - 1] == "i":
                    tokens.append(["COMPLEX_NUMBER",word[:-1]])

                elif word[len(word) - 1] == "!":
                    tokens.append(["FACTORIAL",word[:-1]])

                else:
                    tokens.append(["INTEGER",word])


            elif word == ":": 
                tokens.append(["COLON",":"])

            elif word == "::":
                tokens.append(["SEPARATOR",word])
             
            
            
            elif word== "|**" or word[:3] == "|**" or word == "**|" or word[:-3] == "**|":
                tokens.append(["COMMENT",word])
            
            elif word in "{}":
                tokens.append(["SCOPE_DEFINIER",word])

            elif ('"') in word: 

                matcherReturn = self.getMatcher('"', source_index, source_code)
                
                if matcherReturn[1] == '': tokens.append(["STRING", matcherReturn[0].replace("\s"," ")])

                else:

                    tokens.append(["STRING", matcherReturn[0].replace("\s"," ") ])
                    
                    if ';' in matcherReturn[1]: tokens.append(["SEMIC", ";"])

                    source_index += matcherReturn[2]
                    pass
            
            elif ("'") in word:

                matcherReturn = self.getMatcher("'", source_index, source_code)
                
                if matcherReturn[1] == '': tokens.append(["STRING", matcherReturn[0].replace("\s"," ")])

                else:

                    tokens.append(["STRING", matcherReturn[0].replace("\s"," ") ])
                    
                    if ';' in matcherReturn[1]: tokens.append(["SEMIC", ";"])

                    source_index += matcherReturn[2]
                    pass
            
            elif  word[:1] == "(" or  word[len(word) - 1] == ")" or word == "(" or word == ")" or word in "()":
                if word[:-1] == ";":
                    tokens.append(["BRACKET",word[:-1]])
                else:
                    tokens.append(["BRACKET",word])
                
            
            elif word.startswith("\t"): tokens.append(["TAB","\t"]) 

            if word[len(word) - 1] == ";":
                tokens.append(["SEMIC",';'])

            if word == "," or word[len(word) - 1] == ",":
                tokens.append(["COMMA",","])

            source_index += 1

        return tokens
