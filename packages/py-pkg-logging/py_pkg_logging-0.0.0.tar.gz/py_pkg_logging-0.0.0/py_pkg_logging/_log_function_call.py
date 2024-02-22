
import ABCParse
import inspect
from functools import wraps
import logging


from typing import Callable



class FunctionCallLogger(ABCParse.ABCParse):
    def __init__(self):
        """"""
        self.__parse__(locals())
        
    @property
    def arg_names(self):
        return inspect.getfullargspec(self._func).args

    @property
    def arg_values(self):
        return self._args

    @property
    def cls_method(self):
        return "self" in self.all_args

    @property
    def func_name(self):
        if self.cls_method:
            cls = self.all_args.pop("self").__class__.__name__
            return f"{cls}.{self._func.__name__}"
        return self._func.__name__
    
    @property
    def _arg_message(self):
        return_str = ""
        for key, val in self.all_args.items():
            return_str += f"{key}={val}, "
        return return_str[:-2] # rm final comma
    
    @property
    def log_message(self):
        return print(f"Called: {self.func_name} with args: {self._arg_message}")


    def __call__(self, func, *args, **kwargs):
        
        self.__update__(locals())
        
        self.all_args = dict(zip(self.arg_names, self.arg_values))
        self.all_args.update(kwargs.items())
        
        logger.debug(self.log_message)


def log_function_call(func: Callable, *args, **kwargs):
    
    """
    Args:
        func (Callable)
        
        
    Example:

        ```python

        class MyClass:
            def __init__(self, *args, **kwargs):
                """"""
            @log_function_call
            def special_func(self, a: float, b: float):
                return a + b

        my_cls = MyClass()
        my_cls.special_func(2, 4)
        ```
        >>> Called: MyClass.special_func with args: a=2, b=4
        >>> 6
        """

    @wraps(func)
    def wrapper(*args, **kwargs):
        function_call_logger = FunctionCallLogger()
        function_call_logger(func, *args, **kwargs)
        return func(*args, **kwargs)

    return wrapper
