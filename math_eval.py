from __future__ import division

import ast
import math

def decimal_log(num, base=10):
    return math.log(num, base)

def smart_round(math_function):

    def decorator(num, *args, **kwargs):

        return round(math_function(num, *args, **kwargs), 15)

    return decorator

locals = {key: value for (key, value) in vars(math).items() if key[0] != '_'}
locals.update({"abs": abs, "complex": complex, "min": min,
               "max": max, "pow": pow, "round": smart_round, 
               "log": decimal_log, "sin": smart_round(math.sin),
               "cos": smart_round(math.cos),"ln": math.log})

class ExpressionException(Exception):
    pass

class Visitor(ast.NodeVisitor):


    def visit(self, node):

        if not isinstance(node, self.whitelist):
            raise ValueError(node)
        return super(Visitor, self).visit(node)

    whitelist = (ast.Module, ast.Expr, ast.Load, ast.Expression, ast.Add, ast.Sub, ast.UnaryOp, ast.Num, ast.BinOp,
            ast.Mult, ast.Div, ast.Pow, ast.BitOr, ast.BitAnd, ast.BitXor, ast.USub, ast.UAdd, ast.FloorDiv, ast.Mod,
            ast.LShift, ast.RShift, ast.Invert, ast.Call, ast.Name)



def parse_expression(expression):

    return expression.replace('^', '**')

def evaluate(expression, locals=locals):

    parsed_expression = parse_expression(expression)
    node = ast.parse(parsed_expression, mode='eval')
    Visitor().visit(node)
    try:
        return eval(compile(node, "<string>", "eval"), {'__builtins__': None}, locals)
    except Exception as e:
        raise ExpressionException(e)
