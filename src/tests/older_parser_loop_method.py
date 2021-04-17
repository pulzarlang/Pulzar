    def parse_loop(self, token_stream, isNested):
        # for x :: x < 10 :: x++ {
        tokens_checked = 0
        keyword = ""
        condition = ""
        value = ""
        increment = ""
        var_decl = False
        ast = {'loop': []}

        for token in range(0, len(token_stream)):

            token_type = token_stream[tokens_checked][0]
            token_value = token_stream[tokens_checked][1]

            if token_type == "SCOPE_DEFINIER" and token_value == "{":
                break

            if token == 0:
                ast['loop'].append({'keyword': token_value})
                keyword = token_value

            if token == 1 and keyword == "while":
                condition = token_value

            if token == 1 and token_type in "IDENTIFIER" and keyword != "while":
                self.get_token_value(token_value)
                ast['loop'].append({'name': token_value})
                ast['loop'].append({'start_value': self.get_token_value(token_value)})

            elif token == 1 and token_type == "DATATYPE" and keyword != "while":
                # check variale declaration
                if token_stream[token + 1][0] == "IDENTIFIER" and token_stream[token + 2][0] == "OPERATOR" and \
                        token_stream[token + 3][0] in ["INTEGER", "IDENTIFIER", ]:
                    ast['loop'].append({'name': token_value})
                    ast['loop'].append({'start_value': token_stream[token + 3][1]})

            elif token == [2, 5] and token_type != "SEPARATOR"  and keyword != "while":
                msg = "SyntaxError: at line {}:\nMust be '::'".format(self.lines)
                self.error_message(msg, token_stream, token)

            elif token == 2 and token_type in ["OPERATOR", "COMPARTION_OPERATOR"] and keyword == "while":
                if token_value == "mod":
                    condition += "%"
                else:
                    condition += token_value

            elif token > 2 and keyword == "while":
                condition += token_value

            # elif (token == 4 and token_value != str([ast['loop'][2]['start_value']])):
            # print(token_value, str([ast['loop'][2]['start_value']]))
            # msg = ("ValueError: at line:\nMust be same as ", [ast['loop'][2]['start_value']])
            # self.error_message(msg, token_stream, token)

            elif token == [4, 7] and token_type != "COMPARTION_OPERATOR"  and keyword != "while":
                msg = token_value + "CompertionError at line:\nMust be operator"
                self.error_message(msg, token_stream, token)


            elif token in [5, 8] and token_type in ["INTEGER", "IDENTIFIER"]  and keyword != "while":
                ast['loop'].append({'end_value': token_value})

            elif token == [6, 9] and token_type != "SEPARATOR"  and keyword != "while":
                msg = "SeparatorError: at line:\nMust be '::'"
                self.error_message(msg, token_stream, token)

            elif token == 7 and token_type in ["INCREMENT", "INDETIFIER"]  and keyword != "while":
                ast['loop'].append({'increment': "1"})

            elif token == 7 and token_type in ["DECREMENT", "IDENTIFIER"] and keyword != "while":
                ast['loop'].append({'increment': "1"})

            tokens_checked += 1

        self.token_index += tokens_checked

        scope_tokens = self.get_scope(token_stream[tokens_checked + 1:len(token_stream)])

        if keyword == "while": ast['loop'].append({'condition': condition})
        if isNested == False:
            self.parse_scope(scope_tokens[0], ast, 'loop', False, False)
        else:
            self.parse_scope(scope_tokens[0], ast, 'loop', True, False)

        tokens_checked += scope_tokens[1]

        return [ast, tokens_checked]