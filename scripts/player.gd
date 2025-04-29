extends Node

var printed_name : String = ""
var nickname : String = ""
var states : Dictionary = {}
var body_parts : Dictionary = {}
var clothes : Dictionary = {}

func _ready() -> void:
	var player_info = FileProcessor.read_from_json_file("res://data/zh/player.json")
	setup_player(player_info)
	
func setup_player(json_info):
	printed_name = json_info["name"]
	nickname = json_info["nickname"]
	states = json_info["states"]
	body_parts = json_info["bodyParts"]
	clothes = json_info["clothes"]
	# TODO: It seems now the values of the above dictionaries are just strings
	# need to find a way to parse nested dictionary, or store them in a better type
	
	# TODO: use signal instead
	#var ui = $"../MainUIMargin/UI/StatusDisplayArea/PlayerStatusContainer/StatusBarContainer/StatusBarLabel"
	#ui.set_status_bar_label(states)
	
	
