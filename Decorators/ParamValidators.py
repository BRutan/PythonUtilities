############################
# ParamValidators.py
############################
# Description:
# * Parameter validations for functions.

from varname import varname

class ParamValidator:
    """
    * Execute multiple decorators on function.
    """
    def __init__(self, *args):
        """
        * Create new validation object.
        Inputs:
        * args: Expecting tuples of length 2 or 3 of form
        (ParamIndices, Decorator, ValPredicate) or (ParamIndices, Decorator).
        """
        if not all([True if isinstance(arg, tuple) and isinstance(arg[0], (list, int)) 
                    and isinstance(arg[1], function) and (len(arg) == 2 or isinstance(arg[2], function)) 
                    else False for arg in args]):
            raise Exception('args must be tuples with (ParamIndex, Decorator, ValPredicate or None).')
        self.__validators = args

    def __call__(self, *args):
        messages = []
        for validator in self.__validators:
            indices = [validator[0]] if isinstance(validator[0], int) else validator[0]
            for index in indices:
                messages.extend(validator[1](index,))

def IsNumeric(*args):
    """
    *
    """
    messages = []
    for num, arg in enumerate(args):
        if num in paramindices and not isinstance(arg, (int, float)):
            messages.append(num)
    return messages

def String(paramIndices, valindices, messages = []):
    pass

