from fmg_modules import *
from variables import *

x = FMGApi(ip=ip, user=user, passwd=passwd)

y = x.get_fgt_info()
print(y.text)


y = x.create_adom(adom='myadom', adom_desc='test')
print(y.text)

