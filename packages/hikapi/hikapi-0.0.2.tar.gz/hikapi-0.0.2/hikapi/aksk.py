__all__=["aksk"]

import copy,time,hashlib,hmac,base64,urllib,requests,json,ssl

class aksk(object):

    def __init__(self,appKey,appSecret,server):
        self.请求头={
            "Method":"GET",
            "Accept":"*/*",
#            "Content-MD5":"",
            "Content-Type":"application/json",
#            "Date":"",
        }
        self.appKey=appKey
        self.appSecret=appSecret
        self.access_token=""
        self.server=server

    def aksk(self,方法,url,原始请求头):
        请求头=copy.deepcopy(原始请求头)
#        请求头["Date"]=time.strftime('%a, %d %b %Y %H:%M:%S GMT')
        请求头["Method"]=方法
        请求头["X-Ca-Key"]=self.appKey
        请求头["X-Ca-Timestamp"]="%d" %(time.time())
        请求头["X-Ca-Signature-Headers"]="x-ca-key,x-ca-timestamp"
#        签名字符串="{Method}\n{Accept}\n{Content-Type}\n{Date}\nx-ca-timestamp:{X-Ca-Timestamp}\n".format(**请求头) +url
        签名字符串="{Method}\n{Accept}\n{Content-Type}\nx-ca-key:{X-Ca-Key}\nx-ca-timestamp:{X-Ca-Timestamp}\n".format(**请求头) +url
        请求头["X-Ca-Signature"]=base64.b64encode(hmac.new(self.appSecret.encode("utf8"),签名字符串.encode("utf8"),digestmod=hashlib.sha256).digest()).decode("utf8")
        return 请求头

    def connect(self):
        请求头=self.aksk("POST","/artemis/api/v1/oauth/token",self.请求头)
        结果=self.post("/api/v1/oauth/token",{},请求头)
        if 结果["code"]=="0":
            self.access_token=结果["data"]["access_token"]
            self.过期时间=time.time()+int(结果["data"]["expires_in"])
            return True
        else:
            print(结果)

    def post(self,url,数据={},原始请求头={}):
        请求头=copy.deepcopy(self.请求头)
        for k in 原始请求头:
            if k not in 请求头:
                请求头[k]=原始请求头[k]
        if self.access_token:
            请求头["access_token"]=self.access_token
        url=f"https://{self.server}/artemis"+urllib.parse.quote(url)
        data=json.dumps(数据,ensure_ascii=False,skipkeys=False).encode("utf8")
        req =  urllib.request.Request(url,data=data,headers=请求头,method='POST')
        res_data = urllib.request.urlopen(req,context=ssl._create_unverified_context())
        res = res_data.read()
        结果=json.loads(res.decode("utf8"))
        return 结果
