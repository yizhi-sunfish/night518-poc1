extends Node
class_name Typewriter

var typing_speed := 0.05
var _is_typing := false

# default func, type by char
func type_text(target_node: Node, speed := typing_speed) -> void:
	type_text_by_char(target_node, speed)

func type_text_by_char(target_node: Node, speed := typing_speed) -> void:
	if _is_typing:
		return
	_is_typing = true

	var index := 0
	
	target_node.visible_characters = 0

	while index < target_node.get_total_character_count():
		target_node.visible_characters += 1
		index += 1
		await target_node.get_tree().create_timer(speed).timeout

	_is_typing = false

# TODO: type by line(currently not finished)
func type_text_by_line(target_node: Node, speed := typing_speed) -> void:
	if _is_typing:
		return
	_is_typing = true

	var index := 0
	
	target_node.visible_characters = 0
	var line_length = 20

	while index < target_node.get_total_character_count():
		index += line_length
		target_node.visible_characters += line_length
		await target_node.get_tree().create_timer(speed).timeout

	_is_typing = false
