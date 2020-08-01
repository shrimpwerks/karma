'''
temporary entry point for the slack karma api.
'''

import signal
import sys

from karma import create_app


def signal_handler(sig, frame):
    '''SIGINT received, halting report polling daemon.'''

    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

app = create_app()

if __name__ == "__main__":
    app.run()
