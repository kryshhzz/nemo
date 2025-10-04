from tokens.tokens import nemo_token, token_type

builtin_funcs = {
    'yell' : token_type.t_println,
    'yellc' : token_type.t_print,
    'ask' : token_type.t_input,
}

keywords = {

    'true' : token_type.t_bool_literal,
    'false' : token_type.t_bool_literal,

    'stop' : token_type.t_break,
    
    'macro' : token_type.t_macro,
    'use' : token_type.t_use,
    
    'and' : token_type.t_op_and,
    'or' : token_type.t_op_or,
    'not' : token_type.t_op_not,

    'if' : token_type.t_if,
    'else' : token_type.t_else,
    'elif' : token_type.t_elif,

    'loop' : token_type.t_loop,
    'repeat' : token_type.t_repeat,
}

def check_if_keyword(word) :

    if word in keywords :
        return (
            nemo_token( keywords[word], word)
        )
    
    elif word in builtin_funcs :
        return (
            nemo_token( builtin_funcs[word], word)
        )

    else :
        return None


operators = {
    # Arithmetic
    '+': token_type.t_op_plus,
    '-': token_type.t_op_minus,
    '*': token_type.t_op_multiply,
    '/': token_type.t_op_divide,
    '//' : token_type.t_op_divide_int,
    '%': token_type.t_op_modulo,
    '**': token_type.t_op_power,

    # Assignment
    '=': token_type.t_op_assign,
    '+=': token_type.t_op_plus_assign,
    '-=': token_type.t_op_minus_assign,
    '*=': token_type.t_op_multiply_assign,
    '/=': token_type.t_op_divide_assign,
    '//=': token_type.t_op_divide_assign_int,
    '%=': token_type.t_op_modulo_assign,
    '**=': token_type.t_op_power_assign,

    # Comparison
    '==': token_type.t_op_equal,
    '!=': token_type.t_op_not_equal,
    '<': token_type.t_op_lt,
    '>': token_type.t_op_gt,
    '<=': token_type.t_op_lte,
    '>=': token_type.t_op_gte,

    # Bitwise
    '&': token_type.t_op_bit_and,
    '|': token_type.t_op_bit_or,
    '^': token_type.t_op_bit_xor,
    '~': token_type.t_op_bit_not,
    '<<': token_type.t_op_lshift,
    '>>': token_type.t_op_rshift,
}

def check_if_operator(word) :

    if word in operators :
        return nemo_token( operators[word], word )
    else :
        return None


braces = {
    '(': token_type.t_open_paren,
    ')': token_type.t_close_paren,
    '{': token_type.t_open_curly,
    '}': token_type.t_close_curly
}

def check_if_brace(word) :
    if word in braces :
        return nemo_token( braces[word], word )
    else :
        return None