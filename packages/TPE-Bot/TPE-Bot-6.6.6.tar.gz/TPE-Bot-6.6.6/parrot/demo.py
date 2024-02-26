
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'demo_7e2dfc613d43436db0f936dbcc473cc1.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
