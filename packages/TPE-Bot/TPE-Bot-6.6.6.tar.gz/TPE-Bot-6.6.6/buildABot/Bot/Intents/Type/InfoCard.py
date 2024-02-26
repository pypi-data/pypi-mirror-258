
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'InfoCard_54777dffa6ba47b4bd9c2cebfac4b39e.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
