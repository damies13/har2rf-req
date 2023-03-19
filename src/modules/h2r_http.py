# template Module - This ,odule is not used, it's simply intended as a template for new modules

class h2r_http():
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
		psr = "01:self.h2r_http.response_headers"
		if psr not in self.parent.parsers:
			self.parent.parsers[psr] = {}

		psr = "01:self.h2r_http.response_cookies"
		if psr not in self.parent.parsers:
			self.parent.parsers[psr] = {}

		#
		# Register processors
		#
		pro = "01:self.h2r_http.request_uripath"
		if pro not in self.parent.processors:
			self.parent.processors[pro] = {}

		pro = "01:self.h2r_http.request_headers"
		if pro not in self.parent.processors:
			self.parent.processors[pro] = {}

		pro = "02:self.h2r_http.request_cookies"
		if pro not in self.parent.processors:
			self.parent.processors[pro] = {}

		pro = "02:self.h2r_http.request_statuscode"
		if pro not in self.parent.processors:
			self.parent.processors[pro] = {}







	#
	# Encoders
	#

	#
	# Decoders
	#

	#
	# Paersers
	#
	def response_headers(self):
		self.parent.debugmsg(6, "headers Parser")

		searchkeys = self.parent.parserdata["searchkeys"]
		searchvals = self.parent.parserdata["searchvals"]
		kwname = self.parent.parserdata["kwname"]
		key = self.parent.parserdata["key"]

		for searchval in searchvals.keys():
			self.parent.debugmsg(8, "searchval:", searchval)

			# search history to try and find it
			if "history" in self.parent.workingdata:
				# self.parent.debugmsg(9, "Searching History")
				for e in self.parent.workingdata["history"]:

					resp = e["entrycount"]+1
					ekwname = e["kwname"]
					estep = self.parent.find_estep(resp, ekwname)

					# check headers
					self.parent.debugmsg(6, "is searchval in headers:", searchval)
					for h in e["response"]["headers"]:
						if h["value"] == searchval and h["name"] in searchkeys:
							hkey = h["name"]
							self.parent.debugmsg(8, "found searchval (",searchval,") and hkey (",hkey,") for key (",key,") in header for ", e["request"]["url"])

							newkey = self.parent.saveparam(key, searchval)

							line = "Set Global Variable 	${"+newkey+"}	${resp_"+str(resp)+".headers[\""+hkey+"\"]}"

							self.parent.outdata["*** Keywords ***"][ekwname].insert(estep, line)

							newvalue = "${"+newkey+"}"
							return newvalue

						if searchval in h["value"]:
							lbound, rbound = self.parent.find_in_string(key, searchval, h["value"])
							self.parent.debugmsg(8, "lbound:", lbound, "	rbound:", rbound)

							if len(lbound)>0 and len(rbound)==0:
								# no need to find rbound
								newkey = self.parent.saveparam(key, searchval)

								line = "${"+newkey+"}= 	Fetch From Right 	${resp_" + str(resp) + ".headers[\"" + h["name"] + "\"]} 	" + lbound
								self.parent.outdata["*** Keywords ***"][ekwname].insert(estep, line)

								estep += 1

								line = "Set Global Variable 	${"+newkey+"}	${"+newkey+"}"
								self.parent.outdata["*** Keywords ***"][ekwname].insert(estep, line)

								newvalue = "${"+newkey+"}"
								return newvalue

							if len(lbound)>0 and len(rbound)>0:
								newkey = self.parent.saveparam(key, searchval)

								line = "${"+newkey+"}= 	Get Substring LRB 	${resp_" + str(resp) + ".headers[\"" + h["name"] + "\"]} 	"+lbound+" 	"+rbound
								self.parent.outdata["*** Keywords ***"][ekwname].insert(estep, line)

								estep += 1

								line = "Set Global Variable 	${"+newkey+"}	${"+newkey+"}"
								self.parent.outdata["*** Keywords ***"][ekwname].insert(estep, line)

								newvalue = "${"+newkey+"}"
								return newvalue


		return None


	def response_cookies(self):
		self.parent.debugmsg(6, "cookies Parser")

		searchkeys = self.parent.parserdata["searchkeys"]
		searchvals = self.parent.parserdata["searchvals"]
		kwname = self.parent.parserdata["kwname"]
		key = self.parent.parserdata["key"]

		for searchval in searchvals.keys():
			self.parent.debugmsg(8, "searchval:", searchval)

			# search history to try and find it
			if "history" in self.parent.workingdata:
				# self.parent.debugmsg(9, "Searching History")
				for e in self.parent.workingdata["history"]:

					resp = e["entrycount"]+1
					ekwname = e["kwname"]
					estep = self.parent.find_estep(resp, ekwname)


					# check Cookies
					self.parent.debugmsg(6, "is searchval in cookies:", searchval)
					for c in e["response"]["cookies"]:
						if c["value"] == searchval and c["name"] in searchkeys:
							ckey = c["name"]
							self.parent.debugmsg(8, "found searchval (",searchval,") and ckey (",ckey,") key (",key,") in cookies for ", e["request"]["url"])

							newkey = self.parent.saveparam(key, searchval)

							line = "Set Global Variable 	${"+newkey+"}	${resp_"+str(resp)+".cookies[\""+ckey+"\"]}"

							self.parent.outdata["*** Keywords ***"][ekwname].insert(estep, line)

							newvalue = "${"+newkey+"}"
							return newvalue



		return None

	#
	# processors
	#
	def request_uripath(self, entry):
		self.parent.debugmsg(6, "request statuscode")
		self.parent.debugmsg(9, "entry:", entry)

		kwname = entry["kwname"]
		argdata = ""

		path = entry["request"]["url"].replace(self.parent.workingdata["baseurl"], "")
		patharr = path.split("?")
		if len(patharr)>1:
			path = patharr[0]
			params = ""

			parrin = patharr[1].split("&")
			parrout = []
			for p in parrin:
				if "=" in p:
					key, value = p.split("=", 1)
					newvalue = self.parent.find_variable(key, value)
					parrout.append("=".join([key, newvalue]))
				else:
					key = "${EMPTY}"
					newvalue = self.parent.find_variable("NoKey", p)
					parrout.append("=".join([key, newvalue]))

			params = " 	".join(parrout)

			dname = "params_{}".format(entry["entrycount"])
			line = "&{"+dname+"}= 	Create dictionary 	" + params
			self.parent.outdata["*** Keywords ***"][kwname].append(line)
			argdata += " 	" + "params=${"+dname+"}"

		if len(argdata.strip()) >0:
			if "argdata" in entry["processor"]:
				entry["processor"]["argdata"] += argdata
			else:
				entry["processor"]["argdata"] = argdata

		if "path" in entry["processor"]:
			entry["processor"]["path"] += path
		else:
			entry["processor"]["path"] = path

		return entry

	def request_headers(self, entry):
		self.parent.debugmsg(6, "headers processor")
		self.parent.debugmsg(9, "entry:", entry)

		self.parent.debugmsg(8, "sessiondata:", self.parent.workingdata["sessiondata"])
		session = self.parent.workingdata["sessiondata"]

		# headers
		kwname = entry["kwname"]

		hdrs = ""
		for h in entry["request"]["headers"]:
			self.parent.debugmsg(8, "h:", h["name"], h["value"])
			specialh = ["cookie", "accept-encoding", "content-length"]	# , "pragma", "cache-control"
			if h["name"].lower() not in specialh and h["name"][0] != ":":
				# hdrs[h["name"]] = h["value"]
				value = self.parent.find_variable(h["name"], h["value"])
				if h["name"] not in session.keys() or session[h["name"]] != value:
					hdrs += " 	" + h["name"] + "=" + value
		if len(hdrs.strip())>0:
			line = "&{Req_Headers}= 	Create dictionary" + hdrs
			self.parent.outdata["*** Keywords ***"][kwname].append(line)
			# argdata += " 	" + "headers=${Req_Headers}"
			# entry["processor"]["headers"] = "${Req_Headers}"
			if "argdata" in entry["processor"]:
				entry["processor"]["argdata"] += " 	headers=${Req_Headers}"
			else:
				entry["processor"]["argdata"] = " 	headers=${Req_Headers}"


		return entry


	def request_cookies(self, entry):
		self.parent.debugmsg(6, "headers cookies")
		self.parent.debugmsg(9, "entry:", entry)

		# The original code didn't have do anthing to handle cookies beyond the original session
		# maybe by using the "On Session" keywords this is automatically handled?
		#  I'll leave this as a place holder function in case we need it in the future.

		return entry

	def request_statuscode(self, entry):
		self.parent.debugmsg(6, "request statuscode")
		self.parent.debugmsg(9, "entry:", entry)

		argdata = ""
		statuscode = entry["response"]["status"]
		if statuscode == 302:
			argdata += " 	" + "expected_status={}".format(statuscode)
			argdata += " 	" + "allow_redirects=${False}"
			# if "redirecturl" not in self.workingdata:
				# self.workingdata["redirecturl"] = entry["request"]["url"].replace(self.workingdata["baseurl"], "")
		elif statuscode > 0:
			argdata += " 	" + "expected_status={}".format(statuscode)

		if len(argdata.strip()) >0:
			if "argdata" in entry["processor"]:
				entry["processor"]["argdata"] += argdata
			else:
				entry["processor"]["argdata"] = argdata

		return entry


#
