# base64 Module - encoding and decoding base64 encoded values
import base64

class h2r_base64():
	"""docstring for ."""

	def __init__(self, parent):
		# super(, self).__init__()
		self.parent = parent

		#
		# Register Encoders
		#

		b64 = "03:self.h2r_base64.base64_encode"
		if b64 not in self.parent.encoders:
			self.parent.encoders[b64] = {}
			self.parent.encoders[b64]["robottranscode"] = "self.h2r_base64.base64_decode"

		#
		# Register Decoders
		#

		b64 = "03:self.h2r_base64.base64_decode"
		if b64 not in self.parent.decoders:
			self.parent.decoders[b64] = {}
			self.parent.decoders[b64]["robottranscode"] = "self.h2r_base64.base64_encode"

		#
		# Register Paersers
		#

		#
		# Register processors
		#


	#
	# Encoders
	#

	def base64_encode(self, s):
		self.parent.debugmsg(9, "s:", s)
		try:
			s_bytes = s.encode('utf_8')
			base64_bytes = base64.b64encode(s_bytes)
			base64_s = base64_bytes.decode('utf_8')
			self.parent.debugmsg(5, "s:", s, "	base64_s:", base64_s)
			return base64_s
		except Exception:
			return s

	#
	# Decoders
	#

	def base64_decode(self, s):
		self.parent.debugmsg(9, "s:", s)
		try:
			# s_bytes = s.encode('utf_8')
			s_bytes = s.encode()
			self.parent.debugmsg(8, "s_bytes:", s_bytes)
			dec_bytes = base64.b64decode(s_bytes)
			self.parent.debugmsg(8, "dec_bytes:", dec_bytes)
			# dec_s = dec_bytes.decode('utf_8')
			dec_s = dec_bytes.decode()
			self.parent.debugmsg(8, "dec_s:", dec_s)
			self.parent.debugmsg(5, "s:", s, "	dec_s:", dec_s)
			return dec_s
		except Exception as e:
			self.parent.debugmsg(8, "s:", s)
			self.parent.debugmsg(8, "e:", e)
			return s


	#
	# Paersers
	#



	#
	# processors
	#





#
