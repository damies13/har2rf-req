import sys
import json
import os
from datetime import datetime
import dateutil.parser
import re
import inspect

import urllib.parse
import html


import modules.h2r_html


class har2rfreq():

	pathin = None
	pathout = None
	outdata = {}
	workingdata = {}

	debuglvl = 6

	def __init__(self):
		# self.debugmsg(9, sys.argv)
		self.debugmsg(0, "har2rfreq")
		if len(sys.argv) < 2:
			self.display_help()

		self.debugmsg(9, "Run init_modules")
		self.init_modules()
		self.debugmsg(9, "Run init_outdata")
		self.init_outdata()

		self.pathin = os.path.abspath(sys.argv[1])
		self.debugmsg(9, "self.pathin:", self.pathin)
		self.pathout = os.path.dirname(self.pathin)
		self.debugmsg(9, "self.pathout:", self.pathout)

		self.debugmsg(9, "Run process_files")
		self.process_files()

	def init_modules(self):
		self.h2r_html = modules.h2r_html.h2r_html(self)

	def display_help(self):
		self.debugmsg(0, "")
		self.debugmsg(0, "Help")
		self.debugmsg(0, "")
		self.debugmsg(0, sys.argv[0], "<path to har file>")
		self.debugmsg(0, "")

	def debugmsg(self, lvl, *msg):
		msglst = []
		prefix = ""
		# self.debugmsg(9, self.debuglvl >= lvl, self.debuglvl, lvl, *msg)
		if self.debuglvl >= lvl:
			try:
				if self.debuglvl >= 4:
					stack = inspect.stack()
					the_class = stack[1][0].f_locals["self"].__class__.__name__
					the_method = stack[1][0].f_code.co_name
					the_line = stack[1][0].f_lineno
					prefix = "{}: {}({}): [{}:{}]	".format(str(the_class), the_method, the_line, self.debuglvl, lvl)
					if len(prefix.strip())<32:
						prefix = "{}	".format(prefix)
					if len(prefix.strip())<24:
						prefix = "{}	".format(prefix)

					msglst.append(str(prefix))

				for itm in msg:
					msglst.append(str(itm))
				print(" ".join(msglst))
			except:
				pass

	def process_files(self):

		if os.path.exists(self.pathin):
			if os.path.isdir(self.pathin):
				self.pathout = self.pathin
				tc = os.path.split(self.pathin)[-1]
				self.debugmsg(9, "tc:", tc)
				self.add_test_case(tc)
				# get robot files
				# dir = os.scandir(pathin)
				dir = sorted(os.listdir(self.pathin))
				# self.debugmsg(9, "dir:", dir)
				for item in dir:
					self.debugmsg(9, "item:", item, ".har ==", os.path.splitext(item)[1].lower())
					if os.path.splitext(item)[1].lower() == ".har":
						harpath = os.path.join(self.pathin, item)
						self.debugmsg(9, "harpath:", harpath)
						self.process_har(harpath)

			else:
				# tc = os.path.split(os.path.dirname(pathin))[-1]
				harfilename = os.path.basename(self.pathin)
				tc = os.path.splitext(harfilename)[0]


				self.debugmsg(9, "tc:", tc)
				self.add_test_case(tc)
				self.process_har(self.pathin)

			self.save_robot(self.pathout)

		else:
			import glob
			file_list = glob.glob(self.pathin)
			# self.debugmsg(9, file_list)
			if len(file_list)>0:
				for item in file_list:
					tc = os.path.split(os.path.dirname(item))[-1]
					self.debugmsg(9, "tc:", tc)
					self.add_test_case(tc)
					self.process_har(item)
				self.save_robot(self.pathout)



	def init_outdata(self):
		self.debugmsg(9, "__init__")
		# self.outdata = {"*** Settings ***": ["Library	RequestsLibrary", "Library	String"], "*** Variables ***": [], "*** Test Cases ***": {}, "*** Keywords ***": {}}
		self.outdata["*** Settings ***"] = ["Library	RequestsLibrary", "Library	String"]
		self.outdata["*** Variables ***"] = []
		self.outdata["*** Test Cases ***"] = {}
		self.outdata["*** Keywords ***"] = {}

		self.outdata["*** Keywords ***"]["Get Substring LRB"] = []
		self.outdata["*** Keywords ***"]["Get Substring LRB"].append("[Documentation]	Get Substring using Left and Right Boundaries")
		self.outdata["*** Keywords ***"]["Get Substring LRB"].append("[Arguments]    ${string}	${LeftB}	${RightB}")
		self.outdata["*** Keywords ***"]["Get Substring LRB"].append("${left}= 	Fetch From Right 	${string}	${LeftB}")
		self.outdata["*** Keywords ***"]["Get Substring LRB"].append("${match}= 	Fetch From Left 	${left} 	${RightB}")
		self.outdata["*** Keywords ***"]["Get Substring LRB"].append("[Return]	${match}")



	def load_har(self, harfile):

		with open(harfile, "rb") as f:
			hardata = f.read()
			hartxt = hardata.decode("utf-8")
		# self.debugmsg(9, "hartxt:", hartxt)
		har = json.loads(hartxt)
		self.workingdata["har"] = har
		return har

	def save_robot(self, pathout):
		# self.debugmsg(9, self.outdata)
		ofname = os.path.join(pathout, self.workingdata["testcase"]+".robot")
		self.debugmsg(9, ofname)
		if os.path.exists(ofname):
			os.remove(ofname)

		with open(ofname, "a") as of:
			for section in self.outdata:
				of.write(section + '\n')
				if section in ["*** Settings ***", "*** Variables ***"]:
					for line in self.outdata[section]:
						of.write(line + '\n')

				if section in ["*** Test Cases ***", "*** Keywords ***"]:
					for k in self.outdata[section]:
						of.write(k + '\n')
						for line in self.outdata[section][k]:
							of.write("	"+line + '\n')
						of.write('\n')

				of.write('\n')

	def find_estep(self, respno, kwname):
		starts = "${resp_"+str(respno)+"}"
		i = 0
		for e in self.outdata["*** Keywords ***"][kwname]:
			# self.debugmsg(9, starts, " | ", e)
			if e.startswith(starts):
				i += 1
				# self.debugmsg(9, "i:", i, starts, " | ", e)
				return i
			i += 1

		return -1

	def find_variable(self, key, value):

		self.debugmsg(6, "")
		self.debugmsg(6, "key:", key, "	value:", value)

		if value.strip() != value:
			value = value.strip()
			self.debugmsg(6, "key:", key, "	value:", value)

		newvalue = value
		decvalue = self.decode_value(value)
		kwname = self.workingdata["keyword"]

		if len(value.strip())<1:
			return "${EMPTY}"

		# self.debugmsg(9, "self.find_variable	key:", key, "	value:", value)

		self.debugmsg(6, "has value already been found")

		if "paramnames" not in self.workingdata:
			self.workingdata["paramnames"] = {}
		if "paramvalues" not in self.workingdata:
			self.workingdata["paramvalues"] = {}

		possiblekeys = ["${"+key+"}"]
		possiblekeyn = [key]
		i = 1
		newname = key+"_"+str(i)
		# self.debugmsg(9, "newname:", newname, self.workingdata["paramnames"])
		while newname in self.workingdata["paramnames"]:
			possiblekeys.append("${"+newname+"}")
			possiblekeyn.append(newname)
			i += 1
			newname = key+"_"+str(i)
			# self.debugmsg(9, "newname:", newname)
		self.debugmsg(8, "possiblekeys:", possiblekeys)

		if decvalue in self.workingdata["paramvalues"]:
			self.debugmsg(8, "decvalue key:", self.workingdata["paramvalues"][decvalue], " <=> ", possiblekeys)
			if self.workingdata["paramvalues"][decvalue] in possiblekeys:
				newvalue = self.workingdata["paramvalues"][decvalue]
				return newvalue

		# self.debugmsg(9, "self.find_variable	paramvalues")
		# self.debugmsg(9, "value:", value, self.workingdata["paramvalues"].keys())
		if newvalue == value and value in self.workingdata["paramvalues"]:
			# self.debugmsg(9, "value:", value, "	paramvalues:", self.workingdata["paramvalues"][value])
			self.debugmsg(8, "value key:", self.workingdata["paramvalues"][value], " <=> ", possiblekeys)
			if self.workingdata["paramvalues"][value] in possiblekeys:
				newvalue = self.workingdata["paramvalues"][value]
				return newvalue

		# self.debugmsg(9, "self.find_variable	paramnames")
		# self.debugmsg(9, "value:", value, self.workingdata["paramnames"].keys())
		if newvalue == value and key in self.workingdata["paramnames"]:
			# self.debugmsg(9, "key:", key, "	paramnames:", self.workingdata["paramnames"][key])
			for keyi in possiblekeyn:
				self.debugmsg(8, "keyi:", keyi, "	oval: ", self.workingdata["paramnames"][keyi]["oval"], " <=> ", decvalue)
				if self.workingdata["paramnames"][keyi]["oval"] == decvalue:
					newvalue = self.workingdata["paramnames"][keyi]["nval"]
					return newvalue
				self.debugmsg(8, "keyi:", keyi, "	oval: ", self.workingdata["paramnames"][keyi]["oval"], " <=> ", value)
				if self.workingdata["paramnames"][keyi]["oval"] == value:
					newvalue = self.workingdata["paramnames"][keyi]["nval"]
					return newvalue

		self.debugmsg(6, "is value timestamp now")
		if newvalue == value and value.isdigit() and len(value)>9:
			# check if it was the timestamp at the time of the request in the har file
			sseconds = value[0:10]
			# self.debugmsg(9, "sseconds:", sseconds, "	value:", value)
			intvar = int(sseconds)
			# intime = datetime.fromtimestamp(intvar)
			# self.debugmsg(9, "intime:", intime, "	intvar:", intvar)
			ec = self.workingdata["entrycount"]
			# self.debugmsg(9, "ec:", ec)
			entry = self.workingdata["har"]["log"]["entries"][ec]
			startedDateTime = entry["startedDateTime"]
			# self.debugmsg(8, "startedDateTime:", startedDateTime, "	intvar:", intvar)
			reqtime = dateutil.parser.isoparse(startedDateTime)
			# self.debugmsg(8, "reqtime:", reqtime)
			cseconds = datetime.timestamp(reqtime)
			# timediff = (reqtime - intime).total_seconds()
			timediff = abs(cseconds - intvar)
			self.debugmsg(8, "timediff:", timediff, "	intvar:", intvar, "	cseconds:", cseconds)
			# self.debugmsg(9, "timediff:", timediff)
			if timediff < 60:
				line = "${TS}=		Get Time		epoch"
				self.outdata["*** Keywords ***"][kwname].append(line)
				newvalue = "${TS}"
				return newvalue


		self.debugmsg(6, "is value request's date")
		ec = self.workingdata["entrycount"]
		# self.debugmsg(9, "ec:", ec)
		entry = self.workingdata["har"]["log"]["entries"][ec]
		startedDateTime = entry["startedDateTime"]
		# self.debugmsg(8, "startedDateTime:", startedDateTime)
		reqtime = dateutil.parser.isoparse(startedDateTime)
		# self.debugmsg(8, "reqtime:", reqtime, reqtime.strftime("%Y-%m-%d"))
		reqlst = {}
		reqlst[reqtime.strftime("%Y-%m-%d")] = "%Y-%m-%d"  # ISO Date
		reqlst[reqtime.strftime("%d/%m/%Y")] = "%d/%m/%Y"  # UK Date
		reqlst[reqtime.strftime("%d.%m.%Y")] = "%d.%m.%Y"  # EU Date
		reqlst[reqtime.strftime("%d-%m-%Y")] = "%d-%m-%Y"  # Other Date
		reqlst[reqtime.strftime("%m/%d/%Y")] = "%m/%d/%Y"  # US Date
		reqlst[reqtime.strftime("%m-%d-%Y")] = "%m-%d-%Y"  # US Date -
		reqlst[reqtime.strftime("%m.%d.%Y")] = "%m.%d.%Y"  # US Date .
		if newvalue == value and value in list(reqlst.keys()):
			sformat = reqlst[value]
			self.debugmsg(8, "sformat:", sformat)

			vformat = sformat.replace("%Y", "${yyyy}").replace("%m", "${mm}").replace("%d", "${dd}")
			self.debugmsg(8, "vformat:", vformat)
			# ${yyyy} 	${mm} 	${dd} = 	Get Time 	year,month,day
			line = "${yyyy} 	${mm} 	${dd}= 	Get Time 	year,month,day"
			self.outdata["*** Keywords ***"][kwname].append(line)

			line = "${"+key+"}=		Set Variable		" + vformat
			self.outdata["*** Keywords ***"][kwname].append(line)

			line = "Set Global Variable		${"+key+"} 	${"+key+"}"
			self.outdata["*** Keywords ***"][kwname].append(line)

			newvalue = "${"+key+"}"
			return newvalue

		self.debugmsg(6, "is value today's date")
		todaylst = {}
		todaylst[datetime.now().strftime("%Y-%m-%d")] = "%Y-%m-%d"  # ISO Date
		todaylst[datetime.now().strftime("%d/%m/%Y")] = "%d/%m/%Y"  # UK Date
		todaylst[datetime.now().strftime("%d.%m.%Y")] = "%d.%m.%Y"  # EU Date
		todaylst[datetime.now().strftime("%d-%m-%Y")] = "%d-%m-%Y"  # Other Date
		todaylst[datetime.now().strftime("%m/%d/%Y")] = "%m/%d/%Y"  # US Date
		todaylst[datetime.now().strftime("%m-%d-%Y")] = "%m-%d-%Y"  # US Date -
		todaylst[datetime.now().strftime("%m.%d.%Y")] = "%m.%d.%Y"  # US Date .
		if newvalue == value and value in list(todaylst.keys()):
			self.debugmsg(6, "value is today's date", value)
			idx = list(todaylst.keys()).index(value)
			self.debugmsg(8, "idx", idx, "	todaylst:", todaylst.keys())
			sformat = todaylst[value]
			self.debugmsg(8, "sformat:", sformat)

			vformat = sformat.replace("%Y", "${yyyy}").replace("%m", "${mm}").replace("%d", "${dd}")
			self.debugmsg(8, "vformat:", vformat)
			# ${yyyy} 	${mm} 	${dd} = 	Get Time 	year,month,day
			line = "${yyyy} 	${mm} 	${dd} = 	Get Time 	year,month,day"
			self.outdata["*** Keywords ***"][kwname].append(line)

			line = "${"+key+"}=		Set Variable		" + vformat
			self.outdata["*** Keywords ***"][ekwname].insert(estep, line)

			line = "Set Global Variable		${"+key+"}	${"+key+"}"
			self.outdata["*** Keywords ***"][ekwname].insert(estep, line)

			newvalue = "${"+key+"}}"
			return newvalue




		# self.debugmsg(9, "self.find_variable	history")
		# search history to try and find it
		if newvalue == value and "history" in self.workingdata:
			# self.debugmsg(9, "Searching History")
			for e in self.workingdata["history"]:

				resp = e["entrycount"]+1
				ekwname = e["kwname"]
				estep = self.find_estep(resp, ekwname)

				# check headers
				self.debugmsg(6, "is value in headers")
				for h in e["response"]["headers"]:
					if h["value"] == value and h["name"] == key:
						# self.debugmsg(9, "found value (",value,") and key (",key,") in header for ", e["request"]["url"])

						newkey = self.saveparam(key, value)

						line = "Set Global Variable		${"+newkey+"}	${resp_"+str(resp)+".headers[\""+key+"\"]}"

						self.outdata["*** Keywords ***"][ekwname].insert(estep, line)

						newvalue = "${"+newkey+"}"
						return newvalue

					searchstrings = []
					searchstrings.append(value)
					if value != decvalue:
						searchstrings.append(decvalue)
					htmlx = self.h2r_html.htmlx_encode(decvalue)
					if htmlx != decvalue:
						searchstrings.append(htmlx)
					htmlx = self.h2r_html.htmlX_encode(decvalue)
					if htmlx != decvalue:
						searchstrings.append(htmlx)
					urlenc = self.urlencode_value(decvalue)
					if urlenc != decvalue:
						searchstrings.append(urlenc)


					for searchstring in searchstrings:
						if newvalue == value and searchstring in h["value"]:
							lbound, rbound = self.find_in_string(key, searchstring, h["value"])
							self.debugmsg(9, "lbound:", lbound, "	rbound:", rbound)

							if len(lbound)>0 and len(rbound)==0:
								# no need to find rbound
								newkey = self.saveparam(key, searchstring)

								line = "${"+newkey+"}=		Fetch From Right		${resp_" + str(resp) + ".headers[\"" + h["name"] + "\"]}		" + lbound
								self.outdata["*** Keywords ***"][ekwname].insert(estep, line)

								estep += 1

								line = "Set Global Variable		${"+newkey+"}	${"+newkey+"}"
								self.outdata["*** Keywords ***"][ekwname].insert(estep, line)

								newvalue = "${"+newkey+"}"
								return newvalue

							if len(lbound)>0 and len(rbound)>0:
								newkey = self.saveparam(key, searchstring)

								line = "${"+newkey+"}=		Get Substring LRB		${resp_" + str(resp) + ".headers[\"" + h["name"] + "\"]}		"+lbound+"		"+rbound
								self.outdata["*** Keywords ***"][ekwname].insert(estep, line)

								estep += 1

								line = "Set Global Variable		${"+newkey+"}	${"+newkey+"}"
								self.outdata["*** Keywords ***"][ekwname].insert(estep, line)

								newvalue = "${"+newkey+"}"
								return newvalue




				# check Cookies
				self.debugmsg(6, "is value in cookies")
				for c in e["response"]["cookies"]:
					if c["value"] == value and c["name"] == key:
						# self.debugmsg(9, "found value (",value,") and key (",key,") in cookies for ", e["request"]["url"])

						newkey = self.saveparam(key, value)

						line = "Set Global Variable		${"+newkey+"}	${resp_"+str(resp)+".cookies[\""+key+"\"]}"

						self.outdata["*** Keywords ***"][ekwname].insert(estep, line)

						newvalue = "${"+newkey+"}"
						return newvalue

				# check body
				self.debugmsg(6, "is value in response body")
				if "text" in e["response"]["content"]:
					self.debugmsg(8, "response content has text")

					# check body for raw value
					if value in e["response"]["content"]["text"]:
						self.debugmsg(8, "found value (",value,") in body for ", e["request"]["url"])

						start = 0
						while newvalue == value and start >=0:
							self.debugmsg(9, "body:", e["response"]["content"]["text"])
							self.debugmsg(8, "start:", start, "looking for value:", value)
							pos = e["response"]["content"]["text"].find(value, start)
							self.debugmsg(8, "pos:", pos)
							if pos >=0:
								offset = len(key)*2 + len(value)*2
								self.debugmsg(8, "offset:", offset)
								# excerpt = e["response"]["content"]["text"][(pos-len(key)*2):(pos+len(value)*2)]
								excerpt = e["response"]["content"]["text"][(pos-len(key)-100):(pos+len(value)+100)]
								self.debugmsg(8, "excerpt:", excerpt)
								# excerpt = e["response"]["content"]["text"][(pos-len(key)-offset):(pos+len(value)+offset)]

								srchkey = key
								if key in ['NoKey']:
									self.debugmsg(8, "Special case:", key)
									srchkey = "?"

								if key[0] == '_':
									srchkey = key[1:]


								if srchkey in excerpt:
									# self.debugmsg(9, e["kwname"], "	step:", e["step"], "	entrycount:", e["entrycount"])
									self.debugmsg(8, "found key (",srchkey,") in excerpt:", "|{}|".format(excerpt))

									kpos = excerpt.find(srchkey)
									vpos = excerpt.find(value, kpos)
									if vpos > kpos:
										self.debugmsg(8, "kpos:", kpos, "vpos:", vpos)
										fullprefix = excerpt[0:vpos].strip()
										prefixarr = fullprefix.splitlines()
										prefix = prefixarr[-1].strip()
										self.debugmsg(8, "prefix: |{}|".format(prefix))

										# self.debugmsg(9, "excerpt:", excerpt)
										self.debugmsg(8, "vpos:", vpos, "	len(value):", len(value), "")
										spos = vpos+len(value)
										self.debugmsg(8, "spos:", spos, "	spos+5:", spos+5)
										#	# suffix = excerpt[spos:5]
										#	presuffix = excerpt[kpos:(vpos+len(value)+3)]
										#	self.debugmsg(9, "presuffix: |{}|".format(presuffix))
										#	# suffix = presuffix[-3:-1]
										#	suffix = presuffix[-3:len(presuffix)].strip()

										fullsuffix = excerpt[spos:len(excerpt)]
										suffixarr = fullsuffix.splitlines()
										suffix = suffixarr[0].strip()
										self.debugmsg(8, "suffix: |{}|".format(suffix))


										# line = "${left}= 	Fetch From Right 	${resp_"+str(resp)+".text} 	"+prefix
										# self.outdata["*** Keywords ***"][ekwname].insert(e["step"], line)
										# # self.debugmsg(9, line)

										# line = "${"+key+"}= 	Fetch From Left 	${left} 	"+suffix
										# self.outdata["*** Keywords ***"][ekwname].insert(e["step"]+1, line)
										# # self.debugmsg(9, line)

										newkey = self.saveparam(key, value)

										# test match with prefix and suffix works as expected?
										# find prefix from right
										ml = e["response"]["content"]["text"].rfind(prefix)+len(prefix)
										# find suffix from left
										mr = e["response"]["content"]["text"].find(suffix, ml)
										# get match
										match = e["response"]["content"]["text"][ml:mr]
										# self.debugmsg(9, "ml:", ml, "	mr:", mr, "	match:", match, "	value:", value)

										goffset = 1
										if match == value:

											line = "${"+newkey+"}=		Get Substring LRB		${resp_"+str(resp)+".text}		"+prefix+"		"+suffix
											self.outdata["*** Keywords ***"][ekwname].insert(estep, line)


										else:
											reprefix = re.escape(prefix)
											resuffix = re.escape(suffix)

											# test re pattern
											pattern = reprefix+"(.*?)"+resuffix
											# e["response"]["content"]["text"]
											retest = re.search(pattern, e["response"]["content"]["text"]).group(0)

											self.debugmsg(8, "retest:", retest)

											reprefix = re.escape(prefix).replace('"', r'\"').replace("\\", r"\\")
											resuffix = re.escape(suffix).replace('"', r'\"').replace("\\", r"\\")

											# line = "${regx_match}=		Get Lines Matching Regexp		${resp_"+str(resp)+".text}		"+reprefix+"(.*?)"+resuffix
											line = "${regx_match}=		evaluate		re.search(\"" + reprefix + "(.*?)" + resuffix + "\", \"\"\"${resp_"+str(resp)+".text}\"\"\").group(0)		re"

											self.outdata["*** Keywords ***"][ekwname].insert(estep, line)
											line = "${"+newkey+"}=		Get Substring LRB		${regx_match}		"+prefix+"		"+suffix
											self.outdata["*** Keywords ***"][ekwname].insert(estep+1, line)

											goffset += 1


										line = "Set Global Variable		${"+newkey+"}"
										self.outdata["*** Keywords ***"][ekwname].insert(estep+goffset, line)



										newvalue = "${"+newkey+"}"
										self.debugmsg(8, "newvalue:", newvalue)
										return newvalue

								start = pos+len(value)
							else:
								start = pos
							# else:
								# self.debugmsg(9, "didn't find key (",key,") in excerpt:", excerpt)


					# check body for decoded value
					if value != decvalue and decvalue in e["response"]["content"]["text"]:
						self.debugmsg(8, "found value (",decvalue,") in body for ", e["request"]["url"])

						searchval = decvalue
						start = 0
						while newvalue == value and start >=0:
							# self.debugmsg(9, "body:", e["response"]["content"]["text"])
							# self.debugmsg(9, "start:", start, "looking for value:", value)
							pos = e["response"]["content"]["text"].find(searchval, start)
							# self.debugmsg(9, "pos:", pos)
							if pos >=0:
								offset = len(key)*2 + len(decvalue)*2
								# excerpt = e["response"]["content"]["text"][(pos-len(key)*2):(pos+len(value)*2)]
								excerpt = e["response"]["content"]["text"][(pos-len(key)-100):(pos+len(searchval)+100)]
								# excerpt = e["response"]["content"]["text"][(pos-len(key)-offset):(pos+len(value)+offset)]
								if key in excerpt:
									# self.debugmsg(9, e["kwname"], "	step:", e["step"], "	entrycount:", e["entrycount"])
									self.debugmsg(9, "found key (",key,") in excerpt:", "|{}|".format(excerpt))

									ekwname = e["kwname"]

									kpos = excerpt.find(key)
									vpos = excerpt.find(searchval, kpos)
									if vpos > kpos:
										self.debugmsg(9, "kpos:", kpos, "vpos:", vpos)
										fullprefix = excerpt[0:vpos].strip()
										prefixarr = fullprefix.splitlines()
										prefix = prefixarr[-1].strip()
										self.debugmsg(9, "prefix: |{}|".format(prefix))

										# self.debugmsg(9, "excerpt:", excerpt)
										self.debugmsg(9, "vpos:", vpos, "	len(value):", len(searchval), "")
										spos = vpos+len(searchval)
										self.debugmsg(9, "spos:", spos, "	spos+5:", spos+5)
										#	# suffix = excerpt[spos:5]
										#	presuffix = excerpt[kpos:(vpos+len(value)+3)]
										#	self.debugmsg(9, "presuffix: |{}|".format(presuffix))
										#	# suffix = presuffix[-3:-1]
										#	suffix = presuffix[-3:len(presuffix)].strip()

										fullsuffix = excerpt[spos:len(excerpt)]
										suffixarr = fullsuffix.splitlines()
										suffix = suffixarr[0].strip()
										self.debugmsg(9, "suffix: |{}|".format(suffix))

										resp = e["entrycount"]+1

										# line = "${left}= 	Fetch From Right 	${resp_"+str(resp)+".text} 	"+prefix
										# self.outdata["*** Keywords ***"][ekwname].insert(e["step"], line)
										# # self.debugmsg(9, line)

										# line = "${"+key+"}= 	Fetch From Left 	${left} 	"+suffix
										# self.outdata["*** Keywords ***"][ekwname].insert(e["step"]+1, line)
										# # self.debugmsg(9, line)

										estep = self.find_estep(resp, ekwname)

										newkey = self.saveparam(key, searchval)

										# test match with prefix and suffix works as expected?
										# find prefix from right
										ml = e["response"]["content"]["text"].rfind(prefix)+len(prefix)
										# find suffix from left
										mr = e["response"]["content"]["text"].find(suffix, ml)
										# get match
										match = e["response"]["content"]["text"][ml:mr]
										# self.debugmsg(9, "ml:", ml, "	mr:", mr, "	match:", match, "	value:", value)

										goffset = 1
										if match == searchval:

											line = "${"+newkey+"}=		Get Substring LRB		${resp_"+str(resp)+".text}		"+prefix+"		"+suffix
											self.outdata["*** Keywords ***"][ekwname].insert(estep, line)


										else:
											reprefix = re.escape(prefix)
											resuffix = re.escape(suffix)

											# test re pattern
											pattern = reprefix+"(.*?)"+resuffix
											# e["response"]["content"]["text"]
											retest = re.search(pattern, e["response"]["content"]["text"]).group(0)

											self.debugmsg(9, "retest:", retest)

											reprefix = re.escape(prefix).replace('"', r'\"').replace("\\", r"\\")
											resuffix = re.escape(suffix).replace('"', r'\"').replace("\\", r"\\")

											# line = "${regx_match}=		Get Lines Matching Regexp		${resp_"+str(resp)+".text}		"+reprefix+"(.*?)"+resuffix
											line = "${regx_match}=		evaluate		re.search(\"" + reprefix + "(.*?)" + resuffix + "\", \"\"\"${resp_"+str(resp)+".text}\"\"\").group(0)		re"

											self.outdata["*** Keywords ***"][ekwname].insert(estep, line)
											line = "${"+newkey+"}=		Get Substring LRB		${regx_match}		"+prefix+"		"+suffix
											self.outdata["*** Keywords ***"][ekwname].insert(estep+1, line)

											goffset += 1


										line = "Set Global Variable		${"+newkey+"}"
										self.outdata["*** Keywords ***"][ekwname].insert(estep+goffset, line)



										newvalue = "${"+newkey+"}"
										self.debugmsg(9, "newvalue:", newvalue)
										return newvalue
								start = pos+len(value)
							else:
								start = pos



					htmlvalue = html.escape(decvalue)
					self.debugmsg(8, "Try to find decvalue (", decvalue, ") as html encoded value (", htmlvalue, ")")
					# check body for html enc value
					if value != htmlvalue and htmlvalue in e["response"]["content"]["text"]:
						self.debugmsg(9, "found value (", htmlvalue, ") in body for ", e["request"]["url"])

						searchval = htmlvalue
						start = 0
						while newvalue == value and start >=0:
							# self.debugmsg(9, "body:", e["response"]["content"]["text"])
							# self.debugmsg(9, "start:", start, "looking for value:", value)
							pos = e["response"]["content"]["text"].find(searchval, start)
							# self.debugmsg(9, "pos:", pos)
							if pos >=0:
								offset = len(key)*2 + len(decvalue)*2
								# excerpt = e["response"]["content"]["text"][(pos-len(key)*2):(pos+len(value)*2)]
								excerpt = e["response"]["content"]["text"][(pos-len(key)-100):(pos+len(searchval)+100)]
								# excerpt = e["response"]["content"]["text"][(pos-len(key)-offset):(pos+len(value)+offset)]
								if key in excerpt:
									# self.debugmsg(9, e["kwname"], "	step:", e["step"], "	entrycount:", e["entrycount"])
									self.debugmsg(9, "found key (",key,") in excerpt:", "|{}|".format(excerpt))

									ekwname = e["kwname"]

									kpos = excerpt.find(key)
									vpos = excerpt.find(searchval, kpos)
									if vpos > kpos:
										self.debugmsg(9, "kpos:", kpos, "vpos:", vpos)
										fullprefix = excerpt[0:vpos].strip()
										prefixarr = fullprefix.splitlines()
										prefix = prefixarr[-1].strip()
										self.debugmsg(9, "prefix: |{}|".format(prefix))

										# self.debugmsg(9, "excerpt:", excerpt)
										self.debugmsg(9, "vpos:", vpos, "	len(value):", len(searchval), "")
										spos = vpos+len(searchval)
										self.debugmsg(9, "spos:", spos, "	spos+5:", spos+5)
										#	# suffix = excerpt[spos:5]
										#	presuffix = excerpt[kpos:(vpos+len(value)+3)]
										#	self.debugmsg(9, "presuffix: |{}|".format(presuffix))
										#	# suffix = presuffix[-3:-1]
										#	suffix = presuffix[-3:len(presuffix)].strip()

										fullsuffix = excerpt[spos:len(excerpt)]
										suffixarr = fullsuffix.splitlines()
										suffix = suffixarr[0].strip()
										self.debugmsg(9, "suffix: |{}|".format(suffix))

										resp = e["entrycount"]+1

										# line = "${left}= 	Fetch From Right 	${resp_"+str(resp)+".text} 	"+prefix
										# self.outdata["*** Keywords ***"][ekwname].insert(e["step"], line)
										# # self.debugmsg(9, line)

										# line = "${"+key+"}= 	Fetch From Left 	${left} 	"+suffix
										# self.outdata["*** Keywords ***"][ekwname].insert(e["step"]+1, line)
										# # self.debugmsg(9, line)

										estep = self.find_estep(resp, ekwname)

										newkey = self.saveparam(key, searchval)

										# test match with prefix and suffix works as expected?
										# find prefix from right
										ml = e["response"]["content"]["text"].rfind(prefix)+len(prefix)
										# find suffix from left
										mr = e["response"]["content"]["text"].find(suffix, ml)
										# get match
										match = e["response"]["content"]["text"][ml:mr]
										# self.debugmsg(9, "ml:", ml, "	mr:", mr, "	match:", match, "	value:", value)

										goffset = 1
										if match == searchval:

											line = "${"+newkey+"}=		Get Substring LRB		${resp_"+str(resp)+".text}		"+prefix+"		"+suffix
											self.outdata["*** Keywords ***"][ekwname].insert(estep, line)


										else:
											reprefix = re.escape(prefix)
											resuffix = re.escape(suffix)

											# test re pattern
											pattern = reprefix+"(.*?)"+resuffix
											# e["response"]["content"]["text"]
											retest = re.search(pattern, e["response"]["content"]["text"]).group(0)

											self.debugmsg(9, "retest:", retest)

											reprefix = re.escape(prefix).replace('"', r'\"').replace("\\", r"\\")
											resuffix = re.escape(suffix).replace('"', r'\"').replace("\\", r"\\")

											# line = "${regx_match}=		Get Lines Matching Regexp		${resp_"+str(resp)+".text}		"+reprefix+"(.*?)"+resuffix
											line = "${regx_match}=		evaluate		re.search(\"" + reprefix + "(.*?)" + resuffix + "\", \"\"\"${resp_"+str(resp)+".text}\"\"\").group(0)		re"

											self.outdata["*** Keywords ***"][ekwname].insert(estep, line)
											line = "${"+newkey+"}=		Get Substring LRB		${regx_match}		"+prefix+"		"+suffix
											self.outdata["*** Keywords ***"][ekwname].insert(estep+1, line)

											goffset += 1


										line = "Set Global Variable		${"+newkey+"}"
										self.outdata["*** Keywords ***"][ekwname].insert(estep+goffset, line)



										newvalue = "${"+newkey+"}"
										return newvalue
								start = pos+len(value)
							else:
								start = pos


					self.debugmsg(8, "decvalue:", decvalue, type(decvalue))
					htmlvalue = urllib.parse.quote(decvalue)
					self.debugmsg(8, "htmlvalue:", htmlvalue)
					# htmlvalue = re.sub(r'%(.?.?)', r'&#x\1;', htmlvalue)
					htmlvalue = self.h2r_html.htmlx_encode(decvalue)
					self.debugmsg(8, "htmlvalue:", htmlvalue)
					self.debugmsg(8, "Try to find decvalue (", decvalue, ") as html encoded value (", htmlvalue, ")")
					# check body for html enc value
					if value != htmlvalue and htmlvalue in e["response"]["content"]["text"]:
						self.debugmsg(8, "found value (", htmlvalue, ") in body for ", e["request"]["url"])

						searchval = htmlvalue
						start = 0
						while newvalue == value and start >=0:
							# self.debugmsg(9, "body:", e["response"]["content"]["text"])
							# self.debugmsg(9, "start:", start, "looking for value:", value)
							pos = e["response"]["content"]["text"].find(searchval, start)
							# self.debugmsg(9, "pos:", pos)
							if pos >=0:
								offset = len(key)*2 + len(decvalue)*2
								# excerpt = e["response"]["content"]["text"][(pos-len(key)*2):(pos+len(value)*2)]
								excerpt = e["response"]["content"]["text"][(pos-len(key)-100):(pos+len(searchval)+100)]
								# excerpt = e["response"]["content"]["text"][(pos-len(key)-offset):(pos+len(value)+offset)]
								if key in excerpt:
									# self.debugmsg(9, e["kwname"], "	step:", e["step"], "	entrycount:", e["entrycount"])
									self.debugmsg(8, "found key (",key,") in excerpt:", "|{}|".format(excerpt))

									ekwname = e["kwname"]

									kpos = excerpt.find(key)
									vpos = excerpt.find(searchval, kpos)
									if vpos > kpos:
										self.debugmsg(8, "kpos:", kpos, "vpos:", vpos)
										fullprefix = excerpt[0:vpos].strip()
										prefixarr = fullprefix.splitlines()
										prefix = prefixarr[-1].strip()
										self.debugmsg(8, "prefix: |{}|".format(prefix))

										# self.debugmsg(9, "excerpt:", excerpt)
										self.debugmsg(8, "vpos:", vpos, "	len(value):", len(searchval), "")
										spos = vpos+len(searchval)
										self.debugmsg(8, "spos:", spos, "	spos+5:", spos+5)
										#	# suffix = excerpt[spos:5]
										#	presuffix = excerpt[kpos:(vpos+len(value)+3)]
										#	self.debugmsg(9, "presuffix: |{}|".format(presuffix))
										#	# suffix = presuffix[-3:-1]
										#	suffix = presuffix[-3:len(presuffix)].strip()

										fullsuffix = excerpt[spos:len(excerpt)]
										suffixarr = fullsuffix.splitlines()
										suffix = suffixarr[0].strip()
										self.debugmsg(8, "suffix: |{}|".format(suffix))

										resp = e["entrycount"]+1

										# line = "${left}= 	Fetch From Right 	${resp_"+str(resp)+".text} 	"+prefix
										# self.outdata["*** Keywords ***"][ekwname].insert(e["step"], line)
										# # self.debugmsg(9, line)

										# line = "${"+key+"}= 	Fetch From Left 	${left} 	"+suffix
										# self.outdata["*** Keywords ***"][ekwname].insert(e["step"]+1, line)
										# # self.debugmsg(9, line)

										estep = self.find_estep(resp, ekwname)

										newkey = self.saveparam(key, searchval)

										# test match with prefix and suffix works as expected?
										# find prefix from right
										ml = e["response"]["content"]["text"].rfind(prefix)+len(prefix)
										# find suffix from left
										mr = e["response"]["content"]["text"].find(suffix, ml)
										# get match
										match = e["response"]["content"]["text"][ml:mr]
										# self.debugmsg(9, "ml:", ml, "	mr:", mr, "	match:", match, "	value:", value)

										goffset = 1
										if match == searchval:

											line = "${"+newkey+"}=		Get Substring LRB		${resp_"+str(resp)+".text}		"+prefix+"		"+suffix
											self.outdata["*** Keywords ***"][ekwname].insert(estep, line)


										else:
											reprefix = re.escape(prefix)
											resuffix = re.escape(suffix)

											# test re pattern
											pattern = reprefix+"(.*?)"+resuffix
											# e["response"]["content"]["text"]
											retest = re.search(pattern, e["response"]["content"]["text"]).group(0)

											self.debugmsg(8, "retest:", retest)

											reprefix = re.escape(prefix).replace('"', r'\"').replace("\\", r"\\")
											resuffix = re.escape(suffix).replace('"', r'\"').replace("\\", r"\\")

											# line = "${regx_match}=		Get Lines Matching Regexp		${resp_"+str(resp)+".text}		"+reprefix+"(.*?)"+resuffix
											line = "${regx_match}=		evaluate		re.search(\"" + reprefix + "(.*?)" + resuffix + "\", \"\"\"${resp_"+str(resp)+".text}\"\"\").group(0)		re"

											self.outdata["*** Keywords ***"][ekwname].insert(estep, line)
											line = "${"+newkey+"}=		Get Substring LRB		${regx_match}		"+prefix+"		"+suffix
											self.outdata["*** Keywords ***"][ekwname].insert(estep+1, line)

											goffset += 1



										line = "${"+newkey+"}		Evaluate		html.unescape('${"+newkey+"}')		html"
										self.outdata["*** Keywords ***"][ekwname].insert(estep+goffset, line)

										goffset += 1

										line = "Set Global Variable		${"+newkey+"}"
										self.outdata["*** Keywords ***"][ekwname].insert(estep+goffset, line)



										newvalue = "${"+newkey+"}"
										self.debugmsg(8, "newvalue:", newvalue)
										return newvalue
								start = pos+len(value)
							else:
								start = pos



		# self.debugmsg(9, "find_variable	Last resort")
		# Last resort if it didn't exist anywhere, so create it as a hard coded variable
		if newvalue != decvalue:
			self.debugmsg(6, "Last resort if value didn't exist anywhere")
			newvalue = decvalue
			newkey = self.saveparam(key, decvalue)
			line = "${"+newkey+"}		"+decvalue
			self.outdata["*** Variables ***"].append(line)

			newvalue = "${"+newkey+"}"
			self.debugmsg(8, "last resort", newkey, newvalue)
			return newvalue

		if newvalue == value:
			self.debugmsg(6, "Last resort if value didn't exist anywhere")

			newkey = self.saveparam(key, value)

			line = "${"+newkey+"}		"+value
			self.outdata["*** Variables ***"].append(line)

			newvalue = "${"+newkey+"}"
			self.debugmsg(8, "last resort", newkey, newvalue)
			return newvalue


		return newvalue

	def find_in_string(self, key, searchval, instr):
		self.debugmsg(9, "find_in_string key:", key, "	searchval:", searchval, "	instr:", instr)

		start = 0
		kpos = instr.find(key, start)
		if kpos>0:
			start = kpos + len(key)
		vpos = instr.find(searchval, start)
		lbound = ""
		rbound = ""
		self.debugmsg(9, "kpos:", kpos, "	vpos:", vpos)
		if kpos<0 and len(searchval)<10:
			# probability of returning an unrelated value match is too high
			return (lbound, rbound)

		if kpos>0 and kpos<vpos:
			lbound = instr[kpos:vpos]
		if len(lbound)==0 and vpos>10:
			lbound = instr[vpos-10:vpos]
		if len(lbound)==0 and vpos>0 and vpos<10:
			lbound = instr[:vpos]

		self.debugmsg(9, "lbound:", lbound)
		vepos = vpos+len(searchval)
		if vepos == len(instr) and len(lbound)>0:
			# no need to find rbound
			return (lbound, rbound)

		rlen = len(instr) - vepos
		self.debugmsg(9, "rlen:", rlen, "	and right:", instr[vepos:])
		if rlen < 11:
			rbound = instr[vepos:]

		if rlen > 10:
			rbound = instr[vepos:vepos+10]

		self.debugmsg(9, "rbound:", rbound)
		return (lbound, rbound)


	def urlencode_value(self, value):
		newvalue = value
		if isinstance(value, str):
			# self.debugmsg(9, "urlencode_value value:", value)
			if '%' in newvalue:
				newvalue = urllib.parse.unquote_plus(newvalue)
			# self.debugmsg(9, "urlencode_value newvalue:", newvalue)
		return newvalue

	def decode_value(self, value):
		newvalue = value
		if isinstance(value, str):
			self.debugmsg(9, "decode_value value:", value)
			if '%' in newvalue:
				newvalue = urllib.parse.unquote_plus(newvalue)

			self.debugmsg(9, "decode_value newvalue:", newvalue)
		return newvalue

	def process_entry(self, entry):


		self.debugmsg(9, entry)
		self.debugmsg(7, entry["request"]["method"], entry["request"]["url"])

		kwname = self.workingdata["keyword"]

		# add extra info to entry
		entry["kwname"] = kwname
		entry["entrycount"] = self.workingdata["entrycount"]


		if "session" not in self.workingdata:
			self.add_session()
			# add initial headers
			hdrs = ""
			cook = ""
			updatesess = 0
			for h in entry["request"]["headers"]:
				self.debugmsg(9, "h:", h["name"], h["value"])
				specialh = ["cookie", "accept-encoding"]
				if h["name"].lower() not in specialh and h["name"][0] != ":":
					# hdrs[h["name"]] = h["value"]
					value = self.find_variable(h["name"], h["value"])
					hdrs += "	" + h["name"] + "=" + value

				if h["name"].lower() == "cookie":
					clst = h["value"].split(";")
					for c in clst:
						citm = c.split("=")
						# cook[citm[0].strip()] = citm[1].strip()
						if citm[0].strip() not in ["_ga", "_gid"]:   # don't bother sending Google analytics cookies
							key = citm[0].strip()
							value = self.self.find_variable(key, citm[1].strip())
							cook += "	" + key + "=" + value

			line = "&{Headers}=		Create dictionary" + hdrs
			self.outdata["*** Keywords ***"][kwname].append(line)

			# line = "Log 	${Headers}"
			# self.outdata["*** Keywords ***"][kwname].append(line)

			line = "&{Cookies}=		Create dictionary" + cook
			self.outdata["*** Keywords ***"][kwname].append(line)

			# line = "Log 	${Cookies}"
			# self.outdata["*** Keywords ***"][kwname].append(line)

			line = "Update Session	" + self.workingdata["session"] + "	${Headers}	${Cookies}"
			self.outdata["*** Keywords ***"][kwname].append(line)


		argdata = ""

		# headers

		hdrs = ""
		for h in entry["request"]["headers"]:
			self.debugmsg(8, "h:", h["name"], h["value"])
			specialh = ["cookie", "accept-encoding", "content-length"]	# , "pragma", "cache-control"
			if h["name"].lower() not in specialh and h["name"][0] != ":":
				# hdrs[h["name"]] = h["value"]
				value = self.find_variable(h["name"], h["value"])
				hdrs += "	" + h["name"] + "=" + value
		if len(hdrs)>0:
			line = "&{Req_Headers}=		Create dictionary" + hdrs
			self.outdata["*** Keywords ***"][kwname].append(line)
			argdata += "	" + "headers=${Req_Headers}"


		# GET
		# GET
		# GET
		if entry["request"]["method"] == "GET":
			statuscode = entry["response"]["status"]
			if statuscode == 302:
				argdata += "	" + "expected_status={}".format(statuscode)
				argdata += "	" + "allow_redirects=${False}"
				# if "redirecturl" not in self.workingdata:
					# self.workingdata["redirecturl"] = entry["request"]["url"].replace(self.workingdata["baseurl"], "")
			else:
				argdata += "	" + "expected_status={}".format(statuscode)


			if "redirecturl" in self.workingdata:
				del self.workingdata["redirecturl"]
			else:
				self.workingdata["entrycount"] += 1
				ec = self.workingdata["entrycount"]
				path = entry["request"]["url"].replace(self.workingdata["baseurl"], "")
				patharr = path.split("?")
				if len(patharr)>1:
					path = patharr[0]
					params = ""

					parrin = patharr[1].split("&")
					parrout = []
					for p in parrin:
						if "=" in p:
							key, value = p.split("=", 1)
							newvalue = self.find_variable(key, value)
							parrout.append("=".join([key, newvalue]))
						else:
							key = "${EMPTY}"
							newvalue = self.find_variable("NoKey", p)
							parrout.append("=".join([key, newvalue]))

					params = "	".join(parrout)

					dname = "params_{}".format(ec)
					line = "&{"+dname+"}=		Create dictionary	" + params
					self.outdata["*** Keywords ***"][kwname].append(line)
					argdata += "	" + "params=${"+dname+"}"

				resp = "resp_{}".format(ec)
				line = "${"+resp+"}=		GET On Session		" + self.workingdata["session"] + "		url=" + path + argdata
				self.outdata["*** Keywords ***"][kwname].append(line)

				# line = "Log 	${"+resp+".text}"
				# self.outdata["*** Keywords ***"][kwname].append(line)

		# POST
		# POST
		# POST
		if entry["request"]["method"] == "POST":

			self.workingdata["entrycount"] += 1
			ec = self.workingdata["entrycount"]

			path = entry["request"]["url"].replace(self.workingdata["baseurl"], "")

			patharr = path.split("?")
			if len(patharr)>1:
				path = patharr[0]
				params = ""

				parrin = patharr[1].split("&")
				parrout = []
				for p in parrin:
					key, value = p.split("=", 1)
					newvalue = self.find_variable(key, value)
					parrout.append("=".join([key, newvalue]))

				params = "	".join(parrout)

				dname = "params_{}".format(ec)
				line = "&{"+dname+"}=		Create dictionary	" + params
				self.outdata["*** Keywords ***"][kwname].append(line)
				argdata += "	" + "params=${"+dname+"}"



			if "postData" in entry["request"]:
				pd_try = True
				pd = entry["request"]["postData"]
				if pd_try and "params" in pd:
					pd_try = False
					dictdata = ""
					for param in pd["params"]:
						newvalue = self.find_variable(param["name"], param["value"])
						dictdata += "	" + param["name"] + "=" + newvalue

					dname = "postdata_{}".format(ec)
					line = "&{"+dname+"}=		Create dictionary" + dictdata
					self.outdata["*** Keywords ***"][kwname].append(line)
					argdata += "	" + "data=${"+dname+"}"

				if pd_try and "text" in pd and pd["text"][0] == "{":
					pd_try = False
					jsondata = json.loads(pd["text"])
					dname = "json_{}".format(ec)
					paramname, lines = self.process_dict(dname, jsondata)
					self.debugmsg(8, "paramname:", paramname, "	paramlst:", paramlst)
					self.outdata["*** Keywords ***"][kwname].extend(lines)
					argdata += "	" + "json="+paramname


			statuscode = entry["response"]["status"]
			if statuscode == 302:
				argdata += "	" + "expected_status={}".format(statuscode)
				argdata += "	" + "allow_redirects=${False}"
				# if "redirecturl" not in self.workingdata:
					# self.workingdata["redirecturl"] = entry["request"]["url"].replace(self.workingdata["baseurl"], "")
			else:
				argdata += "	" + "expected_status={}".format(statuscode)


			resp = "resp_{}".format(ec)
			line = "${"+resp+"}=		POST On Session		" + self.workingdata["session"] + "		url=" + path + argdata
			self.outdata["*** Keywords ***"][kwname].append(line)
			# line = "Log 	${"+resp+".text}"
			# self.outdata["*** Keywords ***"][kwname].append(line)


		# append entry to history
		entry["step"] = len(self.outdata["*** Keywords ***"][kwname])+1
		if "history" not in self.workingdata:
			self.workingdata["history"] = []
		self.workingdata["history"].append(entry)

	def process_dict(self, key, dictdata):
		# keyname = "d_"+key
		keyname = key
		dictparam = "${"+keyname+"}"
		dictconstr = []
		dicttems = ""

		for dkey in dictdata.keys():
			value = dictdata[dkey]
			newvalue = "${EMPTY}"
			self.debugmsg(9, "self.process_dict dkey: ", dkey, "	value:", value, type(value))

			if value is None:
				newvalue = "${None}"
			if isinstance(value, str) or isinstance(value, int):
				newvalue = self.find_variable(dkey, str(value))
				# dictdata[key] = newvalue

			if isinstance(value, list):
				dkeyname = keyname + "_" + dkey
				newvalue, paramlst = process_list(dkeyname, value)
				dictconstr.extend(paramlst)

			if isinstance(value, dict):
				dkeyname = keyname + "_" + dkey
				newvalue, paramlst = self.process_dict(dkeyname, value)
				dictconstr.extend(paramlst)

			dicttems = dicttems + "		" + dkey + "=" + newvalue


		self.debugmsg(9, "self.process_dict dictdata: ", dictdata)
		dictconstr.append("&{" + keyname + "}=		Create Dictionary" + dicttems)
		self.debugmsg(9, "new robot line:",dictconstr[-1])

		return (dictparam, dictconstr)

	def process_list(self, key, listdata):
		# keyname = "l_"+key
		keyname = key
		dictparam = "${"+keyname+"}"
		dictconstr = []
		listitems = ""
		for i in range(len(listdata)):
			skey = "{}_{}".format(key, i)
			svalue = listdata[i]
			newvalue = ""
			self.debugmsg(9, "skey: ", skey, "	svalue:", svalue, type(svalue))
			if isinstance(svalue, str) or isinstance(svalue, int):
				newvalue = self.find_variable(skey, str(svalue))

			if isinstance(svalue, list):
				newvalue, paramlst = process_list(skey, svalue)
				dictconstr.extend(paramlst)

			if isinstance(svalue, dict):
				newvalue, paramlst = self.process_dict(skey, svalue)
				dictconstr.extend(paramlst)

			listitems = listitems + "		" + newvalue

		dictconstr.append("@{" + keyname + "}=		Create List" + listitems)
		self.debugmsg(9, "new robot line:",dictconstr[-1])

		return (dictparam, dictconstr)


	def saveparam(self, name, value):
		#


		newname = name
		if name in self.workingdata["paramnames"]:
			i = 0
			while newname in self.workingdata["paramnames"]:
				self.debugmsg(9, "newname:", newname)
				i += 1
				newname = name + "_{}".format(i)

			self.debugmsg(9, "newname:", newname)


		if "paramnames" not in self.workingdata:
			self.workingdata["paramnames"] = {}
		if newname not in self.workingdata["paramnames"]:
			# self.workingdata["paramnames"].append(newname)
			self.workingdata["paramnames"][newname] = {}
			self.workingdata["paramnames"][newname]["nval"] = "${"+newname+"}"
			self.workingdata["paramnames"][newname]["oval"] = value

		if "paramvalues" not in self.workingdata:
			self.workingdata["paramvalues"] = {}
		if value not in self.workingdata["paramvalues"]:
			self.workingdata["paramvalues"][value] = "${"+newname+"}"

		self.debugmsg(9, "saved", "${"+newname+"}", "=", value)
		return newname

	def add_test_case(self, tcname):
		if tcname not in self.outdata["*** Test Cases ***"]:
			self.outdata["*** Test Cases ***"][tcname] = []
			self.workingdata["testcase"] = tcname

	def add_keyword(self, kwname, comment):



		if "testcase" not in self.workingdata:
			add_test_case(kwname)

		tcname = self.workingdata["testcase"]

		if kwname not in self.outdata["*** Keywords ***"]:
			self.outdata["*** Keywords ***"][kwname] = []
			self.workingdata["keyword"] = kwname
			# self.workingdata["entrycount"] = 0
			self.workingdata["entrycount"] = -1

			self.outdata["*** Keywords ***"][kwname].append("[Documentation] 	" + tcname + "	|	" + kwname + "	|	" + comment)
			self.outdata["*** Test Cases ***"][tcname].append(kwname)

	def add_session(self):



		tcname = self.workingdata["testcase"]
		url = self.workingdata["har"]["log"]["entries"][0]["request"]["url"]
		self.debugmsg(9, "url", url)
		urlarr = url.split("/")
		self.debugmsg(9, "urlarr", urlarr)
		basearr = [urlarr[0],urlarr[1],urlarr[2]]
		sessionname = "sess_" + urlarr[2].replace(".", "_")
		# baseurl = basearr.join("/")
		baseurl = "/".join(basearr)
		self.workingdata["baseurl"] = baseurl
		self.workingdata["session"] = sessionname
		# self.outdata["*** Settings ***"].append("Suite Setup           Create Session    " + sessionname + " 	" +	baseurl)
		self.outdata["*** Test Cases ***"][tcname].insert(0, "Create Session    " + sessionname + " 	" +	baseurl + " 	disable_warnings=1")

	def iso2sec(self, isotime):
		reqtime = dateutil.parser.isoparse(isotime)
		# self.debugmsg(9, "reqtime:", reqtime)
		cseconds = datetime.timestamp(reqtime)
		return cseconds

	def process_har(self, harfile):
		har = self.load_har(harfile)
		# self.debugmsg(9, har)
		harfilename = os.path.basename(harfile)
		kwbname = os.path.splitext(harfilename)[0]

		# sort pages
		sortedpages = sorted(har["log"]["pages"], key=lambda k: self.iso2sec(k["startedDateTime"]))
		# sortedpages = har["log"]["pages"]
		# self.debugmsg(9, "sortedpages:", sortedpages)

		# sort pages
		sortedentries = sorted(har["log"]["entries"], key=lambda k: self.iso2sec(k["startedDateTime"]))
		# sortedentries = har["log"]["entries"]
		# self.debugmsg(9, "sortedentries:", sortedentries)

		e0time = self.iso2sec(sortedentries[0]["startedDateTime"])-0.002
		self.debugmsg(9, "e0time:", e0time)

		i = 0
		j = 0
		for page in sortedpages:
			# pagetime = int(iso2sec(page["startedDateTime"]))
			# if i+1 == len(sortedpages):
				# nextpagetime = int(datetime.timestamp(datetime.now()))
			# else:
				# nextpagetime = int(iso2sec(sortedpages[i+1]["startedDateTime"]))
			pagetime = self.iso2sec(page["startedDateTime"])-0.002
			self.debugmsg(9, "pagetime:", pagetime)
			if i==0 and pagetime>e0time:
				pagetime=e0time
				self.debugmsg(9, "pagetime:", pagetime)
			if i+1 == len(sortedpages):
				nextpagetime = datetime.timestamp(datetime.now())
			else:
				nextpagetime = self.iso2sec(sortedpages[i+1]["startedDateTime"])-0.002

			kwname = kwbname + " " + page["id"]
			self.debugmsg(9, kwname, "pagetime:", pagetime, "	nextpagetime:", nextpagetime)

			self.add_keyword(kwname, page["title"])

			for e in sortedentries:
				# self.debugmsg(9, e)
				self.debugmsg(5, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j)
				self.debugmsg(7, "e URL:", e["request"]["method"], e["request"]["url"])

				# etime = int(iso2sec(e["startedDateTime"]))
				etime = self.iso2sec(e["startedDateTime"])
				self.debugmsg(9, "e time:", etime)
				if etime >= pagetime and etime < nextpagetime:
					# self.debugmsg(9, "etime:", etime)
					self.process_entry(e)


				j += 1
				# if j>37:
				# 	break

			i += 1



if __name__ == "__main__":
	h2r = har2rfreq()

#
