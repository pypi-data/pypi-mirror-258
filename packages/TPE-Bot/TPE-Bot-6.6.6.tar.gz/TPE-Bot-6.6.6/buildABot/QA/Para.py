
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Para_1a87196f1e8b4bf989552e38f3755cbb.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
