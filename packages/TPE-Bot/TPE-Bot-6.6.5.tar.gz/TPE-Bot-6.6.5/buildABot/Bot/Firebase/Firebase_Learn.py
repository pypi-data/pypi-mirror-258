
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Firebase_Learn_be84f0d54255469a84243fa7789ddb78.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
