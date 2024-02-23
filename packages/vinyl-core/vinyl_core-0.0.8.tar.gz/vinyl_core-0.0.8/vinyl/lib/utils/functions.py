import os
from functools import wraps

from pydantic import validate_call

validate = validate_call(
    validate_return=False, config={"arbitrary_types_allowed": True}
)


def with_modified_env(var_name, new_value):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Save the original value of the environment variable (if it exists)
            original_value = os.environ.get(var_name, None)

            # Set the new value for the environment variable
            os.environ[var_name] = new_value

            try:
                # Call the actual function
                result = func(*args, **kwargs)
            finally:
                # Restore the original value of the environment variable
                if original_value is not None:
                    os.environ[var_name] = original_value
                else:
                    # The environment variable was not set before, so remove it
                    del os.environ[var_name]

            return result

        return wrapper

    return decorator
