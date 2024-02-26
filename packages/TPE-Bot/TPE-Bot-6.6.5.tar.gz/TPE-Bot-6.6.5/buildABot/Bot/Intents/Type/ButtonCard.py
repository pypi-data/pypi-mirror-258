
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'ButtonCard_ba5be339f81742879fe15532a00d102b.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
