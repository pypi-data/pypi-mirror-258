
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'AccordionCard_a149708519524107a29724e5944f24c4.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
