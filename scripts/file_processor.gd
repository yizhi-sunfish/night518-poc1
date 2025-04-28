extends Node
class_name FileProcessor

func read_from_file(file_path):
	var file = FileAccess.open(file_path, FileAccess.READ)
	var content = file.get_as_text()
	var json = JSON.new()
	var error = json.parse(content)
	if error == OK:
		var data_received = json.data
		if typeof(data_received) == TYPE_DICTIONARY:
			print(data_received) # Prints the array.
		else:
			print("Unexpected data")
			print(typeof(data_received))
		return data_received
	else:
		print("JSON Parse Error: ", json.get_error_message(), " in ", file_path, " at line ", json.get_error_line())
		return ""
		
func _ready() -> void:
	read_from_file("res://data/zh/player.json")
