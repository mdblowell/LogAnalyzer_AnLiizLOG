from pyflowchart import Flowchart

with open('AnLiizLOG_v2.py') as f:
    code = f.read()

fc = Flowchart.from_code(code)
print(fc.flowchart())