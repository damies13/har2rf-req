import sys
import json
import os
from datetime import datetime
import dateutil.parser
import re

import urllib.parse
import html

outdata = {}
workingdata = {}

def init_outdata():
	print("__init__")
	# outdata = {"*** Settings ***": ["Library	RequestsLibrary", "Library	String"], "*** Variables ***": [], "*** Test Cases ***": {}, "*** Keywords ***": {}}
	outdata["*** Settings ***"] = ["Library	RequestsLibrary", "Library	String"]
	outdata["*** Variables ***"] = []
	outdata["*** Test Cases ***"] = {}
	outdata["*** Keywords ***"] = {}

	outdata["*** Keywords ***"]["Get Substring LRB"] = []
	outdata["*** Keywords ***"]["Get Substring LRB"].append("[Documentation]	Get Substring using Left and Right Boundaries")
	outdata["*** Keywords ***"]["Get Substring LRB"].append("[Arguments]    ${string}	${LeftB}	${RightB}")
	outdata["*** Keywords ***"]["Get Substring LRB"].append("${left}= 	Fetch From Right 	${string}	${LeftB}")
	outdata["*** Keywords ***"]["Get Substring LRB"].append("${match}= 	Fetch From Left 	${left} 	${RightB}")
	outdata["*** Keywords ***"]["Get Substring LRB"].append("[Return]	${match}")



def load_har(harfile):
	global workingdata
	with open(harfile, "rb") as f:
		hardata = f.read()
		hartxt = hardata.decode("utf-8")
	# print("hartxt:", hartxt)
	har = json.loads(hartxt)
	workingdata["har"] = har
	return har

def save_robot(pathout):
	# print(outdata)
	ofname = os.path.join(pathout, workingdata["testcase"]+".robot")
	print(ofname)
	if os.path.exists(ofname):
		os.remove(ofname)

	with open(ofname, "a") as of:
		for section in outdata:
			of.write(section + '\n')
			if section in ["*** Settings ***", "*** Variables ***"]:
				for line in outdata[section]:
					of.write(line + '\n')

			if section in ["*** Test Cases ***", "*** Keywords ***"]:
				for k in outdata[section]:
					of.write(k + '\n')
					for line in outdata[section][k]:
						of.write("	"+line + '\n')
					of.write('\n')

			of.write('\n')

def find_estep(respno, kwname):
	starts = "${resp_"+str(respno)+"}"
	i = 0
	for e in outdata["*** Keywords ***"][kwname]:
		# print(starts, " | ", e)
		if e.startswith(starts):
			i += 1
			# print("i:", i, starts, " | ", e)
			return i
		i += 1

	return -1

def find_variable(key, value):
	global outdata
	global workingdata
	newvalue = value
	decvalue = decode_value(value)
	kwname = workingdata["keyword"]

	if len(value.strip())<1:
		return "${EMPTY}"

	# print("find_variable	key:", key, "	value:", value)

	if newvalue == value and value.isdigit() and len(value)>9:
		# check if it was the timestamp at the time of the request in the har file
		sseconds = value[0:10]
		# print("sseconds:", sseconds, "	value:", value)
		intvar = int(sseconds)
		# intime = datetime.fromtimestamp(intvar)
		# print("intime:", intime, "	intvar:", intvar)
		ec = workingdata["entrycount"]
		# print("ec:", ec)
		entry = workingdata["har"]["log"]["entries"][ec]
		startedDateTime = entry["startedDateTime"]
		# print("startedDateTime:", startedDateTime, "	intvar:", intvar)
		reqtime = dateutil.parser.isoparse(startedDateTime)
		# print("reqtime:", reqtime)
		cseconds = datetime.timestamp(reqtime)
		# timediff = (reqtime - intime).total_seconds()
		timediff = abs(cseconds - intvar)
		# print("timediff:", timediff)
		if timediff < 60:
			line = "${TS}=		Get Time		epoch"
			outdata["*** Keywords ***"][kwname].append(line)
			newvalue = "${TS}"
			return newvalue

	if "paramnames" not in workingdata:
		workingdata["paramnames"] = {}
	if "paramvalues" not in workingdata:
		workingdata["paramvalues"] = {}


	if decvalue in workingdata["paramvalues"]:
		if workingdata["paramvalues"][decvalue] == "${"+key+"}":
			newvalue = workingdata["paramvalues"][decvalue]
			return newvalue

	# print("find_variable	paramvalues")
	# print("value:", value, workingdata["paramvalues"].keys())
	if newvalue == value and value in workingdata["paramvalues"]:
		# print("value:", value, "	paramvalues:", workingdata["paramvalues"][value])
		if workingdata["paramvalues"][value] == "${"+key+"}":
			newvalue = workingdata["paramvalues"][value]
			return newvalue

	# print("find_variable	paramnames")
	# print("value:", value, workingdata["paramnames"].keys())
	if newvalue == value and key in workingdata["paramnames"]:
		# print("key:", key, "	paramnames:", workingdata["paramnames"][key])
		if workingdata["paramnames"][key]["oval"] == value:
			newvalue = workingdata["paramnames"][key]["nval"]
			return newvalue

	# print("find_variable	history")
	# search history to try and find it
	if newvalue == value and "history" in workingdata:
		# print("Searching History")
		for e in workingdata["history"]:

			resp = e["entrycount"]+1
			ekwname = e["kwname"]
			estep = find_estep(resp, ekwname)

			# check headers
			for h in e["response"]["headers"]:
				if h["value"] == value and h["name"] == key:
					# print("found value (",value,") and key (",key,") in header for ", e["request"]["url"])

					newkey = saveparam(key, value)

					line = "Set Global Variable		${"+newkey+"}	${resp_"+str(resp)+".headers[\""+key+"\"]}"

					outdata["*** Keywords ***"][ekwname].insert(estep, line)

					newvalue = "${"+newkey+"}"
					return newvalue

				searchstrings = []
				searchstrings.append(value)
				if value != decvalue:
					searchstrings.append(decvalue)
				htmlx = htmlx_encode(decvalue)
				if htmlx != decvalue:
					searchstrings.append(htmlx)
				htmlx = htmlX_encode(decvalue)
				if htmlx != decvalue:
					searchstrings.append(htmlx)
				urlenc = urlencode_value(decvalue)
				if urlenc != decvalue:
					searchstrings.append(urlenc)


				for searchstring in searchstrings:
					if newvalue == value and searchstring in h["value"]:
						lbound, rbound = find_in_string(key, searchstring, h["value"])
						print("lbound:", lbound, "	rbound:", rbound)

						if len(lbound)>0 and len(rbound)==0:
							# no need to find rbound
							newkey = saveparam(key, searchstring)

							line = "${"+newkey+"}=		Fetch From Right		${resp_" + str(resp) + ".headers[\"" + h["name"] + "\"]}		" + lbound
							outdata["*** Keywords ***"][ekwname].insert(estep, line)

							estep += 1

							line = "Set Global Variable		${"+newkey+"}	${"+newkey+"}"
							outdata["*** Keywords ***"][ekwname].insert(estep, line)

							newvalue = "${"+newkey+"}"
							return newvalue

						if len(lbound)>0 and len(rbound)>0:
							newkey = saveparam(key, searchstring)

							line = "${"+newkey+"}=		Get Substring LRB		${resp_" + str(resp) + ".headers[\"" + h["name"] + "\"]}		"+lbound+"		"+rbound
							outdata["*** Keywords ***"][ekwname].insert(estep, line)

							estep += 1

							line = "Set Global Variable		${"+newkey+"}	${"+newkey+"}"
							outdata["*** Keywords ***"][ekwname].insert(estep, line)

							newvalue = "${"+newkey+"}"
							return newvalue




			# check Cookies
			for c in e["response"]["cookies"]:
				if c["value"] == value and c["name"] == key:
					# print("found value (",value,") and key (",key,") in cookies for ", e["request"]["url"])

					newkey = saveparam(key, value)

					line = "Set Global Variable		${"+newkey+"}	${resp_"+str(resp)+".cookies[\""+key+"\"]}"

					outdata["*** Keywords ***"][ekwname].insert(estep, line)

					newvalue = "${"+newkey+"}"
					return newvalue

			# check body
			if "text" in e["response"]["content"]:

				searchstrings = []
				searchstrings.append(("original",value))
				if value != decvalue:
					searchstrings.append(("plain", decvalue))
				htmlx = htmlx_encode(decvalue)
				if htmlx != decvalue:
					searchstrings.append(("html", htmlx))
				htmlx = htmlX_encode(decvalue)
				if htmlx != decvalue:
					searchstrings.append(("html", htmlx))
				urlenc = urlencode_value(decvalue)
				if urlenc != decvalue:
					searchstrings.append(("url", urlenc))

				fullresp = e["response"]["content"]["text"]
				lines = fullresp.splitlines()
				for searchtup in searchstrings:
					searchstring = searchtup[1]
					for line in lines:
						if newvalue == value and searchstring in line:
							print("found value (",searchstring,") in body for ", e["request"]["url"])

							lbound, rbound = find_in_string(key, searchstring, line)
							print("lbound:", lbound, "	rbound:", rbound)

							newkey = ""

							match = substring_LRB(fullresp, lbound, rbound)
							if not check_match(searchstring, match):
								lbound = ""
								rbound = ""

								lbound, rbound = find_in_string(key, searchstring, fullresp)
								match = substring_LRB(fullresp, lbound, rbound)
								if not check_match(searchstring, match):
									lbound = ""
									rbound = ""

							if len(lbound)>0 and len(rbound)==0:
								# no need to find rbound
								newkey = saveparam(key, searchstring)

								line = "${"+newkey+"}=		Fetch From Right		${resp_"+str(resp)+".text}		" + lbound
								outdata["*** Keywords ***"][ekwname].insert(estep, line)


							if len(lbound)>0 and len(rbound)>0:
								newkey = saveparam(key, searchstring)

								line = "${"+newkey+"}=		Get Substring LRB		${resp_"+str(resp)+".text}		"+lbound+"		"+rbound
								outdata["*** Keywords ***"][ekwname].insert(estep, line)


							if len(newkey)>0:

								if searchtup[0] == "html":
									estep += 1
									line = "${"+newkey+"}		Evaluate		html.unescape('${"+newkey+"}')		html"
									outdata["*** Keywords ***"][ekwname].insert(estep, line)

								estep += 1
								line = "Set Global Variable		${"+newkey+"}	${"+newkey+"}"
								outdata["*** Keywords ***"][ekwname].insert(estep, line)

								newvalue = "${"+newkey+"}"
								return newvalue


	# print("find_variable	Last resort")
	# Last resort if it didn't exist anywhere, so create it as a hard coded variable
	if newvalue != decvalue:
		newvalue = decvalue
		newkey = saveparam(key, decvalue)
		line = "${"+newkey+"}		"+decvalue
		outdata["*** Variables ***"].append(line)

		newvalue = "${"+newkey+"}"
		# print("last resort", newkey, newvalue)
		return newvalue

	if newvalue == value:
		# print("last resort", key, value)

		newkey = saveparam(key, value)

		line = "${"+newkey+"}		"+value
		outdata["*** Variables ***"].append(line)

		newvalue = "${"+newkey+"}"
		# print("last resort", newkey, newvalue)
		return newvalue


	return newvalue

def find_in_string(key, searchval, instr):
	print("find_in_string key:", key, "	searchval:", searchval, "	instr:", instr)

	blen = 10
	start = 0
	kpos = instr.find(key, start)
	if kpos>0:
		start = kpos + len(key)
	vpos = instr.find(searchval, start)
	lbound = ""
	rbound = ""
	print("kpos:", kpos, "	vpos:", vpos)
	if kpos<0 and len(searchval)<blen/2:
		# probability of returning an unrelated value match is too high
		return (lbound, rbound)

	if kpos>0 and kpos<vpos:
		lbound = instr[kpos:vpos]

		start = 0
		lbkpos = lbound.find(key, start)
		while lbkpos>0:
			lbound = lbound[lbkpos:]
			lbkpos = lbound.find(key, start)

	if len(lbound)==0 and vpos>blen:
		lbound = instr[vpos-blen:vpos]
	if len(lbound)==0 and vpos>0 and vpos<blen:
		lbound = instr[:vpos]

	if lbound.find('\r', 0)>0:
		lmin = lbound.find('\r', 0)
		lbound = lbound[lmin:]

	if lbound.find('\n', 0)>0:
		lmin = lbound.find('\n', 0)
		lbound = lbound[lmin:]

	print("lbound:", lbound)
	vepos = vpos+len(searchval)
	if vepos == len(instr) and len(lbound)>0:
		# no need to find rbound
		return (lbound, rbound)

	rlen = len(instr) - vepos
	print("rlen:", rlen, "	and right:", instr[vepos:])
	if rlen < blen+1:
		rbound = instr[vepos:]

	if rlen > blen:
		rbound = instr[vepos:vepos+blen]

	if rbound.find('\r', 0)>0:
		rmax = rbound.find('\r', 0)
		rbound = rbound[:rmax]

	if rbound.find('\n', 0)>0:
		rmax = rbound.find('\n', 0)
		rbound = rbound[:rmax]

	# check we got the right value?
	match = substring_LRB(instr, lbound, rbound)
	if check_match(searchval, match):
		print("rbound:", rbound)
		return (lbound, rbound)

	# we didn't get the expected match
	while( ( len(instr) - len(searchval) ) / 2 > blen ):
		blen += 1
		if len(lbound)<blen and vpos>blen:
			lbound = instr[vpos-blen:vpos]
		if len(lbound)<blen and vpos>0 and vpos<blen:
			lbound = instr[:vpos]

		if lbound.find('\r', 0)>0:
			lmin = lbound.find('\r', 0)
			lbound = lbound[lmin:]

		if lbound.find('\n', 0)>0:
			lmin = lbound.find('\n', 0)
			lbound = lbound[lmin:]

		rlen = len(instr) - vepos
		if rlen < blen+1:
			rbound = instr[vepos:]
		if rlen > blen:
			rbound = instr[vepos:vepos+blen]

		if rbound.find('\r', 0)>0:
			rmax = rbound.find('\r', 0)
			rbound = rbound[:rmax]

		if rbound.find('\n', 0)>0:
			rmax = rbound.find('\n', 0)
			rbound = rbound[:rmax]

		match = substring_LRB(instr, lbound, rbound)
		if check_match(searchval, match):
			print("rbound:", rbound)
			return (lbound, rbound)

	return ("", "")

def substring_LRB(searchstring, left, right):
	match = ""
	posl = searchstring.find(left)
	if posl<0:
		return match
	matchl = searchstring[posl+len(left):]
	posr = matchl.find(right)
	if posr<0:
		return match
	match = matchl[:posr]
	return match

def check_match(orig, match):
	if orig == match:
		return True
	else:
		return False

def htmlX_encode(s):
	htmlCodes = (
		('&', '&amp;'),
		("=", '&#x3D;'),
		("'", '&#x27;'),
		('"', '&quot;'),
		('>', '&gt;'),
		('<', '&lt;'),
	)
	for code in htmlCodes:
		s = s.replace(code[0], code[1])
	return s

def htmlx_encode(s):
	htmlCodes = (
		('&', '&amp;'),
		("=", '&#x3d;'),
		("'", '&#x27;'),
		('"', '&quot;'),
		('>', '&gt;'),
		('<', '&lt;'),
	)
	for code in htmlCodes:
		s = s.replace(code[0], code[1])
	return s

def urlencode_value(value):
	newvalue = value
	if isinstance(value, str):
		print("urlencode_value value:", value)
		if '%' in newvalue:
			newvalue = urllib.parse.encode(newvalue)

		print("urlencode_value newvalue:", newvalue)
	return newvalue

def decode_value(value):
	newvalue = value
	if isinstance(value, str):
		print("decode_value value:", value)
		if '%' in newvalue:
			newvalue = urllib.parse.unquote_plus(newvalue)

		print("decode_value newvalue:", newvalue)
	return newvalue

def process_entry(entry):
	global outdata
	global workingdata
	print(entry["request"]["method"], entry["request"]["url"])

	kwname = workingdata["keyword"]

	# add extra info to entry
	entry["kwname"] = kwname
	entry["entrycount"] = workingdata["entrycount"]


	if "session" not in workingdata:
		add_session()
		# add initial headers
		hdrs = ""
		cook = ""
		updatesess = 0
		for h in entry["request"]["headers"]:
			print("h:", h["name"], h["value"])
			specialh = ["cookie", "accept-encoding"]
			if h["name"].lower() not in specialh and h["name"][0] != ":":
				# hdrs[h["name"]] = h["value"]
				value = find_variable(h["name"], h["value"])
				hdrs += "	" + h["name"] + "=" + value

			if h["name"].lower() == "cookie":
				clst = h["value"].split(";")
				for c in clst:
					citm = c.split("=")
					# cook[citm[0].strip()] = citm[1].strip()
					if citm[0].strip() not in ["_ga", "_gid"]:   # don't bother sending Google analytics cookies
						key = citm[0].strip()
						value = find_variable(key, citm[1].strip())
						cook += "	" + key + "=" + value

		line = "&{Headers}=		Create dictionary" + hdrs
		outdata["*** Keywords ***"][kwname].append(line)

		# line = "Log 	${Headers}"
		# outdata["*** Keywords ***"][kwname].append(line)

		line = "&{Cookies}=		Create dictionary" + cook
		outdata["*** Keywords ***"][kwname].append(line)

		# line = "Log 	${Cookies}"
		# outdata["*** Keywords ***"][kwname].append(line)

		line = "Update Session	" + workingdata["session"] + "	${Headers}	${Cookies}"
		outdata["*** Keywords ***"][kwname].append(line)


	argdata = ""

	# GET
	# GET
	# GET
	if entry["request"]["method"] == "GET":
		statuscode = entry["response"]["status"]
		if statuscode == 302:
			argdata += "	" + "expected_status={}".format(statuscode)
			argdata += "	" + "allow_redirects=${False}"
			# if "redirecturl" not in workingdata:
				# workingdata["redirecturl"] = entry["request"]["url"].replace(workingdata["baseurl"], "")
		else:
			argdata += "	" + "expected_status={}".format(statuscode)


		if "redirecturl" in workingdata:
			del workingdata["redirecturl"]
		else:
			workingdata["entrycount"] += 1
			ec = workingdata["entrycount"]
			path = entry["request"]["url"].replace(workingdata["baseurl"], "")
			patharr = path.split("?")
			if len(patharr)>1:
				path = patharr[0]
				params = ""

				parrin = patharr[1].split("&")
				parrout = []
				for p in parrin:
					if "=" in p:
						key, value = p.split("=", 1)
						newvalue = find_variable(key, value)
						parrout.append("=".join([key, newvalue]))
					else:
						newvalue = find_variable("NoKey", p)
						parrout.append(newvalue)

				params = "	".join(parrout)

				dname = "params_{}".format(ec)
				line = "&{"+dname+"}=		Create dictionary	" + params
				outdata["*** Keywords ***"][kwname].append(line)
				argdata += "	" + "params=${"+dname+"}"

			resp = "resp_{}".format(ec)
			line = "${"+resp+"}=		GET On Session		" + workingdata["session"] + "		url=" + path + argdata
			outdata["*** Keywords ***"][kwname].append(line)

			# line = "Log 	${"+resp+".text}"
			# outdata["*** Keywords ***"][kwname].append(line)

	# POST
	# POST
	# POST
	if entry["request"]["method"] == "POST":

		workingdata["entrycount"] += 1
		ec = workingdata["entrycount"]

		path = entry["request"]["url"].replace(workingdata["baseurl"], "")

		patharr = path.split("?")
		if len(patharr)>1:
			path = patharr[0]
			params = ""

			parrin = patharr[1].split("&")
			parrout = []
			for p in parrin:
				key, value = p.split("=", 1)
				newvalue = find_variable(key, value)
				parrout.append("=".join([key, newvalue]))

			params = "	".join(parrout)

			dname = "params_{}".format(ec)
			line = "&{"+dname+"}=		Create dictionary	" + params
			outdata["*** Keywords ***"][kwname].append(line)
			argdata += "	" + "params=${"+dname+"}"



		if "postData" in entry["request"]:
			pd_try = True
			pd = entry["request"]["postData"]
			if pd_try and "params" in pd:
				pd_try = False
				dictdata = ""
				for param in pd["params"]:
					newvalue = find_variable(param["name"], param["value"])
					dictdata += "	" + param["name"] + "=" + newvalue

				dname = "postdata_{}".format(ec)
				line = "&{"+dname+"}=		Create dictionary" + dictdata
				outdata["*** Keywords ***"][kwname].append(line)
				argdata += "	" + "data=${"+dname+"}"

			if pd_try and "text" in pd and pd["text"][0] == "{":
				pd_try = False
				jsondata = json.loads(pd["text"])
				jsondata = process_json(jsondata)

		statuscode = entry["response"]["status"]
		if statuscode == 302:
			argdata += "	" + "expected_status={}".format(statuscode)
			argdata += "	" + "allow_redirects=${False}"
			# if "redirecturl" not in workingdata:
				# workingdata["redirecturl"] = entry["request"]["url"].replace(workingdata["baseurl"], "")
		else:
			argdata += "	" + "expected_status={}".format(statuscode)


		resp = "resp_{}".format(ec)
		line = "${"+resp+"}=		POST On Session		" + workingdata["session"] + "		url=" + path + argdata
		outdata["*** Keywords ***"][kwname].append(line)
		# line = "Log 	${"+resp+".text}"
		# outdata["*** Keywords ***"][kwname].append(line)


	# append entry to history
	entry["step"] = len(outdata["*** Keywords ***"][kwname])+1
	if "history" not in workingdata:
		workingdata["history"] = []
	workingdata["history"].append(entry)

def process_json(jsondata):
	print("jsondata:", jsondata)
	print("jsondata.keys:", jsondata.keys())
	for key in jsondata.keys():
		value = jsondata[key]
		print("key: ", key, "	value:", value, type(value))
		if isinstance(value, str) or isinstance(value, int):
			newvalue = find_variable(key, str(value))
			jsondata[key] = newvalue
		if isinstance(value, list):
			for i in range(len(value)):
				skey = "{}_{}".format(key, i)
				svalue = value[i]
				print("skey: ", skey, "	svalue:", svalue, type(svalue))
				if isinstance(svalue, str) or isinstance(svalue, int):
					newvalue = find_variable(skey, str(svalue))
					value[i] = newvalue
				if isinstance(svalue, dict):
					value[i] = process_json(svalue)

			jsondata[key] = value

		if isinstance(value, dict):
			jsondata[key] = process_json(value)
	print("jsondata:", jsondata)
	return jsondata


def saveparam(name, value):
	# global outdata
	global workingdata

	newname = name
	if name in workingdata["paramnames"]:
		i = 0
		while newname in workingdata["paramnames"]:
			print("newname:", newname)
			i += 1
			newname = name + "_{}".format(i)

		print("newname:", newname)


	if "paramnames" not in workingdata:
		workingdata["paramnames"] = {}
	if newname not in workingdata["paramnames"]:
		# workingdata["paramnames"].append(newname)
		workingdata["paramnames"][newname] = {}
		workingdata["paramnames"][newname]["nval"] = "${"+newname+"}"
		workingdata["paramnames"][newname]["oval"] = value

	if "paramvalues" not in workingdata:
		workingdata["paramvalues"] = {}
	if value not in workingdata["paramvalues"]:
		workingdata["paramvalues"][value] = "${"+newname+"}"

	print("saved", "${"+newname+"}", "=", value)
	return newname

def add_test_case(tcname):
	global outdata
	global workingdata
	if tcname not in outdata["*** Test Cases ***"]:
		outdata["*** Test Cases ***"][tcname] = []
		workingdata["testcase"] = tcname

def add_keyword(kwname, comment):
	global outdata
	global workingdata

	if "testcase" not in workingdata:
		add_test_case(kwname)

	tcname = workingdata["testcase"]

	if kwname not in outdata["*** Keywords ***"]:
		outdata["*** Keywords ***"][kwname] = []
		workingdata["keyword"] = kwname
		# workingdata["entrycount"] = 0
		workingdata["entrycount"] = -1

		outdata["*** Keywords ***"][kwname].append("[Documentation] 	" + tcname + "	|	" + kwname + "	|	" + comment)
		outdata["*** Test Cases ***"][tcname].append(kwname)

def add_session():
	global outdata
	global workingdata

	tcname = workingdata["testcase"]
	url = workingdata["har"]["log"]["entries"][0]["request"]["url"]
	print("url", url)
	urlarr = url.split("/")
	print("urlarr", urlarr)
	basearr = [urlarr[0],urlarr[1],urlarr[2]]
	sessionname = "sess_" + urlarr[2].replace(".", "_")
	# baseurl = basearr.join("/")
	baseurl = "/".join(basearr)
	workingdata["baseurl"] = baseurl
	workingdata["session"] = sessionname
	# outdata["*** Settings ***"].append("Suite Setup           Create Session    " + sessionname + " 	" +	baseurl)
	outdata["*** Test Cases ***"][tcname].insert(0, "Create Session    " + sessionname + " 	" +	baseurl + " 	disable_warnings=1")

def iso2sec(isotime):
	reqtime = dateutil.parser.isoparse(isotime)
	# print("reqtime:", reqtime)
	cseconds = datetime.timestamp(reqtime)
	return cseconds

def process_har(harfile):
	har = load_har(harfile)
	# print(har)
	harfilename = os.path.basename(harfile)
	kwbname = os.path.splitext(harfilename)[0]

	# sort pages
	sortedpages = sorted(har["log"]["pages"], key=lambda k: iso2sec(k["startedDateTime"]))
	# print("sortedpages:", sortedpages)

	# sort pages
	sortedentries = sorted(har["log"]["entries"], key=lambda k: iso2sec(k["startedDateTime"]))
	# print("sortedentries:", sortedentries)

	i = 0
	for page in sortedpages:
		# pagetime = int(iso2sec(page["startedDateTime"]))
		# if i+1 == len(sortedpages):
			# nextpagetime = int(datetime.timestamp(datetime.now()))
		# else:
			# nextpagetime = int(iso2sec(sortedpages[i+1]["startedDateTime"]))
		pagetime = iso2sec(page["startedDateTime"])-0.002
		if i+1 == len(sortedpages):
			nextpagetime = datetime.timestamp(datetime.now())
		else:
			nextpagetime = iso2sec(sortedpages[i+1]["startedDateTime"])-0.002

		kwname = kwbname + " " + page["id"]
		print(kwname, "pagetime:", pagetime, "	nextpagetime:", nextpagetime)

		add_keyword(kwname, page["title"])

		for e in sortedentries:
			# print(e)
			# print(e["request"]["method"], e["request"]["url"])

			# etime = int(iso2sec(e["startedDateTime"]))
			etime = iso2sec(e["startedDateTime"])
			if etime >= pagetime and etime < nextpagetime:
				# print("etime:", etime)
				process_entry(e)

		i +=1




# add_test_case(tcname)

init_outdata()
pathin = os.path.abspath(sys.argv[1])
pathout = os.path.dirname(pathin)
if os.path.exists(pathin):
	if os.path.isdir(pathin):
		pathout = pathin
		tc = os.path.split(pathin)[-1]
		print("tc:", tc)
		add_test_case(tc)
		# get robot files
		# dir = os.scandir(pathin)
		dir = os.listdir(pathin)
		# print("dir:", dir)
		for item in dir:
			print("item:", item, ".har ==", os.path.splitext(item)[1].lower())
			if os.path.splitext(item)[1].lower() == ".har":
				harpath = os.path.join(pathin, item)
				print("harpath:", harpath)
				process_har(harpath)

	else:
		# tc = os.path.split(os.path.dirname(pathin))[-1]
		harfilename = os.path.basename(pathin)
		tc = os.path.splitext(harfilename)[0]


		print("tc:", tc)
		add_test_case(tc)
		process_har(pathin)

	save_robot(pathout)

else:
	import glob
	file_list = glob.glob(pathin)
	# print(file_list)
	if len(file_list)>0:
		for item in file_list:
			tc = os.path.split(os.path.dirname(item))[-1]
			print("tc:", tc)
			add_test_case(tc)
			process_har(item)
		save_robot(pathout)
