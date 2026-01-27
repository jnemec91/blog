import os

if os.environ.get('ENVIRONMENT') == 'production':
    from .production import *
    print("Loaded production settings")
else:
    from .development import *
    print("Loaded development settings")
