from .nodes import *
from .helper import *
from tokens.tokens import * 
from errors.error import *

class parser :

    def __init__(self, nemo_tokens) :
        self.nemo_tokens = nemo_tokens
        self.index = 0
        self.tokens_len = len(nemo_tokens)  

    def peek(self, ahead = 0 ) :
        if self.index + ahead >= self.tokens_len :
            return None 
        else :
            return self.nemo_tokens[self.index + ahead] 

    def consume(self) :
        self.index += 1
        return self.nemo_tokens[self.index-1] 

    def parse_term(self) : 
        if self.peek() is not None and self.peek().type == token_type.t_number_literal :
            return node_number_literal(self.consume())
        elif self.peek() is not None and self.peek().type == token_type.t_string_literal :
            return node_string_literal(self.consume())
        elif self.peek() is not None and self.peek().type == token_type.t_bool_literal :
            return node_bool_literal(self.consume())
        elif self.peek() is not None and self.peek().type == token_type.t_identifier :
            return node_identifier(self.consume())
        else :
            new_error(f'invalid term {self.peek()}')

    def parse_expression(self, delim = None) :
        # can be like a + b
        # a + expression
        # expression + expression
        # + expression 

        expr_stack = []

        # while loop 
        while self.peek() is not None and self.peek().type != token_type.t_newline and self.peek().type != token_type.t_close_paren and self.peek().type != token_type.t_comma and self.peek().type != delim : 
            # parse the expr till there is a new line 
            
            # literal or just identifier 
            if self.peek() is not None and token_type.is_literal(self.peek().type) or self.peek().type == token_type.t_identifier :
                expr_stack.append( self.parse_term() ) 

            # open paren
            elif self.peek() is not None and self.peek().type == token_type.t_open_paren :
                # consuming the open parantheses
                self.consume()
                expr_stack.append( self.parse_expression() ) 
                # consuming the closed parentheses
                if self.peek() is not None and self.peek().type == token_type.t_close_paren :
                    self.consume()
                else :
                    new_error(f'expected ) after expression {self.peek()}')

            # if opertor ( only bin operators )
            elif self.peek() is not None and token_type.is_operator(self.peek().type) and len(expr_stack) > 0: 
                left = expr_stack.pop(-1)

                # cosnume the operator
                op = self.consume() 

                if self.peek() is not None and token_type.is_literal(self.peek().type) or self.peek().type == token_type.t_identifier:
                    right = self.parse_term()
                    expr_stack.append(
                        node_binary_expression(left, op, right)
                    ) 
                elif self.peek() is not None and token_type.t_open_paren == self.peek().type :
                    right = self.parse_expression()
                    expr_stack.append(
                        node_binary_expression(left, op, right)
                    ) 
                else : 
                    new_error(f'expected expression after operator, found : {self.peek()}')
            

            # uanry operators
            elif self.peek() is not None and token_type.is_unary_operator(self.peek().type) and len(expr_stack) == 0: 
                op = self.consume()

                if self.peek() is not None and token_type.is_literal(self.peek().type) or self.peek().type == token_type.t_identifier:
                    right = self.parse_term()
                    expr_stack.append(
                        node_unary_expression(op, right)
                    ) 
                elif self.peek() is not None and token_type.t_open_paren == self.peek().type :
                    right = self.parse_expression()
                    expr_stack.append(
                        node_unary_expression(op, right)
                    ) 
                else : 
                    new_error(f'expected expression after operator, found : {self.peek()}')

            else :
                new_error(f'invalid expression <{self.peek()}>') 

        if len(expr_stack) == 1 :
            return expr_stack.pop(-1)
        print(expr_stack)
        new_error(f'invalid expression bin_exp {expr_stack}')

    def parse_if(self) :

        # consume if
        self.consume()

        # check expression 

        condition = self.parse_expression(token_type.t_open_curly)
        stats = []

        # check for cur braces open 
        if self.peek() is not None and self.peek().type == token_type.t_open_curly :
            # consuming open curly
            self.consume()
            stats = self.parse_statements(token_type.t_close_curly)
        else :
            new_error('expected <{>')

        # consume closed curly
        if self.peek() is not None and self.peek().type == token_type.t_close_curly :
            self.consume()
        else :
            new_error('expected <}>')

        return node_if_statement(
            condition, 
            stats
        )

    def parse_elif(self) :

        # consume elif 
        self.consume()

        # check expression
        condition = self.parse_expression(token_type.t_open_curly)
        stats = []

        # check for cur braces open 
        if self.peek() is not None and self.peek().type == token_type.t_open_curly :
            # consuming open curly
            self.consume()
            stats = self.parse_statements(token_type.t_close_curly)
        else :
            new_error('expected <{>')

        # consume closed curly
        if self.peek() is not None and self.peek().type == token_type.t_close_curly :
            self.consume()
        else :
            new_error('expected <}>')

        return node_elif_statement(
            condition, 
            stats
        )


    def parse_else(self) :

        # consume else
        self.consume()

        stats = []

        # check for cur braces open 
        if self.peek() is not None and self.peek().type == token_type.t_open_curly :
            # consuming open curly
            self.consume()
            stats = self.parse_statements(token_type.t_close_curly)
        else :
            new_error('expected <{>')

        # consume closed curly
        if self.peek() is not None and self.peek().type == token_type.t_close_curly :
            self.consume()
        else :
            new_error('expected <}>')

        return node_else_statement(
            stats
        )
        

    def parse_condition(self) :
        # when if is found this is called and it returns the whole node_cndition_statement

        if_stat = None
        elif_stats = []
        else_stat = None

        if self.peek() is not None and self.peek().type == token_type.t_if :
            if_stat = self.parse_if()
            
            while self.peek() is not None and self.peek().type == token_type.t_elif :
                elif_stats.append(self.parse_elif())

            if self.peek() is not None and self.peek().type == token_type.t_else :
                else_stat = self.parse_else()

        nc = node_condition(
            if_stat,
            elif_stats,
            else_stat
        )

        return nc
    
    def parse_loop(self) :

        # cosnume the loop keyword
        self.consume()

        condition = self.parse_expression(token_type.t_open_curly)
        stats = []

        # check for cur braces open 
        if self.peek() is not None and self.peek().type == token_type.t_open_curly :
            # consuming open curly
            self.consume()
            stats = self.parse_statements(token_type.t_close_curly)
        else :
            new_error('expected <{>')

        # consume closed curly
        if self.peek() is not None and self.peek().type == token_type.t_close_curly :
            self.consume()
        else :
            new_error('expected <}>')

        return node_loop_statement(
            condition, 
            stats
        )

    def parse_repeat(self) :

        # cosnume the repeat keyword
        self.consume()

        condition = self.parse_expression(token_type.t_open_curly)
        stats = []

        # check for cur braces open 
        if self.peek() is not None and self.peek().type == token_type.t_open_curly :
            # consuming open curly
            self.consume()
            stats = self.parse_statements(token_type.t_close_curly)
        else :
            new_error('expected <{>')

        # consume closed curly
        if self.peek() is not None and self.peek().type == token_type.t_close_curly :
            self.consume()
        else :
            new_error('expected <}>')

        return node_repeat_statement(
            condition, 
            stats
        )
    
    


    def parse_args(self) : 
        # cosnume the open paren
        if self.peek() is not None and self.peek().type == token_type.t_open_paren :
            self.consume()
        else :
            new_error(f'function call should have parentheses "{self.peek(-1)}"') 

        args = []
        while self.peek() is not None and self.peek().type != token_type.t_close_paren and self.peek().type != token_type.t_newline: 

            if self.peek().type == token_type.t_comma :
                self.consume()
            else :
                args.append(self.parse_expression())

        # consuming clsoed paremntshese
        if self.peek() is not None and self.peek().type == token_type.t_close_paren :
            self.consume()
        else :
            new_error(f'function call should have parentheses "{self.peek(-1)}"')
        

        return args


    def parse_macro(self) :
        # consuimg macro keyword
        self.consume()

        if self.peek() is not None and self.peek().type == token_type.t_identifier :
            # name
            name = self.consume()
            
            # expecting a {
            if self.peek() is not None and self.peek().type == token_type.t_open_curly :
                # consuimg {
                self.consume()

                # cosnuming stats
                stats = self.parse_statements(token_type.t_close_curly)
                
                # expecting a }
                if self.peek() is not None and self.peek().type == token_type.t_close_curly :
                    self.consume()

                    return node_macro (
                        name, 
                        stats
                    )

                else :
                    new_error(f'expecting a }} to end macro {name.value}')
            else :
                new_error(f'expecting a {{ after macro {name.value}')
            # stats 

        else :
            new_error(f'invalid macro syntax {self.peek().value}')

    def parse_use_macro(self) :
        # consuimg use keyword
        self.consume()

        if self.peek() is not None and self.peek().type == token_type.t_identifier :
            # name
            name = self.consume()
            return node_use_macro(name)
        else :
            new_error(f'invalid macro syntax {self.peek().value}')

    def parse_statements(self, delim = None) :
        # make tokens to nodes

        result_ast = []

        while self.index < self.tokens_len and self.peek() is not None and self.peek().type != delim :             
            
            # newline to semicolon
            if self.peek() is not None and self.peek().type == token_type.t_newline : 
                next_line_no()
                self.consume()
            
            # # var declaration and assignment should happen in one line
            # elif self.peek() is not None and token_type.is_datatype(self.peek().type) :
            #     # if the first token is datatype the next should be identifier 
            #     # can be folowed by = and expression

            #     if self.peek(1) is not None and self.peek(1).type != token_type.t_identifier :
            #         new_error(f'expected variable name after datatype declaration {self.peek()}')
            #     else :
            #         var_type = self.consume()
            #         var_name = self.parse_term()
                    
            #         # if just ( int x )
            #         if self.peek() is not None and self.peek().type == token_type.t_newline :
            #             result_ast.append(
            #                 node_variable_declaration(
            #                     var_type,
            #                     var_name, 
            #                     default_values[var_type.type]
            #                 )
            #             )

            #         # if ( int x = 0 )
            #         else :
            #             if self.peek() is not None and self.peek().type != token_type.t_op_assign :
            #                 new_error(f'expected = after variable declaration {self.peek()}')
            #             else :
            #                 # = found ; find expression now 
            #                 self.consume()
            #                 var_value = self.parse_expression() 
            #                 result_ast.append(
            #                     node_variable_declaration(
            #                         var_type,
            #                         var_name,
            #                         var_value
            #                     )
            #                 ) 
               
            # assignment 
            elif self.peek() is not None and self.peek().type == token_type.t_identifier :
                var_name = self.parse_term()
                
                # check for operator and then check for expr
                if self.peek() is not None and  token_type.is_assignment_op(self.peek().type)  :
                    op = self.consume()
                    val = self.parse_expression()
                    result_ast.append(
                        node_assignment(
                            var_name,
                            op,
                            val
                        )
                    )
                else :
                    new_error(f'expected =, -=, += etc after variable name <{self.peek(-1)}>')

            elif self.peek() is not None and token_type.is_builtin_func(self.peek().type) :
                func_name = self.consume() 
                args = self.parse_args()
                result_ast.append(
                    node_builtin_func_call(
                        func_name,
                        args
                    )
                )

            elif self.peek() is not None and self.peek().type == token_type.t_if :
                result_ast.append(
                    self.parse_condition()
                )

            # while loop statement
            elif self.peek() is not None and self.peek().type == token_type.t_loop :
                result_ast.append(
                    self.parse_loop()
                )
            
            # repeat statement
            elif self.peek() is not None and self.peek().type == token_type.t_repeat :
                result_ast.append(
                    self.parse_repeat()
                )
            
            # break
            elif self.peek() is not None and self.peek().type == token_type.t_break :
                # concsumign the break statement
                self.consume()
                result_ast.append(
                    node_break_statement()
                )

            # macro
            elif self.peek() is not None and self.peek().type== token_type.t_macro :
                result_ast.append(
                    self.parse_macro()
                )
            
            # use macro
            elif self.peek() is not None and self.peek().type== token_type.t_use :
                result_ast.append(
                    self.parse_use_macro()
                )
            


            else :
                new_error(f'invalid syntax {self.peek()}') 

        return result_ast

def parseit(nemo_tokens) :
    pr = parser(nemo_tokens)
    nodes = pr.parse_statements()
    reset_line_no()
    return node_program(nodes)