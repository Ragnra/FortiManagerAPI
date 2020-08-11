from fmg_modules import *
from variables.creds import *
import json

x = FMGApi(ip=ip, user=user, passwd=passwd)

#y = x.get_fgt_info()
#print(y.text)


#y = x.create_adom(adom='myadom', adom_desc='test')
#print(y.text)

#y = x.del_adom(adom='myadom')
#print(y.text)

y = x.set_fw_address(adom='myadom', type='ipmask', name='test123', subnet='1.1.1.1/255.255.255.255')
print(y.text)
#
# y = x.get_fw_address()
# print(y.text)
#print(y.text['results'])
# p = json.loads(y.text)
#print(type(p))
# for i in p['result']:
#     for x in i['data']:
#         if 'subnet' in x:
#             print(x['name']+','+str(x['subnet'][0])+'/'+str(x['subnet'][1]))
#         if x['type'] == 1:
#             print(x['name']+ ','+ x['start-ip']+'-'+x['end-ip'])