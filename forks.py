# coding: utf-8

import pycurl
import urllib
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
  username = user['login']

  if string in username:
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

    email = '%s@gmail.com' % username

    c = pycurl.Curl()
    c.setopt(c.URL, 'https://github.com/join')
    c.setopt(pycurl.COOKIEFILE, filename)
    c.setopt(pycurl.COOKIEJAR, filename)
    data = {
      'utf8': '✓',
      'authenticity_token': csrf_value,
      'user[login]': username,
      'user[email]': email,
      'user[password]': 'secret',
      'source_label': 'Homepage Form',
    }
    c.setopt(pycurl.POSTFIELDS, urllib.urlencode(data))
    c.perform()
    c.close()

    print("Registered account %s" % username)

    buffer = StringIO()

    c = pycurl.Curl()
    c.setopt(c.URL, 'https://github.com/spasmilo/electrum')
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.setopt(pycurl.COOKIEFILE, filename)
    c.setopt(pycurl.COOKIEJAR, filename)
    c.perform()
    c.close()

    body = buffer.getvalue()

    try:
      parts = body.split('/spasmilo/electrum/fork"')
      second_part = parts[1]
      csrf_parts = second_part.split('<input name="authenticity_token" type="hidden" value="')
      quote_parts = csrf_parts[1].split('"')
      csrf_value = quote_parts[0]
    except:
      print "Failed to get CSRF token"
      print "502?"
      print sys.exc_info()
      print body
      raise

    buffer = StringIO()

    c = pycurl.Curl()
    c.setopt(c.URL, 'https://github.com/spasmilo/electrum/fork')
    c.setopt(pycurl.COOKIEFILE, filename)
    c.setopt(pycurl.COOKIEJAR, filename)
    data = {
      'utf8': '✓',
      'authenticity_token': csrf_value,
    }
    c.setopt(pycurl.POSTFIELDS, urllib.urlencode(data))
    c.perform()
    c.close()

    os.remove(filename)

    print("Forked spasmilo/electrum")
