import inspect


# Dynamically wrap inherited methods by default to ensure output is of same class rather than parent class
# Note: ensure_output must be defined in the class
def wrap_inherited_methods(wrapper_func_str="ensure_output", **wrapper_args):
    def class_decorator(cls):
        # Retrieve the wrapper function from the class (or its module)
        wrapper_func = (
            getattr(cls, wrapper_func_str, None) or globals()[wrapper_func_str]
        )

        for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
            # Check if the method is defined in the parent class and not in the current class
            if method.__qualname__.split(".")[0] != cls.__name__:
                # Apply the wrapper with arguments, then apply the resulting decorator to the method
                decorated_method = wrapper_func(**wrapper_args)(method)
                setattr(cls, name, decorated_method)
        return cls  # Return the modified class

    return class_decorator


def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False
