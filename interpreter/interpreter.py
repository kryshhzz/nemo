
from collections import OrderedDict
from parser.nodes import *
from errors.error import *
from tokens.tokens import *
from .helper import *
from transpiler import transpiler
from .ipr import *

class scope(ipr) :

    def __init__(self, nemo_nodes) :
        self.index = 0
        self.nemo_nodes = nemo_nodes
        self.nodes_len = len(nemo_nodes)
        self.cur_len = len(ipr.nemo_variables)
        self.macros_cur_len = len(ipr.nemo_macros)

    def __del__(self) :
        while len(ipr.nemo_variables) > self.cur_len :
            ipr.nemo_variables.popitem(last=True)
        
        while len(ipr.nemo_macros) > self.macros_cur_len :
            ipr.nemo_macros.popitem(last=True)

    def peek(self, ahead = 0 ) :
        if self.index + ahead >= self.nodes_len :
            return None 
        else :
            return self.nemo_nodes[self.index + ahead] 

    def consume(self) :
        self.index += 1
        return self.nemo_nodes[self.index-1] 

    def interpret_expr(self, expr) :
        # unary expr
        # bin expr
        # literals
        if isinstance(expr, node_bool_literal) or isinstance(expr, node_number_literal) or isinstance(expr, node_string_literal) :
            if expr.value.type == token_type.t_number_literal :
                return int(expr.value.value)

            elif expr.value.type == token_type.t_bool_literal :
                if expr.value.value == 'true' :
                    return True
                elif expr.value.value == 'false' :
                    return False
                else :
                    new_error(f'invalid bool type {expr.value.value}')
            
            elif expr.value.type == token_type.t_string_literal :
                return expr.value.value
            
            new_error(f'invalid node_term literal {expr.value.value}') 
        
        elif isinstance(expr, node_identifier) :
            if expr.value.value not in ipr.nemo_variables :
                new_error(f'variable {expr.value.value} not defined')
            return ipr.nemo_variables[expr.value.value]

        elif isinstance(expr, node_binary_expression) :
            # eval bin_exp
            left = self.interpret_expr(expr.lhs)
            right = self.interpret_expr(expr.rhs)
            op = expr.op

            # arithmetic ops
            if token_type.is_arithmetic(op.type) :

                if type(left) != type(right) :
                    new_error(f'datatype mismatch {type(left)} {left} {op} {type(right)} {right}')


                op = op.value
                if op == '+' :
                    return left + right
                elif op == '-' :
                    return left - right 
                elif op == '*' :
                    return left * right
                
                if not isinstance(left, int) :
                    new_error(f'cannot perform arithmetic operation {op} on non int type {type(left)} {left} ')

                if op == '/' :
                    return left * right
                elif op == '//' :
                    return left // right
                elif op == '**' :
                    return left ** right
                elif op == '%' :
                    return left % right
            
            elif token_type.is_comparison_op(op.type) :
                op = op.value

                if type(left) != type(right) :
                    new_error(f'datatype mismatch {type(left)} {left} {op} {type(right)} {right}')

                if op == '>' :
                    return left > right
                elif op == '<' :
                    return left < right
                elif op == '==' :
                    return left == right
                elif op == '!=' :
                    return left != right 
                elif op == '>=' :
                    return left >= right
                elif op == '<=' :
                    return left <= right


            elif token_type.is_logical_op(op.type) :

                op = op.value

                if type(left) != type(right) :
                    new_error(f'datatype mismatch {type(left)} {left} {op} {type(right)} {right}')

                if not isinstance(left, bool) :
                    new_error(f'cannot perform logical operations on non bool type {type(left)} {left}')


                if op == 'and' :
                    return left and right
                elif op == 'or' :
                    return left or right
                else :
                    new_error(f'invalid binary operation {op.value}')

        elif isinstance(expr, node_unary_expression) :
            # eval un_exp 
            
            op = expr.op
            right = self.interpret_expr(expr.operand) 

            if not token_type.is_unary_operator(op.type) :
                new_error(f'invalid unary operator {op.value}')

            if not isinstance(right, int) and not isinstance(right, bool):
                new_error(f'cannot perform unary operations on non bool / non int type {type(left)} {left}')


            op = op.value

            if op == '+' :
                return +right
            elif op == '-' :
                return -right
            elif op == 'not' :
                return not right
            else :
                new_error(f'invalid unary operation <{op}>')

        else :
            new_error(f"invalid expression {expr}")

    def interpret_assignment(self) :
        # assign val to a var
        node = self.consume()
        var_name = node.var_name.value.value
        op = node.op.value
        var_val = node.var_value
        # var_val will be an expression

        var_val = self.interpret_expr(var_val)

        if op == '=' :
            ipr.nemo_variables[var_name] = var_val
            return

        # check if the variable is in the nemo-vars or not
        if var_name not in ipr.nemo_variables :
            new_error(f'variable not defined : {var_name}') 
        
        # check if the var_type of the var in the nemo-vars is the same as the rhs 
        if type(ipr.nemo_variables[var_name]) != type(var_val) :
            new_error(f'datatype mismatch : {var_val} of type {type(var_val)} {op} {var_name} of type {type(ipr.nemo_variables[var_name])}') 


        # works for str, bool, int
        if op == '+=' :
            ipr.nemo_variables[var_name] += var_val
            return 

        # only works for bool and int not str
        if isinstance(ipr.nemo_variables[var_name], str) :
            new_error(f'cannot do operation {op} on type str {var_name}')

        if op == '-=' :
            ipr.nemo_variables[var_name] -= var_val
        elif op == '*=' :
            ipr.nemo_variables[var_name] *= var_val
        elif op == '/=' :
            ipr.nemo_variables[var_name] /= var_val
        elif op == '//=' :
            ipr.nemo_variables[var_name] //= var_val
        elif op == '**=' :
            ipr.nemo_variables[var_name] **= var_val
        elif op == '%=' :
            ipr.nemo_variables[var_name] %= var_val       

        else :
            new_error(f'invalid operator {op}')

    def interpret_args(self, args) :
        res = []
        for arg in args :
            res.append(self.interpret_expr(arg))
        return res

    def interpret_builtin_func(self) :
        node = self.consume()
        args = self.interpret_args(node.args)
        func_name = node.func_name.value

        if func_name in ipr.func_to_func:
            ipr.func_to_func[func_name](args)
        else :
            new_error(f'builtin func not found {func_name}')

    def interpret_condition(self) :
        
        node = self.consume()

        # interpret the if condition
        if_stat = node.if_stat
        elif_stats = node.elif_stats
        else_stat = node.else_stat

        if self.interpret_expr(if_stat.cond) == True :
            # run if stats
            new_scope = scope(if_stat.stats)
            broke = new_scope.interpret_statements()
            del new_scope
            return broke

        else :
            # check elif conds
            for elif_stat in elif_stats :
                elif_cond = elif_stat.cond
                if self.interpret_expr(elif_cond) == True :
                    new_scope = scope(elif_stat.stats)
                    broke = new_scope.interpret_statements()
                    del new_scope
                    return broke

            # running the else block
            else :
                if else_stat is not None :
                    new_scope = scope(else_stat.stats)
                    broke = new_scope.interpret_statements()
                    del new_scope 
                    return broke


    def interpret_loop(self):
        node = self.consume()

        # if the cond is true then start the loop
        cond_eval = self.interpret_expr(node.cond)
        if isinstance(cond_eval, bool) :
            new_scope = scope(node.stats)

            while new_scope.interpret_expr(node.cond) == True :
                broke_response = new_scope.interpret_statements()
                if broke_response == -1 :
                    break

            del new_scope

        else :
            new_error(f'invalid condition for a loop {self.interpret_expr(node.cond)}')

    def interpret_repeat(self):
        node = self.consume()

        # if the cond is true then start the loop
        cond_eval = self.interpret_expr(node.cond)
        if isinstance(cond_eval, int) :
            
            if cond_eval >= 1000 :

                # do lit
                # making a scope so that if any variables are added by lit they can be 
                # removed after usign lit
                print('lit 🔥')
                new_scope = scope([])
                code = transpiler.transpile(node)
                exec(code)
                del new_scope

            else :
                # do normal nemo wihtout lit
                new_scope = scope(node.stats)
                for _ in range(self.interpret_expr(node.cond)) :
                    broke_response = new_scope.interpret_statements()
                    if broke_response == -1 :
                        break
                del new_scope

        else :
            new_error(f'invalid condition for a loop {self.interpret_expr(node.cond)}')



    def interpret_macro(self) :
        
        # we are putting the macros inside the nemo_vars and considering it as a var
        node = self.consume()

        name = node.name.value
        stats = node.stats

        ipr.nemo_macros[name] = stats

    def interpret_use_macro(self) :
        node = self.consume()
        name = node.name.value

        if name not in ipr.nemo_macros :
            new_error(f'macro {name} not found')
        else :
            stats = ipr.nemo_macros[name]
            new_scope = scope(stats)
            new_scope.interpret_statements()
            del new_scope

    def interpret_statements(self) :

        # broke if 1 : normal
        # broke if -1 ; break

        # normal
        broke = 1

        while self.peek() is not None :
            # interpret stats
            if isinstance(self.peek(), node_assignment) :
                # assign 
                self.interpret_assignment()

            elif isinstance(self.peek(), node_builtin_func_call) :
                # builtin funcs
                self.interpret_builtin_func()

            elif isinstance(self.peek(), node_condition):
                # if else if 
                broke = self.interpret_condition()

            elif isinstance(self.peek(), node_loop_statement) :
                # loops
                broke = self.interpret_loop()
            
            elif isinstance(self.peek(), node_break_statement) :
                # break found 
                self.consume()
                self.index = 0
                return -1

            elif isinstance(self.peek(), node_repeat_statement) :
                # repeat
                self.interpret_repeat()

            elif isinstance(self.peek(), node_macro) :
                # macro
                self.interpret_macro()

            elif isinstance(self.peek(), node_use_macro) :
                # macro use
                self.interpret_use_macro()
 
            else :
                new_error(f'invalid node {self.peek()}')

            if broke == -1:  # break
                return -1

        self.index = 0
        return broke


def interpretit(ast_node) :
    nemo_nodes = ast_node.nodes

    # creating the main scope
    main_scope = scope(nemo_nodes)
    main_scope.interpret_statements() 

    # removing all the vars
    del main_scope 

    # exec(transpiler.transpileit(ast_node))
    

