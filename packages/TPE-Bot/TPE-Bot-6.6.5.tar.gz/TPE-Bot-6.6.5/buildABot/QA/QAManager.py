
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'QAManager_70537a6f90a9455c89ef1b6b1432203b.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
