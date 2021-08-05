from GTransPY.types import Lang, LangDetect
from GTransPY.types import WotoTr
from GTransPY.detection import DetectLanguage
from GTransPY.trLang.helpers import ExtractShortLang
from urllib.parse import urlencode
from GTransPY.strongString.values import *
from GTransPY.values import *
import httpx

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
	g_body = googleFQ(fr, to, purify(text))
	my_headers = {
		"User-Agent": ("Mozilla/5.0 " +
		"(X11; Ubuntu; Linux x86_64; rv:88.0) " +
		"Gecko/20100101 Firefox/88.0"),
		"Accept": "*/*",
		"Accept-Language": "en-US,en;q\u003d0.5",
		"Referer": "https://translate.google.com/",
		"X-Same-Domain" : "1",
		"X-Goog-BatchExecute-Bgr": get_batch_exec_value(),
		"Content-Type": ("application/x-www-form-urlencoded;" +
			"charset\u003dutf-8"),
		"Origin": "https://translate.google.com",
		"DNT": "1",
		"Connection": "keep-alive"
	}
	resp = httpx.post(gHostUrl, headers=my_headers, body=g_body)
	print(resp.content)

	pass

def purify(value: str) -> str:
	value = value.replace("\n", " ")
	value = value.replace("\r", " ")
	value = value.replace("[", "(")
	value = value.replace("]", ")")
	value = value.replace("*", "")
	value = value.replace(DoubleQ, DoubleQJ)
	return value



def googleFQ(fr: str, to: str, text: str) -> str:
	return "f.req\u003d" + "%5B%5B%5B%22MkEWBc%22%2C%22%5B%5B%5C%22" +\
		urlencode(text) + "%5C%22%2C%5C%22" + fr +\
		"%5C%22%2C%5C%22" + to + "%5C%22%2Ctrue%5D%2C%5Bnull" +\
		"%5D%5D%22%2Cnull%2C%22generic%22%5D%5D%5D&"

def get_batch_exec_value() -> str:
	return ("[\"!uLulu_bNAAZ-n43Xfp9" +
		"ChR5KyniU7RY7ACkAIwj8Rr5ZYBnKqvI3yOFfAcxDZqjGlJRAj7Wy" +
		"DbSIHd2rmrWJCLwm1AIAAAJAUgAAADJoAQcKALcwYzzTEVUDx7SCQT" +
		"1CoAv4iYyjg9RCfDFMYximkyqYTe38REBHCCV4VZFVBaph5E5VOlJm6Y" +
		"Lr8a_iniF72JIbG931cR_N2whV6a0OOTIxlYuY29VzYgH0lUipEtHoT7O0" +
		"BcWxFMu-mhiHCgIf5CDRGVFl4Y6GWWBXgNqOv2LMtr8nziYtayYIrEvFpV" +
		"wFEITAZp4-3QT3MYAdJ2U7wrHsW8eWZqQzmOC2biGnKa_YYd-NIbvIi_CZAc" +
		"9WmbBfsDWF2NLtoug2oUVk4oyRZoXMnRtRpsuXOp1ydcgogFXl1PKNDvctRzp" +
		"A4E1dJWjLskR1Ht7HpCO611v9o6BePdBLB6-rM-jQOejGLiJvqq-vS3rpCSr" +
		"TRR8OkyZh0emPZTP6B4dcOz_KH_0IYQghx2LnAxy5eaA5DDzYAECp-TsCb-" +
		"AvbLgRVA-PkqoargQ99NyBlxv9CZQngEtbhwyXzSxpdFCPhikJUIPwUPMN5Gc" +
		"1Y5B5HTNh9xnYndYneSQWtXRUHFNW1nMOCenMnoHEN0iq8U_OiYHnakZPlm" +
		"EG752mnidgLBT2CJVLkbTPVUoMN7HiFUTk-koWIzhAOdSWznIHanHiQr" +
		"20OmXSB5uURXCm-3_uNHR25vSJnDw3-MbEKdMmtlMDcyzU8sfwZ-ilCj" +
		"FAby6hJpBJq1MAVibjxniaed6z38EiLqdnCR_vJVhnXZ01cb2Ua9QuvY5" +
		"WtEhvpXGmJ6K9KdppK9n9VOQP9g2QXzfem3WIahR7a0AN_98Gtv_" +
		"Df5tWUfMpyj6hSwSd_8ZdnLkTv5VNPy-R0eWmPIwrmQq00IzvGs42" +
		"VYhrkPNvJhG4FuRdvebmsu63yRHjGX6zt9U_EJOehdii\"" +
		",null,null,51,null,null,null,0]")