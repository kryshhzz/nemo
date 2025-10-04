from .ipr import *

def yell(args):
    for arg in args :
        print(arg, end=' ')
    print()

def yellc(args) :
    for arg in args :
        print(arg, end=' ')

def ask(args) :
    val = input(*args)
    return val


ipr.func_to_func = {
    'yell' : yell,
    'yellc' : yellc,
    'ask' : ask,
}

ipr.func_can_return = {
    'ask'
}