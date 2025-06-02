# Task 1: Writing and Testing a Decorator
import functools
import logging

# One-time logger setup
logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
if not logger.handlers:  # Prevent adding multiple handlers if module is reloaded
    logger.addHandler(logging.FileHandler("./decorator.log", "a"))

def logger_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Prepare argument strings
        pos_args = list(args) if args else "none"
        kw_args = kwargs if kwargs else "none"

        # Call the original function
        result = func(*args, **kwargs)

        # Create the log message
        log_message = (
            f"function: {func.__name__}\n"
            f"positional parameters: {pos_args}\n"
            f"keyword parameters: {kw_args}\n"
            f"return: {result}\n"
        )

        # Write the log message
        logger.log(logging.INFO, log_message)

        return result
    return wrapper


@logger_decorator
def say_hello():
    print("Hello, World!")

@logger_decorator
def always_true(*args):
    return True

@logger_decorator
def return_decorator(**kwargs):
    return logger_decorator

say_hello()
always_true(1, 2, 3)
return_decorator(log_level="INFO", module="decorators")