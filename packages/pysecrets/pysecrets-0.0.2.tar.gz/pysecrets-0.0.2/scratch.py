import os
from src.pysecrets import secrets

secrets()

print(os.environ['APIKEY'])
