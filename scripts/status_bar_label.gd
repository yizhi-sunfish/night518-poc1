extends RichTextLabel

@export var status_bar_length = 12.0

# TODO: Not done, needs to fix status format first

func set_status_bar_label(status_list: Dictionary):
	var status_text = []
	for status in status_list:
		status_text.append( single_status_bar_text(status) )
	self.text = "\n".join(PackedStringArray(status_text))
	
# TODO: Add type for status argument
func single_status_bar_text(status) -> String:
	var status_bar_count = floor(status["value"] * status_bar_length / 100.0)
	var status_bar_text = ""
	status_bar_text += "█".repeat(status_bar_count) + "░".repeat(status_bar_length - status_bar_count)
	return status.key + "： [color=%s]" % status["color"] + status_bar_text + "[/color] " + str(status["value"])
		
