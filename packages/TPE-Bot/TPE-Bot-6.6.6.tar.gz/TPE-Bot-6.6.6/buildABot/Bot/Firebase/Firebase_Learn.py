
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Firebase_Learn_c1b73e96fa18457ea608b4725f3b53b5.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
