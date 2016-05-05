# encoding=utf8
import urllib
import urllib2
import cookielib
import Image
import numpy as np
import pytesseract
import cStringIO

# 10次模拟登陆
for i in range(10):
    try:
        index_url = "http://gdou.com/"
        login_url = "http://gdou.com/sso/login_login.action"
        verify_url = 'http://gdou.com/sso/authimg'
        # 下面这段是关键了，将为urlib2.urlopen绑定cookies
        # MozillaCookieJar(也可以是 LWPCookieJar ，这里模拟火狐，所以用这个了) 提供可读写操作的cookie文件,存储cookie对象
        cookiejar = cookielib.MozillaCookieJar()
        # 将一个保存cookie对象，和一个HTTP的cookie的处理器绑定
        cookieSupport = urllib2.HTTPCookieProcessor(cookiejar)
        # 下面两行为了调试的
        httpHandler = urllib2.HTTPHandler(debuglevel=1)
        httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
        # 创建一个opener，将保存了cookie的http处理器，还有设置一个handler用于处理http的
        opener = urllib2.build_opener(cookieSupport, httpsHandler)
        # 将包含了cookie、http处理器、http的handler的资源和urllib2对象绑定在一起，安装opener,此后调用urlopen()时都会使用安装过的opener对象，
        urllib2.install_opener(opener)

        # 打开登陆页面, 以此来获取cookies   。  但是因为
        # 打开验证码页面就可以获取全部cookies了，所以可以直接跳过这一步。算是可有可无的
        urllib2.urlopen(index_url)
        ##打印cookies
        print    cookiejar
        ##先打开页面获取的cookie与  后打开验证码页面的cookie不同。



        # 提取验证码text(使用pytesseract自动提取或者手动输入验证码)
        file = urllib2.urlopen(verify_url)
        pic = file.read()
        path = "code.jpg"

        localpic = open(path, "wb")
        localpic.write(pic)
        localpic.close()
        print "please  %s,open code.jpg" % path
        # code =raw_input("input code :")
        im = Image.open(path)
        code = pytesseract.image_to_string(im)

        # pix = np.asarray(im)
        # print pix.shape
        # pix = pix.transpose(2,0,1)
        # print pix[0]
        # text =image_to_string(im)
        print code

        # 模拟登陆
        form = {'loginId': 'wjd15', 'passwd': '1111', 'authCode': code}
        form_data = urllib.urlencode(form)
        request = urllib2.Request(login_url, form_data)
        response = urllib2.urlopen(request)
        print response.read()
    except:
        print 'exception!'
