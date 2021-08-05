from GTransPY.types import Lang, LangDetect
from GTransPY.types import WotoTr
from GTransPY.detection import DetectLanguage
from GTransPY.trLang.helpers import ExtractShortLang
from urllib.parse import urlencode

def TranslateIt(lang: Lang, to: str, text: str) -> WotoTr:
	if is_invalid_str(text):
		raise Exception("input text cannot be empty")

	to = ExtractShortLang(to)
	if is_invalid_str(to):
		raise Exception("target language is invalid")
	
	if not lang:
		lang = DetectLanguage(text)
	
	best: LangDetect = None

	if lang:
		best = lang.get_best()
	
	if not best or not best.is_reliable:
		return translateD("auto", to, text)
	

	return translateD(best.language, to, text)


def translateD(fr: str, to: str, text: str) -> WotoTr:
	if is_invalid_str(text):
		raise Exception("input text cannot be empty")
	
	to = ExtractShortLang(to)
	if is_invalid_str(to):
		raise Exception("target language is invalid")

	fr = ExtractShortLang(fr)
	if is_invalid_str(fr):
		fr = "auto"
	


	return None


def Translate(to: str, text: str) -> WotoTr:
	return TranslateIt(None, to, text)



def TranslateText(fr: str, to: str, text: str) -> WotoTr:
	fr = ExtractShortLang(fr)
	if is_invalid_str(fr):
		raise Exception("language " + fr + " is unrecognized")
	
	wTr = Translate(to, text)
	if not wTr:
		raise Exception("something unexpected happened during accessing "+ 
			"Google translate API, please try again later")
		
	if not wTr.HasWrongFrom and wTr.From != fr:
		wTr.HasWrongFrom = True
	elif wTr.HasWrongFrom and wTr.From == fr:
		wTr.HasWrongFrom = False


	return wTr


def is_invalid_str(value: str) -> bool:
	return not value or len(value.strip()) == 0 or value.isspace()
	


def trGoogle(fr: str, to: str, text: str) -> str:
	pass


def googleFQ(fr: str, to: str, text: str) -> str:
	return "f.req\u003d" + "%5B%5B%5B%22MkEWBc%22%2C%22%5B%5B%5C%22" +\
		urlencode(text) + "%5C%22%2C%5C%22" + fr +\
		"%5C%22%2C%5C%22" + to + "%5C%22%2Ctrue%5D%2C%5Bnull" +\
		"%5D%5D%22%2Cnull%2C%22generic%22%5D%5D%5D&"