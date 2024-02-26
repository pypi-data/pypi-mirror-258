
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'CustomResponse_eebdc34d355e4be39e28722088954747.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
