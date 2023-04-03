# URL Module - encoding and decoding URL encoded values
import re

class h2r_url():
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
		psr = "99:self.h2r_url.url_path"
		if psr not in self.parent.parsers:
			self.parent.parsers[psr] = {}


	#
	# Paersers
	#
	def url_path(self):
		self.parent.debugmsg(5, "headers Parser")
		retarr = []
		searchkeys = self.parent.parserdata["searchkeys"]
		searchvals = self.parent.parserdata["searchvals"]
		kwname = self.parent.parserdata["kwname"]
		key = self.parent.parserdata["key"]

		for searchval in searchvals.keys():
			self.parent.debugmsg(5, "searchval:", searchval)

			# check if value has :// in value

			if "://" in searchval:
				self.parent.debugmsg(5, "Full URL:", searchval)

				match = re.search(r'([^:]*):\/\/([^\/]*)(\/[^\?]*)\?*(.*)', searchval)
				if match is not None:
					self.parent.debugmsg(5, "match:", match)
					self.parent.debugmsg(5, "match.group(0):", match.group(0))
					self.parent.debugmsg(5, "match.group(1):", match.group(1))

					if match.group(1) is not None:
						protocol = self.parent.find_variable(key + "_protocol", match.group(1))
						self.parent.debugmsg(5, "protocol:", protocol)
						retarr.append(protocol)
						retarr.append("://")

					self.parent.debugmsg(5, "match.group(2):", match.group(2))
					if match.group(2) is not None:
						host = self.parent.find_variable(key + "_Host", match.group(2))
						self.parent.debugmsg(5, "host:", host)
						retarr.append(host)

					self.parent.debugmsg(5, "match.group(3):", match.group(3))
					if match.group(3) is not None:
						# if key == "path":
						# 	path = self.parent.find_variable(key, match.group(3))
						# else:
						# 	path = self.parent.find_variable(key + "_path", match.group(3))
						path = self.parent.find_variable(key + "_path", match.group(3))
						self.parent.debugmsg(5, "path:", path)
						retarr.append(path)
					self.parent.debugmsg(5, "match.group(4):", match.group(4))
					if match.group(4) is not None and len(match.group(4))>1:
						sparams = self._url_path_params(match.group(4))
						retarr.append(sparams)
					self.parent.debugmsg(5, "retarr:", retarr)
					newvalue = "".join(retarr)
					self.parent.debugmsg(5, "newvalue:", newvalue, "	searchval:", searchval)
					if newvalue != searchval:
						return newvalue

			else:
				if "/" in searchval:
					self.parent.debugmsg(5, "relative URL?:", searchval)

					if len(searchval) < 2:
						return None

					badmatchs = ["text/", "application/", "image/", "Mozilla/", "AppleWebKit/", "Chrome/", "Safari/", "*/", "/*"]
					for badmatch in badmatchs:
						if badmatch in searchval:
							return None

					match = re.search(r'([^\?]*)\?*(.*)', searchval)
					self.parent.debugmsg(5, "match:", match)
					self.parent.debugmsg(5, "match.group(1):", match.group(1))
					if match.group(1) is not None:
						opath = match.group(1)

						if "_path_path" in key:
							return None

						self.parent.debugmsg(5, "key:", key)
						# if key == "path":
						# 	path = self.parent.find_variable(key, opath)
						# else:
						# 	path = self.parent.find_variable(key + "_path", opath)
						path = self.parent.find_variable(key + "_path", opath, False)
						self.parent.debugmsg(5, "path:", path)

						if path is None:
							return None

						if path != opath:
							retarr.append(path)

						if  path == opath:
							patharr = path.split("/")
							self.parent.debugmsg(5, "path:", path)
							self.parent.debugmsg(5, "patharr:", patharr)

							if len(patharr) > 2:
								pathend = "/" + patharr.pop()
								pathbeg = "/".join(patharr)

								self.parent.debugmsg(5, "pathbeg:", pathbeg, "	pathend:", pathend)

								newpathbeg = self.parent.find_variable(key + "_pathpre", pathbeg, False)
								newpathend = self.parent.find_variable(key + "_pathsuf", pathend, False)
								self.parent.debugmsg(5, "pathbeg:", pathbeg, "	pathend:", pathend)
								self.parent.debugmsg(5, "newpathbeg:", newpathbeg, "	newpathend:", newpathend)

								if newpathbeg != pathbeg or newpathend != pathend:
									path = newpathbeg + newpathend
								

					self.parent.debugmsg(5, "match.group(2):", match.group(2))
					if match.group(2) is not None and len(match.group(2))>1:
						sparams = self._url_path_params(match.group(2))
						retarr.append(sparams)

					newvalue = "".join(retarr)
					self.parent.debugmsg(5, "newvalue:", newvalue, "	searchval:", searchval)
					if len(newvalue)>0 and newvalue != searchval:
						return newvalue

		return None


	def _url_path_params(self, sparams):
		params = []
		match2 = re.search(r'&*([^&]*)', sparams)
		if match2 is not None:
			self.parent.debugmsg(5, "match2:", match2)
			self.parent.debugmsg(5, "match2.groups():", match2.groups())
			# self.parent.debugmsg(5, "match2.group(0):", match2.group(0))
			# self.parent.debugmsg(5, "match2.group(1):", match2.group(1))
			for m2 in match2.groups():
				self.parent.debugmsg(5, "m2:", m2)
				match3 = re.search(r'([^=]*)=(.*)', m2)
				if match3 is not None:
					self.parent.debugmsg(5, "match3:", match3)
					m2key = match3.group(1)
					m2val = match3.group(2)
					m2val = self.parent.find_variable(m2key, m2val)
					params.append(m2key + "=" + m2val)
				else:
					# NoKey
					self.parent.debugmsg(5, "m2:", m2)
					m2val = self.parent.find_variable("NoKey", m2)
					params.append(m2val)

		self.parent.debugmsg(5, "params:", params)
		return "?" + "&".join(params)
