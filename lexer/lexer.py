
from tokens.tokens import nemo_token, token_type
from .helper import check_if_keyword, check_if_operator, check_if_brace
from errors.error import *

class tokenizer :


    def __init__(self, content : str) :
        self.content = content
        self.index = 0
        self.content_len = len(content)
        self.result_tokens = []
        self.operators = {'+', '-', '*', '/', '%', '=', '<', '>', '&', '|', '^', '~', '!'}
        self.braces = {'(', ')', '{', '}'}

    def peek(self, ahead = 0 ) :
        if self.index + ahead >= self.content_len :
            return None 
        else :
            return self.content[self.index] 

    def consume(self) :
        self.index += 1
        return self.content[self.index-1]

            
    def tokenize_content(self) :
        buf = []

        while self.index < self.content_len :

            # keywords 
            if self.peek() is not None and self.peek().isalpha() :

                # load into buffer 
                while self.peek() is not None and (self.peek().isalnum() or self.peek() == '_')  :
                    buf.append(self.consume())

                str_buf = ''.join(buf)
                buf.clear()

                # check if it is a keyword, builtin_func
                ntoken = check_if_keyword(str_buf)
                if ntoken is not None :
                    self.result_tokens.append(ntoken)

                else :
                    # invalid keyword hence assuming it as identifier
                    self.result_tokens.append(
                        nemo_token(
                            token_type.t_identifier,
                            str_buf
                        )
                    )

            # number literals
            elif self.peek() is not None and self.peek().isdigit() :

                while self.peek() is not None and self.peek().isdigit() :
                    buf.append(self.consume())

                str_buf = ''.join(buf)
                buf.clear()

                # append the num literal to the result tokens
                self.result_tokens.append(
                    nemo_token(
                        token_type.t_number_literal,
                        str_buf
                    )
                ) 


            # string literals
            elif self.peek() is not None and self.peek() == '"' or self.peek() == "'":
                prev = self.consume()
                while self.peek() is not None and self.peek() != prev :
                    buf.append(self.consume())
                
                str_buf = ''.join(buf)
                buf.clear()
                if self.peek() == prev :
                    self.consume()
                else :
                    new_error(f'<{prev}> not closed ')

                self.result_tokens.append(
                    nemo_token(
                        token_type.t_string_literal,
                        str_buf
                    )
                )

            # comments 
            elif self.peek() is not None and self.peek() == '#' :
                while self.peek() is not None and self.peek() != '\n' :
                    self.consume()

                # adding a new line instead of comment 
                # as it helps in better line numbering in errors
                self.result_tokens.append(
                    nemo_token(
                        token_type.t_newline,
                        None
                    )
                )
                
                # consuming the '\n' too
                next_line_no()
                self.consume()

            # operators 
            elif self.peek() is not None and self.peek() in self.operators : 
                buf = []
                buf.append(self.consume())
                while self.peek() and self.peek() in self.operators :
                    buf.append(self.consume())
                
                str_buf = ''.join(buf)
                buf.clear()
                
                ntoken = check_if_operator(str_buf)
                if ntoken is not None :
                    self.result_tokens.append(ntoken)
                else :
                    new_error(f'Invalid operator : <{str_buf}>')

            # braces
            elif self.peek() is not None and self.peek() in self.braces :
                buf_str = self.consume()
                ntoken = check_if_brace(buf_str)
                if ntoken is not None :
                    self.result_tokens.append(ntoken)
                else :
                    new_error(f'Invalid brace : <{buf_str}>') 

            # comma
            elif self.peek() is not None and self.peek() == ',' :
                self.result_tokens.append(
                    nemo_token(
                        token_type.t_comma,
                        None
                    )
                )
                self.consume()            


            # space
            elif self.peek() is not None and self.peek().isspace() :
                if self.peek() == '\n' :
                    next_line_no()
                    self.result_tokens.append(
                        nemo_token(
                            token_type.t_newline,
                            None
                        )
                    )
                self.consume()

            # invalid char
            else :
                new_error (f'Invalid character : <{self.peek()}>')



def lex(content : str) :
    tr = tokenizer(content)
    tr.tokenize_content()
    reset_line_no()
    return tr.result_tokens