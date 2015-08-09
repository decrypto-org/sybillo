# coding: utf-8

import pycurl
import urllib
import urllib2
import random
import os
import sys
import json


from StringIO import StringIO

buffer = StringIO()

rand = random.randint(0, 2**30)
filename = "data%i.cookie" % rand

response = urllib.urlopen('https://api.github.com/repos/spasmilo/electrum/stargazers?per_page=100')
users = json.loads(response.read())

for user in users:
  c = pycurl.Curl()
  c.setopt(c.URL, 'https://github.com/')
  c.setopt(c.WRITEFUNCTION, buffer.write)
  c.setopt(pycurl.COOKIEJAR, filename)
  c.perform()
  c.close()

  body = buffer.getvalue()

  try:
    csrf_value = body.split('name="authenticity_token" type="hidden" value="')[1].split('"')[0]
  except:
    print "502?"
    print body
    raise

  buffer = StringIO()

  username = user['login']

  c = pycurl.Curl()
  c.setopt(c.URL, 'https://github.com/session')
  c.setopt(pycurl.COOKIEFILE, filename)
  c.setopt(pycurl.COOKIEJAR, filename)
  data = {
    'utf8': '✓',
    'authenticity_token': csrf_value,
    'login': username,
    'password': 'hello12345',
    'commit': 'Sign in',
  }
  c.setopt(pycurl.POSTFIELDS, urllib.urlencode(data))
  c.setopt(c.FOLLOWLOCATION, True)
  c.perform()
  c.close()

  print("Logged in account %s" % username)

  buffer = StringIO()

  c = pycurl.Curl()
  c.setopt(c.URL, 'https://github.com/spasmilo/electrum')
  c.setopt(c.WRITEFUNCTION, buffer.write)
  c.setopt(pycurl.COOKIEFILE, filename)
  c.setopt(pycurl.COOKIEJAR, filename)
  c.perform()
  c.close()

  body = buffer.getvalue()
  array = '{"fruits": ["apple", "banana", "orange"]}'
  data  = json.loads(array)
  print data['fruits']

  try:
    parts = body.split('/spasmilo/electrum/notifications/subscribe"')
    second_part = parts[0]
    csrf_parts = second_part.split('<input name="authenticity_token" type="hidden" value="')
    quote_parts = csrf_parts[1].split('"')
    csrf_value = quote_parts[0]
    print csrf_value
  except:
    print "Failed to get CSRF token for watching"
    print "502?"
    print sys.exc_info()
    print body
    raise

  buffer = StringIO()

  c = pycurl.Curl()
  c.setopt(c.URL, 'https://github.com/notifications/subscribe')
  c.setopt(pycurl.COOKIEFILE, filename)
  c.setopt(pycurl.COOKIEJAR, filename)
  data = {
    'utf8': '✓',
    'authenticity_token': csrf_value,
    'repository_id': '32502966',
    'do': 'subscribed',
  }
  c.setopt(c.FOLLOWLOCATION, True)
  c.setopt(pycurl.POSTFIELDS, urllib.urlencode(data))
  c.perform()
  c.close()

  os.remove(filename)

  print("Watched spasmilo/electrum")
