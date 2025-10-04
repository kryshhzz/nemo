import sys, time, subprocess
from parser import parser
from lexer import lexer
from interpreter import interpreter
from transpiler import transpiler

start = time.time()

file_name = sys.argv[1]

contents = open(file_name, 'r').read().strip()

# adding a new line for ; at the end
contents += '\n'

# lexing
nemo_tokens = lexer.lex(contents)
# for nt in nemo_tokens :
#     print(nt)

# parsing
nemo_ast = parser.parseit(nemo_tokens)

# transpiling 
# code = transpiler.transpileit(nemo_ast)
# exec(code)
# print(code)

# for na in nemo_ast.nodes :
#     print(na)

# interpreting 
interpreter.interpretit(nemo_ast)


end = time.time()
print(f'Time taken by nemo : {round(end - start, 5)} seconds')