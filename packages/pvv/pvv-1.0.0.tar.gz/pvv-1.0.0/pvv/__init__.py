import inspect
from typing import Any, Callable

from coco_models.exceptions import ValidatorError

from .exceptions import ValidatorError


def _annotation_to_string(annotation: Any) -> str:
    """Convert annotation to string representation"""
    return inspect.formatannotation(annotation)


def _get_annotations(func: Callable, decorator_args: tuple) -> tuple:
    """Extract parameter annotations

    It validates whether the annotations can be used with isinstance

    Args:
        func (Callable): function to extract annotations from
        decorator_args (tuple): names of funcions parameters to be validated,
            if empty all parameters will be checked

    Raises:
        ValidatorError: if parameters are not present in function deffinition or their
            type annotations cannot be used with isinstance
    """
    annotations = []
    signature = inspect.signature(func)
    function_parameters = tuple(signature.parameters.keys())
    decorator_args = decorator_args if decorator_args else function_parameters

    args_not_present = set(decorator_args) - set(signature.parameters.keys())
    if args_not_present:
        error_message = (
            "Parameter"
            + ("s " if len(args_not_present) > 1 else " ")
            + ", ".join([f'"{item}"' for item in args_not_present])
            + (" are" if len(args_not_present) > 1 else " is")
            + " not present in function definition"
        )
        raise ValidatorError(error_message)

    for arg in decorator_args:
        annotation = signature.parameters[arg].annotation

        # we check if it can be used with isinstance
        try:
            isinstance(0, annotation)
            annotations.append((arg, annotation))
        except TypeError:
            error_message = (
                f"The annotated type {_annotation_to_string(annotation)} of "
                + f'parameter "{arg}" cannot be used with class and '
                + "instance checks (isinstance)"
            )
            raise ValidatorError(error_message)

    return tuple(annotations)


def _validate_arguments(func: Callable, annotations: list):
    """Validate function arguments against annotations

    Args:
        func (Callable): function to validate arguments for
        annotations (list): tuples containing parameter names and their annotations

    Raises:
        TypeError: if one or more function arguments do not match their annotations

    Returns:
        Callable: the wrapped function
    """
    signature = inspect.signature(func)

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        bound_arguments = signature.bind(*args, **kwargs)
        bound_arguments.apply_defaults()
        bound_arguments.arguments.items()

        # check type annotations
        wrong_types = []
        for name, annotation in annotations:
            if not isinstance(bound_arguments.arguments[name], annotation):
                wrong_types.append((name, _annotation_to_string(annotation)))

        if wrong_types:
            error_message = (
                "Incorrect type of function argument"
                + ("s: " if len(wrong_types) > 1 else ": ")
                + ", ".join(
                    [
                        f'"{name}" must be of type {annotation_str}'
                        for name, annotation_str in wrong_types
                    ]
                )
            )
            raise TypeError(error_message)

        return func(*args, **kwargs)

    return wrapper


def validate(*args: str):
    """Validate function parameters

    This decorator is used to enforce validation of a function's type hints

    Note:
        This function only works with type hints that can be checked using the built-in
        isinstance method. It will not work with

    Args:
        *args (str): names of functions parameters to be validated

    Raises:
        TypeError: when one or more of the type validations fail
            (will also notify of the parameters with incorrect types)
        ValidatorError: when the decorator has incorrect parameters
            (all parameters must be of type string)
    """

    def _validate(func: Callable) -> Callable:
        # we will check beforehand that we can use isinstance with all the type
        # annotations
        annotations = _get_annotations(func, decorator_args)
        return _validate_arguments(func, annotations)

    # make this decorator callable with or without parameters,
    # i.e., @validate, @validate() or @validate('param1', 'param2', ...)
    if len(args) == 1 and callable(args[0]):
        # no decorator arguments, we set decorator arguments to an empty tuple
        decorator_args = ()
        return _validate(args[0])
    else:
        # has decorator, we check all parameters are of type string
        if not all(isinstance(item, str) for item in args):
            raise ValidatorError("All arguments of decorator must be of type 'str'")
        decorator_args = args
        return _validate
