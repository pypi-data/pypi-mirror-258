
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'RelatedIntents_7af0493e8aad456f9841cdd59c952dc6.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
