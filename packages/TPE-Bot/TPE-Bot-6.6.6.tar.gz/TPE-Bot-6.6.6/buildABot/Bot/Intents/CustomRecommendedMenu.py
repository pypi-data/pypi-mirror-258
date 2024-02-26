
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'CustomRecommendedMenu_e007a9a455714c4da532338986346c2f.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
