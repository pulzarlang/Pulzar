from Obj.varObject import VarObject
from Obj.echoObject import echoObject
import math

class Parser(object):

    def __init__(self,tokens,li,source_code):
        self.tokens = tokens
        self.source_code = source_code
        self.li = li
        self.token_index = 0

        self.transpiled_code = ""
        
    
    
    def parse(self):
        for self.token_index  in range(len(self.tokens)):

            #Hold value of token indentifier
            token_type = self.tokens[self.token_index][0]
            # Holds the value of token VAR
            token_value = self.tokens[self.token_index][1]
            
            self.parse_type(self.tokens[self.token_index:len(self.tokens)])
            #If token is var than add tokens to parse_varialbe()
            if token_type == "VAR" and token_value == "var":
                self.parse_variable(self.tokens[self.token_index:len(self.tokens)])
            #If token is echo add tokens to parse_print()
            elif token_type == "ECHO":
                self.parse_print(self.tokens[self.token_index:len(self.tokens)])
            #If token is echo add tokens to parse_input()
            elif token_type == "INPUT":
                self.parse_input(self.tokens[self.token_index:len(self.tokens)])

            self.token_index += 1

        #print(self.transpiled_code)
        #print("----------------------------------------------------")
        #print("#"*22,"OUTPUT","#"*22)

        exec(self.transpiled_code)

    def parse_type(self,token_stream):
		
        tokens_checked = 0

        for token in range(0,len(token_stream)):
			
            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token == 1 and token_type == "TP" and token_value != "Type":
                print("<Error>\nType is missing "+token_value)
                quit()
                
            elif token == 1 and token_value == "Type":
                pass
            
            elif token == 2 and token_value == "Console":
                pass

            elif token == 2 and token_value == "Browser":
                #web =browser.browser()
                pass

    def parse_variable(self, token_stream):

        tokens_checked = 0
        
        name = ""
        operator = ""
        value = ""

        for token in range(0,len(token_stream)):
            
            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]
            #If  semic at end
            if token_type == "SEMIC":break
            #If
            elif token == 1 and token_type == "ID":
                name = token_value
            #Invalid variable name <ERROR>
            elif token == 1 and token_type!="ID":
                print("<Error> at line "+self.li+"\nInvalid Variable name '"+token_value+"'")
                quit()
            
            elif token == 2 and token_type == "OP":
                operator = token_value
            #Invalid operator <Error>
            elif token == 2 and token_type != "OP":
                print("<Error> at line "+self.li+"\nInvalid operator")
                quit()
            
            elif token == 3 and token_type in ['INT', 'STR', 'ID']:
                value = token_value
                print("\n")
            elif token == 3 and token_type not in ['INT', 'STR', 'ID']:
                print("<Error> at line ",self.li,":\nInvalid Variable value '"+token_value+"'")
                quit()
            elif token == 3 and token_value[1:] == '"':
                value = token_value
                value = ("{}".format (token_value1))
            
            elif token > 3:
               pass 

            tokens_checked+=1

        varObj = VarObject()
        self.transpiled_code += varObj.transpile(name,operator,value)

        self.token_index += tokens_checked

    
    def parse_print(self,token_stream):
        tokens_checked = 0
        value1 = ""
        
        for token in range(0,len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token == 2 and token_type == "SEMIC":break

            if token == 1 and token_value[1:] == '"':
                value1 = token_value
            else:
                value1 = token_value
                
            if token == 1 and token_type == ["INT"]:
                value1 = token_value
            
            if token == 1 and token_type == ['ROOT'] and token == 2 and token_type == ['INT']:
                value1 = 'math.',sqrt(token_value)                
    
            tokens_checked+=1

        echoObj = echoObject()
        self.transpiled_code += echoObj.transpile_print(value1)

        self.token_index += tokens_checked

    def parse_input(self,token_stream):
        tokens_checked = 0
        value1 = ""
        op = ""
        
        for token in range(0,len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token == 1 or token > 1 and token_type == "SEMIC":break
            
            elif token == 1 and token_value == "":
                value1 = token_value

            elif token == 1 and not token_value[1:] == '"':
                value1 = token_value
            else:
                value1 = token_value
            
            if token == 2 and token_type == "OP":
                op = token_value

            elif token == 3 and token_type == "INT":
                value = token_value

                    
            tokens_checked+=1

        echoObj = echoObject()
        self.transpiled_code += echoObj.transpile_input(value1)

        self.token_index += tokens_checked
