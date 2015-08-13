#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import commands
import requests
import filecmp
import urllib2

from bs4 import BeautifulSoup
from slacker import Slacker
from selenium import webdriver


USERNAME = "<script>alart(1)</script>"

def slack_message_test(text,username=USERNAME):
  with open("credentials/slack_api_key", "r") as f:
    api_key = f.read()
    slack = Slacker(api_key)
#    text = "test"
    # Send a message to #general channel
    slack.chat.post_message(channel='#detect_log', username=username, text=text)

def web_cloning():
  check_page = requests.get(sys.argv[1])
  
  check_file_date = open('./check_file/check_web_page_date.txt','w')  
  check_file_date.write(check_page.headers['last-modified'])
  check_file_date.close()

  #webページのパーサでブラックリストを取得
  html = urllib2.urlopen(sys.argv[1])
  soup = BeautifulSoup(html, "html.parser")
  iframe = soup.find_all("iframe")
  
  check_file_source = open('./check_file/check_web_page_source.txt','w')
  for tag in iframe:
    check_file_source.write(str(tag))  
  check_file_source.close()
  
def check_web_page():
  
  diff_date = filecmp.cmp('./check_file/check_web_page_date.txt', './default_file/default_web_page_date.txt')
  diff_source = filecmp.cmp('./check_file/check_web_page_source.txt', './default_file/default_web_page_source.txt')
  if diff_date == False & diff_source == False:
    text = "MODIFY_2"
    slack_message_test(text)
  elif diff_date == False & diff_source == True:
    text = "UPDATE_2"
    slack_message_test(text)
  else:
    print "not update"

    
if __name__ == "__main__":
  if len(sys.argv) != 2:
    print "Usage: "+sys.argv[0]+" TARGET_URL"
    exit()
    
  web_cloning()
  check_web_page()  
