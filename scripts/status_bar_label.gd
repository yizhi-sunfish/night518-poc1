extends RichTextLabel

@export var status_bar_length = 12.0

func set_status_bar_label(state_dict: Dictionary):
	var state_text = []
	for state_key in state_dict.keys():
		# TODO: read "hidden" key only when exists, otherwise print state by default
		if state_dict[state_key]["hidden"] != true:
			state_text.append( single_status_bar_text(state_dict, state_key) )
	self.text = "\n".join(PackedStringArray(state_text))

func single_status_bar_text(state_dict:Dictionary,key:String) -> String:
	var status_bar_count = floor(state_dict[key]["value"] * status_bar_length / 100.0)
	var status_bar_text = ""
	status_bar_text += "█".repeat(status_bar_count) + "░".repeat(status_bar_length - status_bar_count)
	return key + "： [color=%s]" % state_dict[key]["color"] + status_bar_text + "[/color] " + "%2d" % int(state_dict[key]["value"])
		
