
from parser.nodes import *
from tokens.tokens import *
from errors.error import *
from .helper import *
from interpreter.interpreter import *

# builtin funcs
def yell(args, tabs) :
    code = []
    for arg in args :
        code.append(transpile_expr(arg))

    return f'{ "\t" * tabs }print( {" , ".join(code)} )'

def yellc(args, tabs) :
    code = []
    for arg in args :
        code.append(transpile_expr(arg))

    return f'{ "\t" * tabs }print( {" , ".join(code)}, end=" ")'

def transpile_expr(expr) :
    code = [] 


    # expr can be a term
    if isinstance(expr, node_term) :
        if isinstance(expr, node_string_literal) :
            return f'"{expr.value.value}"'
        elif isinstance(expr, node_identifier):
            return f'ipr.nemo_variables["{expr.value.value}"]'
        else :
            return expr.value.value
        
    # can be binary expr
    if isinstance(expr, node_binary_expression) :
        left = transpile_expr(expr.lhs)
        right = transpile_expr(expr.rhs)
        op = expr.op.value

        return f'({left}) {op} ({right})'

    # can be unary expr
    if isinstance(expr, node_unary_expression) :

        right = transpile_expr(expr.operand)
        op = expr.op.value

        return f'({op}({right}))'
        
    return ' '.join(code)

def transpile_var_assign(node, tabs) :
    code = []

    if node.var_name != '' :
        code.append( f'{"\t" * tabs}ipr.nemo_variables["{node.var_name.value.value}"]')
    else :
        new_error(f'variable name cannot be empty')

    code.append(node.op.value)

    if isinstance(node.var_value, node_binary_expression) or isinstance(node.var_value, node_unary_expression) or isinstance(node.var_value, node_term) :
        code.append(transpile_expr(node.var_value))
    else :
        new_error(f'transpiler : invalid value for a variable : {node.var_value}')

    return ' '.join(code)


def transpile_if(node, tabs) :
    # if stat node
    code = []

    # adding the condition
    code.append(f'{ "\t" * tabs }if ({transpile_expr(node.cond)}) : ')

    # adding the statements
    for stat in node.stats:
        code.append(transpile(stat, tabs+1))
    
    return '\n'.join(code)

def transpile_elif(node, tabs) :
    # if stat node
    code = []

    # adding the condition
    code.append(f'{ "\t" * tabs }elif ({transpile_expr(node.cond)}) : ')

    # adding the statements
    for stat in node.stats:
        code.append(transpile(stat, tabs+1))

    return '\n'.join(code)

def transpile_else(node, tabs) :
    # if stat node
    code = []

    # adding the condition
    code.append(f'{ "\t" * tabs }else :')

    # adding the statements
    for stat in node.stats:
        code.append(transpile(stat, tabs + 1))

    return '\n'.join(code)


def transpile_conditions(node, tabs) :
    code = []
    
    code.append(transpile_if(node.if_stat, tabs))

    for i in range(len(node.elif_stats)) :
        code.append(transpile_elif(node.elif_stats[i], tabs))

    if node.else_stat is not None :
        code.append(transpile_else(node.else_stat, tabs))

    return ' '.join(code)


def transpile_loop(node, tabs) :
    # if stat node
    code = []

    # adding the condition
    code.append(f'{ "\t" * tabs }while ({transpile_expr(node.cond)}) :')

    # adding the statements
    for stat in node.stats:
        code.append(transpile(stat, tabs + 1))
    
    return '\n'.join(code)

def transpile_repeat(node, tabs) :
    # if stat node
    code = []

    # adding the condition
    code.append(f'{ "\t" * tabs }for _ in range({transpile_expr(node.cond)}) :')

    # adding the statements
    for stat in node.stats:
        code.append(transpile(stat, tabs + 1))
    
    return '\n'.join(code)



def transpile_builtin_func(node, tabs) :
    func_to_func = {
        'yell' : yell,
        'yellc' : yellc
    }

    if node.func_name.value in func_to_func :
        return func_to_func[node.func_name.value](node.args, tabs)
    
    new_error(f'invalid builtin func <{node.func_name}>')

def transpile_use_macro(node, tabs) :
    code = []

    # adding the condition
    name = node.name.value 
    if name not in ipr.nemo_macros :
        new_error(f'macro {name} not defined')
    
    stats = ipr.nemo_macros[name]
    for stat in stats :
        code.append(transpile(stat, tabs ))
    
    return '\n'.join(code)


    # adding the statements
    for stat in node.stats:
        code.append(transpile(stat, tabs + 1))
    
    return '\n'.join(code)


def transpile(node, tabs = 0):
    code = []
    
    if isinstance(node, node_assignment) :
        code.append(transpile_var_assign(node, tabs))

    elif isinstance(node, node_condition) :
        code.append(transpile_conditions(node, tabs))

    elif isinstance(node, node_builtin_func_call) :
        code.append(transpile_builtin_func(node, tabs))

    elif isinstance(node, node_loop_statement):
        code.append(transpile_loop(node, tabs))

    elif isinstance(node, node_repeat_statement):
        code.append(transpile_repeat(node, tabs))

    elif isinstance(node, node_break_statement) :
        code.append(f'{"\t" * tabs}break')
    
    elif isinstance(node, node_use_macro):
        code.append(transpile_use_macro(node, tabs))

    elif isinstance(node, node_macro) :
        name = node.name.value
        stats = node.stats
        ipr.nemo_macros[name] = stats
    
    else :
        new_error(f'invalid node found {node}')

    return '\n'.join(code)


def transpileit(ast_program):
    cpp_code = []
    code = ''
    for stat in ast_program.nodes:
        cpp_code.append(transpile(stat))
    
    code = '\n'.join(cpp_code)

    return code