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
		psr = "self.h2r_http.http_headers"
		if psr not in self.parent.parsers:
			self.parent.parsers[psr] = {}

		psr = "self.h2r_http.http_cookies"
		if psr not in self.parent.parsers:
			self.parent.parsers[psr] = {}






	#
	# Encoders
	#

	#
	# Decoders
	#

	#
	# Paersers
	#
	def http_headers(self):
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


	def http_cookies(self):
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
