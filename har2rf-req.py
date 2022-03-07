import sys
import json
import os
from datetime import datetime
import dateutil.parser
import re

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
	kwname = workingdata["keyword"]

	if len(value.strip())<1:
		return newvalue
	
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
			# print("e:", e)

			# check headers
			for h in e["response"]["headers"]:
				if h["value"] == value and h["name"] == key:
					# print("found value (",value,") and key (",key,") in header for ", e["request"]["url"])
					
					newkey = saveparam(key, value)

					
					resp = e["entrycount"]+1
					line = "Set Global Variable		${"+newkey+"}	${resp_"+str(resp)+".headers[\""+key+"\"]}"
					ekwname = e["kwname"]
					
					estep = find_estep(resp, ekwname)
					
					outdata["*** Keywords ***"][ekwname].insert(estep, line)

					newvalue = "${"+newkey+"}"
					return newvalue

			# check Cookies
			for c in e["response"]["cookies"]:
				if c["value"] == value and c["name"] == key:
					# print("found value (",value,") and key (",key,") in cookies for ", e["request"]["url"])

					newkey = saveparam(key, value)
					
					resp = e["entrycount"]+1
					line = "Set Global Variable		${"+newkey+"}	${resp_"+str(resp)+".cookies[\""+key+"\"]}"
					ekwname = e["kwname"]
					
					estep = find_estep(resp, ekwname)
					outdata["*** Keywords ***"][ekwname].insert(estep, line)

					newvalue = "${"+newkey+"}"
					return newvalue
	
			# check body
			if "text" in e["response"]["content"] and value in e["response"]["content"]["text"]:
				# print("found value (",value,") in body for ", e["request"]["url"])
				
				start = 0
				while newvalue == value and start >=0:
					# print("body:", e["response"]["content"]["text"])
					# print("start:", start, "looking for value:", value)
					pos = e["response"]["content"]["text"].find(value, start)
					# print("pos:", pos)
					if pos >=0:
						offset = len(key)*2 + len(value)*2
						# excerpt = e["response"]["content"]["text"][(pos-len(key)*2):(pos+len(value)*2)]
						excerpt = e["response"]["content"]["text"][(pos-len(key)-100):(pos+len(value)+100)]
						# excerpt = e["response"]["content"]["text"][(pos-len(key)-offset):(pos+len(value)+offset)]
						if key in excerpt:
							# print(e["kwname"], "	step:", e["step"], "	entrycount:", e["entrycount"])
							print("found key (",key,") in excerpt:", "|{}|".format(excerpt))
							
							ekwname = e["kwname"]
							
							kpos = excerpt.find(key)
							vpos = excerpt.find(value, kpos)
							if vpos > kpos:
								print("kpos:", kpos, "vpos:", vpos)
								fullprefix = excerpt[0:vpos].strip()
								prefixarr = fullprefix.splitlines()
								prefix = prefixarr[-1].strip()
								print("prefix: |{}|".format(prefix))
								
								# print("excerpt:", excerpt)
								print("vpos:", vpos, "	len(value):", len(value), "")
								spos = vpos+len(value)
								print("spos:", spos, "	spos+5:", spos+5)
								#	# suffix = excerpt[spos:5]
								#	presuffix = excerpt[kpos:(vpos+len(value)+3)]
								#	print("presuffix: |{}|".format(presuffix))
								#	# suffix = presuffix[-3:-1]
								#	suffix = presuffix[-3:len(presuffix)].strip()

								fullsuffix = excerpt[spos:len(excerpt)]
								suffixarr = fullsuffix.splitlines()
								suffix = suffixarr[0].strip()
								print("suffix: |{}|".format(suffix))
								
								resp = e["entrycount"]+1

								# line = "${left}= 	Fetch From Right 	${resp_"+str(resp)+".text} 	"+prefix
								# outdata["*** Keywords ***"][ekwname].insert(e["step"], line)
								# # print(line)

								# line = "${"+key+"}= 	Fetch From Left 	${left} 	"+suffix
								# outdata["*** Keywords ***"][ekwname].insert(e["step"]+1, line)
								# # print(line)
								
								estep = find_estep(resp, ekwname)

								newkey = saveparam(key, value)

								# test match with prefix and suffix works as expected?
								# find prefix from right
								ml = e["response"]["content"]["text"].rfind(prefix)+len(prefix)
								# find suffix from left
								mr = e["response"]["content"]["text"].find(suffix, ml)
								# get match
								match = e["response"]["content"]["text"][ml:mr]
								# print("ml:", ml, "	mr:", mr, "	match:", match, "	value:", value)
								
								goffset = 1
								if match == value:
								
									line = "${"+newkey+"}=		Get Substring LRB		${resp_"+str(resp)+".text}		"+prefix+"		"+suffix
									outdata["*** Keywords ***"][ekwname].insert(estep, line)

								
								else:
									reprefix = re.escape(prefix)
									resuffix = re.escape(suffix)
									
									# test re pattern
									pattern = reprefix+"(.*?)"+resuffix
									# e["response"]["content"]["text"]
									retest = re.search(pattern, e["response"]["content"]["text"]).group(0)
									
									print("retest:", retest)
									
									reprefix = re.escape(prefix).replace('"', r'\"').replace("\\", r"\\")
									resuffix = re.escape(suffix).replace('"', r'\"').replace("\\", r"\\")

									# line = "${regx_match}=		Get Lines Matching Regexp		${resp_"+str(resp)+".text}		"+reprefix+"(.*?)"+resuffix
									line = "${regx_match}=		evaluate		re.search(\"" + reprefix + "(.*?)" + resuffix + "\", \"\"\"${resp_"+str(resp)+".text}\"\"\").group(0)		re"

									outdata["*** Keywords ***"][ekwname].insert(estep, line)
									line = "${"+newkey+"}=		Get Substring LRB		${regx_match}		"+prefix+"		"+suffix
									outdata["*** Keywords ***"][ekwname].insert(estep+1, line)
								
									goffset += 1
								
								
								line = "Set Global Variable		${"+newkey+"}"
								outdata["*** Keywords ***"][ekwname].insert(estep+goffset, line)



								newvalue = "${"+newkey+"}"
								return newvalue
						start = pos+len(value)
					else:
						start = pos
					# else:
						# print("didn't find key (",key,") in excerpt:", excerpt)
				

	# print("find_variable	Last resort")
	# Last resort if it didn't exist anywhere, so create it as a hard coded variable
	if newvalue == value:
		# print("last resort", key, value)

		newkey = saveparam(key, value)
		
		line = "${"+newkey+"}		"+value
		outdata["*** Variables ***"].append(line)
		
		newvalue = "${"+newkey+"}"
		# print("last resort", newkey, newvalue)
		return newvalue
		
					
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
			if h["name"] != "Cookie" and h["name"][0] != ":":
				# hdrs[h["name"]] = h["value"]
				value = find_variable(h["name"], h["value"])
				hdrs += "	" + h["name"] + "=" + value
			if h["name"] == "Cookie":
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
			line = "${"+resp+"}=		GET On Session		" + workingdata["session"] + "		" + path + argdata
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
			pd = entry["request"]["postData"]
			if "params" in pd:
				dictdata = ""
				for param in pd["params"]:
					newvalue = find_variable(param["name"], param["value"])
					dictdata += "	" + param["name"] + "=" + newvalue
				
				dname = "postdata_{}".format(ec)
				line = "&{"+dname+"}=		Create dictionary" + dictdata
				outdata["*** Keywords ***"][kwname].append(line)
				argdata += "	" + "data=${"+dname+"}"

		statuscode = entry["response"]["status"]
		if statuscode == 302:
			argdata += "	" + "expected_status={}".format(statuscode)
			argdata += "	" + "allow_redirects=${False}"
			# if "redirecturl" not in workingdata:
				# workingdata["redirecturl"] = entry["request"]["url"].replace(workingdata["baseurl"], "")
		else:
			argdata += "	" + "expected_status={}".format(statuscode)
				
		
		resp = "resp_{}".format(ec)
		line = "${"+resp+"}=		POST On Session		" + workingdata["session"] + "		" + path + argdata
		outdata["*** Keywords ***"][kwname].append(line)
		# line = "Log 	${"+resp+".text}"
		# outdata["*** Keywords ***"][kwname].append(line)

	
	# append entry to history	
	entry["step"] = len(outdata["*** Keywords ***"][kwname])+1
	if "history" not in workingdata:
		workingdata["history"] = []
	workingdata["history"].append(entry)


	
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
	outdata["*** Test Cases ***"][tcname].insert(0, "Create Session    " + sessionname + " 	" +	baseurl)

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
