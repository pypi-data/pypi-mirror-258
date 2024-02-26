
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'WelcomeIntent_5b0fa5baa0a94564a864dd47e4e13e76.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
