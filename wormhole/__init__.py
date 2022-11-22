# Check minimum python version
import sys
if not sys.version_info >= (3, 9):
    raise Exception("Python version must be 3.9 or greater to use Wormhole!")

from wormhole.version import __version__

# Setup Gevent Monkey Patching
try:
    from gevent import monkey
    monkey.patch_all()
except ModuleNotFoundError:
    print("Gevent is not installed. Ignoring Monkey Patch.")

from wormhole.core import *
