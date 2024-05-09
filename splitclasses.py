import inspect
import main

clas = inspect.getmembers(main)
clas = [i for i in clas if inspect.isclass(i[1])][1:]
for name,_ in clas:
    # print('from main import *\n'+inspect.getsource(_))
    with open('province/'+_.classname[:-1]+'.py','w',encoding='utf-8') as f:
        f.write('from main import *\n'+inspect.getsource(_))