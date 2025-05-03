# TODO: Almost the same as player.gd, should refactor to avoid duplicated code

extends Node

var printed_name : String = ""
var nickname : String = ""
var states : Dictionary = {}
var body_parts : Dictionary = {}
var clothes : Dictionary = {}

func _ready() -> void:
	var player_info = FileProcessor.read_from_json_file("res://data/zh/npc.json")
	setup_player(player_info)
	
func setup_player(json_info):
	printed_name = json_info["name"]
	# TODO: make it optional to read nickname, based on whether it exists or not
	#nickname = json_info["nickname"]
	states = json_info["states"]
	body_parts = json_info["bodyParts"]
	clothes = json_info["clothes"]
	
	# TODO: use signal instead
	var ui = $"../MainUIMargin/UI/StatusDisplayArea/NpcStatusContainer/StatusBarContainer/StatusBarLabel"
	ui.set_status_bar_label(states)
	
	
