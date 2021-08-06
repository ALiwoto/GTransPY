from GTransPY.trLang import langList
from GTransPY.trLang import langListR

def IsLang(value: str) -> bool:
	if value is not str or (value == "" or value.isspace()):
		return False

	value = value.lower()
	if value in langList:
		return True
	else:
		return value in langListR


def ExtractShortLang(value: str) -> str:
	if not value or value == "" or value.isspace():
		raise Exception("value cannot be empty")

	value = value.lower()
	if value == "auto":
		return value
	elif value in langList:
		return value
	elif value in langListR:
		return value
	else:
		raise Exception(f"{value} is not a valid language")


def RemoveShortsWithStrs(value: str) -> str:
	if value == "" or value.isspace():
		raise Exception("value cannot be empty")

	# iterate throgh langList and replace all these shits
	for lang in langList:
		value = value.replace(f"\"{lang}\"", "")

	return value

