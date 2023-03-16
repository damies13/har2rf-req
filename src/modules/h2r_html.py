# HTML Module - encoding and decoding HTML encoded values

class h2r_html():
	"""docstring for ."""

	def __init__(self, parent):
		# super(, self).__init__()
		self.parent = parent



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
