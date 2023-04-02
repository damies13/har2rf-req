# HTML Module - encoding and decoding HTML encoded values

import html
import re

class h2r_html():
	"""docstring for ."""

	def __init__(self, parent):
		# super(, self).__init__()
		self.parent = parent

		#
		# Register Encoders
		#

		html = "01:self.h2r_html.html_encode"
		if html not in self.parent.encoders:
			self.parent.encoders[html] = {}
			self.parent.encoders[html]["robottranscode"] = "self.h2r_html.html_robotdecode"

		htmlX = "03:self.h2r_html.htmlX_encode"
		if htmlX not in self.parent.encoders:
			self.parent.encoders[htmlX] = {}
			self.parent.encoders[htmlX]["robottranscode"] = "self.h2r_html.htmlX_robotdecode"

		htmlx = "03:self.h2r_html.htmlx_encode"
		if htmlx not in self.parent.encoders:
			self.parent.encoders[htmlx] = {}
			self.parent.encoders[htmlx]["robottranscode"] = "self.h2r_html.htmlX_robotdecode"

		#
		# Register Decoders
		#

		html = "00:self.h2r_html.html_decode"
		if html not in self.parent.encoders:
			self.parent.decoders[html] = {}
			self.parent.decoders[html]["robottranscode"] = "self.h2r_html.html_robotencode"

		#
		# Register Paersers
		#
		psr = "09:self.h2r_html.html_body"
		if psr not in self.parent.parsers:
			self.parent.parsers[psr] = {}
		#
		# Register processors
		#
		pro = "09:self.h2r_html.post_data_params"
		if pro not in self.parent.processors:
			self.parent.processors[pro] = {}




	#
	# Encoders
	#

	def html_encode(self, s):
		return html.escape(s)

	def htmlX_encode(self, s):
		# self.parent.debugmsg(0, "s:", s)
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
		# self.parent.debugmsg(0, "s:", s)
		return s

	def htmlx_encode(self, s):
		# self.parent.debugmsg(0, "s:", s)
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
		# self.parent.debugmsg(0, "s:", s)
		return s

	def html_robotencode(self, varin):
		varout = varin
		return varout

	#
	# Decoders
	#

	def html_decode(self, s):
		return html.unescape(s)


	def htmlX_robotdecode(self, varin):
		varout = varin
		return varout

	def html_robotdecode(self, varin):
		varout = varin
		return varout

	#
	# Paersers
	#

	def html_body(self):
		self.parent.debugmsg(6, "html body Parser")

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

					# resp = e["entrycount"]+1
					resp = e["entrycount"]
					ekwname = e["kwname"]
					estep = self.parent.find_estep(resp, ekwname)
					self.parent.debugmsg(6, "resp:", resp, "	ekwname:", ekwname, "	estep:", estep)

					# check body
					self.parent.debugmsg(8, "is value (" + searchval + ") in response body "+ str(e["entrycount"]) )
					if "text" in e["response"]["content"]:
						self.parent.debugmsg(8, "response content has text")

						# check body for raw value
						if searchval in e["response"]["content"]["text"]:
							self.parent.debugmsg(6, "value (" + searchval + ") is in response body "+ str(e["entrycount"]) )
							self.parent.debugmsg(6, "found searchval (",searchval,") in body for ", e["request"]["url"])

							start = 0
							while start >=0:
								self.parent.debugmsg(9, "body:", e["response"]["content"]["text"])
								self.parent.debugmsg(8, "start:", start, "looking for searchval:", searchval)
								pos = e["response"]["content"]["text"].find(searchval, start)
								self.parent.debugmsg(8, "pos:", pos)
								if pos >=0:
									offset = len(key)*2 + len(searchval)*2
									self.parent.debugmsg(8, "offset:", offset)
									excerpt = e["response"]["content"]["text"][(pos-len(key)-100):(pos+len(searchval)+100)]
									self.parent.debugmsg(8, "excerpt:", excerpt)

									if key in ['NoKey']:
										self.parent.debugmsg(8, "Special case:", key)
										searchkeys.append("?")

									for srchkey in searchkeys:
										if srchkey in excerpt:
											self.parent.debugmsg(6, "found key (",srchkey,") in excerpt:", "|{}|".format(excerpt))
											# self.parent.debugmsg(6, "resp:", resp, "	== e[\"entrycount\"]:", e["entrycount"])

											# if len(srchkey) > 1:
											# 	o = 0
											# 	body = e["response"]["content"]["text"]
											# 	# while o < offset:
											# 	while o < 10:
											# 		# (.{10}Accept.*?application\/json.{10})
											# 		resrchkey = re.escape(srchkey).replace("/", "\/")
											# 		researchval = re.escape(searchval).replace("/", "\/")
											# 		# ptn =  "(.{" + str(o) + "}" + resrchkey +".*?" + researchval + ".{" + str(o) + "})"
											# 		ptn =  "(" + resrchkey +".*?)" + researchval + "(.{" + str(o) + "})"
											# 		# match = re.search(ptn, body)
											# 		match = re.findall(ptn, body)
											#
											# 		if match is not None:
											# 			self.parent.debugmsg(5, "ptn:", ptn, " 	found match:", match)
											# 			# self.parent.debugmsg(5, "match.group(1):", match.group(1))
											# 			# self.parent.debugmsg(5, "match.group(2):", match.group(2))
											#
											# 		o += 1


											# This is non-ideal methods but they mostly work as a last resort
											kpos = excerpt.find(srchkey)
											vpos = excerpt.find(searchval, kpos)
											if vpos > kpos:
												self.parent.debugmsg(8, "kpos:", kpos, "vpos:", vpos)
												fullprefix = excerpt[0:vpos].strip()
												prefixarr = fullprefix.splitlines()
												prefix = prefixarr[-1].strip()
												self.parent.debugmsg(8, "prefix: |{}|".format(prefix))

												self.parent.debugmsg(8, "vpos:", vpos, "	len(searchval):", len(searchval), "")
												spos = vpos+len(searchval)
												self.parent.debugmsg(8, "spos:", spos, "	spos+5:", spos+5)

												fullsuffix = excerpt[spos:len(excerpt)]
												suffixarr = fullsuffix.splitlines()
												suffix = suffixarr[0].strip()
												self.parent.debugmsg(8, "suffix: |{}|".format(suffix))

												newkey = self.parent.saveparam(key, searchval)

												# test match with prefix and suffix works as expected?
												# find prefix from right
												ml = e["response"]["content"]["text"].rfind(prefix)+len(prefix)
												# find suffix from left
												mr = e["response"]["content"]["text"].find(suffix, ml)
												# get match
												match = e["response"]["content"]["text"][ml:mr]
												self.parent.debugmsg(6, "ml:", ml, "	mr:", mr, "	match:", match, "	searchval:", searchval)

												goffset = 1
												if match == searchval:

													line = "${"+newkey+"}= 	Get Substring LRB 	${resp_"+str(resp)+".text} 	"+prefix+" 	"+suffix
													self.parent.outdata["*** Keywords ***"][ekwname].insert(estep, line)


												else:
													reprefix = re.escape(prefix)
													resuffix = re.escape(suffix)

													# test re pattern
													pattern = reprefix+"(.*?)"+resuffix
													# e["response"]["content"]["text"]
													retest = re.search(pattern, e["response"]["content"]["text"]).group(0)

													self.parent.debugmsg(8, "retest:", retest)

													reprefix = re.escape(prefix).replace('"', r'\"').replace("\\", r"\\")
													resuffix = re.escape(suffix).replace('"', r'\"').replace("\\", r"\\")

													# line = "${regx_match}= 	Get Lines Matching Regexp 	${resp_"+str(resp)+".text} 	"+reprefix+"(.*?)"+resuffix
													line = "${regx_match}= 	evaluate 	re.search(\"" + reprefix + "(.*?)" + resuffix + "\", \"\"\"${resp_"+str(resp)+".text}\"\"\").group(0) 	re"

													self.parent.outdata["*** Keywords ***"][ekwname].insert(estep, line)
													line = "${"+newkey+"}= 	Get Substring LRB 	${regx_match} 	"+prefix+" 	"+suffix
													self.parent.outdata["*** Keywords ***"][ekwname].insert(estep+1, line)

													goffset += 1


												self.parent.debugmsg(6, "resp:", resp, "estep:", estep, "	goffset:", goffset)
												line = "Set Global Variable 	${"+newkey+"}"
												self.parent.outdata["*** Keywords ***"][ekwname].insert(estep+goffset, line)



												newvalue = "${"+newkey+"}"
												self.parent.debugmsg(6, "newvalue:", newvalue)
												return newvalue

									start = pos+len(searchval)
								else:
									start = pos
								# else:
									# self.parent.debugmsg(9, "didn't find key (",key,") in excerpt:", excerpt)

							if len(searchval) > 10:
								self.parent.debugmsg(6, "found searchval (",searchval,") in excerpt:", "|{}|".format(excerpt))

								# try 1
								# excerpt = e["response"]["content"]["text"][(pos-len(key)-100):(pos+len(searchval)+100)]
								body = e["response"]["content"]["text"]
								altsearchkeys = ["href", "codebase", "src", "cite", "background", "action", "longdesc", "profile", "usemap", "classid", "data", "formaction", "icon", "manifest", "poster", "archive", "lowsrc", "dynsrc"]
								# https://stackoverflow.com/questions/2725156/complete-list-of-html-tag-attributes-which-have-a-url-value

								for altsearchkey in altsearchkeys:
									# href=['"]([^'"\?]*)
									self.parent.debugmsg(6, "altsearchkey:", altsearchkey)
									ptn = altsearchkey + "=['\"]([^'\"\\?]*)"
									# match = re.match(ptn, body)
									# match = re.search(ptn, body)
									match = re.findall(ptn, body)

									# self.parent.debugmsg(6, "ptn:", ptn, " 	found match:", match)
									if match is not None:
										self.parent.debugmsg(5, "ptn:", ptn, " 	found match:", match)
										# matchurls = list(match.groups())
										# self.parent.debugmsg(6, "matchurls:", matchurls)
										i = 1
										for matchurl in match:
											if matchurl == searchval:
												self.parent.debugmsg(5, "i:", i, "	matchurl:", matchurl, " 	searchval:", searchval)

												# reptn = re.escape(ptn)
												reptn = ptn.replace('\\', '\\\\').replace(r'"', r'\"')

												newkey = self.parent.saveparam(key, searchval)
												# line = "${"+newkey+"}= 	evaluate 	re.findall(\"" + reptn + "\", \"\"\"${resp_"+str(resp)+".text}\"\"\")[" + str(i) + "] 	re"
												line = "${"+newkey+"}= 	evaluate 	re.findall(\"\"\"" + ptn + "\"\"\", \"\"\"${resp_"+str(resp)+".text}\"\"\")[" + str(i) + "] 	re"

												self.parent.outdata["*** Keywords ***"][ekwname].insert(estep, line)
												newvalue = "${"+newkey+"}"
												self.parent.debugmsg(5, "newvalue:", newvalue)
												return newvalue

											i += 1

								# try 2
								# excerptlines = excerpt.splitlines()
								# for excerptline in excerptlines:
								# 	if searchval in excerptline:
								# 		self.parent.debugmsg(6, "found searchval (",searchval,") in excerptline:", "|{}|".format(excerptline))


		return None

	#
	# processors
	#
	def post_data_params(self, entry):
		self.parent.debugmsg(6, "post data")
		self.parent.debugmsg(9, "entry:", entry)

		kwname = entry["kwname"]
		argdata = ""


		if "postData" in entry["request"]:
			pd_try = True
			pd = entry["request"]["postData"]
			if pd_try and "params" in pd:
				pd_try = False
				dictdata = ""
				for param in pd["params"]:
					newvalue = self.parent.find_variable(param["name"], param["value"])
					dictdata += " 	" + param["name"] + "=" + newvalue

				dname = "postdata_{}".format(entry["entrycount"])
				line = "&{"+dname+"}= 	Create dictionary" + dictdata
				self.parent.outdata["*** Keywords ***"][kwname].append(line)
				argdata += " 	" + "data=${"+dname+"}"

			# if pd_try and "text" in pd and pd["text"][0] == "{":
			# 	pd_try = False
			# 	jsondata = json.loads(pd["text"])
			# 	dname = "json_{}".format(entry["entrycount"])
			# 	paramname, lines = self.process_dict(dname, jsondata)
			# 	self.parent.debugmsg(8, "paramname:", paramname, "	paramlst:", paramlst)
			# 	self.parent.outdata["*** Keywords ***"][kwname].extend(lines)
			# 	argdata += " 	" + "json="+paramname

		if len(argdata.strip()) >0:
			if "argdata" in entry["processor"]:
				entry["processor"]["argdata"] += argdata
			else:
				entry["processor"]["argdata"] = argdata


		return entry






#
