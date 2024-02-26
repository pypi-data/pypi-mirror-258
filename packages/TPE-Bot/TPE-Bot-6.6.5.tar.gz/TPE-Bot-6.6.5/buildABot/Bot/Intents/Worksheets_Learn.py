
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Worksheets_Learn_f9c871419d1e4ad3ba7587f5f1506dfc.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
