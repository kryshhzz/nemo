class Node :
    pass

class node_program(Node) :
    
    def __init__(self, nodes = []) :
        self.nodes = nodes

    def append(self, node : Node) :
        self.nodes.append(node) 

class node_statement(Node) :
    # variable declaration, assignment, print
    pass

class node_expression(Node) :
    # binary expression, unary expression
    pass

class node_term(Node) :
    # number literals, bool literals, string literals, identifier
    pass

class node_builtin_func_call(node_statement):
    
    def __init__(self, func_name, args) :
        self.func_name = func_name
        self.args = args

class node_loop_statement(node_statement) :

    def __init__(self, cond, stats) :
        self.cond = cond
        self.stats = stats

class node_repeat_statement(node_statement) :

    def __init__(self, cond, stats) :
        self.cond = cond
        self.stats = stats

class node_break_statement(node_statement) :
    pass


class node_if_statement(node_statement) :

    def __init__(self, cond, stats) :
        self.cond = cond
        self.stats = stats

class node_elif_statement(node_statement) :

    def __init__(self, cond, stats) :
        self.cond = cond
        self.stats = stats

class node_else_statement(node_statement) :

    def __init__(self, stats) :
        self.stats = stats


class node_condition(node_statement) :

    def __init__(self, if_stat, elif_stats, else_stat) :
        self.if_stat = if_stat
        self.elif_stats = elif_stats
        self.else_stat = else_stat

class node_macro(node_statement) :

    def __init__(self, name, stats) :
        self.name = name
        self.stats = stats

class node_use_macro(node_statement) :

    def __init__(self, name) :
        self.name = name

class node_binary_expression(node_expression) :
    def __init__(self, lhs : node_expression, op : any, rhs : node_expression) :
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

class node_unary_expression(node_expression) :

    def __init__(self, op : any, operand : node_expression) :
        self.op = op
        self.operand = operand

# class node_variable_declaration(node_statement) :

#     def __init__(self, var_type , var_name, var_value) :
#         self.var_type = var_type
#         self.var_name = var_name
#         self.var_value = var_value

class node_assignment(node_statement) :

    def __init__(self, var_name : str,op : any, var_value : node_expression) :
        self.var_name = var_name
        self.op = op
        self.var_value = var_value

class node_number_literal(node_term) :

    def __init__(self, value : any) :
        self.value = value

class node_string_literal(node_term) :

    def __init__(self, value : any) :
        self.value = value

class node_bool_literal(node_term) :

    def __init__(self, value : any) :
        self.value = value

class node_identifier(node_term) :

    def __init__(self, value : any) :
        self.value = value

