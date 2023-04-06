import sys
import json
import os
from datetime import datetime
import dateutil.parser
import argparse
import inspect

import urllib.parse


class har2rfreq():

	version = "0.0.2"

	pathin = None
	pathout = None
	outdata = {}
	workingdata = {}

	encoders = {}
	decoders = {}
	parsers = {}
	parserdata = {}
	processors = {}
	limit = 0

	debuglvl = 0

	def __init__(self):
		# self.debugmsg(9, sys.argv)
		# self.debugmsg(0, "har2rfreq")
		# self.debugmsg(0, "	Version", self.version)

		parser = argparse.ArgumentParser(
							prog='har2rfreq',
							description='A tool for converting har files into robot framework tests using Requests Library',
							epilog='Version '+self.version)
		parser.add_argument('-g', '--debug', help='Set debug level, default level is 0')
		parser.add_argument('-l', '--limit', help='limit the number of requests to process, default level is 0 (unlimited)')
		parser.add_argument('-v', '--version', help='Display the version and exit', action='store_true')
		parser.add_argument('path', help='Path to har file or folder of har files')
		self.args = parser.parse_args()

		self.debugmsg(6, "self.args: ", self.args)

		if self.args.debug:
			self.debuglvl = int(self.args.debug)


		if self.args.version:
			exit()

		if self.args.limit:
			self.limit = int(self.args.limit)


		self.debugmsg(9, "Run init_modules")
		self.init_modules()
		self.debugmsg(9, "Run init_outdata")
		self.init_outdata()

		self.pathin = os.path.abspath(self.args.path)
		self.debugmsg(9, "self.pathin:", self.pathin)
		self.pathout = os.path.dirname(self.pathin)
		self.debugmsg(9, "self.pathout:", self.pathout)

		self.debugmsg(9, "Run process_files")
		self.process_files()

	def init_modules(self):

		imports = {}
		excluded_modules = ['h2r_template']

		self.debugmsg(9, 'dirname(__file__):    ', os.path.dirname(__file__))
		modulesdir = os.path.abspath(os.path.join(os.path.dirname(__file__), "modules"))
		self.debugmsg(7, 'modulesdir:    ', modulesdir)
		modules = os.listdir(modulesdir)
		self.debugmsg(9, 'modules:    ', modules)

		for module in modules:
			modname, ext = os.path.splitext(module)
			if ext == '.py' and modname not in excluded_modules:
				self.debugmsg(5, "loading module", modname)

				# import modules.h2r_base
				import_name = "modules."+modname
				self.debugmsg(9, "import_name:", import_name)
				imports[modname] = __import__(import_name)

				# self.h2r_base = modules.h2r_base.h2r_base(self)
				exec_str = "self."+modname+" = imports['"+modname+"']."+modname+"."+modname+"(self)"
				self.debugmsg(9, "exec_str:", exec_str)
				exec(exec_str)

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
		self.outdata["*** Keywords ***"]["Get Substring LRB"].append("[Documentation] 	Get Substring using Left and Right Boundaries")
		self.outdata["*** Keywords ***"]["Get Substring LRB"].append("[Arguments] 	${string} 	${LeftB} 	${RightB}")
		self.outdata["*** Keywords ***"]["Get Substring LRB"].append("${left}= 	Fetch From Right 	${string} 	${LeftB}")
		self.outdata["*** Keywords ***"]["Get Substring LRB"].append("${match}= 	Fetch From Left 	${left} 	${RightB}")
		self.outdata["*** Keywords ***"]["Get Substring LRB"].append("[Return] 	${match}")



	def load_har(self, harfile):
		self.debugmsg(3, "Loading har file:", harfile)
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
			self.debugmsg(1, "Robot file saved:", ofname)

	def find_estep(self, respno, kwname):
		starts = "${resp_"+str(respno)+"}"
		i = 0
		self.debugmsg(9, "i:", i, starts)
		for e in self.outdata["*** Keywords ***"][kwname]:
			self.debugmsg(9, "i:", i, starts, " | ", e)
			if e.startswith(starts):
				i += 1
				self.debugmsg(9, "i:", i, starts, " | ", e)
				return i
			i += 1

		# this is basically a not found condition
		i = -1
		self.debugmsg(9, "ret i:", i, starts)
		return i

	def find_variable(self, key, value, lastresort=True):

		self.debugmsg(6, "")
		self.debugmsg(6, "key:", key, "	value:", value)

		# reset parserdata
		self.parserdata = {}
		self.parserdata["value"] = value
		self.parserdata["key"] = key


		kwname = self.workingdata["keyword"]
		self.debugmsg(8, "kwname:", kwname)
		self.parserdata["kwname"] = kwname
		self.parserdata["ekwname"] = None

		if len(value.strip())<1:
			return "${EMPTY}"

		newvalue = value

		self.debugmsg(6, "Construct list of various ways value might be provided")

		searchvals = {}
		searchvals[value] = []

		if value != value.strip():
			searchvals[value.strip()] = []

		self.debugmsg(6, "find if any decoders can decode the value")

		decoderlist = list(self.decoders.keys())
		decoderlist.sort()
		for decoder in decoderlist:
			self.debugmsg(5, "decoder:", decoder)
			priority, decodername = decoder.split(":")
			decval = eval(decodername +"(value)")
			self.debugmsg(8, "decval:", decval)
			if decval != value:
				searchvals[decval] = []
				searchvals[decval].append(decoder)
				# converters_needed.append(self.decoders[decval]["robotencode"])

		self.debugmsg(6, "find if any encoders can encode the original value or decoded values")

		encoderlist = list(self.encoders.keys())
		encoderlist.sort()
		for searchval in list(searchvals.keys()):
			for encoder in encoderlist:
				self.debugmsg(5, "encoder:", encoder)
				priority, encodername = encoder.split(":")
				evcval = eval(encodername +"(searchval)")
				self.debugmsg(8, "evcval:", evcval)
				if evcval != searchval and evcval not in searchvals.keys():
					searchvals[evcval] = []
					searchvals[evcval].append(encoder)
					# converters_needed.append(self.encoders[encoder]["robotdecode"])


		searchkeys = [key]

		if key[0] == '_':
			searchkeys.append(key[1:])


		self.debugmsg(8, "searchvals:", searchvals)
		self.debugmsg(8, "searchkeys:", searchkeys)

		self.parserdata["searchvals"] = searchvals
		self.parserdata["searchkeys"] = searchkeys

		if "paramnames" not in self.workingdata:
			self.workingdata["paramnames"] = {}
		if "paramvalues" not in self.workingdata:
			self.workingdata["paramvalues"] = {}

		parserlist = list(self.parsers.keys())
		parserlist.sort()
		for parser in parserlist:
			self.debugmsg(5, "parser:", parser)
			priority, parsername = parser.split(":")
			retvalue = eval(parsername +"()")
			self.debugmsg(8, "retvalue:", retvalue)
			if retvalue is not None:
				return retvalue

		if newvalue == value and lastresort:
			self.debugmsg(6, "Last resort if value didn't exist anywhere")

			newkey = self.saveparam(key, value)

			line = "${"+newkey+"} 	"+value
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

		if "processor" not in entry:
			entry["processor"] = {}

		kwname = self.workingdata["keyword"]

		# add extra info to entry
		entry["kwname"] = kwname
		self.workingdata["entrycount"] += 1
		entry["entrycount"] = int(self.workingdata["entrycount"])


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
					hdrs += " 	" + h["name"] + "=" + value
					self.workingdata["sessiondata"][h["name"]] = value

				if h["name"].lower() == "cookie":
					clst = h["value"].split(";")
					for c in clst:
						citm = c.split("=")
						# cook[citm[0].strip()] = citm[1].strip()
						if citm[0].strip() not in ["_ga", "_gid"]:   # don't bother sending Google analytics cookies
							key = citm[0].strip()
							value = self.self.find_variable(key, citm[1].strip())
							cook += " 	" + key + "=" + value
							self.workingdata["cookiedata"][key] = value

			line = "&{Headers}= 	Create dictionary" + hdrs
			self.outdata["*** Keywords ***"][kwname].append(line)

			# line = "Log 	${Headers}"
			# self.outdata["*** Keywords ***"][kwname].append(line)

			line = "&{Cookies}= 	Create dictionary" + cook
			self.outdata["*** Keywords ***"][kwname].append(line)

			# line = "Log 	${Cookies}"
			# self.outdata["*** Keywords ***"][kwname].append(line)

			line = "Update Session	" + self.workingdata["session"] + "	${Headers}	${Cookies}"
			self.outdata["*** Keywords ***"][kwname].append(line)


		processorlist = list(self.processors.keys())
		processorlist.sort()
		for processor in processorlist:
			self.debugmsg(5, "processor:", processor)
			priority, processorname = processor.split(":")
			entry = eval(processorname +"(entry)")

		self.debugmsg(9, entry)

		argdata = ""

		if "argdata" in entry["processor"] and len(entry["processor"]["argdata"].strip())>0:
			argdata += " 	" + entry["processor"]["argdata"].strip()
			self.debugmsg(8, "argdata:", argdata)

		path = "/todo"
		if "path" in entry["processor"]:
			path = entry["processor"]["path"]
			self.debugmsg(6, "path:", path)

			if len(path) > 1:
				newpath = self.find_variable("path", path)
				if newpath is not None and len(newpath) > 1 and newpath != path:
					self.debugmsg(6, "newpath:", newpath)
					path = newpath

		self.debugmsg(6, "path:", path)
		action = entry["request"]["method"]
		resp = "resp_{}".format(entry["entrycount"])
		line = "${"+resp+"}= 	" + action + " On Session 	" + self.workingdata["session"] + " 	url=" + path + argdata
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

			dicttems = dicttems + " 	" + dkey + "=" + newvalue


		self.debugmsg(9, "self.process_dict dictdata: ", dictdata)
		dictconstr.append("&{" + keyname + "}= 	Create Dictionary" + dicttems)
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

			listitems = listitems + " 	" + newvalue

		dictconstr.append("@{" + keyname + "}= 	Create List" + listitems)
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
			self.debugmsg(3, "New test case:", tcname)

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
			self.debugmsg(3, "New keyword:", kwname)

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
		self.workingdata["sessiondata"] = {}
		self.workingdata["cookiedata"] = {}
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
				self.debugmsg(7, "")
				self.debugmsg(7, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j)
				self.debugmsg(7, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j)
				self.debugmsg(7, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j, "j:", j)
				self.debugmsg(7, "")
				self.debugmsg(7, "e URL:", e["request"]["method"], e["request"]["url"])

				# etime = int(iso2sec(e["startedDateTime"]))
				etime = self.iso2sec(e["startedDateTime"])
				self.debugmsg(9, "e time:", etime)
				if etime >= pagetime and etime < nextpagetime:
					# self.debugmsg(9, "etime:", etime)
					self.process_entry(e)


				j += 1
				if self.limit>0 and j>self.limit:
					break

			i += 1



if __name__ == "__main__":
	h2r = har2rfreq()

#
