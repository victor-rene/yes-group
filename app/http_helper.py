import cookielib, urllib, urllib2, base64

opener = None

def auth(url, username, password):
  pwd_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
  pwd_mgr.add_password(None, url, username, password)
  authhandler = urllib2.HTTPBasicAuthHandler(pwd_mgr)
  cookies = cookielib.LWPCookieJar()
  handlers = [
    urllib2.HTTPHandler(debuglevel=1),
    # urllib2.HTTPSHandler(debuglevel=1), doesn't work on the VM
    urllib2.HTTPCookieProcessor(cookies),
    urllib2.HTTPBasicAuthHandler(pwd_mgr)
    ]
  global opener
  opener = urllib2.build_opener(*handlers)
  opener.addheaders = [('User-agent', 'Mozilla/5.0')]

def fetch(uri):
  f = opener.open(uri)
  data = f.read()
  f.close()
  return data
  
def fetch_auth_form(uri, form_data):
  params = urllib.urlencode(form_data)
  f = opener.open(uri, params)
  data = f.read()
  f.close()
  f = opener.open(uri)
  data = f.read()
  f.close()
  return data
  
def dump_cookies():
  for cookie in cookies:
    print cookie.name, cookie.value

def save_cookies():
  cookies.save('cookies.txt')
  
def load_cookies():
  cookies.load('cookies.txt')
  
# base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
# req = urllib2.Request(uri, data)
# req.add_header("Authorization", "Basic %s" % base64string)
# return opener.open(req)