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

		html = "self.h2r_html.html_encode"
		if html not in self.parent.encoders:
			self.parent.encoders[html] = {}
			self.parent.encoders[html]["robottranscode"] = "self.h2r_html.html_robotdecode"

		htmlX = "self.h2r_html.htmlX_encode"
		if htmlX not in self.parent.encoders:
			self.parent.encoders[htmlX] = {}
			self.parent.encoders[htmlX]["robottranscode"] = "self.h2r_html.htmlX_robotdecode"

		htmlx = "self.h2r_html.htmlx_encode"
		if htmlx not in self.parent.encoders:
			self.parent.encoders[htmlx] = {}
			self.parent.encoders[htmlx]["robottranscode"] = "self.h2r_html.htmlX_robotdecode"

		#
		# Register Decoders
		#

		html = "self.h2r_html.html_decode"
		if html not in self.parent.encoders:
			self.parent.decoders[html] = {}
			self.parent.decoders[html]["robottranscode"] = "self.h2r_html.html_robotencode"

		#
		# Register Paersers
		#
		psr = "self.h2r_html.html_body"
		if psr not in self.parent.parsers:
			self.parent.parsers[psr] = {}




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

					resp = e["entrycount"]+1
					ekwname = e["kwname"]
					estep = self.parent.find_estep(resp, ekwname)



					# check body
					self.parent.debugmsg(6, "is value in response body")
					if "text" in e["response"]["content"]:
						self.parent.debugmsg(8, "response content has text")

						# check body for raw value
						if searchval in e["response"]["content"]["text"]:
							self.parent.debugmsg(8, "found searchval (",searchval,") in body for ", e["request"]["url"])

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
											self.parent.debugmsg(8, "found key (",srchkey,") in excerpt:", "|{}|".format(excerpt))

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
												# self.parent.debugmsg(9, "ml:", ml, "	mr:", mr, "	match:", match, "	searchval:", searchval)

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


												line = "Set Global Variable 	${"+newkey+"}"
												self.parent.outdata["*** Keywords ***"][ekwname].insert(estep+goffset, line)



												newvalue = "${"+newkey+"}"
												self.parent.debugmsg(8, "newvalue:", newvalue)
												return newvalue

									start = pos+len(searchval)
								else:
									start = pos
								# else:
									# self.parent.debugmsg(9, "didn't find key (",key,") in excerpt:", excerpt)








#
