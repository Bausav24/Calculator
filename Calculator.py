from collections import namedtuple
from pprint import pprint as pp
from unittest import result
import math
import re


OpInfo = namedtuple('OpInfo', 'prec assoc')
L, R = 'Left Right'.split()

ops = {
 '^': OpInfo(prec=4, assoc=R),
 '*': OpInfo(prec=3, assoc=L),
 '/': OpInfo(prec=3, assoc=L),
 '+': OpInfo(prec=2, assoc=L),
 '-': OpInfo(prec=2, assoc=L),
'sin': OpInfo(prec=4, assoc=R),
 'cos': OpInfo(prec=4, assoc=R),
  'tan': OpInfo(prec=4, assoc=R),
 'cot': OpInfo(prec=4, assoc=R),
  'ln': OpInfo(prec=4, assoc=R),
    'log10': OpInfo(prec=4, assoc=R),
 '(': OpInfo(prec=9, assoc=L),
 ')': OpInfo(prec=0, assoc=L),
 }

NUM, LPAREN, RPAREN = 'NUMBER ( )'.split()



def get_input(inp = None):
    'Inputs an expression and returns list of (TOKENTYPE, tokenvalue)'
    
    if inp is None:
        inp = input('expression: ')
    tokens = inp.strip().split()
    tokenvals = []
    for token in tokens:
        if token in ops:
            tokenvals.append((token, ops[token]))
        #elif token in (LPAREN, RPAREN):
        #    tokenvals.append((token, token))
        else:    
            tokenvals.append((NUM, token))
    return tokenvals

def shunting(tokenvals):
    outq, stack = [], []
    table = ['TOKEN,ACTION,RPN OUTPUT,OP STACK,NOTES'.split(',')]
    for token, val in tokenvals:
        note = action = ''
        if token is NUM:
            action = 'Add number to output'
            outq.append(val)
            table.append( (val, action, ' '.join(outq), ' '.join(s[0] for s in stack), note) )
        elif token in ops:
            t1, (p1, a1) = token, val
            v = t1
            note = 'Pop ops from stack to output' 
            while stack:
                t2, (p2, a2) = stack[-1]
                if (a1 == L and p1 <= p2) or (a1 == R and p1 < p2):
                    if t1 != RPAREN:
                        if t2 != LPAREN:
                            stack.pop()
                            action = '(Pop op)'
                            outq.append(t2)
                        else:    
                            break
                    else:        
                        if t2 != LPAREN:
                            stack.pop()
                            action = '(Pop op)'
                            outq.append(t2)
                        else:    
                            stack.pop()
                            action = '(Pop & discard "(")'
                            table.append( (v, action, ' '.join(outq), ' '.join(s[0] for s in stack), note) )
                            break
                    table.append( (v, action, ' '.join(outq), ' '.join(s[0] for s in stack), note) )
                    v = note = ''
                else:
                    note = ''
                    break
                note = '' 
            note = '' 
            if t1 != RPAREN:
                stack.append((token, val))
                action = 'Push op token to stack'
            else:
                action = 'Discard ")"'
            table.append( (v, action, ' '.join(outq), ' '.join(s[0] for s in stack), note) )
    note = 'Drain stack to output'
    while stack:
        v = ''
        t2, (p2, a2) = stack[-1]
        action = '(Pop op)'
        stack.pop()
        outq.append(t2)
        table.append( (v, action, ' '.join(outq), ' '.join(s[0] for s in stack), note) )
        v = note = ''
    return table

def evalRPN(tokens) -> int:
    try:
        list= ['sin','cos','cot','tan','ln','log10']
        stack = []
        for t in tokens:
            if t not in {"+", "-", "*", "/", "^"} and t not in list:
                stack.append(float(t) if '.' in str(t) else int(t))
            else:
                if t in list:
                    b = stack.pop()
                    if t == "sin": stack.append(math.sin(b))
                    elif t == "cos": stack.append(math.cos(b))
                    elif t == "tan": stack.append(math.tan(b))
                    elif t == "ln": stack.append(math.log(b))
                    elif t == "log10":stack.append(math.log10(b))
                    else: stack.append(1/math.tan(b))
                else:
                    b, a = stack.pop(), stack.pop()
                    if t == "+": stack.append(a + b)
                    elif t == "-": stack.append(a - b)
                    elif t == "*": stack.append(a * b)
                    elif t == "^": stack.append(pow(a,b))
                    else: stack.append(math.trunc(a / b))

        return stack[0]

    except:
        print("Math_Error")



if __name__ == '__main__':
    temp = ""
    while temp != "exit":
        print('\nWelcome to advanced calculator on  console!!')
        print('This calculator requires you to be cautious while inserting your math operators.')
        print('You need to add space after each operators as shown in the below line otherwise you will get error.')
        print('Example on how you should type the operators is given below--')
        print('-5.78 + -1 * ( 4 - 2.23 ) + sin ( 0 ) * cos ( 1 ) / ( 1 + tan ( 2 * ln ( -3 + 2 * ( 1.23 + 99.111 ) ) ) )\n')
        print("PRESS 'exit' to end the calculator program")
        #The equation in the book: -5.78 + -1 * ( 4 - 2.23 ) + sin ( 0 ) * cos ( 1 ) / ( 1 + tan ( 2 * ln ( -3 + 2 * ( 1.23 + 99.111 ) ) ) )
        infix = input('For infix expression: ')
        temp = infix
        if temp == "exit":
            pass
        else:
            rp = shunting(get_input(infix))[-1][2].split()
            print(rp)
            results = evalRPN(rp)
            print('\n The final output is: %r' %results)




