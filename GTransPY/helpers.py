#from GTransPY import trLang
from typing import List
import httpx
import re
from GTransPY.types import Correction, Lang, LangDetect
from GTransPY.types import WotoTr
from GTransPY.detection import DetectLanguage
from GTransPY.trLang.helpers import ExtractShortLang, IsLang, RemoveShortsWithStrs
from urllib.parse import quote
#from GTransPY.values import *


#-----------------------------------------------------



#-----------------------------------------------------


#-----------------------------------------------------


#-----------------------------------------------------


#-----------------------------------------------------


#-----------------------------------------------------
#-----------------------------------------------------





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
    
    #print("my best is: ", best)

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
    
    uText = text.strip()
    text = trGoogle(fr, to, uText)

    wTr = WotoTr(UserText=uText, From=fr, To=to, originalText=text)

    return parseGData(wTr)


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

    # In the query string we have:
    #  * rpcids
    #  * f.sid
    #  * bl
    #  * hl
    #  * soc-app
    #  * soc-platform
    #  * soc-device
    #  * _reqid
    #  * rt
    # and these are present in the request body (the raw data)
    #  * f.req
    #  * at
    resp = httpx.post((("\u0068\u0074\u0074ps\u003a\u002f\u002f\u0074" +
	"ransla\u0074e\u002e\u0067oo\u0067l\u0065\u002e\u0063o\u006d" + "\u002f") + 
	"\u005f\u002fTransla\u0074\u0065W\u0065bs\u0065rv\u0065rUi\u002fda\u0074a\u002f" + 
	"ba\u0074\u0063hex\u0065\u0063u\u0074e\u003f"
	+ "rpcids\u003dMkEWBc" +
	"&f.sid\u003d-6960075458768589634" +
	"&bl\u003d" + ("boq\u005f\u0074ransla\u0074e-webserver\u005f" + "20210512.09" +
	"\u005fp0") +
	"&hl\u003d" + "en-US" +
	"&soc-app\u003d" + "1" +
	"&soc-pla\u0074form\u003d" + "1" +
	"&soc-device\u003d" +  "1" +
	"&\u005freqid\u003d" + "1662330" +
	"&rt\u003d" +  "c"), headers=my_headers, data=g_body)
    return resp.content.decode("utf-8")

def purify(value: str) -> str:
    value = value.replace("\n", " ")
    value = value.replace("\r", " ")
    value = value.replace("[", "(")
    value = value.replace("]", ")")
    value = value.replace("*", "")
    value = value.replace("\"", "”")
    return value



def googleFQ(fr: str, to: str, text: str) -> str:
    return ("f.req\u003d" + "%5B%5B%5B%22MkEWBc%22%2C%22%5B%5B%5C%22" +
        quote(text) + "%5C%22%2C%5C%22" + fr +
        "%5C%22%2C%5C%22" + to + "%5C%22%2Ctrue%5D%2C%5Bnull" +
        "%5D%5D%22%2Cnull%2C%22generic%22%5D%5D%5D&")

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

def valueAcceptable(value: str) -> bool:
    if value == "\\n":
        return False
    
    if value == '\\n,':
        return False

    if value.count("af.httprm") != 0:
        return False
    

    if value.count("\"e\",4,") != 0:
        return False
    
    if value.startswith("null,"):
        value = value.replace("null,", "")
        if value.isalnum():
            return False
    
    if value.startswith("\"di\""):
        return False


    value = value.replace(" ", "")
    value = value.replace(",", "")

    if len(value) == 0:
        return False
    
    if value == ")" or value == "}\'":
        return False
    

    if (not value.count("null")) and (not value.count("\"")):
        return False
    
    if value.count("\"wrb.fr\",\"MkEWBc\"") != 0:
        return False
    
    value = value.replace("\n", "")

    return not value.isalnum()


def parseGData(wTr: WotoTr) -> WotoTr:
    myStrs = re.split(r'\[|\]', wTr.originalText)
    original = []

    for myStr in myStrs:
        if valueAcceptable(myStr):
            original.append(myStr)
            
    

    wTr = parseGparams(original, wTr)



    if wTr.wrongFrom and (not wTr.HasWrongFrom):
        textStr = trGoogle(wTr.From, wTr.To, wTr.UserText)
        w = WotoTr(UserText=wTr.UserText, 
            originalText=textStr, 
            From=wTr.From, 
            To=wTr.To,
            HasWrongFrom=True)
        wTr = w

        return parseGData(wTr)



    return wTr


# There are no key-value pairs in raw protobuf, 
# just values assigned to field numbers. 
# With batchexecute, I think Google is mapping protobuf messages to JSON in a special way.
# There is documentation on this, but it doesn’t quite match up to what we see here. 
# This is how I think the above message would be mapped to JSON in batchexecute
def parseGparams(value: List[str], wTr: WotoTr) -> WotoTr:
    if isWrongFrom(value, wTr):
        return wTr

    p1Set = False  # is original Pronunciation already set??
    p2Set = False  # is translated Pronunciation already set??
    tSet = False   # is trasnlated text already set??
    wCheck = False # is wrongness checked??
    isW = False    # is the current value a wrongness??
    tmp = ""       # the tmp string
    lastStr = ""   # last string checked in loop
    i = 0          # current index of loop
    for current in value:
        current = current.strip()
        tmp = current
        if current == lastStr or current == "null,":
            return
        else:
            lastStr = tmp
        

        if not wCheck:
            isW = isWrongness(current)
            #if not isW:
                #print("\nnot wrong at all" + current + "\n")
        

        # check if pSet is true or not, if not, please try to
        # extract it from current element, if you couldn't extract it
        # at the end, you have to go for next element.
        if i == 0 and not p1Set and not isW:
            prou = getPronunciation(current)
            p1Set = not is_invalid_str(prou)
            wTr.OriginalPronunciation = prou
            # Pronunciation field is mandatory, if you don't
            # find it at the first, you have to iterate over all
            # of the array elements to at the very list find it.
            # Tho we find that if we use only one word for our
            # original text, the first element will be our
            # pronunciation, and in contrary, if we use only
            # more than one word, it will be our second one.
            # Tho we can't tell this for sure, because we don't
            # know if google will continue to send the data with
            # the same algorithm or not (but we are sure that
            # the order of the data WILL NOT change in the future,
            # in ProtoBuff, order of data matters after all.)
            i += 1
            continue
        elif not p1Set:
            p1Set = True


        if not wCheck and isW:
            wStr = extractTextStr(current)
            if not is_invalid_str(wStr):
                setWrongNess(wStr, wTr)

            #print("wchecked passed")
            wCheck = True
            i += 1
            continue
            
        
        if not p2Set and canBePronunciation(current):
            prouu = getPronunciation(current)
            if not is_invalid_str(prouu):
                wTr.TranslatedPronunciation = prouu
                p2Set = True
            i += 1
            continue















        if not tSet:
            if isSeparator(current, wTr):
                tSet = True
                i += 1
                continue

            if current.endswith(",\\\""):
                current = current.rstrip(",\\\"")
                if is_invalid_str(current):
                    i += 1
                    continue
                
                if (not current.endswith("\"") or not current.endswith("\",")):
                    i += 1
                    continue
        

            current = current.strip()
            if current.startswith(",") and current.endswith(","):
                tmpCheck = RemoveShortsWithStrs(current)
                tmpCheck = tmpCheck.replace(",,", "")
                tmpCheck = tmpCheck.replace(" ", "")
                if is_invalid_str(tmpCheck) or tmpCheck.isalnum():
                    i += 1
                    continue


            if current.endswith("\","):
                tmpStr = extractTextStr(current)
                if is_invalid_str(tmpStr):
                    i += 1
                    continue
                tmpStr = tmpStr.strip()
                if wTr.alreadyExists(tmpStr):
                    i += 1
                    continue

                if wTr.To != wTr.From:
                    if (tmpStr.lower() == wTr.UserText.lower() or 
                        tmpStr.lower() == wTr.OriginalPronunciation):
                        i += 1
                        continue
                    if tmpStr.lower() == wTr.OriginalPronunciation:
                        wTr.TranslatedPronunciation = ""
                
                    if not wTr.Translations:
                        wTr.Translations = list()
                
                    wTr.Translations.append(tmpStr)
            
            i += 1
        else:
            break # TODO: detect kind, etc    






    


    return wTr

def isWrongFrom(value: List[str], wTr: WotoTr) -> bool:
    # TODO: detect more complex wrongFrom.
    return isSimpleWrongFrom(value, wTr)


def isSimpleWrongFrom(value: List[str], wTr: WotoTr) -> bool:
    nullCount = 0
    for current in value:
        if nullCount >= 2:
            return True
        
        txt = extractTextStr(current)
        if not txt:
            continue
            
        if IsLang(txt):
            short = ExtractShortLang(txt)
            if short:
                if short.lower() == wTr.From.lower():
                    wTr.wrongFrom = True
                    wTr.From = short
                    return True
        
        current = current.strip()
        if current == "null,":
            nullCount += 1



    return False



def extractTextStr(value: str) -> str:
    l = len(value) - 1
    if l <= 1:
        # we need at least something like "." or "..."
        return None # if it's only "", then return none
    
    pre = False
    find = False
    myStr = ""
    i = 0

    for s in value:
        if find:
            if s == '\\':
                if i == l:
                    return None # not found
                elif value[i + 1] == "\"":
                    return myStr # found
            elif s == "\"":
                return myStr # found
            
            myStr += s
            continue

        if s == '\\':
            if not pre:
                pre = True
        elif pre:
            if s == "\"":
                find = True
        elif s == "\"" and not pre:
            find = True
        
    return myStr # found





def setWrongNess(value: str, wTr: WotoTr):
    if wTr == None:
        return
    
    value = value.strip()
    part = ""
    whole = ""
    parts: List[str] = list()
    delimiters = list((r"\\u003cb\\u003e\\u003ci\\u003e", 
        r"\\u003c/i\\u003e\\u003c/b\\u003e"))
    
    regP = '|'.join(map(re.escape, delimiters))
    myStrs = removeEmptyStrs(re.split(regP, value))
    #print("mystrs is: ", myStrs)
    j = 0
    another = ""
    l = len(myStrs) - 1
    try:
        index = value.index(r'\\u003cb\\u003e\\u003ci\\u003e')
    except ValueError:
        return

    if index != 0:
        index = 1
        whole = myStrs[0].strip() + " "
    
    i = index
    while i <= l:
        j = i + 1
        part = myStrs[i].strip().rstrip('\\')
        if j > l:
            another = ""
        else:
            another = myStrs[j].strip().rstrip('\\')

        parts.append(part)

        if i != index:
            whole += " "
        
        if is_invalid_str(another) == "":
            whole += part
        elif part == "":
            whole += another
        else:
            whole += part + " " + another
        
        i += 2
    # end while loop here.

    wTr.Corrected = Correction(parts, whole)
    #print(wTr.Corrected)
    return

    


def isWrongness(value: str) -> bool:
    return (value.count(r"\\u003cb\\u003e\\u003ci\\u003e") != 0 and 
        value.count(r"\\u003c/i\\u003e\\u003c/b\\u003e") != 0)


def getPronunciation(value: str) -> str:
    myStr = extractTextStr(value)
    if is_invalid_str(myStr):
        return None
    
    finalStr = ""
    lastBad = "."
    i = 0
    for current in myStr:
        if i == 0:
            if (current == "." or current == "?" or current == "!" or
                current == "\\"):
                i += 1
                continue
        else:
            if i == len(myStr) - 1:
                if current == "\\":
                    break
            
            if lastBad == current and current != ".":
                i += 1
                continue
            elif current == "?" or current == "!":
                lastBad = current
            else:
                if current.isspace():
                    lastBad = "."
        i += 1
        finalStr += current
    # end for loop

    return finalStr.strip()


def isSeparator(value: str, wTr: WotoTr) -> bool:
    if wTr == None or wTr.isTrEmpty():
        return False
    
    left = ",\\\"" + wTr.To + "\\\","
    right = ",\\\"" + wTr.From + "\\\","
    b1 = value.startswith(left) or value.endswith(left)
    b2 = value.startswith(right) or value.endswith(right)
    return b1 and b2
    

def canBePronunciation(value: str) -> bool:
    if value and value.endswith(",null,"):
        value = value.rsplit(",null,")
        return len(value) >= 2
    
    return False

def removeEmptyStrs(values: List[str]) -> List[str]:
    myStrs: List[str] = list()
    for s in values:
        if not is_invalid_str(s):
            myStrs.append(s)

    return myStrs

