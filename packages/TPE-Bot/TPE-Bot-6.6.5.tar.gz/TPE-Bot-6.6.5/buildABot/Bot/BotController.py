
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'BotController_3cbdea12e6504bcd8aebed6a99a47f95.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
