
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'FAQ_7aaa3adeefb64f48b150ba1fa4492aa8.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
