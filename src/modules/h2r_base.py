# base Module - sudo Parsers, Endcoders and Decoders

from datetime import datetime
import dateutil.parser

class h2r_base():
	"""docstring for ."""

	def __init__(self, parent):
		# super(, self).__init__()
		self.parent = parent

		#
		# Register Encoders
		#

		#
		# Register Decoders
		#

		#
		# Register Paersers
		#

		ep = "00:self.h2r_base.existing_paramkey"
		if ep not in self.parent.parsers:
			self.parent.parsers[ep] = {}

		ep = "01:self.h2r_base.existing_paramval"
		if ep not in self.parent.parsers:
			self.parent.parsers[ep] = {}

		ep = "03:self.h2r_base.existing_paramsubval"
		if ep not in self.parent.parsers:
			self.parent.parsers[ep] = {}

		bp = "02:self.h2r_base.is_timestamp"
		if bp not in self.parent.parsers:
			self.parent.parsers[bp] = {}

		bp = "02:self.h2r_base.is_datetime"
		if bp not in self.parent.parsers:
			self.parent.parsers[bp] = {}




	#
	# Encoders
	#



	#
	# Decoders
	#



	#
	# Paersers
	#

	def existing_paramkey(self):
		self.parent.debugmsg(6, "has key already been found")

		searchvals = self.parent.parserdata["searchvals"]

		for searchkey in self.parent.parserdata["searchkeys"]:
			self.parent.debugmsg(8, "searchkey:", searchkey)

			self.parent.debugmsg(6, "has key already been found")

			possiblekeys = ["${"+searchkey+"}"]
			possiblekeyn = [searchkey]
			i = 1
			newname = searchkey+"_"+str(i)
			while newname in self.parent.workingdata["paramnames"]:
				possiblekeys.append("${"+newname+"}")
				possiblekeyn.append(newname)
				i += 1
				newname = searchkey+"_"+str(i)
				# self.debugmsg(9, "newname:", newname)
			self.parent.debugmsg(8, "possiblekeys:", possiblekeys)

			if searchkey in self.parent.workingdata["paramnames"]:
				for keyi in possiblekeyn:
					self.parent.debugmsg(8, "keyi:", keyi, "	oval: ", self.parent.workingdata["paramnames"][keyi]["oval"], " <=> ", searchvals)
					if self.parent.workingdata["paramnames"][keyi]["oval"] in searchvals:
						newvalue = self.parent.workingdata["paramnames"][keyi]["nval"]
						return newvalue
					self.parent.debugmsg(8, "keyi:", keyi, "	oval: ", self.parent.workingdata["paramnames"][keyi]["oval"], " <=> ", searchvals)
					if self.parent.workingdata["paramnames"][keyi]["oval"] in searchvals:
						newvalue = self.parent.workingdata["paramnames"][keyi]["nval"]
						return newvalue
		return None



	def existing_paramval(self):
		self.parent.debugmsg(6, "has value already been found")
		kwname = self.parent.parserdata["kwname"]
		key = self.parent.parserdata["key"]

		possiblekeys = []
		possiblekeyn = []
		for searchkey in self.parent.parserdata["searchkeys"]:
			possiblekeys.append("${"+searchkey+"}")
			possiblekeyn.append(searchkey)
			i = 1
			newname = searchkey+"_"+str(i)
			while newname in self.parent.workingdata["paramnames"]:
				possiblekeys.append("${"+newname+"}")
				possiblekeyn.append(newname)
				i += 1
				newname = searchkey+"_"+str(i)
				# self.debugmsg(9, "newname:", newname)
		self.parent.debugmsg(6, "possiblekeys:", possiblekeys)

		for searchval in self.parent.parserdata["searchvals"]:
			if searchval in self.parent.workingdata["paramvalues"]:
				self.parent.debugmsg(6, "value key:", self.parent.workingdata["paramvalues"][searchval], " <=> ", possiblekeys)
				if self.parent.workingdata["paramvalues"][searchval] in possiblekeys:
					newvalue = self.parent.workingdata["paramvalues"][searchval]
					return newvalue
				if len(searchval)>2:
					newvalue = self.parent.workingdata["paramvalues"][searchval]
					return newvalue

		return None

	def existing_paramsubval(self):
		self.parent.debugmsg(6, "has value already been found")
		kwname = self.parent.parserdata["kwname"]
		key = self.parent.parserdata["key"]

		possiblekeys = []
		possiblekeyn = []
		for searchkey in self.parent.parserdata["searchkeys"]:
			possiblekeys.append("${"+searchkey+"}")
			possiblekeyn.append(searchkey)
			i = 1
			newname = searchkey+"_"+str(i)
			while newname in self.parent.workingdata["paramnames"]:
				possiblekeys.append("${"+newname+"}")
				possiblekeyn.append(newname)
				i += 1
				newname = searchkey+"_"+str(i)
				# self.debugmsg(9, "newname:", newname)
		self.parent.debugmsg(6, "possiblekeys:", possiblekeys)

		for searchval in self.parent.parserdata["searchvals"]:

			for pval in self.parent.workingdata["paramvalues"]:
				if searchval in pval:
					pvalkey = self.parent.workingdata["paramvalues"][pval]
					self.parent.debugmsg(6, "searchval (", searchval, ") is substring of existing pval (", pval, ") pvalkey:", pvalkey)

					pvalkeyname = pvalkey
					if pvalkey[:2] == "${":
						pvalkeyname = pvalkey[2:-1]

					lenl = pval.find(searchval)
					lenr = lenl + len(searchval)

					spre = ""
					ssfx = ""
					if lenl > 0:
						spre = pval[:lenl]
					if lenr > 0:
						ssfx = pval[lenr:]

					if len(spre) > 1 and len(ssfx) > 1:
						# get lrb
						newkey = self.parent.saveparam(pvalkeyname + "_sub", searchval)
						# ${NoKey}= 	Get Substring LRB 	${resp_1.text} 	<link rel="icon" href="/web/dist/favicon.ico? 	">
						line = "${"+newkey+"}= 	Get Substring LRB 	" + pvalkey + " 	"+spre+" 	"+ssfx
						self.parent.debugmsg(6, "line:", line)
						self.parent.outdata["*** Keywords ***"][kwname].append(line)

						newvalue = "${"+newkey+"}"
						self.parent.debugmsg(6, "newvalue:", newvalue)
						return newvalue

					if len(spre) > 1 and len(ssfx) < 1:
						# get right
						newkey = self.parent.saveparam(pvalkeyname + "_sub", searchval)
						# ${left}= 	Fetch From Right 	${string} 	${LeftB}
						line = "${"+newkey+"}= 	Fetch From Right 	" + pvalkey + " 	"+spre
						self.parent.debugmsg(6, "line:", line)
						self.parent.outdata["*** Keywords ***"][kwname].append(line)

						newvalue = "${"+newkey+"}"
						self.parent.debugmsg(6, "newvalue:", newvalue)
						return newvalue

					if len(spre) < 1 and len(ssfx) > 1:
						# get left
						newkey = self.parent.saveparam(pvalkeyname + "_sub", searchval)
						# ${match}= 	Fetch From Left 	${left} 	${RightB}
						line = "${"+newkey+"}= 	Fetch From Left 	" + pvalkey + " 	"+ssfx
						self.parent.debugmsg(6, "line:", line)
						self.parent.outdata["*** Keywords ***"][kwname].append(line)

						newvalue = "${"+newkey+"}"
						self.parent.debugmsg(6, "newvalue:", newvalue)
						return newvalue

		return None


	def is_timestamp(self):
		self.parent.debugmsg(6, "is value timestamp now")

		kwname = self.parent.parserdata["kwname"]

		ec = self.parent.workingdata["entrycount"]
		entry = self.parent.workingdata["har"]["log"]["entries"][ec]
		startedDateTime = entry["startedDateTime"]
		reqtime = dateutil.parser.isoparse(startedDateTime)


		for searchval in self.parent.parserdata["searchvals"]:

			if searchval.isdigit() and len(searchval)>9:
				# check if it was the timestamp at the time of the request in the har file
				sseconds = searchval[0:10]
				# self.debugmsg(9, "sseconds:", sseconds, "	value:", value)
				intvar = int(sseconds)
				# self.debugmsg(9, "intime:", intime, "	intvar:", intvar)

				cseconds = datetime.timestamp(reqtime)

				timediff = abs(cseconds - intvar)
				self.parent.debugmsg(8, "timediff:", timediff, "	intvar:", intvar, "	cseconds:", cseconds)

				if timediff < 60:
					line = "${TS}=		Get Time		epoch"
					self.parent.outdata["*** Keywords ***"][kwname].append(line)
					newvalue = "${TS}"
					return newvalue

		return None


	def is_datetime(self):
		self.parent.debugmsg(6, "is value request's date")

		kwname = self.parent.parserdata["kwname"]
		key = self.parent.parserdata["key"]

		ec = self.parent.workingdata["entrycount"]
		entry = self.parent.workingdata["har"]["log"]["entries"][ec]
		startedDateTime = entry["startedDateTime"]
		reqtime = dateutil.parser.isoparse(startedDateTime)

		timelst = {}
		timelst[reqtime.strftime("%Y-%m-%d")] = "%Y-%m-%d"  # ISO Date
		timelst[reqtime.strftime("%d/%m/%Y")] = "%d/%m/%Y"  # UK Date
		timelst[reqtime.strftime("%d.%m.%Y")] = "%d.%m.%Y"  # EU Date
		timelst[reqtime.strftime("%d-%m-%Y")] = "%d-%m-%Y"  # Other Date
		timelst[reqtime.strftime("%m/%d/%Y")] = "%m/%d/%Y"  # US Date
		timelst[reqtime.strftime("%m-%d-%Y")] = "%m-%d-%Y"  # US Date -
		timelst[reqtime.strftime("%m.%d.%Y")] = "%m.%d.%Y"  # US Date .
		timelst[reqtime.strftime("%H:%M:%S")] = "%H:%M:%S"  # Time H:M:S
		timelst[reqtime.strftime("%H:%M")] = "%H:%M"  # Time H:M:S

		for searchval in self.parent.parserdata["searchvals"]:
			if searchval in list(timelst.keys()):
				sformat = timelst[searchval]
				self.parent.debugmsg(8, "sformat:", sformat)

				# >	Robot Framework variables, similarly as keywords, are case-insensitive
				vformat = sformat.replace("%Y", "${yr}").replace("%m", "${mth}").replace("%d", "${dy}").replace("%H", "${hr}").replace("%M", "${min}").replace("%S", "${sec}")
				self.parent.debugmsg(8, "vformat:", vformat)
				# ${yyyy} 	${mm} 	${dd} = 	Get Time 	year,month,day
				line = "${yr} 	${mth} 	${dy} 	${hr} 	${min} 	${sec}= 	Get Time 	year,month,day,hour,min,sec"
				self.parent.outdata["*** Keywords ***"][kwname].append(line)

				line = "${"+key+"}=		Set Variable		" + vformat
				self.parent.outdata["*** Keywords ***"][kwname].append(line)

				line = "Set Global Variable		${"+key+"} 	${"+key+"}"
				self.parent.outdata["*** Keywords ***"][kwname].append(line)

				newvalue = "${"+key+"}"
				return newvalue

		return None











#
