#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import win32clipboard
from urllib.request import Request, urlopen
import urllib.parse
import urllib.error

import json
import gzip

ULR_EVEPRAISAL = "https://evepraisal.com/appraisal.json?market=jita"
ULR_EVEPRAISAL2 = "https://evepraisal.com/appraisal.json?market=jita&persist=no&raw_textarea="


def get_items_name(clipboard):
	print (clipboard)
	if len(clipboard.split(b'\t'.decode()))>0:
		items = clipboard.split(b'\n'.decode())
		items_name = [x.split(b'\t'.decode())[0] for x in items]
		return items_name
	else:
		return []

def get_clipboard():
	win32clipboard.OpenClipboard()
	data = win32clipboard.GetClipboardData()
	win32clipboard.CloseClipboard()
	return data

def fetch_evepraisal(clipboard):
	headers = { 
		'User-Agent' : 'Mozilla', 
		'Content-type': 'application/x-www-form-urlencoded'
	}
	data = urllib.parse.urlencode({}).encode()
	req = urllib.request.Request(url="https://evepraisal.com/appraisal.json?market=jita&persist=no&raw_textarea="+urllib.parse.quote_plus(clipboard), headers=headers, method='POST')
	try:
		with urllib.request.urlopen(req) as response:
			try:
				return json.loads(response.read().decode())
			except:
				print ("Eve praisal: invalid input")
	except urllib.error.HTTPError as err:
		print (err)
	return None

def check():
	clipboard = get_clipboard()
	evepraisal = fetch_evepraisal(clipboard)
	totals = evepraisal["appraisal"]["totals"]

#check()
