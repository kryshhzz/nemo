
from enum import Enum, auto

class token_type(Enum) :

    # builtin funcs 
    t_print = auto()
    t_println = auto()
    t_input = auto()

    # macros
    t_macro = auto()
    t_use = auto()

    # conditions 
    t_if = auto()
    t_elif = auto()
    t_else = auto()

    # loop
    t_loop = auto()
    t_repeat = auto()
    t_break = auto()

    # variable name
    t_identifier = auto()

    # int literal
    t_number_literal = auto()

    # string literal
    t_string_literal = auto()

    # newline
    t_newline = auto()

    # comma
    t_comma = auto()

    # bools
    t_bool_literal = auto()

    # braces
    t_open_paren = auto()
    t_close_paren = auto()
    t_open_curly = auto()
    t_close_curly = auto()

    # Arithmetic operators
    t_op_plus = auto()       # +
    t_op_minus = auto()      # -
    t_op_multiply = auto()   # *
    t_op_divide = auto()     # /
    t_op_divide_int = auto() # //
    t_op_modulo = auto()     # %
    t_op_power = auto()      # **

    # Assignment operators
    t_op_assign = auto()     # =
    t_op_plus_assign = auto()    # +=
    t_op_minus_assign = auto()   # -=
    t_op_multiply_assign = auto()# *=
    t_op_divide_assign = auto()  # /=
    t_op_divide_assign_int = auto()  # /=
    t_op_modulo_assign = auto()  # %=
    t_op_power_assign = auto()   # **=

    # Comparison operators
    t_op_equal = auto()      # ==
    t_op_not_equal = auto()  # !=
    t_op_gt = auto()         # >
    t_op_lt = auto()         # <
    t_op_gte = auto()        # >=
    t_op_lte = auto()        # <=

    # Logical operators
    t_op_and = auto()        # and
    t_op_or = auto()         # or
    t_op_not = auto()        # not

    # Bitwise operators
    t_op_bit_and = auto()    # &
    t_op_bit_or = auto()     # |
    t_op_bit_xor = auto()    # ^
    t_op_bit_not = auto()    # ~
    t_op_lshift = auto()     # <<
    t_op_rshift = auto()     # >>

    @classmethod
    def is_builtin_func(self, token):
        return token in {self.t_print, self.t_println, self.t_input}

    @classmethod
    def is_arithmetic(cls, token):
        return token in {
            cls.t_op_plus, cls.t_op_minus, cls.t_op_multiply,
            cls.t_op_divide, cls.t_op_modulo, cls.t_op_power, cls.t_op_divide_int
        }

    @classmethod
    def is_assignment_op(cls, token):
        return token in {
            cls.t_op_assign, cls.t_op_plus_assign, cls.t_op_minus_assign,
            cls.t_op_multiply_assign, cls.t_op_divide_assign, cls.t_op_divide_assign_int,
            cls.t_op_modulo_assign, cls.t_op_power_assign
        }

    @classmethod
    def is_comparison_op(cls, token):
        return token in {
            cls.t_op_equal, cls.t_op_not_equal,
            cls.t_op_gt, cls.t_op_lt,
            cls.t_op_gte, cls.t_op_lte
        }

    @classmethod
    def is_logical_op(cls, token):
        return token in {
            cls.t_op_and, cls.t_op_or, cls.t_op_not
        }

    @classmethod
    def is_bitwise_op(cls, token):
        return token in {
            cls.t_op_bit_and, cls.t_op_bit_or, cls.t_op_bit_xor,
            cls.t_op_bit_not, cls.t_op_lshift, cls.t_op_rshift
        }

    @classmethod
    def is_operator(cls, token):
        return (
            cls.is_arithmetic(token)
            or cls.is_assignment_op(token)
            or cls.is_comparison_op(token)
            or cls.is_logical_op(token)
            or cls.is_bitwise_op(token)
        )
        
    @classmethod
    def is_unary_operator(self, token):
        return token in {self.t_op_plus, self.t_op_minus, self.t_op_not, self.t_op_bit_not}

    @classmethod
    def is_literal(self, token) :
        return token in {self.t_number_literal, self.t_string_literal, self.t_bool_literal}

    

class nemo_token :

    def __init__(self, t_type : token_type , t_value : any ) :
        self.type = t_type
        self.value = t_value 

    def __str__(self) :
        # return f'Nemo token : {self.type.name} -> {self.value} ' 
        return f'{self.value} ' 


    