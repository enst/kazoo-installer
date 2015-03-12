#!/usr/bin/python

import urllib2
import httplib
import json
import os
import re

api_key=""
account_id=""
CONFIG=""
num_arr = []
action_type = "add"

def http_json_put(token, url, path, values):
	conn = httplib.HTTPConnection(url)
	if not token:
		headers = {"Content-type":"application/json"} #application/x-www-form-urlencoded
	else:
		headers = {"Content-type":"application/json", "X-Auth-Token":token}

	params = (values)
	conn.request("PUT", path, json.JSONEncoder().encode(params), headers)
	response = conn.getresponse()
	data = response.read()
	conn.close()
	return data

def http_json_del(token, url, path, values):
	print url,values
	conn = httplib.HTTPConnection(url)
	if not token:
		headers = {"Content-type":"application/json"} #application/x-www-form-urlencoded
	else:
		headers = {"Content-type":"application/json", "X-Auth-Token":token}

	params = (values)
	conn.request("DELETE", path, json.JSONEncoder().encode(params), headers)
	response = conn.getresponse()
	data = response.read()
	conn.close()
	return data


def get_auth_token(url, path, values):
	return http_json_put(None, url, path, values)	

def add_del_number(action_type, token, url, path, values):
	if action_type == "add":
		return http_json_put(token, url, path, values)
	elif action_type == "del":
		return http_json_del(token, url, path, values)

def activate_number(token, url, path, values):
	print "ready to activate number"
	return http_json_put(token, url, path, values)


def parse_config(file_name):
	global api_key
	global account_id
	global action_type
	global num_arr
	file = open(file_name)
	in_section = 0
	while 1:
		line = file.readline()
		if not line:
			break
		line.strip("\r\n")
		m = re.match(r'\[settings\]$', line)
		if m:
			in_section = 1
			continue


		m = re.match(r'\[number\]', line)
		if m:
			in_section = 2
			continue
		
		if in_section == 1:
			m = re.match(r'key:(\S+)$', line)
			if m:
				api_key = m.groups()[0]	

			m = re.match(r'account_id:(\S+)$', line)
			if m:
				account_id = m.groups()[0]

			m = re.match(r'type:(\S+)$', line)
			if m:
				action_type = m.groups()[0]


		if in_section == 2:
			m = re.match(r'(\S+)$', line)
			if m:
				num_arr.append(m.groups()[0])
			
	return
	

if __name__ == '__main__':
	CONFIG = os.getcwd() + "/config"
	parse_config(CONFIG)

	http_url = "127.0.0.1:8000"
	#############################################################################
	# get the auth token from the kazoo server
	# if there is a token file, we use the token 
	token_or_not = 0
	FILE_RESULT = os.getcwd() + "/token_file"

	try:
		fp = open(FILE_RESULT)
		while 1:
			read_line = fp.readline()
			if not read_line:
				break
			token_or_not = 1
			break
		fp.close()
	except:
		token_or_not = 0
		print "cannot open the file"


	auth_token = ""
	if token_or_not != 1:
		token_path = "/v1/api_auth"
		token_values = {"data":{"api_key":api_key}}
		res = get_auth_token(http_url, token_path, token_values)
		jdata = json.JSONDecoder().decode(res)
		auth_token = jdata["auth_token"]

		fp = open(FILE_RESULT, "w")
		fp.write(auth_token+"\r\n")
		fp.close()
	else:
		auth_token = read_line.strip("\t\r\n ")

	print "the auth_token is " + auth_token

	############################################################################
	# the action: add; activate; delete ; all the numbers are in the num_arr
	for item in num_arr:
		num_list_path = "/v1/accounts/" + account_id + "/phone_numbers"
		num_add_del_path="/v1/accounts/" + account_id + "/phone_numbers/" + item
		num_act_path="/v1/accounts/" + account_id + "/phone_numbers/" + item + "/activate"
		num_values = {"data":{}}
		res = ""
		if action_type == "add":
			print "ready to add the number " + item
			res = add_del_number("add", auth_token, http_url, num_add_del_path, num_values)
		elif action_type == "act":
			res = activate_number(auth_token, http_url, num_act_path, num_values)
		elif action_type == "del":
			print "ready to del the number " + item
			res = add_del_number("del", auth_token, http_url, num_add_del_path, num_values)
		else:
			print "Unknown type"

		print "response is : " + res
