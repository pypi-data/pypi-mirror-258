
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'WelcomeIntent_dc14bb760bb04989870f306421385ce0.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
