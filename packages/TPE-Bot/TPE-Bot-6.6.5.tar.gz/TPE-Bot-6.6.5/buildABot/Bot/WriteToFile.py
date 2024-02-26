
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'WriteToFile_7ff3d88040b24c1ca0bac6c2f30392b7.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
