# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = translator_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")
minimum_condifence: float = 4.8


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class LangDetect:
    language: Optional[str] = None
    is_reliable: Optional[bool] = None
    confidence: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'LangDetect':
        assert isinstance(obj, dict)
        language = from_union([from_str, from_none], obj.get("language"))
        is_reliable = from_union([from_bool, from_none], obj.get("isReliable"))
        confidence = from_union([from_float, from_none], obj.get("confidence"))
        return LangDetect(language, is_reliable, confidence)

    def to_dict(self) -> dict:
        result: dict = {}
        result["language"] = from_union([from_str, from_none], self.language)
        result["isReliable"] = from_union([from_bool, from_none], self.is_reliable)
        result["confidence"] = from_union([to_float, from_none], self.confidence)
        return result


@dataclass
class LangData:
    detections: Optional[List[LangDetect]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'LangData':
        assert isinstance(obj, dict)
        detections = from_union([lambda x: from_list(LangDetect.from_dict, x), from_none], obj.get("detections"))
        return LangData(detections)

    def to_dict(self) -> dict:
        result: dict = {}
        result["detections"] = from_union([lambda x: from_list(lambda x: to_class(LangDetect, x), x), 
            from_none], self.detections)
        return result


@dataclass
class Lang:
    data: Optional[LangData] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Lang':
        assert isinstance(obj, dict)
        data = from_union([LangData.from_dict, from_none], 
            obj.get("data"))
        return Lang(data)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_union([lambda x: to_class(LangData, x), 
            from_none], self.data)
        return result

    # get_best returns the best results between lang detections, if and
    # only if it contains any acceptable one, otherwise it will return None.
    def get_best(self) -> LangDetect:
        if self.is_empty():
            return None
        best: LangDetect = None

        for d in self.data.detections:
            if d.is_reliable:
                if best:
                    if d.confidence > best:
                        best = d
                else:
                    best = d

        if best:
            if best.confidence < minimum_condifence:
                return None

        return best

    def is_empty(self) -> bool:
        return (self.data == None or
            self.data.detections == None or
            len(self.data.detections) == 0)
    


def translator_from_dict(s: Any) -> Lang:
    return Lang.from_dict(s)


def translator_to_dict(x: Lang) -> Any:
    return to_class(Lang, x)


@dataclass
class Correction:
    # an array of the corrected parts of the
	# original input text
    CorrectedParts: List[str]

    # the whole string
    CorrectedValue: str




@dataclass
class WotoTr:
    # Pronunciation of the original text
    OriginalPronunciation: str = None

    # Pronunciation of the translated text
    TranslatedPronunciation: str = None

    # the input text from user
    UserText: str = ""

    # originalText is the original data recieved from google's
	# server (which is in protobuf's format)
    originalText: str = ""

    # Translations is a list of translated string recieved from
	# google's servers
    Translations: List[str] = None

    From: str = "en"
    To: str = ""

    Corrected: Optional[Correction] = None

    HasWrongness: bool = False

    # internal wrong from.
	# when returning final value to the user,
	# this field SHOULD be false.
    wrongFrom: bool = False

    # public wrong from.
	# if 'From' in user's inpur is not correct,
	# this field will be true.
    HasWrongFrom: bool = False


    # isTrEmpty returns true if the translation list in wotoTr value
    # is empty, otherwise it returns false.
    def isTrEmpty(self) -> bool:
        if not self.Translations:
            return True
        
        for t in self.Translations:
            if t and len(t.strip()) != 0:
                return False
        
        return True

    # alreadyExists will check if the str value already exists in the
    # translations list of wotoTr value.
    def alreadyExists(self, value: str) -> bool:
        if not self.Translations:
            return False
        
        for t in self.Translations:
            if t.lower() == value.lower():
                return True
        
        return False






