import re

import rsa

import time

import json

import base64

import logging

import binascii

import requests

import urllib.parse






class WeiBoLogin(object):

    """

    class of WeiBoLogin, to login weibo.com

    """


    def __init__(self):

        """

        constructor

        """

        self.user_name = None

        self.pass_word = None

        self.user_uniqueid = None

        self.user_nick = None



        self.session = requests.Session()

        self.session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"})

        self.session.get("http://weibo.com/login.php")

        return



    def login(self, user_name, pass_word):

        """

        login weibo.com, return True or False

        """

        self.user_name = user_name

        self.pass_word = pass_word

        self.user_uniqueid = None

        self.user_nick = None



        # get json data

        s_user_name = self.get_username()

        json_data = self.get_json_data(su_value=s_user_name)

        if not json_data:

            return False

        s_pass_word = self.get_password(json_data["servertime"], json_data["nonce"], json_data["pubkey"])



        # make post_data

        post_data = {

            "entry": "weibo",

            "gateway": "1",

            "from": "",

            "savestate": "7",

            "userticket": "1",

            "vsnf": "1",

            "service": "miniblog",

            "encoding": "UTF-8",

            "pwencode": "rsa2",

            "sr": "1280*800",

            "prelt": "529",

            "url": "http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",

            "rsakv": json_data["rsakv"],

            "servertime": json_data["servertime"],

            "nonce": json_data["nonce"],

            "su": s_user_name,

            "sp": s_pass_word,

            "returntype": "TEXT",

        }



        # get captcha code

        if json_data["showpin"] == 1:

            url = "http://login.sina.com.cn/cgi/pin.php?r=%d&s=0&p=%s" % (int(time.time()), json_data["pcid"])

            with open("captcha.jpeg", "wb") as file_out:

                file_out.write(self.session.get(url).content)

            code = input("请输入验证码:")

            post_data["pcid"] = json_data["pcid"]

            post_data["door"] = code



        # login weibo.com

        login_url_1 = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)&_=%d" % int(time.time())
        r = requests.get(login_url_1,data=post_data)
        r.encoding = r.apparent_encoding
        print(r.text)

        json_data_1 = self.session.post(login_url_1, data=post_data).json()
        print(json_data_1)

        if json_data_1["retcode"] == "0":

            params = {

                "callback": "sinaSSOController.callbackLoginStatus",

                "client": "ssologin.js(v1.4.18)",

                "ticket": json_data_1["ticket"],

                "ssosavestate": int(time.time()),

                "_": int(time.time()*1000),

            }

            response = self.session.get("https://passport.weibo.com/wbsso/login", params=params)

            json_data_2 = json.loads(re.search(r"\((?P<result>.*)\)", response.text).group("result"))

            

            if json_data_2["result"] is True:

                self.user_uniqueid = json_data_2["userinfo"]["uniqueid"]

                self.user_nick = json_data_2["userinfo"]["displayname"]
                print('1')
                # h = requests.get('http://login.sina.com.cn/signup/signin.php?entry=sso',data = json_data_2)
                # h.encoding = h.apparent_encoding
                # print(h.text)
                #print(requests.get('http://weibo.com/u/6197932220/home?topnav=1&wvr=6').text)

                logging.warning("WeiBoLogin succeed: %s", json_data_2)

            else:
                print('2')

                #logging.warning("WeiBoLogin failed: %s", json_data_2)

        else:
            print('3')

        #print(requests.get('http://weibo.com/6197932220/follow?rightmod=1&wvr=6').text)

            #logging.warning("WeiBoLogin failed: %s", json_data_1)

        url2 = 'http://weibo.com/u/6197932220/home'
        print(requests.get(url2).text)

        return True if self.user_uniqueid and self.user_nick else False



    def get_username(self):

        """

        get legal username

        """

        username_quote = urllib.parse.quote_plus(self.user_name)#username中可能会出现汉字，这个时候用quote函数就可以将汉字转化为url格式的编码方式

        username_base64 = base64.b64encode(username_quote.encode("utf-8"))#用encode将str类型转化为bytes类型

        return username_base64.decode("utf-8")



    def get_json_data(self, su_value):

        """

        get the value of "servertime", "nonce", "pubkey", "rsakv" and "showpin", etc

        """

        # params = {

        #     "entry": "weibo",

        #     "callback": "sinaSSOController.preloginCallBack",

        #     "rsakt": "mod",

        #     "checkpin": "1",

        #     "client": "ssologin.js(v1.4.18)",

        #     "su": su_value,

        #     "_": int(time.time()*1000),

        # }

        # try:

        #     response = self.session.get("http://login.sina.com.cn/sso/prelogin.php", params=params)

        #     json_data = json.loads(re.search(r"\((?P<data>.*)\)", response.text).group("data"))

        # except Exception as excep:

        #     json_data = {}

        #     logging.error("WeiBoLogin get_json_data error: %s", excep)



        # logging.debug("WeiBoLogin get_json_data: %s", json_data)

        # return json_data

        url = 'https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=MTMwNTEyNTYyNjI=&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_=1498013220473'
        data = requests.get(url).text
        p = re.compile('({.*})')
        try:
            json_data = p.search(data).group(1)
            data = json.loads(json_data)
            print("return json success")
            return data
        except:
            print('Get servertime error')
            return None



    def get_password(self, servertime, nonce, pubkey):

        """

        get legal password

        """

        string = (str(servertime) + "\t" + str(nonce) + "\n" + str(self.pass_word)).encode("utf-8")

        public_key = rsa.PublicKey(int(pubkey, 16), int("10001", 16))

        password = rsa.encrypt(string, public_key)

        password = binascii.b2a_hex(password)

        return password.decode()





if __name__ == "__main__":

    #logging.basicConfig(level=logging.DEBUG, format="%(asctime)s\t%(levelname)s\t%(message)s")

    weibo = WeiBoLogin()

    weibo.login("13051256262", "19941210songyue")

    # url = 'http://weibo.com/6197932220/follow?rightmod=1&wvr=6'
    # headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'}
    # print(requests.get(url,headers=headers).text)