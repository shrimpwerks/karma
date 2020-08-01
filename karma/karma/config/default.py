'''base set of configuration details'''

import os

DEBUG = True
LEDGER_ADDR = os.environ.get('HTTP_LEDGER')
DEFAULT_CURRENCY = "gbp"
