
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'WebApp_Learn_f3c12abd61dc480a9e60b3bd54094920.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
