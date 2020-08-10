from fmg_modules import *
#from fmg_api_testing.fmg_modules import fmg_api
#def variables
ip='192.168.3.182'
user='admin'
passwd='P@ssw0rd'
#


# token = fmg_api_token_login(ip=ip, user=user, passwd=passwd)
# print(token)

x = FMGApi(ip=ip, user=user, passwd=passwd)

y = x.get_fgt_info()
print(y.text)
#y = x.discover_fgt_device(fgtip='192.168.3.181',fgtuser='admin',fgtpasswd='P@ssw0rd')
#print(y.text)

y = x.create_adom(adom='myadom', adom_desc='test')
print(y.text)
#

# def rconvert(self, payload, uri):
#   params = {"params": [{"url": uri, }], }
#   payload.update(params)
#   payload_str = json.dumps(payload)
#   return payload_str