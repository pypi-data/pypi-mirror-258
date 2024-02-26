
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Worksheets_Reco_53caf5173ef448c1996556a94e0f107b.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
