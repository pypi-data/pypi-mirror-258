
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'CustomIntents_045a6e407ff04c96a041a9152efbc210.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
