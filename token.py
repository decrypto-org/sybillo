def github_token_get(rep, action):
  import pycurl
  import random

  from StringIO import StringIO

  buffer = StringIO()

  rand = random.randint(0, 2**30)
  filename = "data%i.cookie" % rand

  action_page = {
     'login': 'la',
     'watch': rep
  }
  actions = {
    'watch': 'notifications/subscribe',
    'login': ''
  }
  url = 'https://github.com/' + action_page[action]
  print url
  c = pycurl.Curl()
  c.setopt(c.URL, url)
  c.setopt(c.WRITEFUNCTION, buffer.write)
  c.setopt(pycurl.COOKIEJAR, filename)
  c.perform()
  c.close()

  body = buffer.getvalue()

  try:
    print body.find_element_by_name( 'authenticity_token')
  except:
    print "502?"
    print 'Failed to get token'
    raise

  print csrf_value
  pass

github_token_get( 'dionyziz/endofcodes/', 'login' )
