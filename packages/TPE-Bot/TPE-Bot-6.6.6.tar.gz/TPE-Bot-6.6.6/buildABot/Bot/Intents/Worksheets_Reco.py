
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Worksheets_Reco_6ee900ee551442d3ad3a663021f93fe8.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
