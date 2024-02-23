import requests

def login(loginName:str,password:str,domain:str="qdzx"):
    url = "https://account-wan.yunxiao.com/"
    data = {"loginName":loginName,"password":password,'domain':domain,'captchaValue':'','rememberMe':'false','service':'http://'+domain+'.idsp.yunxiao.com/Portal/LayoutD/CasLogin.aspx?ax'}
    res = requests.post(url=url,data=data)
    #print(res.status_code)
    #print(res.json())
    if res.status_code == 200:
        res1 = requests.get(url=res.json()['service'])
        data = res1.text
        data = data[:data.find("</a>")]
        data = data[data.rfind(">")+1:].replace(' ','').replace('\n','').replace('\r','')
        #print(data,len(data))
        #print(res1.text)
        return data
    elif res.status_code == 400:
        return False

if __name__=='__main__':
    print(login(str(input('输入爱云校账号：')),str(input('输入爱云校密码：'))))
