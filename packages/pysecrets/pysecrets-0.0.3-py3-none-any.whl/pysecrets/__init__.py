from .main import load_secrets

def secrets(file: str = '.secrets'):
    main.load_secrets(file)
