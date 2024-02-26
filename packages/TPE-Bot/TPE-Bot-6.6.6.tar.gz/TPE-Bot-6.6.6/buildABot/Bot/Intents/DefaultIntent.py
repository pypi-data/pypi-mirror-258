
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'DefaultIntent_a3b19159fcb74a1789923ad5fda63b55.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
