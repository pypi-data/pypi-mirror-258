
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'ListCard_0bd472ec0e2d47fb9ec31563e825bd3e.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
