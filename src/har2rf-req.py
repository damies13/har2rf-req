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

	possiblekeys = ["${"+key+"}"]
	possiblekeyn = [key]
	i = 1
	newname = key+"_"+str(i)
	# print("newname:", newname, workingdata["paramnames"])
	while newname in workingdata["paramnames"]:
		possiblekeys.append("${"+newname+"}")
		possiblekeyn.append(newname)
		i += 1
		newname = key+"_"+str(i)
		# print("newname:", newname)
	print("possiblekeys:", possiblekeys)

	if decvalue in workingdata["paramvalues"]:
		print("decvalue key:", workingdata["paramvalues"][decvalue], " <=> ", possiblekeys)
		if workingdata["paramvalues"][decvalue] in possiblekeys:
			newvalue = workingdata["paramvalues"][decvalue]
			return newvalue

	# print("find_variable	paramvalues")
	# print("value:", value, workingdata["paramvalues"].keys())
	if newvalue == value and value in workingdata["paramvalues"]:
		# print("value:", value, "	paramvalues:", workingdata["paramvalues"][value])
		print("value key:", workingdata["paramvalues"][value], " <=> ", possiblekeys)
		if workingdata["paramvalues"][value] in possiblekeys:
			newvalue = workingdata["paramvalues"][value]
			return newvalue

	# print("find_variable	paramnames")
	# print("value:", value, workingdata["paramnames"].keys())
	if newvalue == value and key in workingdata["paramnames"]:
		# print("key:", key, "	paramnames:", workingdata["paramnames"][key])
		for keyi in possiblekeyn:
			print("keyi:", keyi, "	oval: ", workingdata["paramnames"][keyi]["oval"], " <=> ", decvalue)
			if workingdata["paramnames"][keyi]["oval"] == decvalue:
				newvalue = workingdata["paramnames"][keyi]["nval"]
				return newvalue
			print("keyi:", keyi, "	oval: ", workingdata["paramnames"][keyi]["oval"], " <=> ", value)
			if workingdata["paramnames"][keyi]["oval"] == value:
				newvalue = workingdata["paramnames"][keyi]["nval"]
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

				# check body for raw value
				if value in e["response"]["content"]["text"]:
					print("found value (",value,") in body for ", e["request"]["url"])

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


									# line = "${left}= 	Fetch From Right 	${resp_"+str(resp)+".text} 	"+prefix
									# outdata["*** Keywords ***"][ekwname].insert(e["step"], line)
									# # print(line)

									# line = "${"+key+"}= 	Fetch From Left 	${left} 	"+suffix
									# outdata["*** Keywords ***"][ekwname].insert(e["step"]+1, line)
									# # print(line)

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
									print("newvalue:", newvalue)
									return newvalue
							start = pos+len(value)
						else:
							start = pos
						# else:
							# print("didn't find key (",key,") in excerpt:", excerpt)


				# check body for decoded value
				if value != decvalue and decvalue in e["response"]["content"]["text"]:
					print("found value (",decvalue,") in body for ", e["request"]["url"])

					searchval = decvalue
					start = 0
					while newvalue == value and start >=0:
						# print("body:", e["response"]["content"]["text"])
						# print("start:", start, "looking for value:", value)
						pos = e["response"]["content"]["text"].find(searchval, start)
						# print("pos:", pos)
						if pos >=0:
							offset = len(key)*2 + len(decvalue)*2
							# excerpt = e["response"]["content"]["text"][(pos-len(key)*2):(pos+len(value)*2)]
							excerpt = e["response"]["content"]["text"][(pos-len(key)-100):(pos+len(searchval)+100)]
							# excerpt = e["response"]["content"]["text"][(pos-len(key)-offset):(pos+len(value)+offset)]
							if key in excerpt:
								# print(e["kwname"], "	step:", e["step"], "	entrycount:", e["entrycount"])
								print("found key (",key,") in excerpt:", "|{}|".format(excerpt))

								ekwname = e["kwname"]

								kpos = excerpt.find(key)
								vpos = excerpt.find(searchval, kpos)
								if vpos > kpos:
									print("kpos:", kpos, "vpos:", vpos)
									fullprefix = excerpt[0:vpos].strip()
									prefixarr = fullprefix.splitlines()
									prefix = prefixarr[-1].strip()
									print("prefix: |{}|".format(prefix))

									# print("excerpt:", excerpt)
									print("vpos:", vpos, "	len(value):", len(searchval), "")
									spos = vpos+len(searchval)
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

									newkey = saveparam(key, searchval)

									# test match with prefix and suffix works as expected?
									# find prefix from right
									ml = e["response"]["content"]["text"].rfind(prefix)+len(prefix)
									# find suffix from left
									mr = e["response"]["content"]["text"].find(suffix, ml)
									# get match
									match = e["response"]["content"]["text"][ml:mr]
									# print("ml:", ml, "	mr:", mr, "	match:", match, "	value:", value)

									goffset = 1
									if match == searchval:

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
									print("newvalue:", newvalue)
									return newvalue
							start = pos+len(value)
						else:
							start = pos



				htmlvalue = html.escape(decvalue)
				# print("Try to find decvalue (", decvalue, ") as html encoded value (", htmlvalue, ")")
				# check body for html enc value
				if value != htmlvalue and htmlvalue in e["response"]["content"]["text"]:
					print("found value (", htmlvalue, ") in body for ", e["request"]["url"])

					searchval = htmlvalue
					start = 0
					while newvalue == value and start >=0:
						# print("body:", e["response"]["content"]["text"])
						# print("start:", start, "looking for value:", value)
						pos = e["response"]["content"]["text"].find(searchval, start)
						# print("pos:", pos)
						if pos >=0:
							offset = len(key)*2 + len(decvalue)*2
							# excerpt = e["response"]["content"]["text"][(pos-len(key)*2):(pos+len(value)*2)]
							excerpt = e["response"]["content"]["text"][(pos-len(key)-100):(pos+len(searchval)+100)]
							# excerpt = e["response"]["content"]["text"][(pos-len(key)-offset):(pos+len(value)+offset)]
							if key in excerpt:
								# print(e["kwname"], "	step:", e["step"], "	entrycount:", e["entrycount"])
								print("found key (",key,") in excerpt:", "|{}|".format(excerpt))

								ekwname = e["kwname"]

								kpos = excerpt.find(key)
								vpos = excerpt.find(searchval, kpos)
								if vpos > kpos:
									print("kpos:", kpos, "vpos:", vpos)
									fullprefix = excerpt[0:vpos].strip()
									prefixarr = fullprefix.splitlines()
									prefix = prefixarr[-1].strip()
									print("prefix: |{}|".format(prefix))

									# print("excerpt:", excerpt)
									print("vpos:", vpos, "	len(value):", len(searchval), "")
									spos = vpos+len(searchval)
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

									newkey = saveparam(key, searchval)

									# test match with prefix and suffix works as expected?
									# find prefix from right
									ml = e["response"]["content"]["text"].rfind(prefix)+len(prefix)
									# find suffix from left
									mr = e["response"]["content"]["text"].find(suffix, ml)
									# get match
									match = e["response"]["content"]["text"][ml:mr]
									# print("ml:", ml, "	mr:", mr, "	match:", match, "	value:", value)

									goffset = 1
									if match == searchval:

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


				# print("decvalue:", decvalue, type(decvalue))
				htmlvalue = urllib.parse.quote(decvalue)
				# print("htmlvalue:", htmlvalue)
				# htmlvalue = re.sub(r'%(.?.?)', r'&#x\1;', htmlvalue)
				htmlvalue = htmlx_encode(decvalue)
				# print("htmlvalue:", htmlvalue)
				# print("Try to find decvalue (", decvalue, ") as html encoded value (", htmlvalue, ")")
				# check body for html enc value
				if value != htmlvalue and htmlvalue in e["response"]["content"]["text"]:
					print("found value (", htmlvalue, ") in body for ", e["request"]["url"])

					searchval = htmlvalue
					start = 0
					while newvalue == value and start >=0:
						# print("body:", e["response"]["content"]["text"])
						# print("start:", start, "looking for value:", value)
						pos = e["response"]["content"]["text"].find(searchval, start)
						# print("pos:", pos)
						if pos >=0:
							offset = len(key)*2 + len(decvalue)*2
							# excerpt = e["response"]["content"]["text"][(pos-len(key)*2):(pos+len(value)*2)]
							excerpt = e["response"]["content"]["text"][(pos-len(key)-100):(pos+len(searchval)+100)]
							# excerpt = e["response"]["content"]["text"][(pos-len(key)-offset):(pos+len(value)+offset)]
							if key in excerpt:
								# print(e["kwname"], "	step:", e["step"], "	entrycount:", e["entrycount"])
								print("found key (",key,") in excerpt:", "|{}|".format(excerpt))

								ekwname = e["kwname"]

								kpos = excerpt.find(key)
								vpos = excerpt.find(searchval, kpos)
								if vpos > kpos:
									print("kpos:", kpos, "vpos:", vpos)
									fullprefix = excerpt[0:vpos].strip()
									prefixarr = fullprefix.splitlines()
									prefix = prefixarr[-1].strip()
									print("prefix: |{}|".format(prefix))

									# print("excerpt:", excerpt)
									print("vpos:", vpos, "	len(value):", len(searchval), "")
									spos = vpos+len(searchval)
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

									newkey = saveparam(key, searchval)

									# test match with prefix and suffix works as expected?
									# find prefix from right
									ml = e["response"]["content"]["text"].rfind(prefix)+len(prefix)
									# find suffix from left
									mr = e["response"]["content"]["text"].find(suffix, ml)
									# get match
									match = e["response"]["content"]["text"][ml:mr]
									# print("ml:", ml, "	mr:", mr, "	match:", match, "	value:", value)

									goffset = 1
									if match == searchval:

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



									line = "${"+newkey+"}		Evaluate		html.unescape('${"+newkey+"}')		html"
									outdata["*** Keywords ***"][ekwname].insert(estep+goffset, line)

									goffset += 1

									line = "Set Global Variable		${"+newkey+"}"
									outdata["*** Keywords ***"][ekwname].insert(estep+goffset, line)



									newvalue = "${"+newkey+"}"
									print("newvalue:", newvalue)
									return newvalue
							start = pos+len(value)
						else:
							start = pos



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

	start = 0
	kpos = instr.find(key, start)
	if kpos>0:
		start = kpos + len(key)
	vpos = instr.find(searchval, start)
	lbound = ""
	rbound = ""
	print("kpos:", kpos, "	vpos:", vpos)
	if kpos<0 and len(searchval)<10:
		# probability of returning an unrelated value match is too high
		return (lbound, rbound)

	if kpos>0 and kpos<vpos:
		lbound = instr[kpos:vpos]
	if len(lbound)==0 and vpos>10:
		lbound = instr[vpos-10:vpos]
	if len(lbound)==0 and vpos>0 and vpos<10:
		lbound = instr[:vpos]

	print("lbound:", lbound)
	vepos = vpos+len(searchval)
	if vepos == len(instr) and len(lbound)>0:
		# no need to find rbound
		return (lbound, rbound)

	rlen = len(instr) - vepos
	print("rlen:", rlen, "	and right:", instr[vepos:])
	if rlen < 11:
		rbound = instr[vepos:]

	if rlen > 10:
		rbound = instr[vepos:vepos+10]

	print("rbound:", rbound)
	return (lbound, rbound)


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
		# print("urlencode_value value:", value)
		if '%' in newvalue:
			newvalue = urllib.parse.unquote_plus(newvalue)
		# print("urlencode_value newvalue:", newvalue)
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

	# headers

	hdrs = ""
	for h in entry["request"]["headers"]:
		print("h:", h["name"], h["value"])
		specialh = ["cookie", "accept-encoding", "content-length"]	# , "pragma", "cache-control"
		if h["name"].lower() not in specialh and h["name"][0] != ":":
			# hdrs[h["name"]] = h["value"]
			value = find_variable(h["name"], h["value"])
			hdrs += "	" + h["name"] + "=" + value
	if len(hdrs)>0:
		line = "&{Req_Headers}=		Create dictionary" + hdrs
		outdata["*** Keywords ***"][kwname].append(line)
		argdata += "	" + "headers=${Req_Headers}"


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
				dname = "json_{}".format(ec)
				paramname, lines = process_dict(dname, jsondata)
				# print("paramname:", paramname, "	paramlst:", paramlst)
				outdata["*** Keywords ***"][kwname].extend(lines)
				argdata += "	" + "json="+paramname


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

def process_dict(key, dictdata):
	# keyname = "d_"+key
	keyname = key
	dictparam = "${"+keyname+"}"
	dictconstr = []
	dicttems = ""

	for dkey in dictdata.keys():
		value = dictdata[dkey]
		newvalue = "${EMPTY}"
		print("process_dict dkey: ", dkey, "	value:", value, type(value))

		if value is None:
			newvalue = "${None}"
		if isinstance(value, str) or isinstance(value, int):
			newvalue = find_variable(dkey, str(value))
			# dictdata[key] = newvalue

		if isinstance(value, list):
			dkeyname = keyname + "_" + dkey
			newvalue, paramlst = process_list(dkeyname, value)
			dictconstr.extend(paramlst)

		if isinstance(value, dict):
			dkeyname = keyname + "_" + dkey
			newvalue, paramlst = process_dict(dkeyname, value)
			dictconstr.extend(paramlst)

		dicttems = dicttems + "		" + dkey + "=" + newvalue


	print("process_dict dictdata: ", dictdata)
	dictconstr.append("&{" + keyname + "}=		Create Dictionary" + dicttems)
	print("new robot line:",dictconstr[-1])

	return (dictparam, dictconstr)

def process_list(key, listdata):
	# keyname = "l_"+key
	keyname = key
	dictparam = "${"+keyname+"}"
	dictconstr = []
	listitems = ""
	for i in range(len(listdata)):
		skey = "{}_{}".format(key, i)
		svalue = listdata[i]
		newvalue = ""
		print("skey: ", skey, "	svalue:", svalue, type(svalue))
		if isinstance(svalue, str) or isinstance(svalue, int):
			newvalue = find_variable(skey, str(svalue))

		if isinstance(svalue, list):
			newvalue, paramlst = process_list(skey, svalue)
			dictconstr.extend(paramlst)

		if isinstance(svalue, dict):
			newvalue, paramlst = process_dict(skey, svalue)
			dictconstr.extend(paramlst)

		listitems = listitems + "		" + newvalue

	dictconstr.append("@{" + keyname + "}=		Create List" + listitems)
	print("new robot line:",dictconstr[-1])

	return (dictparam, dictconstr)


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
	# sortedpages = har["log"]["pages"]
	# print("sortedpages:", sortedpages)

	# sort pages
	sortedentries = sorted(har["log"]["entries"], key=lambda k: iso2sec(k["startedDateTime"]))
	# sortedentries = har["log"]["entries"]
	# print("sortedentries:", sortedentries)

	e0time = iso2sec(sortedentries[0]["startedDateTime"])-0.002

	i = 0
	for page in sortedpages:
		# pagetime = int(iso2sec(page["startedDateTime"]))
		# if i+1 == len(sortedpages):
			# nextpagetime = int(datetime.timestamp(datetime.now()))
		# else:
			# nextpagetime = int(iso2sec(sortedpages[i+1]["startedDateTime"]))
		pagetime = iso2sec(page["startedDateTime"])-0.002
		if i==0 and pagetime>e0time:
			pagetime=e0time
		if i+1 == len(sortedpages):
			nextpagetime = datetime.timestamp(datetime.now())
		else:
			nextpagetime = iso2sec(sortedpages[i+1]["startedDateTime"])-0.002

		kwname = kwbname + " " + page["id"]
		print(kwname, "pagetime:", pagetime, "	nextpagetime:", nextpagetime)

		add_keyword(kwname, page["title"])

		for e in sortedentries:
			# print(e)
			print("e URL:", e["request"]["method"], e["request"]["url"])

			# etime = int(iso2sec(e["startedDateTime"]))
			etime = iso2sec(e["startedDateTime"])
			print("e time:", etime)
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
		dir = sorted(os.listdir(pathin))
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
