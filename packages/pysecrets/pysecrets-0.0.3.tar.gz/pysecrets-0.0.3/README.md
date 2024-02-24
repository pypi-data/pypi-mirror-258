# PySecrets
The lightest weight package for loading secrets into a project via the `os.environ`.

## Setup
Easy install via pip
```bash
pip install pysecrets
```
The package requires you to have a file in your project directory that is called `.secrets`. This file will look like the following:
```
# passwords file

PASSWORD=hello
APIKEY=17886cd8-6d61-4c29-9482-c64fb995ea14
# comments must be on their own lines
```

## Example Usage
This is for your basic usage with a `.secrets` file.
```python
import os
from pysecrets import secrets

secrets()

print(os.environ['PASSWORD'])
```
If you have secrets for a different environment, simply
```python
...
secrets('.secrets_stage')
...
```
