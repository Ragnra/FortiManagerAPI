from fmg_modules import *
from variables import *
print(ip)

x = FMGApi(ip=ip, user=user, passwd=passwd)

y = x.get_fgt_info()
print(y.text)


y = x.create_adom(adom='myadom', adom_desc='test')
print(y.text)

y = x.del_adom(adom='myadom')
print(y.text)
