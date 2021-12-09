from my_quickbase import logger


# Helper Funcs and Exceptions
class AttrNotSet(NotImplementedError):
    pass


class TokenAndRealmNotSet(NameError):
    pass


def parse_response(response):
    """Grabs JSON from requests response object"""
    try:
        parsed_response = response.json()
        if not parsed_response:
            raise AttributeError("JSON response empty")
    except AttributeError as e:
        logger.warning(f'{response} produced error:\n{e}', exc_info=False)
    else:
        return parsed_response


# Helper Class Decorators
def check_attr_exists(attr_to_check):
    """ Prevents methods from being called unless particular attribute is passed in as parameter to class decorator """
    # Class Decorator
    def class_decorator(cls):
        # Method Decorator
        def method_decorator(method):
            def check_attr_and_run_func(self, *args, **kwargs):
                if getattr(self, attr_to_check) is None:
                    raise AttrNotSet(f"{cls.__name__} must first set {attr_to_check} attribute")
                return method(self, *args, **kwargs)
            return check_attr_and_run_func

        # List of all class methods that are a) not dunder methods b) not a get_{missing attribute} method
        method_lst = [func for func in dir(cls)
                      if callable(getattr(cls, func))
                      and not func.startswith('_')
                      and func != f'get_{attr_to_check}']

        # Class decorator iterates through instance methods, applying method decorator to each method:
        for method_name in method_lst:
            setattr(cls, method_name, method_decorator(getattr(cls, method_name)))
        return cls
    return class_decorator
