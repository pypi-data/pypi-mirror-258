
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'DefaultIntent_825d82cbf09c44e8a4bdcfc006602758.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
