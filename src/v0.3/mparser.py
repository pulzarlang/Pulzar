from Obj.varObject import VarObject
from Obj.builtinObject import BuiltinObject
from Obj.conditionalObject import ConditionalObject
from Obj.loopObject import LoopObject
from Obj.functionObject import FuncObject
from Obj.libObject import libObject

from lib.fmath import *

import math
import os

class Parser(object):

    def __init__(self,tokens,source_code,li,include):
        self.tokens = tokens
        self.source_code = source_code
        self.li = li
        self.include = include

        self.token_index = 0
        self.transpiled_code = ""
        
    
    def parse(self):
        count = 0
        for self.token_index  in range(len(self.tokens)):

            token_type = self.tokens[self.token_index][0]
            token_value = self.tokens[self.token_index][1]

            #If token is echo add tokens to parse_include()
            if token_type == "INCLUDE":
                self.parse_include(self.tokens[self.token_index:len(self.tokens)])

            elif token_type == "PM" and token_value == "Program":          
                count += 1
            
            elif token_type == "VAR" and token_value == "var":
                self.parse_variable(self.tokens[self.token_index:len(self.tokens)])
            
            elif token_type == "ECHO":
                self.parse_builtin(self.tokens[self.token_index:len(self.tokens)],token_type)

            elif token_type == "PRINT":
                self.parse_builtin(self.tokens[self.token_index:len(self.tokens)],token_type) 

            
            elif token_type == "INPUT":
                self.parse_builtin(self.tokens[self.token_index:len(self.tokens)],token_type)
                     
            elif token_type == "IF":
                self.parse_if(self.tokens[self.token_index:len(self.tokens)])
            
            elif token_type == "FOR":
                self.parse_for(self.tokens[self.token_index:len(self.tokens)])
                   
            elif token_type == "SYSTEM":
                self.parse_builtin(self.tokens[self.token_index:len(self.tokens)],token_type)

            elif token_type == "ALERT":
                self.parse_alert(self.tokens[self.token_index:len(self.tokens)],token_type)
            
            elif token_type == "COMMENT":
                self.parse_comment(self.tokens[self.token_index:len(self.tokens)])
            
            elif token_type == "FUNC":
                self.parse_func(self.tokens[self.token_index:len(self.tokens)])
            
            elif token_type == "RUN_FUNC":
                self.find_func(self.tokens[self.token_index:len(self.tokens)])
#Math
#--------------------------------------------------------------------------------------------------

            elif token_type == "FACTORIAL":
                self.parse_math(self.tokens[self.token_index:len(self.tokens)],"fact",False)
            
            elif token_type == "SINUS":
                self.parse_math(self.tokens[self.token_index:len(self.tokens)],"sinus",False)

            elif token_type == "COMPLEX":
                self.parse_math(self.tokens[self.token_index:len(self.tokens)],"complex",False)    

#--------------------------------------------------------------------------------------------------

            elif token_type == "UNDEFINIED":
                self.error_message("SyntaxError: \n Undefinied")

            self.token_index += 1
        if count == 0:
             self.error_message("Program Error: \nType must be included in code")

        if self.include == True:
            print(17*"-" + "CODE GENERATION" + 18*"-")
            print("-"*50)
            print(self.transpiled_code)
            print("#"*21,"OUTPUT","#"*21)
            exec('''import time
start_time = time.time()
'''+self.transpiled_code+'''
print()
print("Executed: %s seconds" % (time.time() - start_time))
            ''')
        else:
            exec('import time\nstart_time = time.time()\n'+self.transpiled_code+'\nprint("Executed: %s seconds" % (time.time() - start_time))\n')
        
    def parse_include(self,token_stream):
        tokens_checked = 0
        list_lib = ["math","tools"]
        lib = ""
        for token in range(0,len(token_stream)):
			
            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]
            
            if token_type == "SEMIC":break
            
            if token == 1 and token_value == "math":
                lib = "lib.fmath"
            
            elif token == 1 and token_value not in list_lib:
                msg = "IncludeError at line:",self.li,"\n'{}' is not definied".format (token_value)
                self.error_message(msg)
            
            tokens_checked+=1

        libObj = libObject()
        self.transpiled_code += libObj.transpile_include(lib)

        self.token_index += tokens_checked
    
    def parse_bracket(self,token_stream):
        
        tokens_checked = 0
        value = ""

        for token in range(0,len(token_stream)):
            
            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token_type == "BRACKET" and token_value == ")":
                value += token_value[:-1]
                break

            if token == 1:
                value = token_value[:2]
            
            elif token > 1 and token_type != "BRACKET" and token_type in ["INT","ID","OP"]:
                value += token_value


        x = "({})".format (value)
        print(x)

        self.token_index += tokens_checked
    
    def parse_math(self,token_stream,iden,var):
        
        if iden == "fact":
            value = ""
            tokens_checked = 0
            for token in range(0,len(token_stream)):
			
                token_type = token_stream[tokens_checked][0]
                token_value = token_stream[tokens_checked][1]
                
                if token_type == "SEMIC":break
                
                if token == 1 and token_type in ["INT","ID"]:
                    value = token_value
                
                elif token == 1 and token_type not in ["INT","ID"]:
                    msg = "Error: "+token_value+" must be int"
                    self.error_message(msg)

                elif token > 1 and token % 2 == 0:
                    value += token_value
                
                elif token > 1 and token % 2 != 0:
                    value += token_value

                tokens_checked+=1

            x = "MathModule().factorial({})".format (value)

            libObj = libObject()
            self.transpiled_code += libObj.transpile_math(x)
        
            self.token_index += tokens_checked

        if iden == "complex":
                    value = ""
                    tokens_checked = 0
                    for token in range(0,len(token_stream)):
                    
                        token_type = token_stream[tokens_checked][0]
                        token_value = token_stream[tokens_checked][1]
                        
                        if token_type == "SEMIC":break
                        
                        if token == 1 and token_type in ["COMPLEX_NUM","ID"]:
                            value = token_value.replace("i","j")
                        
                        elif token == 1 and token_type not in ["COMPLEX_NUM","ID"]:
                            msg = "Error: "+token_value+" must be int"
                            self.error_message(msg)

                        elif token >= 2 and token % 2 == 0 and token_type == "OP":
                            value += token_value
                        
                        elif token >= 2 and token % 2 != 0:
                            value += token_value.replace("i","j")

                        tokens_checked+=1

                    x = "MathModule().complex({})".format (value)

                    libObj = libObject()
                    self.transpiled_code += libObj.transpile_math(x)
                
                    self.token_index += tokens_checked
        
        elif var == True:
            value = ""
            tokens_checked = 0
            for token in range(0,len(token_stream)):
			
                token_type = token_stream[tokens_checked][0]
                token_value = token_stream[tokens_checked][1]
                
                if token_type == "SEMIC":break
                
                if token == 1 and token_type in ["INT","ID"]:
                    value = token_value
                
                elif token == 1 and token_type not in ["INT","ID"]:
                    msg = "Error: "+token_value+" must be int"
                    self.error_message(msg)

                elif token > 1 and token % 2 == 0:
                    value += token_value
                
                elif token > 1 and token % 2 != 0:
                    value += token_value

                tokens_checked+=1
            x = "MathModule().factorial({})".format (value)
            return x

    def parse_type(self,token_stream,):
		
        tokens_checked = 0
        
        name = ""
        operator = ""
        value = ""

        for token in range(0,len(token_stream)):
            
            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token == 1 and token_value not in ["Console","Browser"]:
                self.error_message("Program error: undefinied program '{}'".format (token_value))

    def parse_variable(self, token_stream):

        tokens_checked = 0
        func = ["factorial", "sin",]
        name = ""
        operator = ""
        value = ""

        for token in range(0,len(token_stream)):
            
            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]
            #If  semic at end
            if token_type == "SEMIC" and token != 1:break
            #If
            elif token == 1 and token_type == "ID":
                name = token_value
            #Invalid variable name <ERROR>
            elif token == 1 and token_type != "ID":
                msg = "NameError at line ",self.li,"\nInvalid Variable name '"+token_value+"'"
                self.error_message(msg)	

            elif token == 2 and token_type == "OP":
                operator = token_value
            #Invalid operator <Error>
            elif token == 2 and token_type != "OP":
                msg = "OperatorError at line {} \n Invalid operator".format (self.li)
                self.error_message(msg)
            
            elif token == 3 and token_type in ['INT', 'STR', 'ID','OP','BOOL','COMPLEX_NUM',]:
                value = token_value
            
            elif token == 3 and token_type == "BRACKET":
                self.parse_bracket(self.tokens[self.token_index:len(self.tokens)])
            
            elif token == 3 and token_type == "FACT":
                value = token_value.replace("!","MathModule().factorial("+token_value[:-1]+")")
            
            elif token == 3 and token_type == "SINUS": 
                value = self.parse_math(self.tokens[self.token_index:len(self.tokens)],"sinus")
            
            elif token == 3 and token_value == "true" or token_value == "false":
                value = token_value
            
            elif token_type == "STR":
                value = token_value.replace("\s"," ")

            elif token == 3 and token_type not in ['INT', 'STR', 'ID','LATEX',"COMPLEX_NUM"]:
                msg = "ValueError at line",self.li,":\nInvalid Variable value '"+token_value+"'"
                self.error_message(msg)
            elif token > 3 and token % 2 == 0 and token_type == "OP":
                value += token_value

            elif token > 4 and token % 2 != 0:
                value += token_value
            tokens_checked+=1

        # if "var x;" -> "x = 0"
        if operator == "" and value == "":
            operator = "="
            value = "0"

        varObj = VarObject()
        self.transpiled_code += varObj.transpile(name,operator,value)

        self.token_index += tokens_checked

    
    def parse_builtin(self,token_stream,iden):

        if iden == "PRINT" or iden == "ECHO":
            tokens_checked = 0
            value = ""
            case = 0
            for token in range(0,len(token_stream)):

                token_type = token_stream[tokens_checked][0]
                token_value = token_stream[tokens_checked][1]

                if token_type == "SEMIC":break

                if token == 0 and token_type == "ECHO":
                    case = 1
                
                elif token == 0 and token_type == "PRINT":
                    case = 2
            
                if token == 1 and token_type in ["INT","STR","ID"]:
                    value = token_value
                    
                elif token > 1 and token % 2 == 0:
                    value += token_value

                elif token > 1 and token % 2 != 0:
                    value += token_value


                tokens_checked+=1

            echoObj = BuiltinObject()
            self.transpiled_code += echoObj.transpile_print(value,case)

            self.token_index += tokens_checked
        
        elif iden == "INPUT":
            tokens_checked = 0
            var = ""
            typ = ""
        
            for token in range(0,len(token_stream)):

                token_type = token_stream[tokens_checked][0]
                token_value = token_stream[tokens_checked][1]

                if token_type == "SEMIC":break
                
                if token == 1:
                    var = token_value
                
                elif token != 2 and token_value in ["int","INT"] :
                    typ = "int"

                elif token != 2 and token_value in ["str","STR"]:
                    typ = "str"

                elif token != 2 and token_value in ["bool","BOOL"]:
                    typ = "bool"
                
                else:
                    typ = ""
            
                tokens_checked+=1

            echoObj = BuiltinObject()
            self.transpiled_code += echoObj.transpile_input(var,typ)

            self.token_index += tokens_checked
        
        elif iden == "SYSTEM":
            tokens_checked = 0
            value = ""
            
            for token in range(0,len(token_stream)):

                token_type = token_stream[tokens_checked][0]
                token_value = token_stream[tokens_checked][1]

                if token == 2 and token_type == "SEMIC":break
                
                if token == 1 and token_type == 'STR':
                    value = token_value
                else:
                    value = token_value


            echoObj = BuiltinObject()
            self.transpiled_code += echoObj.transpile_system(value)

            self.token_index += tokens_checked
        
    def parse_if(self,token_stream):

        tokens_checked = 0
        value = ""
        comp_op = ""
        value2 = ""
        command = ""
        
        for token in range(0,len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            #If '{' is found it countinues to netxt line
            if  token_type == "SCOPE" and token_value == "{":
                
                break
            
            if token == 1 and token_type in ["STR","INT","ID"]:
                value = token_value
			
            elif token == 2 and token_type == "COMP_OP":
                comp_op = token_value
			
            elif token == 3 and token_type in ["STR","INT","ID"]:
                value2 = token_value
                
            if token_value == "\n":
                continue

            if token_value == "\t":
                continue
				
            if token > 5:
                value += token_value
            
            tokens_checked += 1
				
        ifObj = ConditionalObject()
        self.transpiled_code += ifObj.transpile_if(value,comp_op,value2,command)

        self.token_index += tokens_checked
    


    def parse_for(self,token_stream):
#for x :: x < 10 :: x++ {
        tokens_checked = 0
        value = ""
        value2 = ""
        increment = ""
        command = ""
        tokens = []
        
        for token in range(0,len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]
            
            if token > 7 and token_type != "SCOPE":
                tokens.append([token_type,token_value])
                          
            if token_type == "SCOPE" and token_value == "}":break
            
            if token == 1 and token_type in "ID":
                value = token_value

            elif token == 2 and token_type != "SEPARATOR":
                msg = "SEPARATORError: at line:",self.li,"\nMust be '::'"
                self.error_message(msg)
			
            elif token == 3 and token_value != value:
                msg = "ValueError: at line:",self.li,"\nMust be same as ",value,
                self.error_message(msg)

            
            elif token == 4 and token_type != "COMP_OP":
                msg = "OperatorError: at line:",self.li,"\nMust be operator"
                self.error_message(msg)

            
            elif token == 5 and token_type in ["INT","ID"]:
                value2 = token_value
            
            elif token == 6 and token_type != "SEPARATOR":
                msg = "SEPARATORError: at line:",self.li,"\nMust be '::'"
                self.error_message(msg)
            
            elif token == 7 and token_value == value + "++":
                increment = "1"
            
            elif token == 7 and token_value == value + "--":
                increment = "-1"
            
            elif token == 7 and token_value == value:
                continue

            elif token == 8 and token_type == "OP":
                continue

            elif token  == 9 and token_type in ["INT","ID"]:
                increment = token_value

                       
            tokens_checked+=1

        print(tokens)
	
        forObj = LoopObject()
        self.transpiled_code += forObj.transpile_for(value,value2,increment,command)

        self.token_index += tokens_checked
    
    def parse_func(self,token_stream):
        tokens_checked = 0
        
        name = ""
        argument = ""
        
        for token in range(0,len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if  token_type == "SCOPE" and token_value == "{":continue
            
            if  token_type == "SCOPE" and token_value == "}":break

            if token == 1 and token_type == "ID":
                name = token_value

            elif token == 2 and token_type != "COLON":
                self.error_message("Error:")
            
            elif token == 3 and token_value == "0":
                argument = ""
            
            elif token == 3 and token_type == "ID":
                argument = token_value
            
            elif token_type != "SCOPE" and token_value != "}":
                value = "\t" + token_value

            tokens_checked+=1
        funcObj = FuncObject()
        self.transpiled_code += funcObj.transpile_func(name,argument)

        self.token_index += tokens_checked


    def parse_comment(self,token_stream):
        tokens_checked = 0
        comment_str = ""
        number = 0
        
        for token in range(0,len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token_stream[token][0] == 1 and token_type == "COMMENT": break
            
            if token > 1:
                comment_str += str(token_stream[token][1]) + " "
                

            tokens_checked+=1

#---------------------------BROWSER------------------------------------

    def parse_alert(self,token_stream):

        tokens_checked = 0
        value = ""
        
        for token in range(0,len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token == 2 and token_type == "SEMIC":break
             
            if token == 1 and token_type == 'STR':
                value = token_value
            else:
                value = token_value
            
            tokens_checked+=1

        echoObj = BuiltinObject()
        self.transpiled_code += echoObj.transpile_alert(value)

        self.token_index += tokens_checked
#-------------------------------CALL FUNCTION------------------------------
    def find_func(self,token_stream):
        tokens_checked = 0
        
        name = ""
        argument = ""
        
        for token in range(0,len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]
            
            if  token_type == "SEMIC":break

            elif token == 1  and token_type != "ID":
                self.error_message("Error")

            elif token == 1 and token_type == "ID":
                name = token_value
            
            elif token == 3 and token_type in ["ID","INT","STR","BOOL"]:
                argument = token_value
            

            tokens_checked+=1


        funcObj = FuncObject()
        self.transpiled_code += funcObj.transpile_run_func(name,argument)

        self.token_index += tokens_checked
#--------------------------------------------------------------------------

    def error_message(self,msg):
        print(msg)
        quit()