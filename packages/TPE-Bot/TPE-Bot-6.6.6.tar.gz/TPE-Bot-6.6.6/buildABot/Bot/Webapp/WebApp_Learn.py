
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'WebApp_Learn_99cce4f6331041e0a538b5ea32667f23.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
