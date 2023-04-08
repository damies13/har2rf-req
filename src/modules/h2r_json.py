# Module for dealing with standard JSON
import json

class h2r_json():
	"""docstring for ."""

	def __init__(self, parent):
		# super(, self).__init__()
		self.parent = parent

		#
		# Register processors
		#
		pro = "08:self.h2r_json.post_data_json"
		if pro not in self.parent.processors:
			self.parent.processors[pro] = {}




	#
	# processors
	#
	def post_data_json(self, entry):
		self.parent.debugmsg(6, "post data")
		self.parent.debugmsg(9, "entry:", entry)

		kwname = entry["kwname"]
		argdata = ""


		if "postData" in entry["request"]:
			pd_try = True
			pd = entry["request"]["postData"]

			if pd_try and "text" in pd and len(pd["text"]) > 1 and pd["text"][0] == "{":
				pd_try = False
				jsondata = json.loads(pd["text"])
				dname = "json_{}".format(entry["entrycount"])
				paramname, lines = self.parent.process_dict(dname, jsondata)
				self.parent.debugmsg(8, "paramname:", paramname, "	lines:", lines)
				self.parent.outdata["*** Keywords ***"][kwname].extend(lines)
				argdata += " 	" + "json="+paramname

		if len(argdata.strip()) >0:
			if "argdata" in entry["processor"]:
				entry["processor"]["argdata"] += argdata
			else:
				entry["processor"]["argdata"] = argdata


		return entry






#
