import os

def read_from_env(variablename):
    try:
        return os.environ[variablename]
    except KeyError:
        raise Exception(f"Set the {variablename} environment variable")


if os.environ.get('DJANGO_ENV') == 'production':
    from .production import *
else:
    from .development import *