# template Module - This ,odule is not used, it's simply intended as a template for new modules

class h2r_template():
	"""docstring for ."""

	def __init__(self, parent):
		# super(, self).__init__()
		self.parent = parent

		#
		# Register Encoders
		#
		html = "self.h2r_template.example_encode"
		if html not in self.parent.encoders:
			self.parent.encoders[html] = {}
			self.parent.encoders[html]["robottranscode"] = "self.h2r_template.example_robotdecode"


		#
		# Register Decoders
		#
		html = "self.h2r_template.example_decode"
		if html not in self.parent.encoders:
			self.parent.decoders[html] = {}
			self.parent.decoders[html]["robottranscode"] = "self.h2r_template.example_robotencode"

		#
		# Register Paersers
		#
		ep = "self.h2r_template.example_parser"
		if ep not in self.parent.parsers:
			self.parent.parsers[ep] = {}






	#
	# Encoders
	#

	def example_encode(self, s):
		# do something with strin s
		return s

	def example_robotencode(self, varin):
		varout = varin
		return varout

	#
	# Decoders
	#

	def example_decode(self, s):
		# do something with strin s
		return s

	def example_robotdecode(self, varin):
		varout = varin
		return varout

	#
	# Paersers
	#
	def example_parser(self):
		self.parent.debugmsg(6, "Example Parser")
		#  do something to find the value
		# return the paramater to replace the value with if found
		# if not found return None
		return None
