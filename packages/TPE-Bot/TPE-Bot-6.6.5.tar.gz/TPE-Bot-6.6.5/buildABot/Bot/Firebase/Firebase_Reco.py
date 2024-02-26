
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Firebase_Reco_10bb1dad46524e4f972d98b60b3f640a.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
