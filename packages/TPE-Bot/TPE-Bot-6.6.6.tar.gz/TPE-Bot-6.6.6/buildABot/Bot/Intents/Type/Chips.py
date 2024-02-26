
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Chips_9521d133ba8b4cc58d6a862aa86794dd.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
