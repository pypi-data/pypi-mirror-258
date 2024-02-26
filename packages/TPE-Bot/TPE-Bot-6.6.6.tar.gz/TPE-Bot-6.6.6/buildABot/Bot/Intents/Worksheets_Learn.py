
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Worksheets_Learn_4a4cb0ba96f647f4b4457ecf05272b6d.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
