
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'QAManager_8beb0c8c0e434ae982985e8ea80706e4.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
