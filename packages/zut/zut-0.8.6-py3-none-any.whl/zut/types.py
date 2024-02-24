from __future__ import annotations
from configparser import RawConfigParser
from decimal import Decimal
import inspect
import re
import sys
from typing import Any, Callable, Iterable, TypeVar, overload

if sys.version_info < (3, 8):
    from typing_extensions import Literal
else:
    from typing import Literal

T = TypeVar('T')


def get_iterable_element_type(iterable: Iterable, *possible_types: type) -> type|None:
    """
    Get the type of all elements of the iterable amongst the possible types given as argument.
    """
    if not possible_types:
        raise NotImplementedError() # TODO: requires more thinking
    
    remaining_types = list(possible_types)

    for element in iterable:
        types_to_remove = []

        for possible_type in remaining_types:
            if not issubclass(type(element), possible_type):
                types_to_remove.append(possible_type)

        for type_to_remove in types_to_remove:
            remaining_types.remove(type_to_remove)
    
    return remaining_types[0] if remaining_types else None


def is_iterable_of(iterable: Iterable, element_type: type|tuple[type]):
    for element in iterable:
        if not isinstance(element, element_type):
            return False
        
    return True


def get_leaf_classes(cls: type[T]) -> list[type[T]]:
    cls_list = []

    def recurse(cls: type):
        subclasses = cls.__subclasses__()
        if subclasses:
            for subcls in subclasses:
                recurse(subcls)
        else:
            cls_list.append(cls)

    recurse(cls)
    return cls_list


@overload
def convert(value: Any, to: type[T], *, nullval = None, if_none = None) -> T:
    ...


def convert(value: Any, to: type[T]|Callable, *, nullval = None, if_none = None):
    if value == nullval:
        return None
    
    if not isinstance(to, type):
        return to(value)
    
    if isinstance(value, to):
        return value
    
    if value is None:
        return if_none
    
    strvalue = str(value)

    if to == str:
        return strvalue
    
    elif to == bool:
        lower = strvalue.lower()
        if lower not in RawConfigParser.BOOLEAN_STATES:
            raise ValueError('Not a boolean: %s' % strvalue)
        return RawConfigParser.BOOLEAN_STATES[lower]

    elif to in [float,Decimal]:
        return to(strvalue.replace(',', '.'))
    
    elif to == list:
        strvalue = strvalue.strip()
        if not strvalue:
            return []
        return re.split(r'[\W,;|]+', strvalue)
    
    else:
        return to(strvalue)


def convert_to_bool(value: Any, *, nullval = None, if_none = None):
    return convert(value, bool, nullval=nullval, if_none=if_none)

def convert_to_int(value: Any, *, nullval = None, if_none = None):
    return convert(value, int, nullval=nullval, if_none=if_none)

def convert_to_decimal(value: Any, *, nullval = None, if_none = None):
    return convert(value, Decimal, nullval=nullval, if_none=if_none)


def convert_str_args(func: Callable, *args: str):
    if not args:
        return tuple(), dict()
    
    # Determine argument types
    signature = inspect.signature(func)
    var_positional_type = None
    var_keyword_type = None
    parameter_types = {}
    positional_types = []
    for parameter in signature.parameters.values():
        parameter_type = None if parameter.annotation is inspect.Parameter.empty else parameter.annotation
        if parameter.kind == inspect.Parameter.VAR_POSITIONAL:
            var_positional_type = parameter_type
        elif parameter.kind == inspect.Parameter.VAR_KEYWORD:
            var_keyword_type = parameter_type
        else:
            parameter_types[parameter.name] = parameter_type
            if parameter.kind in [inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD]:
                positional_types.append(parameter_type)
    
    # Distinguish args and kwargs
    positionnal_args = []
    keyword_args = {}
    for arg in args:
        m = re.match(r'^([a-z0-9_]+)=(.+)$', arg)
        if m:
            keyword_args[m[1]] = m[2]
        else:
            positionnal_args.append(arg)

    # Convert kwargs
    for parameter, value in keyword_args.items():
        if parameter in parameter_types:
            target_type = parameter_types[parameter]
            if target_type:
                keyword_args[parameter] = convert(value, target_type)

        elif var_keyword_type:
            keyword_args[parameter] = convert(value, var_keyword_type)

    # Convert args
    for i, value in enumerate(positionnal_args):
        if i < len(positional_types):
            target_type = positional_types[i]
            if target_type:
                positionnal_args[i] = convert(value, target_type)

        elif var_positional_type:
            positionnal_args[i] = convert(value, var_positional_type)

    return positionnal_args, keyword_args



__all__ = (
    'Literal', 'get_iterable_element_type', 'is_iterable_of', 'get_leaf_classes',
    'convert', 'convert_to_bool', 'convert_to_int', 'convert_to_decimal',
    'convert_str_args',
)
