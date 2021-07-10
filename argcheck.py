from exceptions import (InvalidArguement)


def argcheck(func):
    def func_wrapper(*args, **kwargs):
        """
        Validation of arguements
        """
        for key, value in kwargs.items():
            """
            Api key validation which can be fetched from database
            """
            if (key == 'api_key' and value != 'HcyKuwNhuwfd'):
                raise InvalidArguement('Invalid api key')
            """
            Token validation which can be fetched from cache storages
            by storing it when users login
            """
            if (key == 'token' and
                  value != 'SCT3kRCwOhjUmQT6GfhXSKstynoQFK27'):
                raise InvalidArguement('Invalid token')
    return func_wrapper
