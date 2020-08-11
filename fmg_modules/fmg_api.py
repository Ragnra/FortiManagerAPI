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
                try:
                    self.session_key = login_response_json["session"]
                except:
                    print('no session key received, ensure user as rpc-read-write permissions and login creds are correct')
                    raise AccountError
                    exit(2)
        else:
            print('check L3 connectivity and https socket connectivity')
            raise SocketError
            exit(2)

####
    ###Code Block for methods that aren't directly called
    def rconvert(self, payload, *args):
        '''
        :param payload: this will be presented by the calling method (rget, rset, rexec) and will look like "payload = {"session":self.session_key, "method":"get"}"
        :param args: this will be extra args, that include, uri and other options
        The function wil then iterate over the presented key word arguments and merge them into a format required for the API call
        :return: this will return the payload required by rget, rset, rexec and rdel as a string
        '''
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
        '''
        :param uri: presented by the calling method
        :param data: presented by the calling method, if required
        :return: returns the jsonrpc api response
        '''
        payload = {"session":self.session_key, "method":"get"}
        if data is not None:
            payload_str = self.rconvert(payload, uri, data)
        else:
            payload_str = self.rconvert(payload, uri)
        req = self.s.post(self.url, data=payload_str)
        return req

    def rexec(self, uri=None, data=None):
        '''
        :param uri: presented by the calling method
        :param data: presented by the calling method, if required
        :return: returns the jsonrpc api response
        '''
        payload = {"session":self.session_key, "method":"exec"}
        if data is not None:
            payload_str = self.rconvert(payload, uri, data)
        else:
            payload_str = self.rconvert(payload, uri)
        req = self.s.post(self.url, data=payload_str)
        return req

    def rset(self, uri=None, data=None):
        '''
        :param uri: presented by the calling method
        :param data: presented by the calling method, if required
        :return: returns the jsonrpc api response
        '''

        payload = {"session":self.session_key, "method":"set"}
        if data is not None:
            payload_str = self.rconvert(payload, uri, data)
        else:
            payload_str = self.rconvert(payload, uri)
        req = self.s.post(self.url, data=payload_str)
        return req

    def rdel(self, uri=None, data=None):
        '''
        :param uri: presented by the calling method
        :param data: presented by the calling method, if required
        :return: returns the jsonrpc api response
        '''
        payload = {"session":self.session_key, "method":"delete"}
        if data is not None:
            payload_str = self.rconvert(payload, uri, data)
        else:
            payload_str = self.rconvert(payload, uri)
        req = self.s.post(self.url, data=payload_str)
        return req

    def radd(self, uri=None, data=None):
        '''
        :param uri: presented by the calling method
        :param data: presented by the calling method, if required
        :return: returns the jsonrpc api response
        '''
        payload = {"session":self.session_key, "method":"add"}
        if data is not None:
            payload_str = self.rconvert(payload, uri, data)
        else:
            payload_str = self.rconvert(payload, uri)
        req = self.s.post(self.url, data=payload_str)
        return req
####
    ###Code block for methods that are directly called

##Device Info
    def get_fgt_info(self):
        uri = {"url":"/dvmdb/device"}
        r = self.rget(uri=uri)
        return r

    def get_fmg_info(self, option="member"):
        uri = {"url": "/cli/global/system/global"}
        data = {"option":option}
        r = self.rget(uri=uri, data=data)
        return r


##Device Adding
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

##ADOMS
    def create_adom(self, adom='root', adom_desc='description'):
        uri = {"url":"/dvmdb/adom"}
        data = {"data":{"name":adom, "desc": adom_desc}}
        r = self.rset(uri=uri, data=data)
        return r

    def del_adom(self, adom=None):
        uri = {"url":"/dvmdb/adom/"+adom}
        r = self.rdel(uri=uri)
        return r

##CLI Scripts
    def get_cli_script(self, adom='root', script_name=None):
        if script_name is not None:
            #IF script_name variable is set, grab only the specific script
            uri = {"url": "/dvmdb/adom/" + adom + "/script/"+script_name}
        else:
            #IF script_name variable is not set retrieve all scripts
            uri = {"url": "/dvmdb/adom/" + adom + "/script"}
        r = self.rget(uri=uri)
        return r
    
    def create_cli_script(self, adom='root', cli_script='config firewall address', script_name=None):
        #create a cli script
        uri = {"url": "/dvmdb/adom/"+adom+"/script"}
        data = {"data":[{"content":cli_script, "name":script_name}]}
        r = self.rset(uri=uri, data=data)
        return r

    def execute_cli_script(self, adom='root', package='default', script_name=None):
        #execute the cli script based off name
        if script_name is None:
            raise Exception('Provide script_name variable')
        uri = {"url": "/dvmdb/adom/"+adom+"/script/execute"}
        data = {"adom":adom_name, "script":script_name, "package":package}
        r = self.rexec(uri=uri, data=data)
        return r

    def del_cli_script(self, adom='root', script_name=None):
        if script_name is None:
            raise Exception('Provide script_name variable')
        uri = {"url": "/dvmdb/adom/" + adom + "/script/delete"}
        r = self.rdel(uri=uri)
        return r

    def set_custom_protocol_options(self):
        pass

    def get_fw_address(self, adom='root', name=None):
        if name is None:
            uri = {"url": "/pm/config/adom/" + adom + "/obj/firewall/address"}
            r = self.rget(uri=uri)
            return r
        else:
            uri = {"url":"/pm/config/adom/"+ adom + "/obj/firewall/address/"+name}
            r = self.rget(uri=uri, data=data)
            return r

    def set_fw_address(self, adom='root', type='ipmask', name=None, subnet=None):
        uri = {"url":"/pm/config/adom/"+adom+"/obj/firewall/address"}
        data = {"data": {"name":name, "type":type, "subnet":subnet}}
        r = self.rset(uri=uri, data=data)
        return r
        
    def del_fw_address(self):
        uri = {"url":"/pm/config/adom/"+adom+"/obj/firewall/address"}
        r = self.rdel(uri=uri)
        return r