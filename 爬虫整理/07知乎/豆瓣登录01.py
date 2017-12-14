import requests  
from bs4 import BeautifulSoup  
import urllib  
import re  
  
loginUrl = 'https://accounts.douban.com/login'  
formData={  
    "redir":"http://movie.douban.com/mine?status=collect",  
    "form_email":'1752685917@qq.com',  
    "form_password":'19941210songyue',  
    "login":u'登录'  
}  
headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}  
r = requests.post(loginUrl,data=formData,headers=headers)  
page = r.text  


'''''获取验证码图片'''  
#利用bs4获取captcha地址  
soup = BeautifulSoup(page,"html.parser")  

if soup.find('img',id='captcha_image'):
    captchaAddr = soup.find('img',id='captcha_image')['src']  
    #利用正则表达式获取captcha的ID  
    reCaptchaID = r'<input type="hidden" name="captcha-id" value="(.*?)"/'  
    captchaID = re.findall(reCaptchaID,page)  
    #print captchaID  
    #保存到本地  
    with open('1.jpg','wb') as f:
        f.write(requests.get(captchaAddr).content)
    captcha = input('请输入验证码：')  
    print(captcha)
      
    formData['captcha-solution'] = captcha  
    formData['captcha-id'] = captchaID  

r = requests.post(loginUrl,data=formData,headers=headers)  
page = r.text  
print(r.url)
if r.url=='https://movie.douban.com/mine?status=collect':  
    print('Login successfully!!!')  
    print ('我看过的电影','-'*60)  
    #获取看过的电影  
    soup = BeautifulSoup(page,"html.parser")  
    result = soup.findAll('li',attrs={"class":"title"})  
    print('success')
    #print result  

else:  
    print ("failed!")