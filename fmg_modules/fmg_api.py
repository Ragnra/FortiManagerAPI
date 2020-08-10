import requests, json

class FMGApi:
    def __init__(self, ip, user, passwd, verify=False):
        #create login url through the jsonrpc api
        self.url = 'https://' + ip + '/jsonrpc'
        #establish a requests session
        self.s = requests.Session()
        #login_url for jsonrpc
        self.login_url = "/sys/login/user"
        #login payload for session token generation
        payload_login = {"method": "exec", "params": [{"data": {"user": user, "passwd": passwd}, "url": self.login_url}]}
        #headers
        self.headers = {'Content-Type': 'text/plain'}
        #convert payload to str
        payload_str = json.dumps(payload_login)
        #return value
        self.r = self.s.post(self.url, data=payload_str, headers=self.headers, verify=False)
        #print login status code
        login_response_json = json.loads(self.r.text.encode('utf8'))
        print('Login Code for FMG:', self.r.status_code)

        if self.r.status_code == 200:
            if login_response_json["session"]:
                self.session_key = login_response_json["session"]
            elif not x["session"]:
                print('no session key received, ensure user as rpc-read-write permissions and login creds are correct')
                exit(2)
        else:
            print('check L3 connectivity and https socket connectivity')
            exit(2)

####
    ###Code Block for methods that aren't directly called
    def rconvert(self, payload, *args):
        dict_array = [i for i in args]
        merged_dict = {}
        for d in dict_array:
            merged_dict.update(d)
        print(merged_dict)

        params = {"params":[]}
        params['params'].append(merged_dict)
        payload.update(params)
        payload_str = json.dumps(payload)
        print(payload_str)
        return payload_str

    def rget(self, uri=None, data=None):
        payload = {"session":self.session_key, "method":"get"}
        payload_str = self.rconvert(payload, uri)
        req = self.s.post(self.url, data=payload_str)
        return req

    def rexec(self, uri=None, data=None):
        payload = {"session":self.session_key, "method":"exec"}
        payload_str = self.rconvert(payload, uri, data)
        req = self.s.post(self.url, data=payload_str)
        return req

    def rset(self, uri=None, data=None):
        payload = {"session":self.session_key, "method":"set"}
        payload_str = self.rconvert(payload, uri, data)
        req = self.s.post(self.url, data=payload_str)
        return req

    def rdel(self, uri=None, data=None):
        payload = {"session":self.session_key, "method":"delete"}
        payload_str = self.rconvert(payload, uri, data)
        req = self.s.post(self.url, data=payload_str)
        return req
####
    ###Code block for methods that are directly called

    def get_fgt_info(self):
        uri = {"url":"/dvmdb/device"}
        r = self.rget(uri=uri)
        return r

    def get_fmg_info(self, option="member"):
        uri = {"url": "/cli/global/system/global"}
        data = {"option":option}
        r = self.rget(uri=uri, data=data)
        return r

    def discover_fgt_device(self, fgtip=None, fgtuser=None, fgtpasswd=None):
        #i use this to discover devices to populate variables to iterate over an array with the next add_fgt_device method
        uri = {"url":"/dvm/cmd/discover/device"}
        data = {"data":{"device":[{"ip":fgtip, "adm_usr":fgtuser, "adm_pass":fgtpasswd,}]}}
        r = self.rexec(uri=uri, data=data)
        return r

    def add_fgt_device(self, fgtip=None, fgtuser=None, fgtpasswd=None, fgtname=None, mgmt_mode="unreg", adom='root', platform='FortiGate-VM64', sn=None):
        #this iterates over variables discovered by discover_fgt_device (SN and platform) but you can manually populate them yourself
        uri ={"url": "/dvm/cmd/add/device"}
        data = {"data":{"adom":adom,"device":[{"ip":fgtip,"adm_usr":fgtuser,"platform_str":platform,"mgmt_mode":mgmt_mode,"adm_pass":fgtpasswd,"sn":sn}]}}
        r = self.rexec(self, uri=uri, data=data)
        return r

    def create_adom(self, adom='root', adom_desc='description'):
        uri = {"url":"/dvmdb/adom"}
        data = {"data":{"name":adom, "desc": adom_desc}}
        r = self.rset(uri=uri, data=data)
        return r

    def del_adom(self, adom=None):
        uri = {"url":"/dvmdb/adom/"+adom}
        r = self.rdel(uri=uri)
        return r

    def create_cli_script(self, adom='root', cli_script='config firewall address', script_name=None):
        uri = {"url": "/dvmdb/adom/"+adom+"/script"}
        data = {"data":[{"content":cli_script, "name":script_name}]}
        r = self.rset(uri=uri, data=data)
        return r

    def execute_cli_script(self, adom='root', package='default', script_name=None):
        uri = {"url": "/dvmdb/adom/"+adom+"/script/execute"}
        data = {"adom":adom_name, "script":script_name, "package":package}
        r = self.rexec(uri=uri, data=data)
        return r

    def del_cli_script(self, adom='root', script_name=None):
        pass


