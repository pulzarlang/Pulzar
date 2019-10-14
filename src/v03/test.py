import lexer
import mparser
code = ""
li = 0
parse = mparser.Parser([['PM', 'Program'], ['ID', 'Console'], ['SEMIC', ';'], ['INCLUDE', 'include'], ['ID', 'math'], ['SEMIC', ';'], ['VAR', 'var'], ['ID', 'a'], ['SEMIC', ';']],code,li,True)
                            
parse.parse()