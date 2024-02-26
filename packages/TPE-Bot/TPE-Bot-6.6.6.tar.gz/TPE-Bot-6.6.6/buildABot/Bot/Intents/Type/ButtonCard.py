
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'ButtonCard_071285fd813f4e849f28c5a8586f34d1.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
