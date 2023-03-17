# HTML Module - encoding and decoding HTML encoded values

import html

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
