
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Paraphraser_6036ef0ca2194466bdce305d527c4413.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
