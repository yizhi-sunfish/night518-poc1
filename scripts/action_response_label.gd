extends Label

var typewriter := preload("res://scripts/ui_typewriter.gd").new()

func _ready():
	typewriter.type_text(self, 0.05)
