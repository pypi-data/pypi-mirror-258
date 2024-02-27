import os

from spectral_cli.abis.abis import load_abis

ABIS = load_abis()

if os.getenv('SPECTRAL_CLI_ENV') == 'test':
    print('loading TEST config')
    from spectral_cli.test_constants import *
elif os.getenv('SPECTRAL_CLI_ENV') == 'dev':
    print('loading DEV config')
    from spectral_cli.dev_constants import *
else:
    from spectral_cli.prod_constants import *

CONFIG_PATH = os.path.expanduser(f'~/.spectral/{CONFIG_FILE_NAME}')

os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
