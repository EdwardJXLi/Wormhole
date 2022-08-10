# Setup Gevent Monkey Patching
try:
    from gevent import monkey
    monkey.patch_all()
except ModuleNotFoundError:
    print("Gevent is not installed. Ignoring Monkey Patch.")

from wormhole.core import *
