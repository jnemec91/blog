import os

if os.getenv('ENVIRONMENT') == 'production':
    from .production import *
    print("Loaded production settings")
else:
    from .development import *
    print("Loaded development settings")
