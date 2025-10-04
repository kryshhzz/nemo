
import inspect

nemo_line_no = 1

def next_line_no() :
    global nemo_line_no
    nemo_line_no += 1

def reset_line_no() :
    global nemo_line_no
    nemo_line_no = 1

def get_line_no():
    global nemo_line_no
    return nemo_line_no

def new_error(msg) :
    stack = inspect.stack()
    caller = stack[1]

    step = caller.filename.split('\\')
    step = step[-1][:-3]

    if step == 'transpiler' or step == 'interpreter' :
        raise SystemExit(f'nemoerror [{step}] : {msg}')

    raise SystemExit(f'nemoerror [{step}] : line {nemo_line_no} : {msg}')